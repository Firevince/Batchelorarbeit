import sqlite3
import pandas as pd
import json

database_path = "data/transcripts.sqlite"

def db_get_df(coloumns=["*"], table="transcript_segments"):
    con = sqlite3.connect(database_path)
    df = pd.read_sql_query(f"SELECT {', '.join(coloumns)} FROM {table}", con)
    con.close()
    return df

def db_save_df(df, tablename):
    with sqlite3.connect(database_path) as con:
        df.to_sql(tablename, con, index=False, if_exists='replace')


def db_insert_row(data, filename):
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

def create_database():
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



