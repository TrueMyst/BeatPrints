"""
This module provides functionalities related to interacting with the Spotify API.

Imports:
    - re: Module for regular expressions used in string manipulation.
    - os: Module for interacting with the operating system.
    - datetime: Module for working with dates and times.
    - pathlib: Module for working with filesystem paths.
    - print: Function from the rich library for enhanced output formatting.
    - Language, LanguageDetectorBuilder: Classes from the lingua library for language detection.
"""

import re
import os
import datetime
import pathlib

from rich import print
from lingua import Language
from lingua import LanguageDetectorBuilder


def special_code():
    """
    Generates a special code based on the current timestamp.

    Returns:
        int: The generated special code.
    """
    return ((int(datetime.datetime.now().timestamp()) % 10000) + 10000) % 10000


def create_folder():
    """
    Creates a folder named 'images' if it doesn't exist.

    Prints a message indicating the creation of the folder.
    """
    cur = pathlib.Path(__file__).parent.resolve()
    if not os.path.exists(cur / "../images/"):
        os.makedirs(cur / "../images/")
        print(
            "[📦] Created a folder called "
            "[bold underline turquoise4]../images[/bold underline turquoise4] "
            "outside of this directory for output."
        )


def create_filename(song, artist):
    """
    Creates a safe filename based on the song and artist names.

    Args:
        song (str): The name of the song.
        artist (str): The name of the artist.

    Returns:
        str: The safe filename.
    """
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
    """
    Asks the user for confirmation with a given message.

    Args:
        message (str): The message to display for confirmation.

    Returns:
        bool: True if user confirms with 'y', False if user denies with 'n'.
    """
    while True:
        user_response = input(message + " (y/n): ").lower()
        if user_response == "y":
            return True
        elif user_response == "n":
            return False
        else:
            print("\n[🙅] Please enter 'y' for yes or 'n' for no.\n")


def decide_font(text: str, weight: int):
    """
    Determines the font to use based on the text and font weight.

    Args:
        text (str): The text to analyze for language detection.
        weight (int): The weight of the font.

    Returns:
        str: The path to the selected font file.
    """
    path = "../fonts/"

    lang = {
        "en": "Oswald/Oswald",
        "ko": "NotoSansKR/NotoSansKR",
        "ja": "NotoSansJP/NotoSansJP",
        "zh": "NotoSansTC/NotoSansTC",
    }

    variant = ["ExtraLight", "Light", "Regular", "Medium", "Semibold", "Bold"]

    # Language detection
    detector = LanguageDetectorBuilder.from_languages(
        Language.ENGLISH, Language.KOREAN, Language.JAPANESE, Language.CHINESE
    ).build()
    detected = str(detector.detect_language_of(text).iso_code_639_1.name).lower()

    # Construct font path
    font = f"{path}{lang[detected]}-{variant[weight]}.tff"

    return font
