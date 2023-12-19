from pydub import AudioSegment
import io
import datetime
import json
from db_connect import db_get_df, db_save_df
import os

def delete_files_in_directory(directory):
    try:
        # Iterate through all files in the directory
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            
            # Check if it's a file (not a subdirectory) and delete it
            if os.path.isfile(file_path):
                os.remove(file_path)
        print(f"All files in {directory} deleted.")
    except Exception as e:
        print(f"Error deleting files: {str(e)}")


def split_audio(audio_filename, start, end):
    # print(len(audio_file))
    path = "/Users/br/Projects/Bachelorarbeit/data/Episode_audio_files/"
    audio_file = AudioSegment.from_file(path + audio_filename)
    start_time = start * 1000
    end_time = end * 1000
    segment = audio_file[start_time:end_time]
    return segment


def produce_snippets():

    # with open(ranked_json, 'r') as j:
    #     ranked_timestamped = json.loads(j.read())
    
    ranked_timestamped_df = db_get_df("best_fitting")
    path = "/Users/br/Projects/Bachelorarbeit/data/audio_segments"
    delete_files_in_directory(path)

    for i, row in ranked_timestamped_df.iterrows():
        audio_filename = row['filename'].replace('-', ' ').replace('.json','.mp3')
        start = row["start"] 
        end = row["end"]    
        audio_segment = split_audio(audio_filename, start, end)

        output_file = f"{path}/segment_{i}.mp3"
        audio_segment.export(output_file, format="mp3")
        print(f"Segment {i} saved as {output_file}")

