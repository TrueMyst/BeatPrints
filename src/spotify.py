"""
This module provides functionalities related to interacting with the Spotify API.

Imports:
    - datetime: Module for manipulating dates and times.
    - pathlib: Module for working with filesystem paths.
    - os: Module for interacting with the operating system.
    - requests: Module for making HTTP requests.
    - print: For enhanced output formatting.
    - load_dotenv: For loading environment variables from a .env file.
    - image: Module for image manipulation.
"""

import os
import image
import datetime
import requests

import pathlib
from pathlib import Path

from rich import print
from dotenv import load_dotenv

load_dotenv()

# Retrieving Spotify API credentials from environment variables
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

# Getting the current directory
current_dictionary = pathlib.Path(__file__).parent.resolve()


def get_token():
    """
    Retrieves the access token for Spotify's API.

    Returns:
        str: The access token.
    """
    endpoint = "https://accounts.spotify.com/api/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    payload = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }

    # Requesting token from Spotify API
    data = requests.post(endpoint, headers=headers, params=payload)
    token = data.json()["access_token"]

    return token


def authorization_header(token: str):
    """
    Constructs the authorization header required for API requests.

    Args:
        token (str): The access token.

    Returns:
        dict: Authorization header.
    """
    return {"Authorization": f"Bearer {token}"}


def search_track(track_name: str, want_image: bool = False):
    """
    Searches for a track through Spotify's API and provides track information.

    Args:
        track_name (str): The name of the track to search.
        want_image (bool, optional): Flag to include track image or not. Defaults to False.

    Returns:
        dict: Information about the selected track.
    """
    endpoint = "https://api.spotify.com/v1"
    header = authorization_header(get_token())

    query_params = {"q": track_name, "type": "track", "limit": 10}
    track_data = requests.get(
        f"{endpoint}/search", params=query_params, headers=header
    ).json()

    # Displaying search results to the user
    for i, item in enumerate(
        track_data.get("tracks", {}).get("items", [])[:10], start=1
    ):
        t_name = item["name"]
        t_artist = item["album"]["artists"][0]["name"]
        t_album = item["album"]["name"]

        print(
            f"[bold underline white]{i}[/bold underline white]. "
            f"[bold turquoise4]{t_name}[/bold turquoise4] by "
            f"[bold steel_blue]{t_artist}[/bold steel_blue] from "
            f"[bold magenta]{t_album}[/bold magenta]"
        )

    # Asking user to select a track
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

    # Extracting track information
    track_info = {
        "image": selected_track["album"]["images"][0]["url"],
        "name": selected_track["name"],
        "year": selected_track["album"]["release_date"],
        "artist": selected_track["album"]["artists"][0]["name"],
        "duration": f"{(selected_track['duration_ms'] // 60000):02d}:{(selected_track['duration_ms'] // 1000 % 60):02d}",
        "album_id": album_id,
        "track_id": selected_track["id"],
    }

    # Optionally allowing the user to provide a custom image
    if not want_image:
        with open(current_dictionary / "assets/spotify_banner.jpg", "wb") as banner:
            banner.write(requests.get(track_info["image"]).content)
            track_info["path"] = "./assets/spotify_banner.jpg"
    else:
        path = input("[🤭] Write the path to your custom image: ")
        image.crop_to_square(
            Path(path), current_dictionary / "./assets/custom_image.jpg"
        )

        track_info["path"] = current_dictionary / "./assets/custom_image.jpg"

    return track_info


def label(album_id: str):
    """
    Retrieves the name of the album and the release date from Spotify's API.

    Args:
        album_id (str): The ID of the album.

    Returns:
        list: A list containing the release date and album label.
    """
    endpoint = "https://api.spotify.com/v1"
    header = authorization_header(get_token())

    album_info = requests.get(f"{endpoint}/albums/{album_id}", headers=header).json()
    album_label = album_info["label"]

    release_date_str = album_info.get("release_date", "")
    release_precision = album_info.get("release_date_precision", "")

    format_str = {"day": "%Y-%m-%d", "month": "%Y-%m", "year": "%Y"}.get(
        release_precision, ""
    )

    # Formatting the release date
    release_date = datetime.datetime.strptime(release_date_str, format_str).strftime(
        "%B %d, %Y"
    )
    return [release_date, album_label]


def get_code(id: str):
    """
    Downloads the Spotify scan code for a particular song.

    Args:
        identification (str): The ID of the track.

    Returns:
        str: Message indicating success.
    """
    main = (
        f"https://scannables.scdn.co/uri/plain/png/101010/white/1024/spotify:track:{id}"
    )
    data = requests.get(main)

    with open(current_dictionary / "assets/spotify_code.png", "wb") as img:
        img.write(data.content)

    # Removing white pixels from the downloaded image
    image.remove_white_pixel(current_dictionary / "assets/spotify_code.png")

    return "\n[🍉] Yay! Retrieved the Spotify code properly!\n"
