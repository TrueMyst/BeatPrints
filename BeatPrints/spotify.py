"""
Module: spotify.py

Provides methods to retrieve track and album metadata from search queries, IDs, URIs, or URLs.
"""

import re
import random
import spotipy
import datetime

from typing import List
from dataclasses import dataclass

from spotipy.exceptions import SpotifyException
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.cache_handler import MemoryCacheHandler

from BeatPrints.errors import (
    NoMatchingTrackFound,
    NoMatchingAlbumFound,
    InvalidSearchLimit,
)


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
    A class for interacting with the Spotify API to search and retrieve track and album metadata.
    """

    def __init__(self, CLIENT_ID: str, CLIENT_SECRET: str) -> None:
        """
        Initializes the Spotify client with credentials and obtains an access token.

        Args:
            CLIENT_ID (str): Spotify API client ID.
            CLIENT_SECRET (str): Spotify API client secret.
        """
        authorization = SpotifyClientCredentials(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            cache_handler=MemoryCacheHandler(),
        )

        self.spotify = spotipy.Spotify(client_credentials_manager=authorization)

    def _is_spotify_id(self, id: str) -> bool:
        """
        Checks if the provided string is a valid Spotify ID, URI, or URL.

        A valid Spotify identifier can be one of the following formats:
        - Spotify URI: "spotify:{type}:{id}"
        - Spotify URL: "https://open.spotify.com/{type}/{id}"
        - Spotify ID: A 22-character Base62 string

        Args:
            id (str): The string to be checked.

        Returns:
            bool: True if the input matches any of the valid Spotify ID formats.
        """
        # Remove query parameters (e.g., ?si=...)
        id = id.split("?")[0]

        # Spotify URI: spotify:album:id or spotify:track:id
        if re.fullmatch(r"spotify:(track|album):[0-9A-Za-z]{22}", id):
            return True

        # Spotify URL: http(s)://open.spotify.com/album/id or /track/id
        if re.fullmatch(
            r"https?://open\.spotify\.com/(track|album)/[0-9A-Za-z]{22}", id
        ):
            return True

        # Spotify ID: 22-character Base62 string
        if re.fullmatch(r"[0-9A-Za-z]{22}", id):
            return True

        return False

    def _get_track_metadata(self, track: dict) -> TrackMetadata:
        """
        Returns TrackMetadata from a Spotify track object.

        Args:
            track (dict): Spotify track object

        Returns:
            List[TrackMetadata]: A list of track metadata.
        """

        album = self.spotify.album(track["album"]["id"])

        metadata = {
            "name": track["name"],
            "artist": track["artists"][0]["name"],
            "album": album["name"],
            "released": self._format_released(
                track["album"]["release_date"], track["album"]["release_date_precision"]
            ),
            "duration": self._format_duration(track["duration_ms"]),
            "image": track["album"]["images"][0]["url"],
            "label": (
                album["label"]
                if len(album["label"]) < 35
                else track["artists"][0]["name"]
            ),
            "id": track["id"],
        }

        return TrackMetadata(**metadata)

    def _get_album_metadata(self, album: dict, shuffle: bool) -> AlbumMetadata:
        """
        Returns AlbumMetadata from a Spotify album object.

        Args:
            album (dict): Spotify album object

        Returns:
            List[AlbumMetadata]: A list of album metadata with track listings.
        """

        # Extract track names
        tracks = [track["name"] for track in album["tracks"]["items"]]

        if shuffle:
            random.shuffle(tracks)

        metadata = {
            "name": album["name"],
            "artist": album["artists"][0]["name"],
            "released": self._format_released(
                album["release_date"], album["release_date_precision"]
            ),
            "image": album["images"][0]["url"],
            "label": (
                album["label"]
                if len(album["label"]) < 35
                else album["artists"][0]["name"]
            ),
            "id": album["id"],
            "tracks": tracks,
        }

        return AlbumMetadata(**metadata)

    def _format_released(self, release_date: str, precision: str) -> str:
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
        Searches for tracks based on a query or Spotify ID/URI/URL and retrieves their metadata.

        Args:
            query (str): The search query or Spotify ID/URI/URL for the track.
            limit (int, optional): Max number of tracks to retrieve (only applies to search by text). Defaults to 6.

        Returns:
            List[TrackMetadata]: A list of track metadata.

        Raises:
            InvalidSearchLimit: If the limit is less than 1.
            NoMatchingTrackFound: If no matching tracks are found.
        """

        try:
            # If query is a Spotify ID/URI/URL, fetch a single track directly
            if self._is_spotify_id(query):
                track = self.spotify.track(query)
                return [self._get_track_metadata(track)]

            else:
                if limit < 1:
                    raise InvalidSearchLimit

                search = self.spotify.search(q=query, type="track", limit=limit)
                return [
                    self._get_track_metadata(track)
                    for track in search["tracks"]["items"]
                ]

        except SpotifyException:
            raise NoMatchingTrackFound

    def get_album(
        self, query: str, limit: int = 6, shuffle: bool = False
    ) -> List[AlbumMetadata]:
        """
        Searches for album based on a query or Spotify ID/URI/URL and retrieves their metadata.

        Args:
            query (str): The search query or Spotify ID/URI/URL for the album.
            limit (int, optional): Max number of albums to retrieve (only applies to search by text). Defaults to 6.
            shuffle (bool, optional): Whether to shuffle the track list. Defaults to False.

        Returns:
            List[AlbumMetadata]: A list of album metadata with track listings.

        Raises:
            InvalidSearchLimit: If the limit is less than 1.
            NoMatchingAlbumFound: If no matching albums are found.
        """

        try:
            # If query is a Spotify ID/URI/URL, fetch a single album directly
            if self._is_spotify_id(query):
                album = self.spotify.album(query)
                return [self._get_album_metadata(album, shuffle)]

            else:
                if limit < 1:
                    raise InvalidSearchLimit

                result = self.spotify.search(q=query, type="album", limit=limit)
                return [
                    self._get_album_metadata(self.spotify.album(album["id"]), shuffle)
                    for album in result["albums"]["items"]
                ]

        except SpotifyException:
            raise NoMatchingAlbumFound
