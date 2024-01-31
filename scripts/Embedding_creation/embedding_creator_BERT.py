import torch
from transformers import BertModel, BertTokenizer


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
    
    token_embeddings = torch.stack(hidden_states, dim=0)
    token_embeddings = torch.squeeze(token_embeddings, dim=1)
    token_embeddings = token_embeddings.permute(1,0,2)
    layer_vecs = torch.mean(token_embeddings, dim=0)

    embed_2 = torch.mean(layer_vecs[2:], dim=0)
    return embed_2
    


