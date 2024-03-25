import json
import os
import random

import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
API_KEY = os.getenv("OPENAI_KEY")
client = OpenAI(api_key=API_KEY)


def ask_gpt_json(system_prompt, user_prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": f"""
                    {system_prompt}
                """,
            },
            {"role": "user", "content": user_prompt},
        ],
    )
    try:
        response_json = json.loads(response.choices[0].message.content)
    except:
        print("Answer not in right format - no keywords found")

    return response_json


def gpt_get_keywords(df):
    query = "\n".join(df["sentence"])

    system_prompt = """
            Schreibe 5 weiterführende Themenüberschriften, die zu diesen Textabschnitten passen.
            Sie sollen spezifisch auf eine Sache aus diesem Abschnitt abzielen, oder ein ähnliches Thema beschreiben. 
            Jede Themenüberschrift soll aus 1-3 Wörtern Stichwörtern bestehen.
            Antworte in JSON Format als ein Array 'Themen' in welchem nur die Themen stehen 
            """
    user_prompt = query

    response = ask_gpt_json(system_prompt, user_prompt)
    keywords = response["Themen"]

    return keywords


def gpt_order_segments(df):
    query = [f"{i+1}: {segment}" for i, segment in enumerate(df["sentence"])]
    query = "\n".join(query)
    # print(query)

    system_prompt = """
            Bringe die Abschnitte in eine logische Reihenfolge.
            Antworte in JSON Format als ein Array 'Reihenfolge' in welchem nur die Nummern der Segmente stehen """
    user_prompt = query

    response = ask_gpt_json(system_prompt, user_prompt)
    try:
        order = response["Reihenfolge"]
        df["order"] = order
        df = df.sort_values("order").reset_index(drop=True)

    except:
        print("Answer not in right format - using default order")
        # TODO retry chatgpt

    return df


def gpt_filter_segments(df, query):
    segments = [f"{i+1}: {segment}" for i, segment in enumerate(df["sentence"])]
    segments = "\n".join(segments)
    # print(query)

    system_prompt = f"""
            Sortiere aus den folgenden Segmenten die aus, die nicht ao gut zu der Frage passen.
            Bringe die Abschnitte in eine logische Reihenfolge.
            {segments}
            Antworte in JSON Format als ein Array 'Reihenfolge' in welchem nur die Nummern der Segmente stehen, die zu der Frage passen in der Reihenfolge wie sie aufeinander folgen sollen.
            """
    user_prompt = query

    response = ask_gpt_json(system_prompt, user_prompt)

    try:
        order = json.loads(response.choices[0].message.content)["Reihenfolge"]
        df["order"] = order
        df = df.sort_values("order").reset_index(drop=True)

    except:
        print("Answer not in right format - using default order")
        # TODO retry chatgpt
    return df


def gpt_segment_boundaries(df_file, query):
    sentences = [f"{i}: {sentence}" for i, sentence in enumerate(df_file["sentence"])]
    document = "\n".join(sentences)

    system_prompt = f"""
            Schau dir das folgende Dokument an und wähle aus, welcher Abschnitt zur Beantwortung der Frage geeignet ist.

            {document}

            Antworte in JSON Format mit einem Text 'Begründung', der beschreibt warum dieser Textausschnitt dazu passt. 
            Außerdem einen 'Start' für die Nummer des Satzes, ab dem der Abschnitt beginnt und 
            einem 'Ende' für die Nummer des Satzes wo der Abschnitt aufhört.
            Wenn es keinen Abschnitt gibt der wirklich passt, antworte mit 'Start': 0 und 'Ende':0"""
    user_prompt = query

    response = ask_gpt_json(system_prompt, user_prompt)
    print(response)
    try:
        start = int(response["Start"])
        end = int(response["Ende"])
        segment_df = pd.DataFrame(
            {
                "filename": df_file.loc[0, "filename"],
                "start": df_file.loc[start, "start"],
                "end": df_file.loc[end, "end"],
                "sentence": "\n".join(df_file.loc[start:end, "sentence"]),
                "segment_id": 0,
            },
            index=[random.randint(0, 1000000)],
        )

    except Exception as e:
        print(e)
        # print("Answer not in right format - returning empty df")s
        segment_df = df_file.iloc[0:0]
    return segment_df


def gpt_expand_topic(query):
    expanded_query = query

    system_prompt = f"""
                Du bist ein Assistent der Themen erweitert.
                Spezifiziere folgendes Thema, indem du weitere interessante Aspekte hinzufügst, die dazu passen.
                Antworte im JSON format mit einem String "Thema"
                Beispiele:
                User: Oktoberfest
                Assistent: Oktoberfest auf der Theresienwiese mit Bier und Trachten
                User: Nürnberg
                Assistent: Nürnberg Kaiserburg, Lebkuchen, Albrecht Dürer
                """
    user_prompt = f"User: {query}"

    response = ask_gpt_json(system_prompt, user_prompt)

    try:
        expanded_query = json.loads(response.choices[0].message.content)["Thema"]
    except:
        print("Answer not in right format - using default query")

    return expanded_query


# gpt_sosrt()


# if response.status_code == 200:
#     # Print the response from ChatGPT
# else:
#     print(f"Request failed with status code {response.status_code}:")
#     print(response.text)

# unsortiert
# 1. Die Siedlung wuchs, wurde zu einem kleinen Hafen, und am 27. Oktober 1275 wurde Amsterdam von Graf Florens V. von Holland erstmals urkundlich erwähnt, noch als Amstelledamme.
# 2. Danach blieb der Widerstand in Amsterdam lange Zeit schwach.
# 3. Die niederländischen Rebellen blockierten nun den Amsterdamer Hafen, so dass die Stadt schnell verarmte.
# 4. Die Geschichte der Stadt Amsterdam reicht bis in die Römerzeit zurück.
# 5. Während der Zeit entwickelte sich Amsterdam von einer auf Pfählen gebauten Siedlung zu der über 800.000 Einwohner zählenden Hauptstadt der Niederlande.
# 6. Um das Jahr 1250 entstanden die ersten von Bauern und Fischern bewohnten Siedlungen bei Amsterdam.
# 7. Demonstranten zogen durch die Straßen und riefen: „Weg mit den Judenpogromen!“
# 8. Züge und Straßenbahnen standen still, Werft- und Fabrikarbeiter legten die Arbeit nieder.
# 9. Die in die Stadt kommenden Kaufleute lehnten sich gegen die vom Adel unterstützten Katholiken auf.
# 10. Erst als sich 1943 die deutsche Niederlage abzeichnete, entwickelte sich eine breitere Bewegung.
# 11. Am nächsten Tag wurde der Streik brutal unterdrückt.
# sortiert
#  1. Die Geschichte der Stadt Amsterdam reicht bis in die Römerzeit zurück.
#  2. Während der Zeit entwickelte sich Amsterdam von einer auf Pfählen gebauten Siedlung zu der über 800.000 Einwohner zählenden Hauptstadt der Niederlande.
#  3. Um das Jahr 1250 entstanden die ersten von Bauern und Fischern bewohnten Siedlungen bei Amsterdam.
#  4. Die Siedlung wuchs, wurde zu einem kleinen Hafen, und am 27. Oktober 1275 wurde Amsterdam von Graf Florens V. von Holland erstmals urkundlich erwähnt, noch als Amstelledamme.
#  5. Die in die Stadt kommenden Kaufleute lehnten sich gegen die vom Adel unterstützten Katholiken auf.
#  6. Die niederländischen Rebellen blockierten nun den Amsterdamer Hafen, so dass die Stadt schnell verarmte.
#  7. Züge und Straßenbahnen standen still, Werft- und Fabrikarbeiter legten die Arbeit nieder.
#  8. Demonstranten zogen durch die Straßen und riefen: „Weg mit den Judenpogromen!“
#  9. Am nächsten Tag wurde der Streik brutal unterdrückt.
#  10. Danach blieb der Widerstand in Amsterdam lange Zeit schwach.
#  11. Erst als sich 1943 die deutsche Niederlage abzeichnete, entwickelte sich eine breitere Bewegung."""}


# client = OpenAI(api_key=API_KEY)
# response = client.chat.completions.create(
#     model="gpt-3.5-turbo-1106",
#     response_format={ "type": "json_object" },
#     messages=[
#         {
#             "role": "system",
#             "content": """
#                 Bringe die Abschnitte in eine logische Reihenfolge.
#                 Antworte in JSON Format als ein Array 'Reihenfolge' in welchem nur die Nummern der Sätze stehen """
#         },
#         {
#             "role": "user",
#             "content": """
#                 1. Die Siedlung wuchs, wurde zu einem kleinen Hafen, und am 27. Oktober 1275 wurde Amsterdam von Graf Florens V. von Holland erstmals urkundlich erwähnt, noch als Amstelledamme.
#                 2. Danach blieb der Widerstand in Amsterdam lange Zeit schwach.
#                 3. Die niederländischen Rebellen blockierten nun den Amsterdamer Hafen, so dass die Stadt schnell verarmte.
#                 4. Die Geschichte der Stadt Amsterdam reicht bis in die Römerzeit zurück.
#                 5. Während der Zeit entwickelte sich Amsterdam von einer auf Pfählen gebauten Siedlung zu der über 800.000 Einwohner zählenden Hauptstadt der Niederlande.
#                 6. Um das Jahr 1250 entstanden die ersten von Bauern und Fischern bewohnten Siedlungen bei Amsterdam.
#                 7. Demonstranten zogen durch die Straßen und riefen: „Weg mit den Judenpogromen!“
#                 8. Züge und Straßenbahnen standen still, Werft- und Fabrikarbeiter legten die Arbeit nieder.
#                 9. Die in die Stadt kommenden Kaufleute lehnten sich gegen die vom Adel unterstützten Katholiken auf.
#                 10. Erst als sich 1943 die deutsche Niederlage abzeichnete, entwickelte sich eine breitere Bewegung.
#                 11. Am nächsten Tag wurde der Streik brutal unterdrückt.
#             """
#         }
# ])
