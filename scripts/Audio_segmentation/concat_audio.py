from pydub import AudioSegment
import os

def concatenate_segments_with_sound(segment_files, output_file, inbetween_sound_file):
    concatenated_audio = AudioSegment.empty()
    inbetween_sound = AudioSegment.from_file(inbetween_sound_file)

    for segment_file in segment_files:
        segment = AudioSegment.from_file(segment_file)
        concatenated_audio += inbetween_sound
        concatenated_audio += segment

    concatenated_audio.export(output_file, format="mp3")

def produce_audio():
    segment_files = []
    output_file = "/Users/br/Projects/Bachelorarbeit/scripts/server/audio/concatenated_audio.mp3" 
    inbetween_sound_file = "/Users/br/Projects/Bachelorarbeit/data/inter.wav"  
    path = "/Users/br/Projects/Bachelorarbeit/data/audio_segments/"

    for filename in os.listdir(path ):
        segment_files.append(path + filename)  


    concatenate_segments_with_sound(segment_files, output_file, inbetween_sound_file)
