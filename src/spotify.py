import os
import image
import requests
import datetime
import pathlib

from rich import print
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

cur = pathlib.Path(__file__).parent.resolve()


def get_token():
    endpoint = "https://accounts.spotify.com/api/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    payload = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }

    data = requests.post(endpoint, headers=headers, params=payload)
    token = data.json()["access_token"]

    return token


def authorization_header(token: str):
    return {"Authorization": "Bearer {0}".format(token)}


def search_track(track_name: str, want_image: bool = False):
    """
    Searches track through Spotify's API.
    """
    endpoint = "https://api.spotify.com/v1"
    header = authorization_header(get_token())

    query_params = {"q": track_name, "type": "track", "limit": 7}
    track_data = requests.get(
        f"{endpoint}/search", params=query_params, headers=header
    ).json()

    for i, item in enumerate(
        track_data.get("tracks", {}).get("items", [])[:7], start=1
    ):
        t_name = item["name"]
        t_artist = item["album"]["artists"][0]["name"]
        t_album = item["album"]["name"]

        print(
            f"[bold underline white]{i}[/bold underline white]. [bold turquoise4]{t_name}[/bold turquoise4] by [bold steel_blue]{t_artist}[/bold steel_blue] from [bold magenta]{t_album}[/bold magenta]"
        )

    while True:
        try:
            choice = int(input("\n[✨] Select one of them to show information: "))
            if 1 <= choice <= 7:
                break
            else:
                print("Please enter a number between 1 and 7.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    selected_track = track_data["tracks"]["items"][choice - 1]
    album_id = selected_track["album"]["id"]

    track_info = {
        "image": selected_track["album"]["images"][0]["url"],
        "name": selected_track["name"],
        "year": selected_track["album"]["release_date"],
        "artist": selected_track["album"]["artists"][0]["name"],
        "duration": f"{(selected_track['duration_ms'] // 60000):02d}:{(selected_track['duration_ms'] // 1000 % 60):02d}",
        "album_id": album_id,
        "track_id": selected_track["id"],
    }

    if not want_image:
        with open(cur / "assets/spotify_banner.jpg", "wb") as banner:
            banner.write(requests.get(track_info["image"]).content)
            track_info["path"] = "./assets/spotify_banner.jpg"
    else:
        path = input("[🤭] Write the path to your custom image: ")
        image.crop_to_square(path, cur / "./assets/custom_image.jpg")

        track_info["path"] = cur / "./assets/custom_image.jpg"

    return track_info


def label(album_id: str):
    """
    Retrivies the name of the album and the release date.
    """
    endpoint = "https://api.spotify.com/v1"
    header = authorization_header(get_token())

    album_info = requests.get(f"{endpoint}/albums/{album_id}", headers=header).json()
    label = album_info["label"]

    release_date_str = album_info.get("release_date", "")
    release_precision = album_info.get("release_date_precision", "")

    format_str = {"day": "%Y-%m-%d", "month": "%Y-%m", "year": "%Y"}.get(
        release_precision, ""
    )

    release_date = datetime.datetime.strptime(release_date_str, format_str).strftime(
        "%B %d, %Y"
    )
    return [release_date, label]


def get_code(id: str):
    """
    Downloads the spotify scan code for a particular song.
    """
    main = (
        f"https://scannables.scdn.co/uri/plain/png/101010/white/256/spotify:track:{id}"
    )
    data = requests.get(main)

    with open(cur / "assets/spotify_code.png", "wb") as img:
        img.write(data.content)

    image.remove_white_pixel(cur / "assets/spotify_code.png")

    return "\n[🍉] Yay! Retrieved the spotify code properly!\n"
