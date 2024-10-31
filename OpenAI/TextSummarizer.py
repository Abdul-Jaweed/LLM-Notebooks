from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

user_text = str(input("Enter your query here : "))

completion = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {"role": "user", "content": f"""
     
     your task is to summarize the given text into a 50 words.
     
     here is the text : ```{user_text}```
     
     """}
  ],
  temperature=0.7
  )


print(completion.choices[0].message.content)