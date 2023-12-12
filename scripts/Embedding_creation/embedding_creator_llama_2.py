from transformers import AutoModel, AutoTokenizer
from sklearn.metrics.pairwise import cosine_similarity
from db_connect import db_get_df, db_save_df
import pandas as pd
from datetime import datetime


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

