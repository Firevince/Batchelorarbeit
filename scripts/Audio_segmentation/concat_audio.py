import os

from dotenv import load_dotenv
from pydub import AudioSegment

load_dotenv()
DATA_PATH = os.getenv("DATA_PATH")
SERVER_PATH = os.getenv("SERVER_PATH")


def concatenate_segments_with_sound(segment_files, output_file, inbetween_sound_file):
    concatenated_audio = AudioSegment.empty()
    inbetween_sound = AudioSegment.from_file(inbetween_sound_file)

    for segment_file in segment_files:
        segment = AudioSegment.from_file(segment_file)
        concatenated_audio += inbetween_sound
        concatenated_audio += segment
    concatenated_audio.export(output_file, format="mp3")


def produce_final_audio(out_filename):
    segment_files = []
    output_file = os.path.join(SERVER_PATH, "static/audio", out_filename)
    inbetween_sound_file = os.path.join(DATA_PATH, "inter.wav")
    snippets_path = os.path.join(DATA_PATH, "audio_segments/")

    for filename in os.listdir(snippets_path):
        segment_files.append(snippets_path + filename)

    concatenate_segments_with_sound(segment_files, output_file, inbetween_sound_file)
