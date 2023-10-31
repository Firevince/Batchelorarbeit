import os
from flask import Flask, render_template, request, send_file
from your_module import get_most_similar_documents, produce_snippets, produce_audio

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    user_input_text = request.form['text']
    user_input_time = int(request.form['time'])

    # Führe die gewünschten Funktionen aus
    get_most_similar_documents(user_input_text, user_input_time)
    produce_snippets()
    produce_audio()

    # Sende das generierte Audio-Datei zurück
    audio_path = 'temp.mp3'
    return send_file(audio_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
