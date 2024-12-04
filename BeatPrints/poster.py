"""
Module: poster.py

Generates poster based on the track info and lyrics.
"""

import os, requests, random
from typing import Optional, Union
from PIL import Image, ImageDraw

from . import image, write, utils

from .consts import *
from .errors import PathNotFoundError
from .spotify import TrackMetadata, AlbumMetadata


class Poster:
    """
    A class to generate and save posters containing track or album information.

    Attributes:
        save_path (str): Directory where generated posters will be saved.
    """

    def __init__(self, save_path: str):
        """
        Initializes the Poster instance.

        Args:
            save_path (str): Path where posters will be saved.
        """
        self.save_path = save_path
        self.P_MEDIA = os.path.join(save_path, "media")

    def _ensure_directory(self):
        """
        Ensures the save and media directories exist.
        """
        if not self.save_path or not os.path.exists(self.save_path):
            raise PathNotFoundError

        else:
            os.makedirs(self.P_MEDIA, exist_ok=True)

    def _fetch_or_crop_image(
        self, image_url: str, custom_path: Optional[str], save_to: str
    ):
        """
        Fetches an image from a URL or processes a custom one.

        Args:
            image_url (str): URL to fetch image.
            custom_path (Optional[str]): Path to custom image.
            save_to (str): Destination to save processed image.
        """

        if custom_path:
            image.crop(custom_path, save_to)
        else:
            with open(save_to, "wb") as file:
                file.write(requests.get(image_url).content)
            image.magicify(save_to)

    def _get_theme(self, dark_theme: bool):
        """
        Determines theme-related properties.

        Args:
            dark_theme (bool): Whether to use a dark theme.

        Returns:
            Tuple containing theme color, template path, and cover path.
        """
        color, template = (
            (CL_DARK_MODE, "banner_dark.png")
            if dark_theme
            else (CL_LIGHT_MODE, "banner_light.png")
        )
        template_path = os.path.join(P_TEMPLATES, template)
        cover_path = os.path.join(self.P_MEDIA, "cover.jpg")
        return color, template_path, cover_path

    def _add_common_text(
        self,
        draw: ImageDraw.ImageDraw,
        metadata: Union[TrackMetadata, AlbumMetadata],
        color: tuple,
    ):
        """
        Adds common text like title, artist, and label info.

        Args:
            draw (ImageDraw.ImageDraw): Draw context.
            metadata: Metadata containing the required text.
            color (tuple): Text color.
        """
        write.heading(
            draw,
            C_HEADING,
            875,
            metadata.name.upper(),
            color,
            write.font("Bold"),
            S_HEADING,
        )
        write.text(
            draw,
            C_ARTIST,
            metadata.artist,
            color,
            write.font("Regular"),
            S_ARTIST,
            anchor="ls",
        )
        write.text(
            draw,
            C_LABEL,
            f"{metadata.released}\n{metadata.label}",
            color,
            write.font("Regular"),
            S_LABEL,
            anchor="rt",
        )

    def _add_images(
        self,
        draw: ImageDraw.ImageDraw,
        poster: Image.Image,
        cover_path: str,
        scannable_path: str,
        accent: bool,
    ):
        """
        Adds images like cover art and spotify scannable code to the poster.

        Args:
            draw (ImageDraw.ImageDraw): Draw context.
            poster (Image.Image): Poster canvas.
            cover_path (str): Path to cover art.
            scannable_path (str): Path to Spotify code.
            accent (bool): Whether to add design accents.
        """
        with Image.open(cover_path) as cover:
            cover = cover.resize(S_COVER)

        with Image.open(scannable_path) as scannable:
            scannable = scannable.resize(
                S_SPOTIFY_CODE, Image.Resampling.BICUBIC
            ).convert("RGBA")

        poster.paste(cover, C_COVER)
        poster.paste(scannable, C_SPOTIFY_CODE, scannable)
        image.draw_palette(draw, cover_path, accent)

    def generate_poster(
        self,
        metadata: TrackMetadata,
        lyrics: str,
        accent: bool = False,
        dark_theme: bool = False,
        custom_cover: Optional[str] = None,
    ):
        """
        Generates a track poster.

        Args:
            metadata (TrackMetadata): Track metadata.
            lyrics (str): Track lyrics.
            accent (bool): Adds design accents.
            dark_theme (bool): Use dark theme.
            custom_cover (Optional[str]): Path to custom cover art.
        """
        self._ensure_directory()
        color, template_path, cover_path = self._get_theme(dark_theme)
        self._fetch_or_crop_image(metadata.image, custom_cover, cover_path)
        scannable_path = image.scannable(metadata.id, self.P_MEDIA, dark_theme)

        with Image.open(template_path) as poster:
            poster = poster.convert("RGB")
            draw = ImageDraw.Draw(poster)

            self._add_images(draw, poster, cover_path, scannable_path, accent)
            self._add_common_text(draw, metadata, color)

            write.text(
                draw,
                C_DURATION,
                metadata.duration,
                color,
                write.font("Regular"),
                S_DURATION,
                anchor="rs",
            )
            write.text(
                draw,
                C_LYRICS,
                lyrics,
                color,
                write.font("Light"),
                S_LYRICS,
                anchor="lt",
            )

            filename = utils.create_filename(metadata.name, metadata.artist)
            poster.save(os.path.join(self.save_path, filename))
            print(
                f"✨ Poster for {metadata.name} by {metadata.artist} saved to {self.save_path}"
            )

    def generate_album(
        self,
        metadata: AlbumMetadata,
        accent: bool = False,
        dark_theme: bool = False,
        indexing: bool = False,
        coverart: Optional[str] = None,
    ):
        """
        Generates an album poster with album info and track listing.

        Args:
            metadata (AlbumMetadata): Album metadata containing tracks, name, artist, etc.
            accent (bool): Adds design accents.
            dark_theme (bool): Use dark theme.
            indexing (bool): Add index numbers to track listings.
            covertart (Optional[str]): Path to custom cover art.
        """
        self._ensure_directory()
        color, template_path, cover_path = self._get_theme(dark_theme)
        self._fetch_or_crop_image(metadata.image, coverart, cover_path)

        scannable_path = image.scannable(
            metadata.id, self.P_MEDIA, dark_theme, is_album=True
        )

        with Image.open(template_path) as poster:
            poster = poster.convert("RGB")
            draw = ImageDraw.Draw(poster)

            self._add_images(draw, poster, cover_path, scannable_path, accent)
            self._add_common_text(draw, metadata, color)

            # Shuffle and optionally index tracks
            tracks = metadata.tracks[:]
            random.shuffle(tracks)
            if indexing:
                tracks = [f"{i + 1}. {track}" for i, track in enumerate(tracks)]

            # Organize tracks into columns
            tracklist, track_widths = utils.organize_tracks(tracks)

            # Render each column of tracks
            x, y = C_TRACKS
            for track_column, column_width in zip(tracklist, track_widths):
                write.text(
                    draw,
                    (x, y),
                    "\n".join(track_column),
                    color,
                    write.font("Light"),
                    S_TRACKS,
                    anchor="lt",
                    spacing=0,
                )
                x += column_width + S_SPACING  # Move x-coordinate for next column

            # Save the poster
            filename = utils.create_filename(metadata.name, metadata.artist)
            poster.save(os.path.join(self.save_path, filename))
            print(
                f"✨ Album poster for {metadata.name} by {metadata.artist} saved to {self.save_path}"
            )
