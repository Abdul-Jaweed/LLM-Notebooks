from pymongo import MongoClient
from sklearn.metrics.pairwise import cosine_similarity
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langgraph.graph.message import MessagesState
# from langchain_ollama.chat_models import ChatOllama
from langchain_openai.chat_models.azure import AzureChatOpenAI
from langgraph.graph import START, StateGraph
from langgraph.prebuilt import tools_condition, ToolNode
from langgraph.graph.state import CompiledStateGraph

import os
from dotenv import load_dotenv
load_dotenv()

MONGODB_URI="mongodb://localhost:27017"
client = MongoClient(MONGODB_URI)
db = client['Zero2MLOps']
collection = db['IndianConstitutionDataEmbeddings']

def GetOllamaEmbeddings(text:str):
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    return embeddings.embed_query(text=text)

def GetIndianConstitutionData(user_query:str, top_k:int = 5):
    """GetIndianConstitutionData Function is used to fetch the Indian Constitution related data from MongoDB based on the user query.
    
    Args:
        user_query (str): The query string used to search the database.
    
    Returns:
        list[dict]: A list of dictionaries containing the top results and their similarity scores.
    """
    
    query_embedding = GetOllamaEmbeddings(text=user_query)
    
    cursor = collection.find(
        {},
        {
            "embeddings":1,
            "text":1
        }
    )
    
    results = []
    for doc in cursor:
        similarity = cosine_similarity([query_embedding],[doc["embeddings"]])[0][0]
        results.append(
            {
                "text":doc['text'],
                "similarity":similarity
            }
        )
    
    results = sorted(results, key=lambda x:x["similarity"], reverse=True)
    
    return results[:top_k]

tools = [GetIndianConstitutionData]


# llm = ChatOllama(model="llama3.2:3b")

def AzureChatOpenAILLM():
    
    return AzureChatOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        model=os.getenv("AZURE_OPENAI_LLM_MODEL")
    )


llm = AzureChatOpenAILLM()

llm_with_tools = llm.bind_tools(tools)


class State(MessagesState):
    pass


def llm_assistant(state:MessagesState) -> MessagesState:
    
    sys_prompt:SystemMessage = SystemMessage(
        content="Youre a helpful assistant and your name is jarvis created by IronMan"
    )
    
    return {
        "messages":[llm_with_tools.invoke([sys_prompt] + state["messages"])]
    }


builder:StateGraph = StateGraph(MessagesState)

builder.add_node("assistant", llm_assistant)
builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, "assistant")
builder.add_conditional_edges("assistant", tools_condition)

builder.add_edge("tools", "assistant")

reactGraph: CompiledStateGraph = builder.compile()

