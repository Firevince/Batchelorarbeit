import whisper
import json
import os
from tqdm import tqdm

model = whisper.load_model("medium")



for filename in tqdm(os.listdir("Podcast_files")):
    result = model.transcribe(f"Podcast_files/{filename}")
    with open(f"Podcast_transcripts_timestamped/{filename.replace('.mp3', '.json')}", "w") as file:
        file.write(json.dumps(result["segments"]))

