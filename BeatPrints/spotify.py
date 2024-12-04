"""
Module: spotify.py

Provides functionalities related to interacting with the Spotify API.
"""

import requests
import datetime

from typing import List
from dataclasses import dataclass

from .errors import NoMatchingTrackFound, NoMatchingAlbumFound, InvalidSearchLimit


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


@dataclass
class AlbumMetadata:
    name: str
    artist: str
    released: str
    image: str
    label: str
    id: str
    tracks: List[str]


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

    def _format_release_date(self, release_date: str, precision: str) -> str:
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

    def _format_duration(self, duration_ms: int) -> str:
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

    def get_track(self, query: str, limit: int = 6) -> List[TrackMetadata]:
        """
        Searches for tracks matching the given query.

        Args:
            query (str): The search query for the track.
            limit (int, optional): Maximum number of tracks to retrieve. Defaults to 6.

        Returns:
            List[TrackMetadata]: A list of the track's metadata.

        Raises:
            InvalidSearchLimit: If the limit is less than 1.
            NoMatchingSongFound: If no matching songs are found.
        """
        if limit < 1:
            raise InvalidSearchLimit

        tracklist = []
        params = {"q": query, "type": "track", "limit": limit}
        track_response = requests.get(
            f"{self.__BASE_URL}/search", params=params, headers=self.__AUTH_HEADER
        ).json()

        tracks = track_response.get("tracks", {}).get("items", [])

        if not tracks:
            raise NoMatchingTrackFound

        for track in tracks:

            # Retrieve album details
            id = track["album"]["id"]
            album_details = requests.get(
                f"{self.__BASE_URL}/albums/{id}", headers=self.__AUTH_HEADER
            ).json()

            # Format metadata
            metadata = {
                "name": track["name"],
                "artist": track["artists"][0]["name"],
                "album": track["album"]["name"],
                "released": self._format_release_date(
                    track["album"]["release_date"],
                    track["album"]["release_date_precision"],
                ),
                "duration": self._format_duration(track["duration_ms"]),
                "image": track["album"]["images"][0]["url"],
                "label": album_details["label"],
                "id": track["id"],
            }

            tracklist.append(TrackMetadata(**metadata))

        return tracklist

    def get_album(self, query: str, limit: int = 6) -> List[AlbumMetadata]:
        """
        Retrieves album metadata and track listing.

        Args:
            query (str): The search query for the album.
            limit (int, optional): Maximum number of albums to retrieve. Defaults to 6.

        Returns:
            List[AlbumMetadata]: A list of album metadata, including track listings.

        Raises:
            InvalidSearchLimit: If the limit is less than 1.
            NoMatchingSongFound: If no matching albums are found.
        """
        if limit < 1:
            raise InvalidSearchLimit

        albumlist = []
        params = {"q": query, "type": "album", "limit": limit}
        album_response = requests.get(
            f"{self.__BASE_URL}/search", params=params, headers=self.__AUTH_HEADER
        ).json()

        albums = album_response.get("albums", {}).get("items", [])

        if not albums:
            raise NoMatchingAlbumFound

        # Process albums in one loop
        for album in albums:
            id = album["id"]
            album_details = requests.get(
                f"{self.__BASE_URL}/albums/{id}", headers=self.__AUTH_HEADER
            ).json()

            # Fetch track names directly from album details
            tracks = [
                track["name"]
                for track in album_details.get("tracks", {}).get("items", [])
            ]

            metadata = {
                "name": album["name"],
                "artist": album["artists"][0]["name"],
                "released": self._format_release_date(
                    album["release_date"], album["release_date_precision"]
                ),
                "image": album["images"][0]["url"],
                "label": album_details.get("label", "Unknown"),
                "id": album["id"],
                "tracks": tracks,
            }

            albumlist.append(AlbumMetadata(**metadata))

        return albumlist
