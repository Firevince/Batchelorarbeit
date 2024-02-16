import os
from concurrent.futures import ThreadPoolExecutor

from audio_downloader.episodes_downloader import download_on_demand
from db_connect import db_get_df, db_save_df
from dotenv import load_dotenv
from pydub import AudioSegment
from utils.utils import delete_files_in_directory

load_dotenv(override=True)
AUDIO_SOURCE_PATH = os.getenv("AUDIO_SOURCE_PATH")
AUDIO_SEGMENT_PATH = os.getenv("AUDIO_SEGMENT_PATH")


def split_audio(audio_filename, start, end, output_file):
    file_path = os.path.join(AUDIO_SOURCE_PATH, audio_filename)
    if not os.path.isfile(file_path):
        print(f"File not found - downloading {audio_filename}")
        print(AUDIO_SOURCE_PATH)
        download_on_demand(audio_filename, AUDIO_SOURCE_PATH)

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
            audio_filename = row["filename"]
            start = row["start"]
            end = row["end"]
            output_file = os.path.join(AUDIO_SEGMENT_PATH, f"segment_{i}.wav")
            futures.append(executor.submit(split_audio, audio_filename, start, end, output_file))

        for future in futures:
            future.result()


# df = db_get_df("best_fitting")
# produce_audio_snippets(df)
