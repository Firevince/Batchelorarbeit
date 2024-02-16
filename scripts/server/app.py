import html
import json
import os

from audio_downloader.episodes_downloader import download_on_demand
from audio_segmentation.concat_audio import produce_final_audio
from audio_segmentation.get_audio_metadata import save_all_images
from audio_segmentation.split_audio import produce_audio_snippets
from db_connect import db_append_df, db_get_df, db_save_df
from flask import Flask, jsonify, render_template, request, send_from_directory
from flask_assets import Bundle, Environment
from player import mocked_data
from segment_ranking.chatgpt_help import gpt_get_keywords
from segment_ranking.rank_segments import get_most_similar_segments

app = Flask(__name__)

assets = Environment(app)
assets.url = app.static_url_path
scss = Bundle("css/scss/player.scss", filters="pyscss", output="all.css")


assets.config["SECRET_KEY"] = "secret!"
assets.config["PYSCSS_LOAD_PATHS"] = assets.load_path
assets.config["PYSCSS_STATIC_URL"] = assets.url
assets.config["PYSCSS_STATIC_ROOT"] = assets.directory
assets.config["PYSCSS_ASSETS_URL"] = assets.url
assets.config["PYSCSS_ASSETS_ROOT"] = assets.directory

assets.register("scss_all", scss)


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

    df_documents, audio_filename = produce_audio(user_input_text, user_input_time)

    save_all_images(df_documents)
    keywords = gpt_get_keywords(df_documents)
    rows = [row[1] for row in df_documents.iterrows()]

    return render_template(
        "index.html", rows=rows, keywords=keywords, audio_filename=audio_filename
    )


def produce_audio(user_query, time):
    print(f"processing '{user_query}' for {time} minutes")
    documents_df = get_most_similar_segments("TF_IDF", user_query, time, 5)
    produce_audio_snippets(documents_df)
    out_filename = html.escape(user_query) + ".mp3"

    documents_df["out_filename"] = [out_filename] * len(documents_df)
    db_append_df(documents_df, "best_fitting")

    print("OUTFILE", out_filename)
    produce_final_audio(out_filename)
    return (documents_df, out_filename)


@app.route("/api")
def api():
    user_input_text = request.args.get("text", default="", type=str)
    user_input_time = int(request.args.get("time", default=5))
    _, out_filename = produce_audio(user_input_text, user_input_time)
    return_dict = {"url": os.path.join("/static/audio", out_filename)}
    return jsonify(return_dict)


@app.route("/player")
def player():
    currentTrack = {
        "name": "Hello World",
        "Artist": "Domingi",
        "cover": "static/images/cover_0.jpg",
    }
    duration = 100
    time = "yesterday"
    return render_template("player.html", currentTrack=currentTrack, duration=duration, time=time)


@app.route("/tracks")
def tracks():
    df = db_get_df("best_fitting")
    data = []
    for out_filename in df["out_filename"].unique():
        title = out_filename
        source = os.path.join("/static/audio", out_filename)
        author = "Podcast Generator"
        df_temp = df[df["out_filename"] == out_filename]
        transcript_sentences = df_temp["sentence"].to_list()
        audio = {
            "title": title,
            "source": source,
            "author": author,
            "sentences": transcript_sentences,
        }
        data.append(audio)

    return jsonify(data)


@app.route("/audio/<filename>")
def audio(filename):
    return send_from_directory("audio", path=filename)


if __name__ == "__main__":
    app.run(debug=True)
