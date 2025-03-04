"""
Module: spotify.py

Provides functionality related to interacting with the Spotify API.
"""

import random
import requests
import datetime
import re

from typing import List, Optional
from dataclasses import dataclass

from .errors import (InvalidAlbumUrlError, InvalidSearchLimit,
                     InvalidTrackUrlError, MissingParameterError,
                     NoMatchingAlbumFound, NoMatchingTrackFound)


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


TYPE_TRACK = "track"
TYPE_ALBUM = "album"


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

    def parse_url(self, url: str) -> tuple:
        """
        Parses a Spotify URL to extract the type and ID.

        Args:
            url (str): The Spotify URL to be parsed.

        Returns:
            tuple: A tuple containing two elements:
                - The type of the Spotify URL (e.g., "track", "album").
                - The ID of the Spotify URL.
        """

        # Extract the type and ID from the Spotify URL
        match = re.match(r"https://open.spotify.com/(track|album)/(\w+)", url)

        if match:
            return match.groups()

        return None, None

    def get_track(
        self, query: Optional[str] = None, url: Optional[str] = None, limit: int = 6
    ) -> List[TrackMetadata]:
        """
        Searches for tracks using a query to retrieve metadata.
        Alternatively, fetches track details directly from a Spotify album URL.

        Args:
            query (str): The search query for the track (e.g. track name - artist).
            url (str): The Spotify track URL.
            limit (int, optional): Maximum number of tracks to retrieve. Defaults to 6.

        Returns:
            List[TrackMetadata]: A list of track metadata.

        Raises:
            InvalidSearchLimit: If the limit is less than 1.
            NoMatchingTrackFound: If no matching tracks are found.
            MissingParameterError: If no query or URL is provided.
        """
        if limit < 1:
            raise InvalidSearchLimit

        if not query and not url:
            raise MissingParameterError("query or url")

        tracklist = []

        if url:
            response, _ = self.get_from_url(url, TYPE_TRACK)
            tracks = [response]
        else:
            params = {"q": query, "type": TYPE_TRACK, "limit": limit}
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

            # If the label name is too long, switch to the artist's name
            label = (
                track["artists"][0]["name"]
                if len(album["label"]) > 45
                else album["label"]
            )

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
                "label": label,
                "id": track["id"],
            }

            tracklist.append(TrackMetadata(**metadata))

        return tracklist

    def get_album(
        self,
        query: Optional[str] = None,
        url: Optional[str] = None,
        limit: int = 6,
        shuffle: bool = False,
    ) -> List[AlbumMetadata]:
        """
        Searches for albums using a query parameter to retrieve metadata, including track listings.
        Alternatively, fetches album details directly from a Spotify album URL.

        Args:
            query (str): The search query for the album (e.g. album name - artist).
            url (str): The Spotify album URL.
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

        if not query and not url:
            raise MissingParameterError("query or url")

        albumlist = []

        if url:
            response, _ = self.get_from_url(url, TYPE_ALBUM)
            albums = [response]
        else:
            params = {"q": query, "type": TYPE_ALBUM, "limit": limit}
            response = requests.get(
                f"{self.__BASE_URL}/search", params=params, headers=self.__AUTH_HEADER
            ).json()

            albums = response.get("albums", {}).get("items", [])

        if not albums:
            raise NoMatchingAlbumFound

        # Process each album to get details and tracklist
        for album in albums:
            id = album["id"]

            if query:
                # If searching by query, fetch additional album details using the album ID
                album_details = requests.get(
                    f"{self.__BASE_URL}/albums/{id}", headers=self.__AUTH_HEADER
                ).json()
            else:
                # If using URL, we already have full album details from the initial request
                album_details = album

            # Extract track names from album details
            tracks = [
                track["name"]
                for track in album_details.get("tracks", {}).get("items", [])
            ]

            # Shuffle tracks if true
            if shuffle:
                random.shuffle(tracks)

            # If the label name is too long, switch to the artist's name
            label = (
                album["artists"][0]["name"]
                if len(album_details["label"]) > 45
                else album_details["label"]
            )

            # Create AlbumMetadata object with formatted data
            metadata = {
                "name": album["name"],
                "artist": album["artists"][0]["name"],
                "released": self._format_release_date(
                    album["release_date"], album["release_date_precision"]
                ),
                "image": album["images"][0]["url"],
                "label": label,
                "id": album["id"],
                "tracks": tracks,
            }

            albumlist.append(AlbumMetadata(**metadata))

        return albumlist

    def get_from_url(self, url: str, type: Optional[str] = None) -> tuple[dict, str]:
        """
        Fetches a track or album from a Spotify URL.

        Args:
            url (str): The Spotify track or album URL.
            type (str, optional): The type of the URL (track or album). Defaults to None.

        Returns:
            tuple[dict, str]: A tuple containing:
                - dict: The track or album metadata from Spotify API
                - str: The type of content ('track' or 'album')

        Raises:
            InvalidTrackUrlError: If the URL provided is not a valid track URL.
            InvalidAlbumUrlError: If the URL provided is not a valid album URL.
        """

        resource_type, id = self.parse_url(url)

        # Verify the URL matches the expected content type (track/album)
        if type and type != resource_type:
            if type == TYPE_TRACK:
                raise InvalidTrackUrlError
            else:
                raise InvalidAlbumUrlError

        response = requests.get(
            f"{self.__BASE_URL}/{resource_type}s/{id}", headers=self.__AUTH_HEADER
        ).json()

        return response, resource_type
