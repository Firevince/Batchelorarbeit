import os
import requests
import pandas as pd
from scripts.db_connect import db_get_df, db_save_df, db_insert_transcript, db_insert_audio_binary
import sqlite3


graphql_url = "https://api.ardaudiothek.de/graphql"


def download_mp3(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Downloaded MP3")
            return response.content
        else:
            print(f"Failed to download MP3. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    return None

def get_graphql(query):
    response = requests.post(graphql_url, json={"query": query})

    # df = df = pd.DataFrame()

    if response.status_code == 200:
        return response.json()
    else:
        raise f"GraphQL request failed with status code {response.status_code}"

def download_newest_episodes():

    # GraphQL query
    query = """
    {
        programSet(id: 5945518) {
        title
        items(
            orderBy: PUBLISH_DATE_DESC
            filter: {
            isPublished: {
                equalTo: true
            }
            }
            first: 10
        ) {
            nodes {
            audios {
                downloadUrl
            }
            }
        }
        }
    }
    """
    data = get_graphql(query)
    df = db_get_df(["url", "filename", "file_path", "transkript", "audio_file", "tokens", "embedding"])

    download_dir = "./Episode_files"
    os.makedirs(download_dir, exist_ok=True)
    for audio_data in data["data"]["programSet"]["items"]["nodes"]:

        audio_url = audio_data["audios"][0]["downloadUrl"]
        if (df['url'].eq(audio_url)).any():
            continue


        filename = os.path.basename(audio_url)
        file_path = os.path.join(download_dir, filename)

        audio_file = download_mp3(audio_url)
        
        df_entry = {'url': audio_url, 'filename': filename, 'file_path': file_path, 'audio_file': audio_file,'transkript': None, 'tokens': None, 'embedding': None}
        df = df._append(df_entry, ignore_index=True)

    db_save_df(df, "transcripts")


def download_episode_from_name(name):
    query = """
    {{
      programSet(id: 5945518) {{
        title
        items(
          orderBy: PUBLISH_DATE_DESC
          filter: {{
            isPublished: {{
              equalTo: true
            }}
            title:{{
                equalTo:"{name}"
              }}
          }}
          first: 10
        ) {{
          nodes {{
            audios {{
              downloadUrl
            }}
          }}
        }}
      }}
    }}
    """.format(name=name)
    data = get_graphql(query)
    print(query)
    print(data)
    audio_url = data["data"]["programSet"]["items"]["nodes"][0]["audios"][0]["downloadUrl"]
    audio_file = download_mp3(audio_url)
    db_insert_transcript({"filename":name, "download_url":audio_url, "audio_binary":audio_file, "segment_count":0})

    print(query)


def download_url_and_insert_binary(url, filename):
    
    audio = download_mp3(url)
    db_insert_audio_binary(audio, filename)


df = db_get_df(["filename", "download_url"], table="transcripts")
for index, row in df.iterrows():
    download_url_and_insert_binary(row['download_url'], row['filename'])