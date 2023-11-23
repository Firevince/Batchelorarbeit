import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_distances
from tqdm import tqdm
from sklearn.metrics.pairwise import linear_kernel
from db_connect import db_get_df, db_save_df
import numpy as np
import json
import joblib


def calc_all_tf_idf():
    df = db_get_df(table="transcript_segments")
    tfidf_vectorizer = TfidfVectorizer()

    tfidf_matrix = tfidf_vectorizer.fit_transform(df['segment_text'])
    tfidf_array = tfidf_matrix.toarray()

    joblib.dump(tfidf_vectorizer, 'tfidf_vectorizer.pkl')
    df['tfidf_representation_json'] = df['segment_text'].apply(lambda x: json.dumps(tfidf_array[df.index[df['segment_text'] == x][0]].tolist()))
    db_save_df(df, tablename="transcript_segments_tf_idf")


def calculate_distances(message):
    df = db_get_df(table="transcript_segments_tf_idf")
    tfidf_vectorizer = joblib.load('tfidf_vectorizer.pkl')

    tfidf_vectorizer.fit(df['segment_text'])
    tfidf_message = tfidf_vectorizer.transform([message])

    df['tfidf_representation'] = [json.loads(rep) for rep in tqdm(df['tfidf_representation_json'])]

    distances = cosine_distances(tfidf_message, df["tfidf_representation"].tolist())
    df['distance'] = distances[0]
    df = df.drop(columns=['tfidf_representation', 'tfidf_representation_json'])

    return df


# calc_all_tf_idf()
# Example usage
# userInput = "Oktoberfest in Bayern"
# best = calculate_distances_and_return_top_5(userInput)
# print(best["segment_text"])

#TODO try save as multiindexed or seperate table