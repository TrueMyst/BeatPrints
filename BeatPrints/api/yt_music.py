"""
Module: yt_music.py

Provides functionality related to interacting with the YouTube Music API.
"""

import re
import random
import asyncio

from typing import List

from ytmusicapi import YTMusic


from BeatPrints.errors import (
    NoMatchingTrackFound,
    NoMatchingAlbumFound,
    InvalidSearchLimit,
)
from BeatPrints.metadata import AlbumMetadata, TrackMetadata
from BeatPrints.utils import format_released, format_duration


class YtMusic:
    """
    A class for interacting with the YouTube Music API
    to search and retrieve track/album information.
    """

    def __init__(self) -> None:
        """
        Initializes the YouTube Music client.
        """
        self.yt_music = YTMusic()

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
        result = self.yt_music.search(query=query, limit=limit, filter="songs")

        if not result:
            raise NoMatchingTrackFound

        for track in result:
            if (
                track.get("album")
                and track.get("album").get("id")
                and track.get("resultType") == "song"
            ):
                tracklist.append(track)

        # A track requires to get its album for additional data,
        # meaning too many blocking events would occur
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(
                asyncio.gather(*(self.get_track_metadata(track) for track in tracklist))
            )
        finally:
            loop.close()

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

        result = self.yt_music.search(query=query, filter="albums", limit=limit)

        if not result:
            raise NoMatchingAlbumFound

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(
                asyncio.gather(
                    *(
                        self.get_album_data(album["browseId"], shuffle)
                        for album in result
                    )
                )
            )
        finally:
            loop.close()

    def format_time_ms(self, duration: str):
        """
        Formats a string duration (HH:MM:SS) to miliseconds.

        Args:
            duration (str): The duration to convert to ms
        Returns:
            int: The duration of the track in ms
        """
        durations = duration.split(":")

        mults = [60 * 60 * 1000, 60 * 1000, 1000]
        if len(durations) == 2:
            mults = [60 * 1000, 1000]
        elif len(durations) == 1:
            mults = [1000]

        duration_ms = 0
        for duration, mult in zip(durations, mults):
            duration_ms += int(duration) * mult

        return duration_ms

    async def get_track_metadata(self, track: dict):
        """
        Asynchronously get metadata from a tracK.

        Args:
            track: The track to get the metadata from

        Returns:
            TrackMetadata: The metadata related to the track
        """
        loop = asyncio.get_running_loop()
        album = await loop.run_in_executor(
            None, self.yt_music.get_album, track.get("album").get("id")
        )
        id = track.get("videoId")
        name = track["title"]
        album_name = track.get("album").get("name")
        artist = track["artists"][0]["name"]
        # Replace img url with a higher res one
        image = self._get_upscaled_image(track["thumbnails"][0]["url"])
        # YT Music doesn't record the label
        label = artist
        duration = format_duration(self.format_time_ms(track["duration"]))
        release_date = album.get("releaseDate")
        # Worst case scenario: get the date from the track, which could be the upload date!
        if release_date is None:
            song = await loop.run_in_executor(None, self.yt_music.get_song, id)
            release_date = (
                song["microformat"].get("microformatDataRenderer").get("publishDate")
            )
        released = format_released(release_date.split("T")[0], "day")

        url = None
        if id:
            url = f"https://music.youtube.com/watch?v={id}"

        # Create TrackMetadata object with formatted data
        metadata = {
            "name": name,
            "artist": artist,
            "album": album_name,
            "released": released,
            "duration": duration,
            "image": image,
            "label": label,
            "url": url,
            "id": id,
        }
        return TrackMetadata(**metadata)

    async def get_album_data(self, id: str, shuffle: bool = False):
        """
        Asynchronously get metadata from an album.

        Args:
            id: The album id to get metadata from

        Returns:
            AlbumMetadata: The metadata related to the album
        """
        loop = asyncio.get_running_loop()
        album = await loop.run_in_executor(None, self.yt_music.get_album, id)
        if album is not None:
            # Extract track names from album details
            tracks = [track["title"] for track in album["tracks"]]

            # Shuffle tracks if true
            if shuffle:
                random.shuffle(tracks)

            name = album["title"]
            artist = album["artists"][0]["name"]
            image = self._get_upscaled_image(album["thumbnails"][0]["url"])

            # If the label name is too long, use the artist's name
            label = artist

            song = self.yt_music.get_song(album.get("tracks")[0].get("videoId"))
            released_date = album.get("year")
            precision = "year"
            if song.get("microformat") is not None:
                released_date = (
                    song.get("microformat")
                    .get("microformatDataRenderer")
                    .get("publishDate")
                    .split("T")[0]
                )
                precision = "day"
            released = format_released(
                released_date,
                precision=precision,
            )

            url = None
            if album.get("audioPlaylistId"):
                url = f"https://music.youtube.com/playlist?list={album.get("audioPlaylistId")}"

            # Create AlbumMetadata object with formatted data
            metadata = {
                "name": name,
                "artist": artist,
                "released": released,
                "image": image,
                "label": label,
                "id": id,
                "tracks": tracks,
                "url": url,
            }

            return AlbumMetadata(**metadata)

    def _get_upscaled_image(self, url: str, width=2400, height=2400):
        """
        Returns a URL that points to a higher res track/album image
        for YT Music.

        Args:
            url: The URL to change
            width: The image width
            height: The image height
        Returns:
            The URL that points to the image of specified width and height
        """
        parts = url.split("=", 1)
        if len(parts) != 2:
            return url

        base, params = parts
        params = re.sub(r"w\d+", f"w{width}", params)
        params = re.sub(r"h\d+", f"h{height}", params)
        return f"{base}={params}"
