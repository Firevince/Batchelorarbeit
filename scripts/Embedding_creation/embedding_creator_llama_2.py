from transformers import AutoModel, AutoTokenizer
from sklearn.metrics.pairwise import cosine_similarity
from db_connect import db_get_df, db_save_df
import pandas as pd
from datetime import datetime


model = AutoModel.from_pretrained('mesolitica/llama2-embedding-1b-8k', trust_remote_code = True)
tokenizer = AutoTokenizer.from_pretrained('mesolitica/llama2-embedding-1b-8k')

df = db_get_df(["*"], "transcript_segments")

input_ids = tokenizer(
    df["segment_text"][1500:1800].to_list(), 
    return_tensors = 'pt',
    padding = True
) 
print(datetime.now(), " starting embedding calculation")
v = model.encode(input_ids).detach().numpy()
print(datetime.now(), " ended embedding calculation")

df = pd.DataFrame(v)
db_save_df(df, "transcript_segments_llama_2_y")

