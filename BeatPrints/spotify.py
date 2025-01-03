"""
Module: spotify.py

Provides functionality related to interacting with the Spotify API.
"""

import random
import requests
import datetime

from typing import List
from dataclasses import dataclass

from .errors import NoMatchingTrackFound, NoMatchingAlbumFound, InvalidSearchLimit


@dataclass
class TrackMetadata:
    """
    Data structure to store metadata for a track.
    """

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
    """
    Data structure to store metadata for an album, including a track list.
    """

    name: str
    artist: str
    released: str
    image: str
    label: str
    id: str
    tracks: List[str]


class Spotify:
    """
    A class for interacting with the Spotify API to search and retrieve track/album information.
    """

    def __init__(self, CLIENT_ID: str, CLIENT_SECRET: str) -> None:
        """
        Initializes the Spotify client with credentials and obtains an access token.

        Args:
            CLIENT_ID (str): Spotify API client ID.
            CLIENT_SECRET (str): Spotify API client secret.
        """
        self.CLIENT_ID = CLIENT_ID
        self.CLIENT_SECRET = CLIENT_SECRET
        self.__BASE_URL = "https://api.spotify.com/v1"
        self.__authorization_header()

    def __authorization_header(self) -> None:
        """
        Constructs the authorization header required for API requests.
        Retrieves an access token from Spotify's accounts service.
        """
        endpoint = "https://accounts.spotify.com/api/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        payload = {
            "grant_type": "client_credentials",
            "client_id": self.CLIENT_ID,
            "client_secret": self.CLIENT_SECRET,
        }

        # Request token from Spotify API
        data = requests.post(endpoint, headers=headers, params=payload)
        token = data.json()["access_token"]

        # Store authorization header for use in API requests
        self.__AUTH_HEADER = {"Authorization": f"Bearer {token}"}

    def _format_release_date(self, release_date: str, precision: str) -> str:
        """
        Formats the release date of a track or album.

        Args:
            release_date (str): Release date string from Spotify API.
            precision (str): Precision of the release date ('day', 'month', 'year').

        Returns:
            str: Formatted release date in 'Month Day, Year' format.
        """
        # Format the release date based on the precision
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
        # Convert milliseconds to minutes and seconds
        minutes = duration_ms // 60000
        seconds = (duration_ms // 1000) % 60
        return f"{minutes:02d}:{seconds:02d}"

    def get_track(self, query: str, limit: int = 6) -> List[TrackMetadata]:
        """
        Searches for tracks based on a query and retrieves their metadata.

        Args:
            query (str): The search query for the track (e.g. track name - artist).
            limit (int, optional): Maximum number of tracks to retrieve. Defaults to 6.

        Returns:
            List[TrackMetadata]: A list of track metadata.

        Raises:
            InvalidSearchLimit: If the limit is less than 1.
            NoMatchingTrackFound: If no matching tracks are found.
        """
        if limit < 1:
            raise InvalidSearchLimit

        tracklist = []
        params = {"q": query, "type": "track", "limit": limit}
        response = requests.get(
            f"{self.__BASE_URL}/search", params=params, headers=self.__AUTH_HEADER
        ).json()

        tracks = response.get("tracks", {}).get("items", [])

        if not tracks:
            raise NoMatchingTrackFound

        # Extract track details and format them
        for track in tracks:

            # Get the track's album using the album ID
            id = track["album"]["id"]
            album = requests.get(
                f"{self.__BASE_URL}/albums/{id}", headers=self.__AUTH_HEADER
            ).json()

            # Create TrackMetadata object with formatted data
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
                "label": album["label"],
                "id": track["id"],
            }

            tracklist.append(TrackMetadata(**metadata))

        return tracklist

    def get_album(
        self, query: str, limit: int = 6, shuffle: bool = False
    ) -> List[AlbumMetadata]:
        """
        Searches for albums based on a query and retrieves their metadata, including track listing.

        Args:
            query (str): The search query for the album (e.g. album name - artist).
            limit (int, optional): Maximum number of albums to retrieve. Defaults to 6.
            shuffle (bool, optional): Shuffle the tracks in the tracklist. Defaults to False.

        Returns:
            List[AlbumMetadata]: A list of album metadata with track listings.

        Raises:
            InvalidSearchLimit: If the limit is less than 1.
            NoMatchingAlbumFound: If no matching albums are found.
        """
        if limit < 1:
            raise InvalidSearchLimit

        albumlist = []
        params = {"q": query, "type": "album", "limit": limit}
        response = requests.get(
            f"{self.__BASE_URL}/search", params=params, headers=self.__AUTH_HEADER
        ).json()

        albums = response.get("albums", {}).get("items", [])

        if not albums:
            raise NoMatchingAlbumFound

        # Process each album to get details and tracklist
        for album in albums:
            id = album["id"]
            album_details = requests.get(
                f"{self.__BASE_URL}/albums/{id}", headers=self.__AUTH_HEADER
            ).json()

            # Extract track names from album details
            tracks = [
                track["name"]
                for track in album_details.get("tracks", {}).get("items", [])
            ]

            # Shuffle tracks if true
            if shuffle:
                random.shuffle(tracks)

            # Create AlbumMetadata object with formatted data
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
