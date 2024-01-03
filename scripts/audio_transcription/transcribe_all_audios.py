from db_connect import db_get_df, db_save_df
from faster_whisper_word_level import transcribe
import os
import pandas as pd
from tqdm import tqdm

directory = "/home/neumannvi84434/Bachelorarbeit/Bachelorarbeit/data/Episode_audio_files"

# Loop through all files in the directory
data = {'filename': [], 'index': [], 'word': [], 'start': [], 'end': []}
df = pd.DataFrame(data)
for filename in tqdm(os.listdir(directory)):
    if filename.endswith(".mp3"):
        path = directory + "/" + filename
        df_temp = transcribe(path)
        df = pd.concat([df,df_temp], ignore_index=True)

db_save_df(df, "transcript_word_level")