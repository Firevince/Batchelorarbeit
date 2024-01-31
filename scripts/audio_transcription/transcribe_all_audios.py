import os

import pandas as pd
from db_connect import db_get_df, db_save_df
from faster_whisper_word_level import transcribe
from tqdm import tqdm

# directory = "/home/neumannvi84434/Bachelorarbeit/Bachelorarbeit/data/Episode_audio_files"
directory = "/nfs/scratch/students/neumannvi84434/Podcast_Episoden/"


try:
    df = db_get_df("transcript_word_level_2237")
except:
    data = {'filename': [], 'index': [], 'word': [], 'start': [], 'end': []}
    df = pd.DataFrame(data)

for filename in tqdm(os.listdir(directory)):
    path = os.path.join(directory, filename)
    if filename.endswith(".mp3") and path not in df["filename"].to_list():

        
        df_temp = transcribe(path)
        df = pd.concat([df,df_temp], ignore_index=True)
        db_save_df(df, "transcript_word_level_2237")
        print(f"TRANSCRIBED {filename}")