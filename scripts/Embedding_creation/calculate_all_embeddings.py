import json

from db_connect import db_get_df, db_save_df, save_pkl
from embedding_creator_MINI_L6 import all_document_embeddings_batchwise_MINI_LM
from tqdm import tqdm

from scripts.Embedding_creation.embedding_creator_BERT import dokument_embedding

# embed_func = document_embedding_MINI_LM
# df = db_get_df(["filename", "segment_text", "start", "end", "segment_id"])
# df["embedding_json"] = [json.dumps(embed_func(chunk_text).tolist()) for chunk_text in tqdm(df["segment_text"])]
# db_save_df(df, "transcript_segments_MiniLM_L6")


def calc_all_MINI_L6():
    df = db_get_df("transcript_sentences")
    embeddings = all_document_embeddings_batchwise_MINI_LM(df["sentence"].to_list())
    save_pkl(df["sentence"], embeddings, "MINI_L6_embeddings.pkl")


calc_all_MINI_L6()
