import os
import requests
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.getenv("OPENAI_KEY")

client = OpenAI(api_key=api_key)

response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", 
     "content": "Antworte ohne Erklärung nur mit 3 Stichwörtern, die zu dem Userinput passen"},
    {"role": "user", "content": "Oktoberfest Bayern"}
  ]
)

def old_call():
    endpoint_url = "https://api.openai.com/v1/engines/davinci/completions"

    input_text = "Translate the following English text to French: 'Hello, how are you?'"

    response = requests.post(
        endpoint_url,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "prompt": input_text,
            "max_tokens": 50,  #
        },
    )

print(response.json())
# if response.status_code == 200:
#     # Print the response from ChatGPT
# else:
#     print(f"Request failed with status code {response.status_code}:")
#     print(response.text)
