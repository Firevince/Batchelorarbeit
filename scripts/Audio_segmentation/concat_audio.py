from pydub import AudioSegment
import os

def concatenate_segments_with_sound(segment_files, output_file, sound_file, duration_between_segments_ms):
    concatenated_audio = AudioSegment.empty()

    for i, segment_file in enumerate(segment_files):
        segment = AudioSegment.from_file(segment_file)
        concatenated_audio += segment

    concatenated_audio.export(output_file, format="mp3")

if __name__ == "__main__":
    segment_files = []
    for filename in os.listdir("Audio_segmentation/audio_segments/"):
        segment_files.append("Audio_segmentation/audio_segments/" + filename)  

    output_file = "concatenated_audio.mp3" 
    sound_file = "beep.mp3"  
    duration_between_segments_ms = 1000 

    concatenate_segments_with_sound(segment_files, output_file, sound_file, duration_between_segments_ms)
