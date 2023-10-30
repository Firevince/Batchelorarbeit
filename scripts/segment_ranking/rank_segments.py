from db_connect import db_get_df, db_save_df
from scipy.spatial.distance import cosine
from Embedding_creation.embedding_creator import dokument_embedding
import json


def calculate_document_question_distance(sentence_embedding,document_embedding):
    
    # Calculate the cosine similarity between question and document
    diff_bank = 1 - cosine(sentence_embedding, document_embedding)

    # print('Vector similarity for *different* meanings:  %.2f' % diff_bank)
    return diff_bank

def get_most_similar_documents(message, amount):
    # Initialisiere den DataFrame mit der Funktion aus db_init.py
    print("saved")
    df = db_get_df(["filename", "segment_text", "embedding_json", "start", "end"], table="transcript_segments")
    question_embedding = dokument_embedding(message)
    df["distance"] = [calculate_document_question_distance(question_embedding, json.loads(document_embedding))for document_embedding in df["embedding_json"]]
    most_similar_documents = df.nsmallest(amount, "distance")
    db_save_df(most_similar_documents, "best_fitting")
    return most_similar_documents

# user_input = "gulliver"
# db_save_df(get_5_most_similar_documents(user_input), "best_fitting")
