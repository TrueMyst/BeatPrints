"""
Module: deez.py

Provides methods for searching and fetching music metadata by using Deezer API client.
"""

import time
import random
import deezer

from typing import List, Literal
from dataclasses import dataclass

from BeatPrints.errors import (
    NoMatchingTrackFound,
    NoMatchingAlbumFound,
    InvalidSearchLimit,
)


@dataclass
class TrackMetadata:
    title: str
    artists: list[str]
    album: str
    released: str
    duration: str
    cover: str
    label: str


@dataclass
class AlbumMetadata:
    title: str
    artists: list[str]
    released: str
    tracks: List[str]
    cover: str
    label: str


class Deezer:
    """
    A wrapper around the Deezer API client for searching and fetching music metadata.
    """

    def __init__(self):
        self._client = deezer.Client()

    def search(
        self, query: str, stype: Literal["track", "album"] = "track", limit: int = 5
    ) -> List[dict]:
        """Searches for tracks or albums on Deezer and returns a list of results.

        Args:
            query: The search query string (e.g. "Apples - Rocco").
            stype: The type of content to search for. Must be "track" or "album". Defaults to "track".
            limit: The maximum number of results to return. Must be at least 1. Defaults to 5.

        Returns:
            A list of dicts, each containing:
                - "id" (int): The Deezer ID of the item.
                - "title" (str): The title of the track or album.
                - "artists" (list[str]): A list of contributing artist names.

        Raises:
            ValueError: If `stype` is not "track" or "album".
            InvalidSearchLimit: If `limit` is less than 1.
            NoMatchingTrackFound: If no tracks are found for the given query.
            NoMatchingAlbumFound: If no albums are found for the given query.
        """
        handlers = {
            "track": (self._client.search, NoMatchingTrackFound),
            "album": (self._client.search_albums, NoMatchingAlbumFound),
        }

        if stype not in handlers:
            raise ValueError('Invalid search type. Use "track" or "album" instead.')

        search_fn, exception = handlers[stype]

        if limit < 1:
            raise InvalidSearchLimit

        searches = search_fn(query)[:limit]

        if not searches:
            raise exception

        return [
            {
                "id": item.id,
                "title": item.title,
                "artists": [artist.name for artist in item.contributors],
            }
            for item in searches
        ]

    def get_track(self, id: int) -> TrackMetadata:
        """Fetches full metadata for a track by its Deezer ID.

        Args:
            id: The unique Deezer ID of the track.

        Returns:
            A TrackMetadata instance filled with the track's details.
        """
        track = self._client.get_track(id)

        return TrackMetadata(
            title=track.title,
            artists=[artist.name for artist in track.contributors],
            album=track.album.title,
            released=track.release_date.strftime("%B %d, %Y"),
            duration=time.strftime("%M:%S", time.gmtime(track.duration)),
            cover=track.album.cover_xl,
            label=track.album.label,
        )

    def get_album(self, id: int, shuffle: bool = False) -> AlbumMetadata:
        """Fetches full metadata for an album by its Deezer ID.

        Args:
            id: The unique Deezer ID of the album.
            shuffle: If True, the track listing will be returned in a random order. Defaults to False.

        Returns:
            An AlbumMetadata instance filled with the album's details.
        """
        album = self._client.get_album(id)
        tracks = [track.title for track in album.tracks]

        if shuffle:
            random.shuffle(tracks)

        return AlbumMetadata(
            title=album.title,
            artists=[artist.name for artist in album.contributors],
            released=album.release_date.strftime("%B %d, %Y"),
            tracks=tracks,
            cover=album.cover_xl,
            label=album.label,
        )
