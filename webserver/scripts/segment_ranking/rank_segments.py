import json

import numpy as np
import pandas as pd
import scipy.sparse as sparse
from db_connect import db_get_df, db_save_df, load_npz, load_pkl
from scipy.spatial.distance import cosine
from segment_ranking.chatgpt_help import gpt_order_segments, gpt_segment_boundaries
from segment_ranking.chromadb_connect import (
    get_most_similar_documents_openai,
    get_most_similar_documents_voyage,
)
from sklearn.metrics.pairwise import pairwise_distances
from tqdm import tqdm


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


def enrich_all_segments_gpt(df_distance, df_all, query):
    segments = []
    for filename in df_distance["filename"].unique():
        df_file = df_all[df_all["filename"] == filename].reset_index(drop=True)
        df_segment = gpt_segment_boundaries(df_file, query)
        segments.append(df_segment)

    df_segments = pd.concat(segments)
    df_segments = df_segment.reset_index(drop=True)
    print(df_segments)
    return df_segments


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

    most_similar_documents = None
    df = db_get_df("transcript_sentences")

    if model_type == "OPENAI":
        most_similar_documents = get_most_similar_documents_openai(message, amount)
    else:
        raise Exception("Modeltype not supported")

    # most_similar_documents = enrich_all_segments_gpt(most_similar_documents, df, message)
    most_similar_documents = enrich_all_segments(most_similar_documents, df, segment_size)

    if sort_gpt:
        most_similar_documents = gpt_order_segments(most_similar_documents)

    return most_similar_documents
