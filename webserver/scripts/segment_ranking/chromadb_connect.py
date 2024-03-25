import os
import sys

import chromadb
from dotenv import load_dotenv

sys.path.append("..")
import os
from typing import Generic, TypeVar

import chromadb.utils.embedding_functions as embedding_functions
import numpy as np
import pandas as pd
import voyageai
from chromadb import Documents, EmbeddingFunction, Embeddings
from db_connect import db_get_df, db_save_df, load_npz, load_pkl, save_npz, save_pkl
from dotenv import load_dotenv
from tqdm import tqdm
from transformers import AutoTokenizer

load_dotenv(override=True)
CHROMADB_HOST = os.getenv("CHROMADB_HOST")
CHROMADB_PATH = os.getenv("CHROMADB_PATH")
CHROMADB_PORT = os.getenv("CHROMADB_PORT")
OPENAI_KEY = os.getenv("OPENAI_KEY")
VOYAGE_API_KEY = os.getenv("VOYAGE_API_KEY")


def get_most_similar_documents_openai(query, amount):
    openai_ef = embedding_functions.OpenAIEmbeddingFunction(
        api_key=OPENAI_KEY, model_name="text-embedding-3-small"
    )
    chroma_client = chromadb.HttpClient(host=CHROMADB_HOST, port=CHROMADB_PORT)

    collection = chroma_client.get_collection(name="sentence_openai", embedding_function=openai_ef)

    result = collection.query(query_texts=[query], n_results=amount)
    df = pd.DataFrame({"sentence": result["documents"][0]})
    df["end"] = [metadata["end"] for metadata in result["metadatas"][0]]
    df["start"] = [metadata["start"] for metadata in result["metadatas"][0]]
    df["filename"] = [metadata["filename"] for metadata in result["metadatas"][0]]
    df["segment_id"] = [metadata["sentence_id"] for metadata in result["metadatas"][0]]
    return df


def get_most_similar_documents_voyage(query, amount):

    voyage_ef = Embedding_Voyage[str]()
    chroma_client = chromadb.HttpClient(host=CHROMADB_HOST, port=CHROMADB_PORT)

    collection = chroma_client.get_collection(name="sentence_voyage", embedding_function=voyage_ef)

    result = collection.query(query_texts=[query], n_results=amount)

    # print(result)
    df_original = db_get_df("transcript_sentences")

    df = pd.DataFrame({"sentence": result["documents"][0]})

    df["segment_id"] = result["ids"][0]
    # print(df["segment_id"])
    result_df = pd.concat(
        [df_original[df_original["u_id"] == segment_id] for segment_id in df["segment_id"]]
    )

    # df["end"] = result_df["end"]
    # df["start"] = [metadata["start"] for metadata in result["metadatas"][0]]
    # df["filename"] = [metadata["filename"] for metadata in result["metadatas"][0]]
    return result_df


# Assuming Embeddable, Embeddings, and other necessary imports are defined elsewhere
D = TypeVar("D", bound=str)


class Embedding_Voyage(EmbeddingFunction[D], Generic[D]):
    def __call__(self, input: D) -> Embeddings:
        model = "voyage-lite-02-instruct"
        vo = voyageai.Client()

        # Check and format the input accordingly
        if isinstance(input, str):
            formatted_input = [input.replace("\n", " ")]
        elif isinstance(input, list) and all(isinstance(i, str) for i in input):
            formatted_input = [i.replace("\n", " ") for i in input]
        else:
            raise TypeError("Unsupported input type for embedding")

        result = vo.embed(formatted_input, model=model, input_type="query")
        return result.embeddings


# print(get_most_similar_documents_voyage("wie viele Quadratmeter?", 4))
