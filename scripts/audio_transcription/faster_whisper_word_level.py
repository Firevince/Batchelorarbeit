from db_connect import db_get_df, db_save_df
from faster_whisper import WhisperModel
import pandas as pd
import torch

def transcribe(filename):
    device = "cuda" if torch.cuda.is_available() else "cpu"

    model_size = "medium"
    model = WhisperModel(model_size, device=device, compute_type="int8")

    segments, _ = model.transcribe(filename, word_timestamps=True)
    words = []
    for segment in segments:
        for i, word in enumerate(segment.words):
            # print("[%.2fs -> %.2fs] %s" % (word.start, word.end, word.word))
            words.append({"filename": filename, 
                          "index": i,
                          "word": word.word,
                          "start": word.start,
                          "end": word.end})
    df = pd.DataFrame(words)
    return df

