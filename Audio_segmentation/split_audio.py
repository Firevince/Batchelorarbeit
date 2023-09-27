from pydub import AudioSegment
import datetime
import json

def split_audio(input_audio_file, start, end):
    audio = AudioSegment.from_file(input_audio_file)

    start_time = start * 1000
    end_time = end * 1000
    segment = audio[start_time:end_time]
    return segment

# ranked_json is list of snippets
def produce_snippets(ranked_json):

    with open(ranked_json, 'r') as j:
        ranked_timestamped = json.loads(j.read())
     

    for i, segment in enumerate(ranked_timestamped):
        input_audio_file = "Podcast_files/" + segment["filename"] 
        start = segment["start"] 
        end = segment["end"]    
        audio_segment = split_audio(input_audio_file, start, end)

        output_file = f"Audio_segmentation/audio_segments/segment_{i}.mp3"
        audio_segment.export(output_file, format="mp3")
        print(f"Segment {i} saved as {output_file}")

produce_snippets("Audio_segmentation/mocked_ranked.json")
