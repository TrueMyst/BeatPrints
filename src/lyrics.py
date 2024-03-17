import os
import sys

from rich import print
from pymusix import PyMusix
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
USER_TOKEN = os.getenv("MUSIXMATCH_USERTOKEN")

song = PyMusix()
song.set_secrets(CLIENT_ID, CLIENT_SECRET, USER_TOKEN)


def select_lines(lyrics: str, selection: str):
    """
    Let's you select the lines of the lyrics using range eg. 2-5, 7-10.
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

        selected_lines = lines[selected[0] - 1 : selected[1]]
        return "\n".join(selected_lines)

    except ValueError:
        return (
            "Invalid input. Please provide a valid range using the format 'line x-y'."
        )


def get_extract(name: str, artist: str):
    """
    Returns the extracted portion of the lyrics.
    """
    song.search_track(name, artist)
    lyrics = song.lyrics

    try:
        print("\n[💫] Retrieved lyrics sucessfully\n")

        for line_num, line in enumerate(lyrics.split("\n")):
            print(f"[bold magenta]{line_num + 1:2}[/bold magenta] {line}")

        while True:
            lines = input(
                "\n[🎺] You may ignore the spaces between the lines of the song.\n[🍀] Select any 4 of favorite lines from here (e.g., 2-5, 7-10): "
            )

            result = select_lines(lyrics, lines)
            result = "\n".join(line for line in result.split("\n") if line.strip())

            if not result.startswith("Invalid"):
                selected_lines = result.split("\n")
                if 2 <= len(selected_lines) <= 4:
                    return result
                else:
                    print("Please select exactly 4 lines.")

    except Exception:
        print("\n[😓] Unfortunately no lyrics were found from MusixMatch.")
        sys.exit()
