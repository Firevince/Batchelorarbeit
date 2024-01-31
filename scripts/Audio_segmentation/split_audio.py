import datetime
import io
import json
import os
from concurrent.futures import ThreadPoolExecutor

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
    
    with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        futures = []
        for i, row in best_fitting_df.iterrows():
            audio_filename = row['filename']
            start = row["start"]
            end = row["end"]
            output_file = os.path.join(AUDIO_SEGMENT_PATH, f"segment_{i}.wav")
            futures.append(executor.submit(split_audio, audio_filename, start, end, output_file))
            
        for future in futures:
            future.result() 



