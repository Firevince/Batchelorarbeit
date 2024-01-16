import os
from flask import Flask, render_template, request, send_from_directory
from segment_ranking.rank_segments import get_most_similar_documents_Bert, get_most_similar_documents_tf_idf, get_most_similar_documents_MINI_LM, get_most_similar_documents_Llama2
from Audio_segmentation.split_audio import produce_snippets
from Audio_segmentation.concat_audio import produce_audio

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    user_input_text = request.form['text']
    user_input_time = int(request.form['time'])

    # Führe die gewünschten Funktionen aus
    get_most_similar_documents_tf_idf(user_input_text, user_input_time)
    produce_snippets()
    produce_audio()

    # Sende das generierte Audio-Datei zurück
    audio_path = '../../concatenated_audio.mp3'
    return render_template('index.html')

@app.route('/audio/<filename>')
def audio(filename):
    return send_from_directory('audio', path=filename)

if __name__ == '__main__':
    app.run(debug=True)
