"""
Module: spotify.py

Provides functionalities related to interacting with the Spotify API.
"""

import requests
import datetime

from typing import List
from dataclasses import dataclass

from .errors import NoMatchingSongFound, InvalidTrackLimit


@dataclass
class TrackMetadata:
    name: str
    artist: str
    album: str
    released: str
    duration: str
    image: str
    label: str
    id: str


class Spotify:
    """
    Uses Spotify's API to search and retrieve information about a track.
    """

    def __init__(self, CLIENT_ID: str, CLIENT_SECRET: str) -> None:
        """
        Initializes the Spotify client with credentials and obtains an access token.

        Args:
            CLIENT_ID (str): Spotify API client ID.
            CLIENT_SECRET (str): Spotify API client secret.
        """
        self.__CLIENT_ID = CLIENT_ID
        self.__CLIENT_SECRET = CLIENT_SECRET
        self.__BASE_URL = "https://api.spotify.com/v1"
        self.__authorization_header()

    def __authorization_header(self) -> None:
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

    def search(self, query: str, limit: int = 6) -> List[TrackMetadata]:
        """
        Searches Spotify for tracks matching the given query.

        Args:
            query (str): The search query for the track.
            limit (int, optional): Maximum number of tracks to retrieve. Defaults to 6.

        Returns:
            List[TrackMetadata]: A list of TrackMetadata instances, where each instance holds metadata
                                about a track, including details such as the track's name, artist, album,
                                and release date.

        Raises:
            InvalidTrackLimit: If the limit is less than 1.
            NoMatchingSongFound: If no matching songs are found.
        """
        if limit < 1:
            raise InvalidTrackLimit

        track_list = []
        params = {"q": query, "type": "track", "limit": limit}
        search_response = requests.get(
            f"{self.__BASE_URL}/search", params=params, headers=self.__AUTH_HEADER
        ).json()

        tracks = search_response["tracks"]["items"]

        if len(tracks) != 0:
            for track_info in tracks:
                # Retrieve album details
                album_id = track_info["album"]["id"]
                album_response = requests.get(
                    f"{self.__BASE_URL}/albums/{album_id}", headers=self.__AUTH_HEADER
                ).json()

                # Format metadata
                metadata = {
                    "name": track_info["name"],
                    "artist": track_info["artists"][0]["name"],
                    "album": track_info["album"]["name"],
                    "released": self.format_release_date(
                        track_info["album"]["release_date"],
                        track_info["album"]["release_date_precision"],
                    ),
                    "duration": self.format_duration(track_info["duration_ms"]),
                    "image": track_info["album"]["images"][0]["url"],
                    "label": album_response["label"],
                    "id": track_info["id"],
                }

                track_list.append(TrackMetadata(**metadata))
        else:
            raise NoMatchingSongFound

        return track_list

    def format_release_date(self, release_date: str, precision: str) -> str:
        """
        Formats the release date of a track.

        Args:
            release_date (str): Release date string from Spotify API.
            precision (str): Precision of the release date
                ('day', 'month', 'year').

        Returns:
            str: Formatted release date.
        """
        date_format = {"day": "%Y-%m-%d", "month": "%Y-%m", "year": "%Y"}.get(
            precision, ""
        )
        return datetime.datetime.strptime(release_date, date_format).strftime(
            "%B %d, %Y"
        )

    def format_duration(self, duration_ms: int) -> str:
        """
        Formats the duration of a track from milliseconds to MM:SS format.

        Args:
            duration_ms (int): Duration of the track in milliseconds.

        Returns:
            str: Formatted duration in MM:SS format.
        """
        minutes = duration_ms // 60000
        seconds = (duration_ms // 1000) % 60
        return f"{minutes:02d}:{seconds:02d}"
