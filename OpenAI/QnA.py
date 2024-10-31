from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

user_input = str(input("Enter your query here : "))

completion = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {"role": "system", "content": "You're are a sarcastic assistant."},
    {"role": "user", "content": f"{user_input}"}
  ],
  temperature=0.7
  )


print(completion.choices[0].message.content)