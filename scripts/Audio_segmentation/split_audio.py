from pydub import AudioSegment
import io
import datetime
import json
from db_connect import db_get_df, db_save_df
import os
from dotenv import load_dotenv

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


def split_audio(audio_filename, start, end):
    file_path = os.path.join(AUDIO_SOURCE_PATH, audio_filename)
    audio_file = AudioSegment.from_file(file_path)
    start_time = start * 1000
    end_time = end * 1000
    segment = audio_file[start_time:end_time]
    return segment


def produce_audio_snippets(best_fitting_df):    
    # ranked_timestamped_df = db_get_df("best_fitting")
    delete_files_in_directory(AUDIO_SEGMENT_PATH)

    for i, row in best_fitting_df.iterrows():
        audio_filename = row['filename']
        start = row["start"] 
        end = row["end"]    
        audio_segment = split_audio(audio_filename, start, end)

        output_file = os.path.join(AUDIO_SEGMENT_PATH, f"segment_{i}.mp3")
        audio_segment.export(output_file, format="mp3")
        print(f"Segment {i} saved as {output_file}")

