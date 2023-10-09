from transformers import  BertTokenizer
from db_connect import db_get_df, db_save_df

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

df = db_get_df("data/transcripts.sqlite", ["url", "filename", "file_path", "transcript", "audio_file", "tokens", "embedding"])
df["tokens"] = [tokenizer.tokenize(transcript) for transcript in df["transcript"]]
db_save_df("data/transcripts.sqlite", df, "transcripts")