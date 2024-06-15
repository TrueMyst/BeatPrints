"""
This module provides a lot of useful functions related to Spotify and Lyrics.

Imports:
    - re: Module for regular expressions used in string manipulation.
    - os: Module for interacting with the operating system.
    - datetime: Module for working with dates and times.
    - pathlib: Module for working with filesystem paths.
    - rich: Function from the rich library for enhanced output formatting.
    - typing: Module for type hints.

    - utils: Module containing utility functions.
    - writing: Module containing functions related to writing.
    - errors: Module containing custom error classes.
"""

import re
import os
import datetime
import pathlib
import writing

from rich import print
from typing import Literal, Union
from lyrics import Lyrics


def special_code() -> int:
    """
    Generates a special code based on the current timestamp.

    Returns:
        int: The generated special code.
    """
    return ((int(datetime.datetime.now().timestamp()) % 10000) + 10000) % 10000


def create_filename(song: str, artist: str) -> str:
    """
    Creates a safe filename based on the song and artist names.

    Args:
        song (str): The name of the song.
        artist (str): The name of the artist.

    Returns:
        str: The safe filename.
    """
    full_text = f"{song} by {artist}"
    safe_text = (re.sub(r'[<>:"/\\|?*\x00-\x1F\x7F]', "_",
                        full_text).strip().strip(".").lower().replace(
                            " ", "_"))
    safe_text = re.sub(r"_{2,}", "_", safe_text)
    return safe_text[:255]


def c_input(message: str) -> bool:
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
            print("\n╰─ 🙅 • Please enter 'y' for yes or 'n' for no.\n")


def validate_image_path() -> str:
    while True:
        image_path = input(
            "╰─ 🎷 • Awesome, write the path to the image file: ")

        if os.path.exists(image_path):
            return image_path

        else:
            print("╰─ ❓️ • File not found. Please provide a valid file path.")


def remove_column(data: list, column_index: int) -> list:
    return [row[:column_index] + row[column_index + 1:] for row in data]


def font(weight: Literal["Regular", "Bold", "Light"]) -> dict:
    fonts_path = os.path.realpath("assets/fonts")
    fonts = writing.load_fonts(
        os.path.join(fonts_path, "Oswald", f"Oswald-{weight}.ttf"),
        os.path.join(fonts_path, "NotoSansJP", f"NotoSansJP-{weight}.ttf"),
        os.path.join(fonts_path, "NotoSansKR", f"NotoSansKR-{weight}.ttf"),
        os.path.join(fonts_path, "NotoSansTC", f"NotoSansTC-{weight}.ttf"),
        os.path.join(fonts_path, "NotoSansSC", f"NotoSansSC-{weight}.ttf"),
        os.path.join(fonts_path, "NotoSans", f"NotoSans-{weight}.ttf"))
    return fonts


def get_extract(lyrics: Union[str, None]):
    """
    Retrieves a portion of its lyrics.

    Args:
        lyrics (str): The lyrics of the song

    Returns:
        str: The extracted portion of the lyrics.
    """

    ly = Lyrics()

    if lyrics != None:
        splitted = lyrics.split('\n')

        # Prompt the user to select favorite lines
        for line_num, line in enumerate(splitted):
            print(f"[bold magenta]{line_num + 1:2}[/bold magenta] {line}")

        print(
            "\n🎺 • You may ignore the spaces between the lines of the song.\n")

        while True:
            lines = input("🍀 • Select any 4 of your favorite lines from here "
                          "(e.g., 2-5, 7-10): ")

            try:
                result = ly.select_lines(lyrics, lines)
                return result

            except Exception as e:
                print(e)
                continue

    else:
        print(
            "\n😦 • Unfortunately, I couldn't find the lyrics from my sources")
        print("📝 • But don't worry, you can paste the lyrics manually below:")

        # Allow user to input lyrics manually
        manual_lyrics = []

        for _ in range(4):
            line = input()
            manual_lyrics.append(line)

        return "\n".join(manual_lyrics)
