import html
import json
import os

from audio_downloader.episodes_downloader import download_on_demand
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
def process_web_post():
    user_input_text = request.form["text"]
    user_input_time = int(request.form["time"])
    return process_web(user_input_text, user_input_time)


@app.route("/process", methods=["GET"])
def process_web_get():
    user_input_text = request.args.get("text", default="", type=str)
    user_input_time = int(request.args.get("time", default=5))
    return process_web(user_input_text, user_input_time)


def process_web(user_input_text, user_input_time):

    df_documents, out_filename = produce_audio(user_input_text, user_input_time)

    save_all_images(df_documents)
    keywords = gpt_get_keywords(df_documents)
    rows = [row[1] for row in df_documents.iterrows()]

    return render_template("index.html", rows=rows, keywords=keywords)


def produce_audio(user_query, time):
    print(f"processing '{user_query}' for {time} minutes")
    documents = get_most_similar_segments("TF_IDF", user_query, time, 5)
    produce_audio_snippets(documents)
    out_filename = html.escape(user_query)
    produce_final_audio(out_filename)
    return (documents, out_filename)


@app.route("/api")
def api():
    user_input_text = request.args.get("text", default="", type=str)
    user_input_time = int(request.args.get("time", default=5))
    _, out_filename = produce_audio(user_input_text, user_input_time)
    return_dict = {"url": os.path.join("/static/audio", out_filename)}
    return jsonify(return_dict)


@app.route("/audio/<filename>")
def audio(filename):
    return send_from_directory("audio", path=filename)


if __name__ == "__main__":
    app.run(debug=True)
