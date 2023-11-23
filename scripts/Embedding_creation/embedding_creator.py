import sqlite3
import pandas as pd
from db_connect import db_get_df, db_save_df
from transformers import BertModel, BertTokenizer
import torch
from tqdm import tqdm
from scipy.spatial.distance import cosine
import json


def dokument_embedding(dokument_text):
    tokenizer = BertTokenizer.from_pretrained('bert-base-german-cased')
    model = BertModel.from_pretrained('bert-base-german-cased', output_hidden_states = True)

    dokument_text = "[CLS]" + dokument_text + "[SEP]"
    tokens = tokenizer.tokenize(dokument_text)
    attetion_mask = [0 if token == "[PAD]" else 1 for token in tokens]
    token_idss = tokenizer.convert_tokens_to_ids(tokens)
    tokens_tensor = torch.tensor([token_idss])
    attetion_mask_tensor = torch.tensor([attetion_mask])

    with torch.no_grad():
        outputs = model(tokens_tensor, attetion_mask_tensor)
        hidden_states = outputs[2]
    

   
    # stack the layer list 
    token_embeddings = torch.stack(hidden_states, dim=0)
    # remove the batches dim
    token_embeddings = torch.squeeze(token_embeddings, dim=1)
    # Swap dimensions 0 and 1.
    token_embeddings = token_embeddings.permute(1,0,2)
    # average all token embeds
    layer_vecs = torch.mean(token_embeddings, dim=0)


    # # last layer
    # embed_1 = layer_vecs[12]

    # Calculate the average of layer 3 to 13
    embed_2 = torch.mean(layer_vecs[2:], dim=0)

    # # sum of layer 3 to 13
    # embed_3 = layer_vecs[2:].sum(0)

    # # sum of last four layer
    # embed_4 = layer_vecs[-4:].sum(0) 

    # #concat last four layers
    # embed_5 = torch.cat([layer_vecs[i] for i in [-1,-2,-3,-4]], dim=0)
    

    return embed_2
    


