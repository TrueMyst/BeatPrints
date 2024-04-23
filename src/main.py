"""
Module: main.py

This module serves as the main entry point for the BeatPrints application. 
It orchestrates the process of generating posters for songs, 
including fetching song information, processing images, and generating posters.

Dependencies:
    - pathlib: Provides an object-oriented interface for working with filesystem paths.
    - PIL: Python Imaging Library for image processing tasks.
    - image: Custom module for image processing functions.
    - lyrics: Custom module for retrieving and processing song lyrics.
    - spotify: Custom module for interacting with the Spotify API.
    - utils: Custom module containing utility functions.

Usage:
    Run this module to generate posters for songs based on user input.

"""

from PIL import Image
from PIL import ImageDraw

import image
import lyrics
import spotify
import utils
import pathlib

from fontfallback import writing

# Get the current directory
current_dictionary = pathlib.Path(__file__).parent.resolve()

# Ask user if they want to include a custom image
WANT_CUSTOM_IMAGE = utils.confirm_input(
    "[🌃] Do you want to include a custom image as the cover of the posters?"
)

# Ask user if they want to add a stylish color accent
WANT_ACCENT = utils.confirm_input(
    "[🤌] Would you like to add a stylish color accent at the bottom of your poster?"
)

# Search for song on Spotify
search = spotify.search_track(input("[🍀] Enter song to search: "), WANT_CUSTOM_IMAGE)

# Get the path of the image
path = current_dictionary / search["path"]
id = search["track_id"]
name = search["name"].upper()
year = search["year"].split("-")[0]
artist = search["artist"]
duration = search["duration"]
label = spotify.label(search["album_id"])

# Get the lyrics of the song
color = (50, 47, 48)
music_lyrics = lyrics.get_extract(search["name"], search["artist"])

# Generate the Spotify code for the song
spotify.get_code(id)

# Open the banner image
with Image.open(path) as banner:
    banner = banner.resize((510, 510))

# Open the Spotify code image
with Image.open(current_dictionary / "assets/spotify_code.png") as spotify_code:
    spotify_code = spotify_code.resize((150, 38), Image.BICUBIC).convert("RGBA")

# Open the poster template image
with Image.open(current_dictionary / "assets/banner_v1.png") as poster:

    # Paste the banner image onto the poster
    poster.paste(banner, (30, 30))

    # Paste the Spotify code onto the poster
    poster.paste(spotify_code, (20, 807), spotify_code)

    # Set font family and paths
    # font_dir = pathlib.Path.resolve(current_dictionary / f"../fonts/{FONT_FAMILY}/")

    fonts_regular = writing.load_fonts(
        "../fonts/Oswald/Oswald-Regular.ttf",
        "../fonts/NotoSansJP/NotoSansJP-Regular.ttf",
        "../fonts/NotoSansKR/NotoSansKR-Regular.ttf",
        "../fonts/NotoSansTC/NotoSansTC-Regular.ttf",
        "../fonts/NotoSansSC/NotoSansSC-Regular.ttf",
    )

    fonts_bold = writing.load_fonts(
        "../fonts/Oswald/Oswald-Bold.ttf",
        "../fonts/NotoSansJP/NotoSansJP-Bold.ttf",
        "../fonts/NotoSansKR/NotoSansKR-Bold.ttf",
        "../fonts/NotoSansTC/NotoSansTC-Bold.ttf",
        "../fonts/NotoSansSC/NotoSansSC-Bold.ttf",
    )

    fonts_light = writing.load_fonts(
        "../fonts/Oswald/Oswald-Light.ttf",
        "../fonts/NotoSansJP/NotoSansJP-Light.ttf",
        "../fonts/NotoSansKR/NotoSansKR-Light.ttf",
        "../fonts/NotoSansTC/NotoSansTC-Light.ttf",
        "../fonts/NotoSansSC/NotoSansSC-Light.ttf",
    )

    # Create ImageDraw object for drawing on the poster
    draw = ImageDraw.Draw(poster)

    # Draw the color palette on the poster
    image.draw_palette(draw, path, WANT_ACCENT)

    # Write the title (song name and year) on the poster
    image.heading(draw, (30, 635), 420, name, (50, 47, 48), fonts_bold)

    # # Write the artist name and duration on the poster
    writing.draw_text_v2(
        draw, (30, 670), artist, (50, 47, 48), fonts_regular, 30, anchor="ls"
    )
    writing.draw_text_v2(
        draw, (496, 635), duration, (50, 47, 48), fonts_regular, 20, anchor="ls"
    )

    # # Write the lyrics on the poster
    writing.draw_multiline_text_v2(
        draw, (30, 685), music_lyrics, (50, 47, 48), fonts_light, 21
    )

    # # Write the label information on the poster
    writing.draw_text_v2(
        draw, (545, 810), label[0], (50, 47, 48), fonts_regular, 13, anchor="rt"
    )
    writing.draw_text_v2(
        draw, (545, 825), label[1], (50, 47, 48), fonts_regular, 13, anchor="rt"
    )

    # Create folder to save the poster image
    utils.create_folder()

    # Generate a unique filename for the poster image
    filename = f"{utils.create_filename(name, artist)}_{utils.special_code()}"
    output_path = current_dictionary / f"../images/{filename}.png"

    # Save the poster image
    poster.save(output_path)
    poster.show()
    print(f"[☕] Image saved to {output_path}")
