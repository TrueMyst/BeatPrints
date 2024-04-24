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

import image
import lyrics
import spotify
import utils
import pathlib
import tabulate

from PIL import Image
from PIL import ImageDraw

from utils import font
from fontfallback import writing


# Get the current directory
current_dictionary = pathlib.Path(__file__).parent.resolve()

# Ask user if they want to include a custom image
WANT_CUSTOM_IMAGE = utils.confirm_input(
    "🌃 • Do you want to include a custom image as the cover of the poster?"
)

# Get custom image if user wants
CUSTOM_IMAGE = utils.validate_image_path() if WANT_CUSTOM_IMAGE else None

# Ask user if they want to add a stylish color accent
WANT_ACCENT = utils.confirm_input(
    "🤌 • Would you like to add a stylish color accent at the bottom of your poster?"
)

# Search for song on Spotify and Print them out
search_list = spotify.search_track(input("🍀 • Enter song to search: "))
heading_list = ["*", "Name", "Artist", "Album"]
format = "rounded_outline"

modified_search_list = utils.remove_column(search_list, 4)
print(tabulate.tabulate(modified_search_list, heading_list, format))

while True:
    try:
        choice = int(
            input("📋️ • Choose any song based on their index number (1 - 10): ")
        )
        if 1 <= choice <= 10:
            break
        else:
            print("🤨 • Your choice must be between 1 and 10.")
    except ValueError:
        print("🤨 • Invalid choice, try to enter a valid integer.")

track = spotify.get_trackinfo(search_list[choice - 1], CUSTOM_IMAGE)

# Get the necessary details of the song
color = (50, 47, 48)
path = current_dictionary / track["path"]
id = track["track_id"]
name = track["name"].upper()
year = track["year"].split("-")[0]
artist = track["artist"]
duration = track["duration"]
label = spotify.label(track["album_id"])
lyrics = lyrics.get_extract(track["name"], track["artist"])

# Generate the Spotify code for the song
spotify.get_code(id)


# Open the poster template image
with Image.open(current_dictionary / "assets/banner_v1.png") as poster:

    # Open the banner image
    with Image.open(path) as banner:
        banner = banner.resize((510, 510))

    # Open the Spotify code image
    with Image.open(current_dictionary / "assets/spotify_code.png") as spotify_code:
        spotify_code = spotify_code.resize((150, 38), Image.BICUBIC).convert("RGBA")

    # Paste the banner image onto the poster
    poster.paste(banner, (30, 30))

    # Paste the Spotify code onto the poster
    poster.paste(spotify_code, (20, 807), spotify_code)

    # Set font family and paths

    draw = ImageDraw.Draw(poster)

    # Draw the color palette on the poster
    image.draw_palette(draw, path, WANT_ACCENT)

    # Write the title (song name and year) on the poster
    image.heading(draw, (30, 635), 420, name, (50, 47, 48), font("Bold"))

    # Write the artist name and duration on the poster
    writing.draw_text_v2(
        draw, (30, 675), artist, (50, 47, 48), font("Regular"), 30, anchor="ls"
    )
    writing.draw_text_v2(
        draw, (496, 635), duration, (50, 47, 48), font("Regular"), 20, anchor="ls"
    )

    # Write the lyrics on the poster
    writing.draw_multiline_text_v2(
        draw, (30, 685), lyrics, (50, 47, 48), font("Light"), 21
    )

    # Write the label information on the poster
    writing.draw_text_v2(
        draw, (545, 810), label[0], (50, 47, 48), font("Regular"), 13, anchor="rt"
    )
    writing.draw_text_v2(
        draw, (545, 825), label[1], (50, 47, 48), font("Regular"), 13, anchor="rt"
    )

    # Create folder to save the poster image
    utils.create_folder()

    # Generate a unique filename for the poster image
    filename = f"{utils.create_filename(name, artist)}_{utils.special_code()}.png"
    save_path = current_dictionary / f"../images/{filename}"

    # Save the poster image
    poster.save(save_path)
    poster.show()

    print(f"☕ • Image saved in the image folder of this repository")
