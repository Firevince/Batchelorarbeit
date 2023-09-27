import sqlite3
import pandas as pd
from transformers import BertModel, BertTokenizer
import torch
from tqdm import tqdm
from scipy.spatial.distance import cosine

model = BertModel.from_pretrained('bert-base-uncased')

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')



html_df["tokens"] = [tokenizer.tokenize(text) for text in html_df["text"]]
