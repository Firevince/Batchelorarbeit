from datetime import datetime

import pandas as pd
from db_connect import db_get_df, db_save_df
from sklearn.metrics.pairwise import cosine_similarity
from transformers import AutoModel, AutoTokenizer


def calc_part():
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

def document_embedding_LLama_2(doc_text):
    model = AutoModel.from_pretrained('mesolitica/llama2-embedding-1b-8k', trust_remote_code = True)
    tokenizer = AutoTokenizer.from_pretrained('mesolitica/llama2-embedding-1b-8k')
   

    input_ids = tokenizer(
        doc_text, 
        return_tensors = 'pt',
        padding = True
    )
    doc_embedding = model.encode(input_ids).detach().numpy()[0]
    return doc_embedding

