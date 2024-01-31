import os

import joblib
import numpy as np
import spacy
from db_connect import db_get_df, load_npz, load_pkl, save_npz, save_pkl
from scipy import sparse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import pairwise_distances
from tqdm import tqdm


def calc_all_tf_idf():
    df = db_get_df(table="transcript_sentences")
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(df["sentence"])

    vocab_len = len(tfidf_vectorizer.get_vocab())

    vectorizer_name = f"tfidf_vectorizer{vocab_len//1000}k.pkl"
    matrix_name = f"tf_idf_matrix{vocab_len//1000}k.npz"
    save_pkl(tfidf_vectorizer, vectorizer_name)
    save_npz(tfidf_matrix, matrix_name)


def calculate_batchwise_distances(message_embedding, tfidf_matrix):
    all_distances = np.array([])

    batch_size = 1000
    for i in tqdm(range(0, tfidf_matrix.shape[0], batch_size)):
        batch_distances = pairwise_distances(
            tfidf_matrix[i : i + batch_size], message_embedding, metric="cosine"
        )
        all_distances = np.concatenate((all_distances, batch_distances.flatten()))

    return all_distances


def calculate_distances_batchwise(message, df):
    print("loading vectorizer")
    tfidf_vectorizer = load_pkl("tfidf_vectorizer_230k.pkl")
    tfidf_matrix = load_npz("tf_idf_matrix_230k.npz")

    print("calculating distances")
    tfidf_message = tfidf_vectorizer.transform([message])
    all_distances = calculate_batchwise_distances(tfidf_message, tfidf_matrix)

    df["distance"] = all_distances
    return df


## old code


def calculate_distances_old(message):
    df = db_get_df(table="transcript_sentences")
    tfidf_vectorizer = joblib.load("tfidf_vectorizer.pkl")
    tfidf_matrix = sparse.load_npz("tf_idf_matrix.npz")

    tfidf_message = tfidf_vectorizer.transform([message])
    # df['tfidf_representation'] = [json.loads(rep) for rep in tqdm(df['tfidf_representation_json'])]
    print("now calcing distances")
    tfidf_array = tfidf_matrix.toarray()
    all_distances = np.array([]).reshape(
        0,
    )
    batch = 1000
    for i in tqdm(range(0, len(tfidf_array) - 1, batch)):
        distances = pairwise_distances(tfidf_array[i : i + batch], tfidf_message)
        np.concatenate((all_distances, distances[0]), axis=0)
    print("finished")
    df["distance"] = all_distances[0]

    return df


def get_idf_from_doc(document):
    tfidf_vectorizer = joblib.load("tfidf_vectorizer.pkl")
    feature_names = tfidf_vectorizer.get_feature_names_out()
    idf_values = tfidf_vectorizer.idf_
    idf_dict = dict(zip(feature_names, idf_values))
    nlp = spacy.load("de_core_news_md")

    def lemmatize_german_sentence(input_sentence, nlp):
        doc = nlp(input_sentence)
        lemmatized_words = []
        for token in doc:
            lemma = token.lemma_
            if lemma:
                lemmatized_words.append(lemma)
            else:
                lemmatized_words.append(token)
        return lemmatized_words

    message_lemmatized = lemmatize_german_sentence(document, nlp)

    encoded_words = [
        (idf_dict[word.lower()], word)
        for word in message_lemmatized
        if word.lower() in idf_dict
    ]
    return encoded_words


def calculate_distances_custom(message):
    df = db_get_df(table="transcript_sentences")
    idf_values = get_idf_from_doc(message)
    words = sorted(idf_values, key=lambda x: x[0])[-1][1].lower()
    for sentence in tqdm(df["sentence"]):
        if word in sentence.lower():
            occurences.append(word)


# calc_all_tf_idf()
# Example usage
# userInput = "Oktoberfest in Bayern"
# best = calculate_distances_and_return_top_5(userInput)
# print(best["segment_text"])

# df = calculate_distances("Oktoberfest")
# print(df.sort_values(by="distance")["sentence"].head(5))

# calc_all_tf_idf()

# tfidf_vectorizer = joblib.load('tfidf_vectorizer_230k.pkl')
# print(len(tfidf_vectorizer.get_vocab()))

# TODO try save as multiindexed or seperate table
