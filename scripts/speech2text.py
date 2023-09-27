import whisper
import json
import os
from tqdm import tqdm

model = whisper.load_model("medium")



for filename in tqdm(os.listdir("Episode_files")):
    result = model.transcribe(f"Episode_files/{filename}")
    with open(f"Episode_transcripts_timestamped/{filename.replace('.mp3', '.json')}", "w") as file:
        file.write(json.dumps(result["segments"]))

