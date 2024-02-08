import datetime
import io
import json
import os
from concurrent.futures import ThreadPoolExecutor

import requests
from db_connect import db_get_df, db_save_df
from dotenv import load_dotenv
from pydub import AudioSegment

load_dotenv()
AUDIO_SOURCE_PATH = os.getenv("AUDIO_SOURCE_PATH")
AUDIO_SEGMENT_PATH = os.getenv("AUDIO_SEGMENT_PATH")


def delete_files_in_directory(directory):
    try:
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
        print(f"All files in {directory} deleted.")
    except Exception as e:
        print(f"Error deleting files: {str(e)}")


def split_audio(audio_filename, start, end, output_file):
    file_path = os.path.join(AUDIO_SOURCE_PATH, audio_filename)
    audio_file = AudioSegment.from_file(file_path)
    start_time = start * 1000
    end_time = end * 1000
    segment = audio_file[start_time:end_time]
    segment.export(output_file, format="wav")
    print(f"Segment saved as {output_file}")


def produce_audio_snippets(best_fitting_df):
    delete_files_in_directory(AUDIO_SEGMENT_PATH)
    for i, row in best_fitting_df.iterrows():
        audio_filename = row["filename"]
        start = row["start"]
        end = row["end"]


# https://mcdn.br.de/br/hf/7t/b1/b1obb_20240201T092900+0100.mp4/clipFrom/189860/clipTo/222090/index.m3u8
