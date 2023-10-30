from pydub import AudioSegment
import os

def concatenate_segments_with_sound(segment_files, output_file, sound_file, duration_between_segments_ms):
    concatenated_audio = AudioSegment.empty()

    for i, segment_file in enumerate(segment_files):
        segment = AudioSegment.from_file(segment_file)
        concatenated_audio += segment

    concatenated_audio.export(output_file, format="mp3")

def produce_audio():
    segment_files = []
    path = "/Users/br/Projects/Bachelorarbeit/data/audio_segments/"
    for filename in os.listdir(path ):
        segment_files.append(path + filename)  

    output_file = "concatenated_audio.mp3" 
    sound_file = "beep.mp3"  
    duration_between_segments_ms = 1000 

    concatenate_segments_with_sound(segment_files, output_file, sound_file, duration_between_segments_ms)
