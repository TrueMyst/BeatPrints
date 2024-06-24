"""
This module provides a lot of useful functions related to Spotify and Lyrics.

Imports:
    - re: Provides regular expressions.
    - os: Provides OS interaction.
    - datetime: Work with dates and times.
    - typing: Type hinting support.
    - rich: Renders rich text in the terminal.
    - lyrics: Retrieve lyrics through LRClib API.
"""

import re
import os
import datetime

from rich import print
from lyrics import Lyrics
from typing import Union


def special_code() -> int:
    """
    Generates a special code based on the current timestamp.

    Returns:
        int: The generated special code.
    """
    return (
        (int(datetime.datetime.now().timestamp()) % 100000) + 100000) % 100000


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
    """
    Prompts the user for an image file path until a valid path is provided.

    Returns:
        str: Validated image file path.
    """
    while True:
        image_path = input(
            "╰─ 🎷 • Awesome, write the path to the image file: ")

        if os.path.exists(image_path):
            return image_path
        else:
            print("╰─ ❓️ • File not found. Please provide a valid file path.")


def remove_column(data: list, column_index: int) -> list:
    """
    Removes the specified column from a 2D list.

    Args:
        data (list): 2D list of data.
        column_index (int): Index of the column to remove.

    Returns:
        list: 2D list with the specified column removed.
    """
    return [row[:column_index] + row[column_index + 1:] for row in data]


def get_extract(lyrics: Union[str, None]):
    """
    Retrieves a portion of its lyrics.

    Args:
        lyrics (str): The lyrics of the song

    Returns:
        result (str): The extracted portion of the lyrics.
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
