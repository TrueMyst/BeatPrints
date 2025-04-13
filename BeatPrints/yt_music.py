"""
Module: yt_music.py

Provides functionality related to interacting with the YouTube Music API.
"""

import re

from ytmusicapi import YTMusic
import random
import datetime

from typing import List
from dataclasses import dataclass

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
    url: str = None


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
    url: str = None


class YtMusic:
    """
    A class for interacting with the YouTube Music API to search and retrieve track/album information.
    """

    def __init__(self) -> None:
        """
        Initializes the Spotify client with credentials and obtains an access token.
        """
        self.yt_music = YTMusic()

    def _format_released(self, release_date: str, precision: str) -> str:
        """
        Formats the release date of a track or album.

        Args:
            release_date (str): Release date string from Spotify API.
            precision (str): Precision of the release date ('day', 'month', 'year').

        Returns:
            str: Formatted release date in 'Month Day, Year' format.
        """
        print(release_date)
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
        result = self.yt_music.search(query=query, limit=limit, filter="songs")

        if not result:
            raise NoMatchingTrackFound

        tracks = result

        for track in tracks:
            # TODO: better way to get an album
            video_id = track["videoId"]
            album = self.yt_music.search(query=query, limit=1, filter="albums")[0]

            if album["browseId"] is None:
                continue

            if album["browseId"] is not None:
                id = video_id
                song = self.yt_music.get_song(id)
                name = track["title"]
                album_name = album["title"]
                artist = track["artists"][0]["name"]
                # replace img url with a higher res one
                image = self._get_upscaled_image(track["thumbnails"][0]["url"])
                # TODO: get label
                label = artist
                duration = track["duration"]

                # TODO: find how to get a more precise release date
                release_date = album.get("releaseDate")
                if release_date is None:
                    release_date = (
                        song["microformat"]
                        .get("microformatDataRenderer")
                        .get("publishDate")
                    )
                released = self._format_released(release_date.split("T")[0], "day")

                url = None
                if video_id:
                    url = f"https://music.youtube.com/watch?v={video_id}"

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
        result = self.yt_music.search(query=query, filter="albums", limit=limit)

        if not result:
            raise NoMatchingAlbumFound

        albums = result

        for album in albums:
            id = album["browseId"]
            album = self.yt_music.get_album(id)

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
                released = self._format_released(
                    released_date,
                    precision=precision,
                )
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

                albumlist.append(AlbumMetadata(**metadata))
        return albumlist

    def _get_upscaled_image(self, url: str, width=2048, height=2048):
        """
        Returns a URL that points to a higher res track/album image/
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
