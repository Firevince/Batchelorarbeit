import os

import joblib
import numpy as np
import torch
from dotenv import load_dotenv
from scipy import sparse
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import pairwise_distances
from tqdm import tqdm

load_dotenv()
DATA_PATH = os.getenv("DATA_PATH")


def document_embedding_MINI_LM(doc_text):
    device = "cuda" if torch.cuda.is_available() else "cpu"

    model = SentenceTransformer("paraphrase-MiniLM-L6-v2", device=device)
    doc_embedding = model.encode(doc_text)
    return doc_embedding


def calculate_distances_optimized(message, tfidf_vectorizer, tfidf_matrix):
    tfidf_message = tfidf_vectorizer.transform([message])
    all_distances = np.array([])

    batch_size = 1000
    for i in tqdm(range(0, tfidf_matrix.shape[0], batch_size)):
        batch_distances = pairwise_distances(
            tfidf_matrix[i : i + batch_size], tfidf_message, metric="cosine"
        )
        all_distances = np.concatenate((all_distances, batch_distances.flatten()))

    return all_distances


def calculate_distances(message, df):
    embeddings = joblib.load(os.path.join(DATA_PATH, "matrices/MINI_L6_embeddings.pkl"))
    message_embedding = document_embedding_MINI_LM(message)

    all_distances = calculate_distances_optimized(
        message, embeddings, message_embedding
    )
    df["distance"] = all_distances
    return df
