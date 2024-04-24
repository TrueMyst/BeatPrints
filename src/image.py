"""
Module: image.py

Dependicies:
    1. PIL: Image Processing
    2. color: Extract color palette
"""

import pathlib
from pathlib import Path

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import color
from fontTools.ttLib import TTFont
from typing import Dict

from fontfallback import writing

# Get the current dictionary path
path_to_current_dictionary = pathlib.Path(__file__).parent.resolve()


def draw_palette(draw: ImageDraw.ImageDraw, image_path: str, accent: bool):
    """
    Draws the color palette on the image.

    Args:
        draw (ImageDraw.ImageDraw): An ImageDraw object to draw on the image.
        image_path (str): The path of the image file.
        accent (bool): Flag indicating whether to highlight the accent color.
    """

    # Get the color palette from the image
    color_palette = color.get_color_palette(image_path)
    # Draw rectangles for each color in the palette

    for i in range(6):
        start, end = 85 * i, 85 * (i + 1)
        draw.rectangle(((30 + start, 560), (30 + end, 580)), fill=color_palette[i])

    # Optionally draw a rectangle to highlight the accent color
    if accent:
        draw.rectangle(((0, 860), (570, 870)), fill=color_palette[-1])


def crop_to_square(image_path: Path, save_path: Path):
    """
    Crops the image to a square aspect ratio and saves it.

    Args:
        image_path (str): The path of the original image file.
        save_path (str): The path where the cropped image will be saved.
    """

    # Open the image
    image = Image.open(image_path)

    # Function to crop the image to a square aspect ratio
    def chop(image):
        width, height = image.size
        min_dimension = min(width, height)
        left = (width - min_dimension) / 2
        top = (height - min_dimension) / 2
        right = (width + min_dimension) / 2
        bottom = (height + min_dimension) / 2
        return image.crop((left, top, right, bottom))

    # Crop the image to a 1:1 ratio and save it
    cropped_image = chop(image)
    cropped_image.save(save_path)


def remove_white_pixel(image_path: Path):
    """
    Removes white pixels from the image background and makes them transparent.

    Args:
        image_path (str): The path of the image file.
    """

    # Open the image as img
    with Image.open(image_path) as img:

        # Convert the image into RGBA mode
        img = img.convert("RGBA")
        pixels = img.load()

        # Define colors
        transparent = (0, 0, 0, 0)
        white = (255, 255, 255, 255)

        width, height = img.size

        # Iterate through pixels and make white pixels transparent
        for x in range(width):
            for y in range(height):
                pixels[x, y] = (
                    transparent if pixels[x, y] != white else (50, 47, 48, 255)
                )

        # Save the modified image
        img.save(path_to_current_dictionary / "assets/spotify_code.png")


def heading(
    draw: ImageDraw.ImageDraw,
    xy: tuple,
    width_limit: int,
    text: str,
    color: tuple,
    fonts: Dict[str, TTFont],
):
    """
    A custom made function that draws a title consisting of a song name and year on the image.

    Args:
        draw (ImageDraw.ImageDraw): An ImageDraw object to draw on the image.
        textbox (tuple): Coordinates (x1, y1, x2, y2) defining the bounding box for the title.
        name (str): The song name.
        year (str): The release year of the song.
        font (str): The path to the font file.
        initial_size (int): The initial font size.
    """

    font_size = 35
    total_length_of_heading = 0
    chunked = writing.merge_chunks(text, fonts)

    while True:
        for word, path in chunked:
            font = ImageFont.truetype(path, font_size)
            total_length_of_heading += font.getlength(word)

        if total_length_of_heading > width_limit:
            font_size -= 1
            total_length_of_heading = 0

        elif total_length_of_heading <= width_limit:
            break

    y_offset = 0

    # Draw song name and year
    for words, path in chunked:
        xy_ = (xy[0] + y_offset, xy[1])

        font = ImageFont.truetype(path, font_size)
        draw.text(
            xy=xy_,
            text=words,
            fill=color,
            font=font,
            anchor="ls",
            embedded_color=True,
        )

        draw.text
        box = font.getbbox(words[0])
        y_offset += box[2] - box[0]
