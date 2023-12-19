from db_connect import db_get_df, db_save_df
from faster_whisper import WhisperModel
import pandas as pd

def transcribe(filename):
    model_size = "base"
    model = WhisperModel(model_size, device="cpu", compute_type="int8")

    segments, _ = model.transcribe(filename, word_timestamps=True)
    words = []
    for segment in segments:
        for i, word in enumerate(segment.words):
            print("[%.2fs -> %.2fs] %s" % (word.start, word.end, word.word))
            words.append({"filename": filename, 
                          "index": i,
                          "word": word.word,
                          "start": word.start,
                          "end": word.end})
    df = pd.DataFrame(words)
    return df
