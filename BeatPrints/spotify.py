"""
Module: spotify.py

Provides functionality related to interacting with the Spotify API.
"""

import spotipy
import random
import datetime

from typing import List
from dataclasses import dataclass

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
    A class for interacting with the Spotify API to search and retrieve track/album information.
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
        result = self.spotify.search(q=query, type="track", limit=limit)

        if not result:
            raise NoMatchingTrackFound

        tracks = result["tracks"]["items"]

        for track in tracks:
            album_id = track["album"]["id"]

            # If a track doesn't have an album id, skip it
            if album_id is None:
                continue

            album = self.spotify.album(album_id)

            if album is not None:
                id = track["id"]
                name = track["name"]
                album_name = album["name"]
                artist = track["artists"][0]["name"]
                image = track["album"]["images"][0]["url"]

                # If the label name is too long, use the artist's name
                label = album["label"] if len(album["label"]) < 35 else artist

                duration = self._format_duration(track["duration_ms"])
                released = self._format_released(
                    track["album"]["release_date"],
                    track["album"]["release_date_precision"],
                )

                # Create TrackMetadata object with formatted data
                metadata = {
                    "name": name,
                    "artist": artist,
                    "album": album_name,
                    "released": released,
                    "duration": duration,
                    "image": image,
                    "label": label,
                    "id": id,
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
        result = self.spotify.search(q=query, type="album", limit=limit)

        if not result:
            raise NoMatchingAlbumFound

        albums = result["albums"]["items"]

        for album in albums:
            id = album["id"]
            album = self.spotify.album(id)

            if album is not None:
                # Extract track names from album details
                items = album["tracks"]["items"]
                tracks = [track["name"] for track in items]

                # Shuffle tracks if true
                if shuffle:
                    random.shuffle(tracks)

                id = album["id"]
                name = album["name"]
                artist = album["artists"][0]["name"]
                image = album["images"][0]["url"]

                # If the label name is too long, use the artist's name
                label = album["label"] if len(album["label"]) < 35 else artist

                released = self._format_released(
                    album["release_date"],
                    album["release_date_precision"],
                )

                # Create AlbumMetadata object with formatted data
                metadata = {
                    "name": name,
                    "artist": artist,
                    "released": released,
                    "image": image,
                    "label": label,
                    "id": id,
                    "tracks": tracks,
                }

                albumlist.append(AlbumMetadata(**metadata))

        return albumlist
