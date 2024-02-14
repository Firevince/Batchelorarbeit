import json

import numpy as np
import pandas as pd
import scipy.sparse as sparse
from db_connect import db_get_df, db_save_df, load_npz, load_pkl

# from Embedding_creation.embedding_creator_BERT import dokument_embedding
from embedding_creation.embedding_creator_MINI_L6 import document_embedding_MINI_LM
from embedding_creation.embedding_creator_TF_IDF import (
    question_embedding_tf_idf_lemma_compound_split,
)
from scipy.spatial.distance import cosine
from segment_ranking.chatgpt_help import gpt_order_segments
from sklearn.metrics.pairwise import pairwise_distances
from tqdm import tqdm

# from Embedding_creation.embedding_creator_llama_2 import document_embedding_LLama_2


def enrich_segment(segment, transcript_df, num_prev_sentences=5, num_next_sentences=5):
    segment = segment.copy()
    segment_id = segment.loc["segment_id"]
    filename = segment.loc["filename"]

    # Filter rows by filename
    rows_df = transcript_df[transcript_df["filename"] == filename]
    rows_df = rows_df.sort_values("segment_id").reset_index(drop=True)

    start_id = max(0, segment_id - num_prev_sentences)
    end_id = min(segment_id + num_next_sentences, rows_df["segment_id"].max())

    # Zusammenführen der Sätze und Anpassen von Start- und Endzeit
    combined_sentences = " ".join(rows_df.loc[start_id:end_id, "sentence"])
    segment.loc["sentence"] = combined_sentences
    segment.loc["start"] = rows_df.loc[start_id, "start"]
    segment.loc["end"] = rows_df.loc[end_id, "end"]

    return segment.to_frame().T


def enrich_all_segments(df_distance, df_all, segment_size):
    enriched_segments_df = pd.concat(
        [
            enrich_segment(row, df_all, segment_size // 2 - 1, segment_size // 2)
            for _, row in df_distance.iterrows()
        ]
    )
    enriched_segments_df = enriched_segments_df.reset_index(drop=True)
    return enriched_segments_df


def calculate_distances_batchwise(message_embedding, embeddings_matrix):
    all_distances = np.array([])

    batch_size = 1000
    for i in tqdm(range(0, embeddings_matrix.shape[0], batch_size)):
        batch_distances = pairwise_distances(
            embeddings_matrix[i : i + batch_size], message_embedding, metric="cosine"
        )
        all_distances = np.concatenate((all_distances, batch_distances.flatten()))

    return all_distances


def get_embedding(model_type, message):
    """
    Generate an embedding for the input message based on the specified model type.

    :param model_type: A string indicating the type of model ('MINI_LM' or 'TF_IDF').
    :param message: The input message for which to generate the embedding.
    :return: The embedding of the input message.
    """
    if model_type == "MINI_LM":
        return document_embedding_MINI_LM(message)
    elif model_type == "TF_IDF":
        embedding = question_embedding_tf_idf_lemma_compound_split(message)
        return embedding
    elif model_type == "TF_IDF_MINI_LM":
        embed_mini_lm = document_embedding_MINI_LM(message)
        embed_mini_lm_sparse = sparse.csr_matrix(embed_mini_lm)
        embed_tf_idf = question_embedding_tf_idf_lemma_compound_split(message)
        return sparse.hstack([embed_tf_idf, embed_mini_lm_sparse], format="csr")
    else:
        print(f"No embedding method for model type {model_type} found")


def load_model_data(model_type):
    """
    Load model-specific data required for calculating distances.

    :param model_type: A string indicating the type of model ('MINI_LM' or 'TF_IDF').
    :return: Model-specific data required for calculating distances.
    """
    if model_type == "MINI_LM":
        return load_pkl("MINI_L6_embeddings.pkl")
    elif model_type == "TF_IDF":
        return load_npz("tf_idf_matrix_compound_split_87k.npz")
    elif model_type == "TF_IDF_MINI_LM":
        return load_npz("tf_idf_mini_lm_matrix.npz")
    else:
        print(f"No model for model type {model_type} found")


def get_most_similar_segments(
    model_type: str, message: str, amount: int, segment_size: int, sort_gpt=False
):
    """
    Find the most similar documents to the given message using the specified model.

    :param model_type: A string indicating the model to use ('MINI_LM' or 'TF_IDF').
    :param message: The message to find similar documents for.
    :param amount: The number of similar documents to return.
    :return: A DataFrame containing the most similar documents.
    """
    df = db_get_df("sentences_compound_split")
    message_embedding = get_embedding(model_type, message)
    model_data = load_model_data(model_type)

    df["distance"] = calculate_distances_batchwise(message_embedding, model_data)
    most_similar_documents = df.nsmallest(amount, "distance")
    most_similar_documents = enrich_all_segments(most_similar_documents, df, segment_size)

    if sort_gpt:
        most_similar_documents = gpt_order_segments(most_similar_documents)

    db_save_df(most_similar_documents, "best_fitting")
    return most_similar_documents


# def get_most_similar_documents_Llama2(message, amount):
#     df = db_get_df("transcript_segments_Llama_2")
#     question_embedding = document_embedding_LLama_2(message)

#     df["distance"] = [
#         cosine(question_embedding, json.loads(document_embedding))
#         for document_embedding in df["embedding_json"]
#     ]

#     most_similar_documents = df.nsmallest(amount, "distance")
#     most_similar_documents = enrich_all_segments(most_similar_documents)
#     db_save_df(most_similar_documents, "best_fitting")
#     return most_similar_documents


# print(get_most_similar_segments("TF_IDF_MINI_LM", "Oktoberfest Bayern", 4, 4))
