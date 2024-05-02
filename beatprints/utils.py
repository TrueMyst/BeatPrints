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

import writing
from rich import print
from typing import Literal


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
            "📦 • Created a folder called "
            "[images]"
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


def validate_image_path():
    while True:
        image_path = input("[🎷] Awesome, write the path to the image file: ")

        if os.path.exists(image_path):
            return image_path

        else:
            print("[❓️] File not found. Please provide a valid file path.")


def remove_column(data, column_index):
    return [row[:column_index] + row[column_index + 1:] for row in data]


def font(weight: Literal["Regular", "Bold", "Light"]):
    fonts = writing.load_fonts(
        f"../fonts/Oswald/Oswald-{weight}.ttf",
        f"../fonts/NotoSansJP/NotoSansJP-{weight}.ttf",
        f"../fonts/NotoSansKR/NotoSansKR-{weight}.ttf",
        f"../fonts/NotoSansTC/NotoSansTC-{weight}.ttf",
        f"../fonts/NotoSansSC/NotoSansSC-{weight}.ttf",
    )

    return fonts


def select_lines(lyrics: str, selection: str):
    """
    Selects specific lines from the lyrics based on the provided range.

    Args:
        lyrics (str): The full lyrics of the song.
        selection (str): The range of lines to select (e.g., "2-5, 7-10").

    Returns:
        str: The selected lines of lyrics.
    """

    lines = lyrics.strip().split("\n")
    line_count = len(lines)

    try:
        selected = [int(num) for num in selection.split("-")]
        if (
            len(selected) != 2
            or selected[0] >= selected[1]
            or selected[0] <= 0
            or selected[1] > line_count
        ):
            return "Invalid selection. Please provide a valid range within the line numbers."

        selected_lines = lines[selected[0] - 1: selected[1]]
        return "\n".join(selected_lines)

    except ValueError:
        return (
            "Invalid input. Please provide a valid range using the format 'line x-y'."
        )
