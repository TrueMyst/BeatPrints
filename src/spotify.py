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

from dotenv import load_dotenv
from typing import List, Tuple

load_dotenv()

# Retrieving Spotify API credentials from environment variables
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

# Getting the current directory
current_dictionary = pathlib.Path(__file__).parent.resolve()


def authorization_header():
    """
    Constructs the authorization header required for API requests.

    Args:
        token (str): The access token.

    Returns:
        dict: Authorization header.
    """

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

    return {"Authorization": f"Bearer {get_token()}"}


header = authorization_header()


def search_track(track_name: str):
    """
    Searches for a track through Spotify's API and provides track information.

    Args:
        track_name (str): The name of the track to search.
        want_image (bool, optional): Flag to include track image or not. Defaults to False.

    Returns:
        dict: Information about the selected track.
    """
    searched_tracks = []

    endpoint = "https://api.spotify.com/v1"

    query_params = {"q": track_name, "type": "track", "limit": 10}
    track_data = requests.get(
        f"{endpoint}/search", params=query_params, headers=header
    ).json()

    # Displaying search results to the user
    for i, item in enumerate(
        track_data.get("tracks", {}).get("items", [])[:10], start=1
    ):
        name = item["name"]
        artist = item["artists"][0]["name"]
        album = item["album"]["name"]
        trackid = item["id"]

        searched_tracks.append([i, name, artist, album, trackid])

    return searched_tracks


def get_trackinfo(track: List[Tuple[int, str, str, str, str]], custom_image=None):

    endpoint = "https://api.spotify.com/v1"

    data = requests.get(f"{endpoint}/tracks/{track[4]}", headers=header).json()

    # Extracting track information
    track_info = {
        "album_id": data["album"]["id"],
        "name": data["name"],
        "artist": data["artists"][0]["name"],
        "year": data["album"]["release_date"],
        "duration": f"{(data['duration_ms'] // 60000):02d}:{(data['duration_ms'] // 1000 % 60):02d}",
        "image": data["album"]["images"][0]["url"],
        "track_id": data["id"],
    }

    # Optionally allowing the user to provide a custom image
    if custom_image == None:

        with open(current_dictionary / "assets/spotify_banner.jpg", "wb") as cover:
            cover.write(requests.get(track_info["image"]).content)
            track_info["path"] = "./assets/spotify_banner.jpg"

    elif custom_image != None:
        image.crop_to_square(
            Path(custom_image), current_dictionary / "./assets/custom_image.jpg"
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
