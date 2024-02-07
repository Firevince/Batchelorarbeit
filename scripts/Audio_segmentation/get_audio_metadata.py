import os

from dotenv import load_dotenv
from mutagen.id3 import APIC, ID3
from mutagen.mp3 import MP3

load_dotenv()
AUDIO_SOURCE_PATH = os.getenv("AUDIO_SOURCE_PATH")
DATA_PATH = os.getenv("DATA_PATH")


def save_image(filename, i):
    # image_path = os.path.join(DATA_PATH, "images/cover_images", f"cover_{i}.jpg")
    image_path = (
        f"/Users/br/Projects/Bachelorarbeit/scripts/server/static/images/cover_{i}.jpg"
    )
    try:
        tags = ID3(filename)

        if "APIC:" in tags:
            # Extract the first album cover (you can loop through all if there are multiple)
            cover = tags["APIC:"].data

            with open(image_path, "wb") as f:
                f.write(cover)

            print(f"Album cover image saved as 'cover_{i}.jpg'")
        else:
            print("No album cover image found in the MP3 file.")

    except Exception as e:
        print("Error:", e)
    return f"static/images/cover_{i}.jpg"


def save_all_images(df):
    images = []
    for i, filename in enumerate(df["filename"]):
        audio_path = os.path.join(AUDIO_SOURCE_PATH, filename)
        image_path = save_image(audio_path, i)
        images.append(image_path)
    df["image_path"] = images
    return df
