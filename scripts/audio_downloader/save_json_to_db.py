import json
import os

from scripts.db_connect import db_insert_transcript

for filename in os.listdir("data/Episode_transcripts_timestamped"):
    # Load JSON data
    with open("data/Episode_transcripts_timestamped/" + filename, 'r') as file:
        json_data = json.load(file)
        row = {"filename":filename.replace(".json", "").replace("-", " "),
               "audio_binary": None,
               "download_url": None,
               "segment_count": len(json_data)}
        # Insert data into the database
        db_insert_transcript(row)