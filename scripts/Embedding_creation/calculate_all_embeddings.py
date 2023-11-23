from db_connect import db_get_df, db_save_df
from tqdm import tqdm
import json
from embedding_creator import dokument_embedding


df = db_get_df(["filename", "segment_text", "start", "end", "segment_id"])
df["embedding_json"] = [json.dumps(dokument_embedding(chunk_text).tolist()) for chunk_text in tqdm(df["segment_text"])]
db_save_df(df, "transcript_segments_MiniLM_L6")