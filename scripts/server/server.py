import json
import os

from audio_segmentation.concat_audio import produce_final_audio
from audio_segmentation.get_audio_metadata import save_all_images
from audio_segmentation.split_audio import produce_audio_snippets
from flask import Flask, jsonify, render_template, request, send_from_directory
from segment_ranking.chatgpt_help import gpt_get_keywords
from segment_ranking.rank_segments import get_most_similar_segments

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", text="text")


@app.route("/process", methods=["POST"])
def process():
    user_input_text = request.form["text"]
    user_input_time = int(request.form["time"])
    print(f"processing {user_input_text} for {user_input_time} minutes")

    df_documents = get_most_similar_segments("TF_IDF_MINI_LM", user_input_text, user_input_time, 3)

    df_documents = save_all_images(df_documents)
    produce_audio_snippets(df_documents)
    produce_final_audio()

    keywords = gpt_get_keywords(df_documents)

    rows = [row[1] for row in df_documents.iterrows()]

    return render_template("index.html", rows=rows, keywords=keywords)


@app.route("/api")
def api():
    user_input_text = request.args.get("text", default="", type=str)
    user_input_time = int(request.args.get("time", default=5))
    print(f"processing {user_input_text} for {user_input_time} minutes")
    documents = get_most_similar_segments("TF_IDF_MINI_LM", user_input_text, user_input_time)
    produce_audio_snippets(documents)
    produce_final_audio()
    return_dict = {"url": "/static/audio/concatenated_audio.mp3"}
    return jsonify(return_dict)


@app.route("/audio/<filename>")
def audio(filename):
    return send_from_directory("audio", path=filename)


if __name__ == "__main__":
    app.run(debug=True)
