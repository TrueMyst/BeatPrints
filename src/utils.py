"""
This module provides a lot of useful functions related to Spotify and Lyrics.

Imports:
    - re: Module for regular expressions used in string manipulation.
    - os: Module for interacting with the operating system.
    - datetime: Module for working with dates and times.
    - pathlib: Module for working with filesystem paths.
    - rich: Function from the rich library for enhanced output formatting.
    - utils: Module containing utility functions.
    - writing: Module containing functions related to writing.
    - typing: Module for type hints.
    - errors: Module containing custom error classes.
"""

import re
import os
import datetime
import pathlib

import utils
import writing

from rich import print
from typing import Literal

from errors import InvalidInputError, InvalidSelectionError, LineLimitExceededError


def special_code() -> int:
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
    safe_text = (
        re.sub(r'[<>:"/\\|?*\x00-\x1F\x7F]', "_", full_text)
        .strip()
        .strip(".")
        .lower()
        .replace(" ", "_")
    )
    safe_text = re.sub(r"_{2,}", "_", safe_text)
    return safe_text[:255]


def confirm_input(message: str) -> bool:
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


def validate_image_path() -> str:
    while True:
        image_path = input("[🎷] Awesome, write the path to the image file: ")

        if os.path.exists(image_path):
            return image_path

        else:
            print("[❓️] File not found. Please provide a valid file path.")


def remove_column(data: list, column_index: int) -> list:
    return [row[:column_index] + row[column_index + 1:] for row in data]


def font(weight: Literal["Regular", "Bold", "Light"]) -> dict:
    fonts = writing.load_fonts(
        f"../fonts/Oswald/Oswald-{weight}.ttf",
        f"../fonts/NotoSansJP/NotoSansJP-{weight}.ttf",
        f"../fonts/NotoSansKR/NotoSansKR-{weight}.ttf",
        f"../fonts/NotoSansTC/NotoSansTC-{weight}.ttf",
        f"../fonts/NotoSansSC/NotoSansSC-{weight}.ttf",
    )

    return fonts


def select_lines(lyrics: str, selection: str) -> str:
    """
    Selects specific lines from the lyrics based on the provided range.

    Args:
        lyrics (str): The full lyrics of the song.
        selection (str): The range of lines to select (e.g., "2-5, 7-10").

    Returns:
        str: The selected lines of lyrics.
    """

    # Remove empty lines from the lyrics
    lines = [line for line in lyrics.strip().split("\n") if line.strip()]
    line_count = len(lines)

    selected = []

    try:
        selected = [int(num) for num in selection.split("-")]

        if (
            len(selected) != 2
            or selected[0] >= selected[1]
            or selected[0] <= 0
            or selected[1] > line_count
        ):
            raise InvalidSelectionError

        elif len(lines[selected[0] - 1: selected[1]]) > 4:
            raise LineLimitExceededError

        selected_lines = lines[selected[0] - 1: selected[1]]
        result = "\n".join(selected_lines).strip()
        return result

    except ValueError:
        raise InvalidInputError


def get_extract(lyrics: str) -> str:
    """
    Retrieves a portion of its lyrics.

    Args:
        lyrics (str): The lyrics of the song

    Returns:
        str: The extracted portion of the lyrics.
    """

    # Prompt the user to select favorite lines
    if len(lyrics.split('\n')) > 0:

        for line_num, line in enumerate(lyrics.split("\n")):
            print(f"[bold magenta]{line_num + 1:2}[/bold magenta] {line}")

        print("\n🎺 • You may ignore the spaces between the lines of the song.\n")

        while True:
            lines = input(
                "🍀 • Select any 4 of your favorite lines from here "
                "(e.g., 2-5, 7-10): "
            )

            try:
                result = utils.select_lines(lyrics, lines)
                return "\n".join(result)

            except Exception as e:
                print(e)
                continue
    else:
        print("😦 • Unfortunately, I couldn't find the lyrics from my sources")
        print("📝 • You can paste the lyrics manually below:")

        # Allow user to input lyrics manually
        manual_lyrics = []
        for _ in range(4):
            line = input()
            manual_lyrics.append(line)

        return "\n".join(manual_lyrics)
