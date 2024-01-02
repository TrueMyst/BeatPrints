import re
import os
import datetime

from rich import print
from lingua import Language, LanguageDetectorBuilder


def special_code():
    return ((int(datetime.datetime.now().timestamp()) % 10000) + 10000) % 10000


def create_folder():
    if not os.path.exists("../images/"):
        os.makedirs("../images/")
        print(
            "[📦] Created a folder called [bold underline turquoise4]../images[/bold underline turquoise4] outside of this directory for output."
        )


def create_filename(song, artist):
    full_text = f"{song} by {artist}"
    safe_text = (
        re.sub(r'[<>:"/\\|?*\x00-\x1F\x7F]', "_", full_text)
        .strip()
        .strip(".")
        .lower()
        .replace(" ", "_")
    )
    safe_text = re.sub(r"_{2,}", "_", safe_text)
    return safe_text[:255]


def confirm_input(message):
    while True:
        user_response = input(message + " (y/n): ").lower()
        if user_response == "y":
            return True
        elif user_response == "n":
            return False
        else:
            print("\n[🙅] Please enter 'y' for yes or 'n' for no.\n")


def decide_font(text: str, weight: int):
    path = "../fonts/"

    lang = {
        "en": "Oswald/Oswald",
        "ko": "NotoSansKR/NotoSansKR",
        "ja": "NotoSansJP/NotoSansJP",
        "zh": "NotoSansTC/NotoSansTC",
    }

    variant = ["ExtraLight", "Light", "Regular", "Medium", "Semibold", "Bold"]

    detector = LanguageDetectorBuilder.from_languages(
        Language.ENGLISH, Language.KOREAN, Language.JAPANESE, Language.CHINESE
    ).build()
    detected = str(detector.detect_language_of(text).iso_code_639_1.name).lower()
    font = f"{path}{lang[detected]}-{variant[weight]}.tff"

    return font
