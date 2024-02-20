import os

import numpy as np
import torch
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

load_dotenv()
DATA_PATH = os.getenv("DATA_PATH")


def MINI_LM_embed(doc_text):
    device = "cuda" if torch.cuda.is_available() else "cpu"

    model = SentenceTransformer("paraphrase-MiniLM-L6-v2", device=device)
    doc_embedding = model.encode(doc_text)
    return [doc_embedding]


def all_document_embeddings_batchwise_MINI_LM(documents):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = SentenceTransformer("paraphrase-MiniLM-L6-v2", device=device)

    all_embeddings_list = []

    batch_size = 1000
    for i in tqdm(range(0, len(documents), batch_size)):
        batch_embedding = model.encode(documents[i : i + batch_size])
        all_embeddings_list.append(batch_embedding)

    # Convert the list of batch embeddings to a 2D NumPy array
    all_embeddings = np.vstack(all_embeddings_list)

    return all_embeddings
