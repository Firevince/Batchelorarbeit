import sqlite3
import pandas as pd
import json
import os
from dotenv import load_dotenv

load_dotenv()
database_path = os.getenv("DATABASE_PATH")

def db_get_df(table="transcript_segments", coloumns=["*"]):
    con = sqlite3.connect(database_path)
    df = pd.read_sql_query(f"SELECT {', '.join(coloumns)} FROM {table}", con)
    con.close()
    return df

def db_save_df(df, tablename):
    with sqlite3.connect(database_path) as con:
        df.to_sql(tablename, con, index=False, if_exists='replace')


def db_insert_transcript_segment(data, filename):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    for item in data:
        print(item)
        cursor.execute('''
            INSERT INTO transcript_segments (
                filename,
                segment_id,
                segment_text,
                start,
                end,
                tokens,
                embedding
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            filename,
            item['id'],
            item['text'],
            item['start'],
            item['end'],
            json.dumps(item['tokens']),
            ''
        ))

    conn.commit()
    conn.close()

def create_table_transcript_segments():
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transcript_segments (
            filename TEXT,
            segment_id INTEGER,
            segment_text TEXT,
            start REAL,
            end REAL,
            tokens TEXT,
            embedding TEXT
        )
    ''')
    conn.commit()
    conn.close()

def create_table_transcripts():
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transcripts (
            filename TEXT,
            download_url TEXT,
            audio_binary BLOB,
            segment_count INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def db_insert_transcript(data):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO transcripts (
            filename,
            download_url,
            segment_count
        ) VALUES (?, ?, ?)
    ''', (
        data['filename'],
        data['download_url'],
        data['segment_count']
    ))

    conn.commit()
    conn.close()

def db_insert_audio_binary(audio_file, filename):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE transcripts SET audio_binary=?
        where filename=?''', 
        (audio_file, filename)
    )

    conn.commit()
    conn.close()

# 'https://media.neuland.br.de/file/2051900/c/feed/jonathan-swift-gullivers-reisen-2.mp3',
# 'https://media.neuland.br.de/file/2052706/c/feed/weltweite-lieferketten-wer-verbindet-wer-haelt-wer-bedroht-sie.mp3',
# 'https://media.neuland.br.de/file/1842747/c/feed/erben-und-vererben-was-steckt-hinter-dem-streit-ums-geld.mp3',
# 'https://media.neuland.br.de/file/1574984/c/feed/sozialer-wohnungsbau-geschichte-eines-umstrittenen-konzepts.mp3',
# 'https://media.neuland.br.de/file/1855770/c/feed/das-jahr-1000-als-die-globalisierung-begann-1.mp3',
# 'https://media.neuland.br.de/file/2052397/c/feed/vater-mutter-kind-ist-die-kleinfamilie-am-ende.mp3',
# 'https://media.neuland.br.de/file/1840258/c/feed/tierische-paar-ungs-geschichten-alles-natur.mp3',
# 'https://media.neuland.br.de/file/1810432/c/feed/oriana-fallaci-kompromisslos-stolz-und-unbequem-1.mp3',
# 'https://media.neuland.br.de/file/2046355/c/feed/ocker-die-edle-farbe-aus-der-erde-alles-natur.mp3',
# 'https://media.neuland.br.de/file/32581/c/feed/das-muenchener-oktoberfest-brotzeit-bier-und-belustigung.mp3',
# 'https://media.neuland.br.de/file/2051896/c/feed/die-legende-vom-sannikow-land-ein-paradies-im-eis.mp3',
# 'https://media.neuland.br.de/file/2039883/c/feed/das-erste-maschinenzeitalter-von-der-kuriositaet-zur-revolution-1.mp3',
# 'https://media.neuland.br.de/file/2041361/c/feed/autofiktion-wer-schreibt-hier-eigentlich.mp3',
# 'https://media.neuland.br.de/file/2041360/c/feed/das-pseudonym-geheimnis-oder-verkaufsstrategie.mp3'