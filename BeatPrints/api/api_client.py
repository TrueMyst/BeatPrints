"""
Module: api_client.py

Provides functionality related to interacting with any API.
"""

from typing import List
from BeatPrints.api.spotify import Spotify
from BeatPrints.api.yt_music import YtMusic
from BeatPrints.metadata import AlbumMetadata, TrackMetadata
from BeatPrints.consts import Logos


class Client:
    """
    A class for interacting with any API. Currently supports Spotify and YT Music.
    """

    def __init__(self):
        self.l = Logos()
        self.client = YtMusic()
        self.logo = self.l.YT_MUSIC
        self.use_scannable_code = False

    def set_spotify_client(self, CLIENT_ID: str, CLIENT_SECRET: str) -> None:
        """
        Sets a spotify API client as the client in use.

        Args:
            CLIENT_ID (str): Spotify API client ID.
            CLIENT_SECRET (str): Spotify API client secret.
        """
        self.client = Spotify(CLIENT_ID, CLIENT_SECRET)
        self.use_scannable_code = True
        self.logo = None

    def set_yt_music_client(self) -> None:
        """
        Sets a YouTube Music API client as the client in use.
        """
        self.client = YtMusic()
        self.use_scannable_code = False
        self.logo = self.l.YT_MUSIC

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
        track = self.client.get_track(query, limit)
        return track

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
        album = self.client.get_album(query, limit, shuffle)
        return album
