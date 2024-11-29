## LangChain based LLM App

# import os
# from dotenv import load_dotenv
# from langchain.prompts import ChatPromptTemplate
# from langchain_openai.chat_models import ChatOpenAI

# load_dotenv()

# prompt = ChatPromptTemplate.from_template("tell me a joke about {topic}")

# model = ChatOpenAI(
#     api_key=os.getenv("OPENAI_API_KEY"),
#     model="gpt-4o-mini",
#     temperature=0.7
# )

# chains = prompt | model

# print(chains.invoke({"topic":"Donald Trump"}))



## Convert into API using LangServe



import os
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain_openai.chat_models import ChatOpenAI
from fastapi import FastAPI
from langserve import add_routes

load_dotenv()

prompt = ChatPromptTemplate.from_template("tell me a joke about {topic} and translate into {lang} language")

model = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-4o-mini",
    temperature=0.7
)

# chains = prompt | model


# LangServe Code

app = FastAPI(
    title="Langserve Based API",
    version="0.0.1",
    description="THis is a Langchain LLM App API using Langserve"
)

add_routes(
    app,
    prompt | model,
    path="/jokes"
)


if __name__=="__main__":
    import uvicorn
    
    uvicorn.run(app, host="localhost", port=8087)


