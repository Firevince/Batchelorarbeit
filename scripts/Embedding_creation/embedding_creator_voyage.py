import json
import os

import voyageai
from dotenv import load_dotenv
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("voyageai/voyage")

load_dotenv()
API_KEY = os.getenv("VOYAGE_API_KEY")

vo = voyageai.Client()


def get_embedding_voyage(input, model="voyage-2"):
    if isinstance(input, str):
        input = [input.replace("\n", " ")]

    # request =  {
    #     "input": json.dumps(input),

    # }
    # input = json.dumps(input)

    result = vo.embed(input, model=model, input_type="document")
    return result.embeddings
