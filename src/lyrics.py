import os
import requests

from rich import print
from bs4 import BeautifulSoup
from dotenv import load_dotenv


load_dotenv()

MUSIXMATCH_APIKEY = os.getenv("MUSIXMATCH_API")


def search_track(query: str, artist: str):
    endpoint = f"http://api.musixmatch.com/ws/1.1/track.search?"
    params = {
        "q_track": query,
        "q_artist": artist,
        "page_size": 10,
        "apikey": MUSIXMATCH_APIKEY,
    }
    data = requests.get(endpoint, params=params)
    tracks = data.json()["message"]["body"]["track_list"]

    print("Checking lyrics from the database...\n")

    for i, track in enumerate(tracks):
        track_name = track["track"]["track_name"]
        track_artist = track["track"]["artist_name"]

        print(
            f"[bold underline white]{i+1}[/bold underline white]. [bold turquoise4]{track_name}[/bold turquoise4] by [bold steel_blue]{track_artist}[/bold steel_blue]"
        )

    choice = int(input("\n[✨] Just to be sure which lyrics do you want?: "))
    track = data.json()["message"]["body"]["track_list"][choice - 1]

    base_url, _ = track["track"]["track_share_url"].split("?")

    data = {
        "track_name": track["track"]["track_name"],
        "track_artist": track["track"]["artist_name"],
        "track_share_url": base_url,
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
    }
    response = requests.get(data["track_share_url"], headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    cols = soup.findAll(class_="lyrics__content__ok", string=True)

    lyrics = (
        "\n".join(x.text for x in cols)
        if cols
        else "Oops, seems like the lyrics aren't posted yet."
    )

    return lyrics


def select_lines(lyrics: str, selection: str):
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
    lyrics = search_track(name, artist)

    for line_num, line in enumerate(lyrics.split("\n")):
        print(f"[bold magenta]{line_num + 1:2}[/bold magenta] {line}")

    while True:
        lines = input(
            "\n[🍀] Select any 4 of favorite lines from here (e.g., 2-5, 7-10): "
        )

        result = select_lines(lyrics, lines)
        result = "\n".join(line for line in result.split("\n") if line.strip())

        if not result.startswith("Invalid"):
            selected_lines = result.split("\n")
            if 2 <= len(selected_lines) <= 4:
                return result
            else:
                print("Please select exactly 4 lines.")
        else:
            print(result)
