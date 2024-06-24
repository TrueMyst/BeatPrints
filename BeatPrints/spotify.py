"""
Module: spotify.py

Provides functionalities related to interacting with the Spotify API.

Imports:
    - os: Provides OS interaction
    - typing: Type hinting support.
    - datetime: Work with dates and times.
    - requests: Simplifies HTTP requests.
"""

import os
import datetime
import requests

from typing import Any, List, Tuple, Dict, Union


class Spotify:
    """
    Uses Spotify's API to search and retrieve information about a track.
    """

    def __init__(self, CLIENT_ID, CLIENT_SECRET):
        self.__CLIENT_ID = CLIENT_ID
        self.__CLIENT_SECRET = CLIENT_SECRET
        self.__BASE_URL = "https://api.spotify.com/v1"
        self.authorization_header()

    def authorization_header(self):
        """
        Constructs the authorization header required for API requests.
        """

        endpoint = "https://accounts.spotify.com/api/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        payload = {
            "grant_type": "client_credentials",
            "client_id": self.__CLIENT_ID,
            "client_secret": self.__CLIENT_SECRET,
        }

        # Requesting token from Spotify API
        data = requests.post(endpoint, headers=headers, params=payload)
        token = data.json()["access_token"]

        self.__AUTH_HEADER = {"Authorization": f"Bearer {token}"}

    def search_track(
            self,
            name: str,
            limit: int = 6
    ) -> Union[List[Tuple[int, str, str, str, str]], None]:
        """
        Searches for a track through Spotify's API and provides the track information.

        Args:
            name (str): The name of the track to search.
            limit (int, optional): The maximum number of tracks to return. Defaults to 5.

        Returns:
            tracks (Union[List[Tuple[int, str, str, str, str]], None]): 
                A list of tuples containing track information if tracks are found, otherwise None. 
        """

        tracks = []
        params = {"q": name, "type": "track", "limit": limit}
        track_data = requests.get(f"{self.__BASE_URL}/search",
                                  params=params,
                                  headers=self.__AUTH_HEADER).json()

        # Displaying search results to the user
        if len(track_data) != 0:
            for num, item in enumerate(track_data.get("tracks",
                                                      {}).get("items",
                                                              [])[:10],
                                       start=1):
                name = item["name"]
                artist = item["artists"][0]["name"]
                album = item["album"]["name"]
                track_id = item["id"]
                tracks.append((num, name, artist, album, track_id))

            return tracks
        else:
            return None

    def trackinfo(self, track_id: str) -> Dict[str, Any]:
        """
        Retrieves detailed information about a track.

        Args:
            track_id (str): Track ID of the song.

        Returns:
            track_info (Dict[str, Any]): Detailed information about the track.
        """
        track_data = requests.get(f"{self.__BASE_URL}/tracks/{track_id}",
                                  headers=self.__AUTH_HEADER).json()

        album_data = requests.get(
            f"{self.__BASE_URL}/albums/{track_data['album']['id']}",
            headers=self.__AUTH_HEADER,
        ).json()

        album_label = album_data["label"]

        # Formatting the release date
        release_date = track_data["album"]["release_date"]
        release_date_precision = track_data["album"]["release_date_precision"]
        date_format = {
            "day": "%Y-%m-%d",
            "month": "%Y-%m",
            "year": "%Y"
        }.get(release_date_precision, "")
        formatted_release_date = datetime.datetime.strptime(
            release_date, date_format).strftime("%B %d, %Y")

        # Extracting track information
        track_info = {
            "album_id": track_data["album"]["id"],
            "name": track_data["name"],
            "artist": track_data["artists"][0]["name"],
            "year": track_data["album"]["release_date"],
            "duration":
            f"{(track_data['duration_ms'] // 60000):02d}:{(track_data['duration_ms'] // 1000 % 60):02d}",
            "image": track_data["album"]["images"][0]["url"],
            "label": f"{formatted_release_date}\n{album_label}",
            "track_id": track_data["id"],
        }

        # Path for the Spotify folder
        assets_path = os.path.realpath("assets")
        spotify_path = os.path.join(assets_path, "spotify")

        if not os.path.exists(spotify_path):
            os.makedirs(spotify_path)

        # Setting spotify banner's path
        spotify_banner_path = os.path.join(spotify_path, "spotify_banner.jpg")

        with open(spotify_banner_path, "wb") as cover_file:
            cover_file.write(requests.get(track_info["image"]).content)
            track_info["cover"] = spotify_banner_path

        return track_info
