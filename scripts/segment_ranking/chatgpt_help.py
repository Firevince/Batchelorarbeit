import json
import os

import requests
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
API_KEY = os.getenv("OPENAI_KEY")


def gpt_get_keywords(df):
    query = "\n".join(df["sentence"])
    # print(query)

    client = OpenAI(api_key=API_KEY)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": """
            Schreibe 5 Stichwörter, die zu diesen Textabschnitten passen.
            Antworte in JSON Format als ein Array 'Stichwörter' in welchem nur Stichwörter stehen """,
            },
            {"role": "user", "content": query},
        ],
    )
    keywords = ""
    try:
        keywords = json.loads(response.choices[0].message.content)["Stichwörter"]
    except:
        print("Answer not in right format - no keywords found")

    return keywords


def gpt_order_segments(df):
    query = [f"{i+1}. {segment}" for i, segment in enumerate(df["sentence"])]
    query = "\n".join(query)
    # print(query)

    client = OpenAI(api_key=API_KEY)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": """
            Bringe die Abschnitte in eine logische Reihenfolge.
            Antworte in JSON Format als ein Array 'Reihenfolge' in welchem nur die Nummern der Sätze stehen """,
            },
            {"role": "user", "content": query},
        ],
    )
    try:
        order = json.loads(response.choices[0].message.content)["Reihenfolge"]
        df["order"] = order
        df = df.sort_values("order").reset_index(drop=True)
    except:
        print("Answer not in right format - using default order")
        # TODO retry chatgpt
    return df


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
