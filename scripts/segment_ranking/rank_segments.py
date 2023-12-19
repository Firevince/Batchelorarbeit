from db_connect import db_get_df, db_save_df
from scipy.spatial.distance import cosine
from Embedding_creation.embedding_creator import dokument_embedding
from Embedding_creation.embedding_creator_MINI_L6 import document_embedding_MINI_LM
from Embedding_creation.TF_IDF_creator import calculate_distances
from Embedding_creation.embedding_creator_llama_2 import document_embedding_LLama_2
import json
import pandas as pd


def get_surrounding_segments(segment):
    # segment is vertical as are all 
    df = db_get_df(["filename", "segment_text", "segment_id", "start", "end"], table="transcript_segments")

    id = segment.loc["segment_id"]
    filename = segment.loc["filename"]

    filtered_rows = df[df["filename"] == filename]
    filtered_sorted_rows = filtered_rows.sort_values("segment_id").reset_index(drop=True)
    

    row_list = []
    if id >= 2 :
        row_list.append(filtered_sorted_rows.loc[id - 2].to_frame().T)
        row_list.append(filtered_sorted_rows.loc[id - 1].to_frame().T)

    row_list.append(segment.to_frame().T)

    if id < filtered_sorted_rows.loc[len(filtered_sorted_rows)-3, "segment_id"]:
        row_list.append(filtered_sorted_rows.loc[id + 1].to_frame().T)
        row_list.append(filtered_sorted_rows.loc[id + 2].to_frame().T)

    # print("1:", row_list[0])
    # print("2:", row_list[1])

    rich_segment_df = pd.concat(row_list, axis=0).reset_index(drop=True)
    print(rich_segment_df)
    print("done")
    return rich_segment_df

def extend_segment_time(segment):
    segment = segment.copy()
    # segment is vertical as are all 
    df = db_get_df("transcript_segments")
    id = segment.loc["segment_id"]
    filename = segment.loc["filename"]
    print(filename)
    print(id)
    filtered_rows = df[df["filename"] == filename]
    filtered_sorted_rows = filtered_rows.sort_values("segment_id").reset_index(drop=True)
    if id >= 2 :
        segment.loc["start"] = filtered_sorted_rows.loc[id - 2, "start"]

    if id < filtered_sorted_rows.loc[len(filtered_sorted_rows)-3, "segment_id"]:
        segment.loc["end"] = filtered_sorted_rows.loc[id + 2, "end"]
    return segment.to_frame().T

def enrich_segments(df):
    enriched_segments_df = extend_segment_time(df.iloc[0])
    
    for i in range(len(df)):
        enriched_segments_df = pd.concat([enriched_segments_df, extend_segment_time(df.iloc[i])]).reset_index(drop=True)

    print(enriched_segments_df)
    return enriched_segments_df


def calculate_document_question_distance(sentence_embedding, document_embedding):
    diff_bank = cosine(sentence_embedding, document_embedding)
    return diff_bank

def get_most_similar_documents_Bert(message, amount):
    df = db_get_df(["filename", "segment_text", "embedding_json", "start", "end"], 
                   table="transcript_segments")
    question_embedding = dokument_embedding(message)


    df["distance"] = [calculate_document_question_distance(question_embedding, json.loads(document_embedding))for document_embedding in df["embedding_json"]]

    most_similar_documents = df.nsmallest(amount, "distance")
    db_save_df(most_similar_documents, "best_fitting")
    return most_similar_documents


def get_most_similar_documents_MINI_LM(message, amount):
    df = db_get_df("transcript_segments_MiniLM_L6")
    question_embedding = document_embedding_MINI_LM(message)


    df["distance"] = [calculate_document_question_distance(question_embedding, json.loads(document_embedding))for document_embedding in df["embedding_json"]]

    most_similar_documents = df.nsmallest(amount, "distance")
    most_similar_documents = enrich_segments(most_similar_documents)
    db_save_df(most_similar_documents, "best_fitting")
    return most_similar_documents

def get_most_similar_documents_Llama2(message, amount):
    df = db_get_df("transcript_segments_Llama_2")
    question_embedding = document_embedding_LLama_2(message)

    df["distance"] = [calculate_document_question_distance(question_embedding, json.loads(document_embedding))for document_embedding in df["embedding_json"]]

    most_similar_documents = df.nsmallest(amount, "distance")
    most_similar_documents = enrich_segments(most_similar_documents)
    db_save_df(most_similar_documents, "best_fitting")
    return most_similar_documents

def get_most_similar_documents_tf_idf(message, amount):
    best_fitting = calculate_distances(message)
   
    # reset_ index important
    most_similar_documents = best_fitting.sort_values("distance").head(amount).reset_index(drop=True)

    most_similar_documents_enriched = enrich_segments(most_similar_documents)

    db_save_df(most_similar_documents_enriched, "best_fitting")

    return most_similar_documents_enriched

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