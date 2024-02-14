import json
import os

import requests
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
API_KEY = os.getenv("OPENAI_KEY")

client = OpenAI(api_key=API_KEY)


def get_embedding_openai(input, model="text-embedding-3-small"):
    if isinstance(input, str):
        input = [input.replace("\n", " ")]
    return client.embeddings.create(input=input, model=model).data


# print(get_embedding_openai(["hallo, ich brauche deine embeddings", "Bitte, bitte, bitte"]))
