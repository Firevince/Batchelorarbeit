import pandas as pd
from scripts.db_connect import db_get_df, db_save_df, db_insert_transcript, db_insert_audio_binary
from episodes_downloader import get_names_and_urls_all_episodes

df = db_get_df(["filename", "download_url"], table="transcripts")
for index, row in df.iterrows():
    titles, audio_urls = get_names_and_urls_all_episodes()
    