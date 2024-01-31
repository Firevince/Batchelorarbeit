import os

from Audio_segmentation.concat_audio import produce_final_audio
from Audio_segmentation.get_audio_metadata import save_all_images
from Audio_segmentation.split_audio import produce_audio_snippets
from flask import Flask, render_template, request, send_from_directory
from segment_ranking.rank_segments import (get_most_similar_documents_Llama2,
                                           get_most_similar_documents_MINI_LM,
                                           get_most_similar_documents_tf_idf)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', text="text")

@app.route('/process', methods=['POST'])
def process():
    user_input_text = request.form['text']
    user_input_time = int(request.form['time'])

    # Führe die gewünschten Funktionen aus
    df_documents = get_most_similar_documents_tf_idf(user_input_text, user_input_time)
    df_documents = save_all_images(df_documents)
    produce_audio_snippets(df_documents)
    produce_final_audio()
    # text = ''
    # if not documents.empty:
    #     text = '\n'.join(row['sentence'] for _,row in documents.iterrows())
    rows = [row[1] for row in df_documents.iterrows()]
    print("ROWS")
    print(rows)
    # Sende das generierte Audio-Datei zurück
    audio_path = '../../concatenated_audio.mp3'
    return render_template('index.html', 
                           rows=rows)

@app.route('/api')
def api():
    user_input_text = request.args.get('text', default = '', type = str)
    user_input_time = int(request.args.get('time'), default = 3, type = int)
    documents = get_most_similar_documents_tf_idf(user_input_text, user_input_time)
    produce_audio_snippets(documents)
    produce_final_audio()
    return send_from_directory('audio', path='concatenated_audio.mp3')

@app.route('/audio/<filename>')
def audio(filename):
    return send_from_directory('audio', path=filename)

if __name__ == '__main__':
    app.run(debug=True)
