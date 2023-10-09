import sqlite3
import json
import tqdm
import os
from scripts.db_connect import db_insert_row


for filename in os.listdir("data/Episode_transcripts_timestamped"):
    # Load JSON data
    with open("data/Episode_transcripts_timestamped/" + filename, 'r') as file:
        json_data = json.load(file)

        # Insert data into the database
        db_insert_row(json_data, filename)
    

print("Data has been successfully inserted into the database.")
