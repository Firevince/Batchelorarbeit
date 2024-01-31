import json

import pandas as pd
from db_connect import db_get_df, db_save_df
from Embedding_creation.embedding_creator_llama_2 import document_embedding_LLama_2

# from Embedding_creation.embedding_creator_BERT import dokument_embedding
from Embedding_creation.embedding_creator_MINI_L6 import document_embedding_MINI_LM
from Embedding_creation.embedding_creator_TF_IDF import calculate_distances
from scipy.spatial.distance import cosine
from segment_ranking.chatgpt_help import gpt_order_segments


def enrich_segment(segment, transcript_df, num_prev_sentences=2, num_next_sentences=2):
    segment = segment.copy()
    segment_id = segment.loc["segment_id"]
    filename = segment.loc["filename"]
    print(filename)
    print(segment_id)

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


def enrich_segments(df_distance, df_all):
    enriched_segments_df = pd.concat(
        [enrich_segment(row, df_all) for _, row in df_distance.iterrows()]
    )
    enriched_segments_df = enriched_segments_df.reset_index(drop=True)
    return enriched_segments_df


def calculate_document_question_distance(sentence_embedding, document_embedding):
    diff_bank = cosine(sentence_embedding, document_embedding)
    return diff_bank


# def get_most_similar_documents_Bert(message, amount):
#     df = db_get_df(["filename", "segment_text", "embedding_json", "start", "end"],
#                    table="transcript_segments")
#     question_embedding = dokument_embedding(message)


#     df["distance"] = [calculate_document_question_distance(question_embedding, json.loads(document_embedding))for document_embedding in df["embedding_json"]]

#     most_similar_documents = df.nsmallest(amount, "distance")
#     db_save_df(most_similar_documents, "best_fitting")
#     return most_similar_documents


def get_most_similar_documents_MINI_LM(message, amount):
    df = db_get_df("transcript_segments_MiniLM_L6")
    question_embedding = document_embedding_MINI_LM(message)

    df["distance"] = [
        calculate_document_question_distance(
            question_embedding, json.loads(document_embedding)
        )
        for document_embedding in df["embedding_json"]
    ]

    most_similar_documents = df.nsmallest(amount, "distance")
    most_similar_documents = enrich_segments(most_similar_documents)
    db_save_df(most_similar_documents, "best_fitting")
    return most_similar_documents


def get_most_similar_documents_Llama2(message, amount):
    df = db_get_df("transcript_segments_Llama_2")
    question_embedding = document_embedding_LLama_2(message)

    df["distance"] = [
        calculate_document_question_distance(
            question_embedding, json.loads(document_embedding)
        )
        for document_embedding in df["embedding_json"]
    ]

    most_similar_documents = df.nsmallest(amount, "distance")
    most_similar_documents = enrich_segments(most_similar_documents)
    db_save_df(most_similar_documents, "best_fitting")
    return most_similar_documents


def get_most_similar_documents_tf_idf(message, amount):
    df = db_get_df(table="transcript_sentences")
    df_distance = calculate_distances(message, df)
    # reset_ index important
    df_distance = (
        df_distance.sort_values("distance").head(amount).reset_index(drop=True)
    )
    df_distance = enrich_segments(df_distance, df)

    print(df_distance["sentence"])
    print("asking chatgpt")
    df_distance = gpt_order_segments(df_distance)
    print(df_distance["sentence"])

    db_save_df(df_distance, "best_fitting")

    return df_distance


# sample_segment = pd.DataFrame(
#     # columns=[, , , , ],
#     index=[0],
#     data= {"filename": "jonathan-swift-gullivers-reisen-2.json",
#                "segment_text": "ARD. Radio Wissen. Die ganze Welt des Wissens. Ein Podcast von bayern 2 in der ARD-Audiothek.",
#                "segment_id": 5,
#                "start": 0.0,
#                "end": 13.92})

# print(get_surrounding_segments(sample_segment))
# print(extend_segment_time(sample_segment)[["filename","start", "end"]].to_markdown())
# with pd.option_context('display.max_colwidth', None,
#                        'display.max_columns', None,
#                        'display.max_rows', None):
#     print(get_most_similar_documents_MINI_LM("Oktoberfest in Bayern", 3)["segment_text"])

# print(get_most_similar_documents_Llama2("Reisen", 3))

# print(get_most_similar_documents_tf_idf("Oktoberfest", 8))
