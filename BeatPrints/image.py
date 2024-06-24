"""
Module: image.py

Provides essential image functions for poster generation.

Imports:
    - os: Provides OS interaction
    - typing: Type hinting support.
    - PIL: Image processing Library
    - requests: Simplifies HTTP requests.
    - haishoku: Extracts dominant colors from images.
    - dim: Cords & Sizes for necessary texts.
"""

import os
import dim
import requests

from PIL import Image
from PIL import ImageDraw
from typing import Tuple
from haishoku.haishoku import Haishoku


def color_palette(path) -> list:
    """
    Extract the color palette from an image.

    Args:
        path (str): The path of the image file.

    Returns:
        palette (list): A list containing the colors extracted from the image.
    """

    # Get the palette
    image = Haishoku.getPalette(path)

    # Only retrieves the color
    palette = [color for _, color in image]

    # Gets the dominant color
    dominant = Haishoku.getDominant(path)
    palette.append(dominant)

    # Gets rid of duplicate colors
    np = []
    [np.append(x) for x in palette if x not in np]

    def luminance(color: Tuple[int, int, int]) -> float:
        r, g, b = color
        return 0.299 * r + 0.587 * g + 0.114 * b

    return sorted(np, key=luminance, reverse=False)


def draw_palette(draw: ImageDraw.ImageDraw, image_path: str, accent: bool):
    """
    Uses Pillow to draw the color palette on the image.

    Args:
        draw (ImageDraw.ImageDraw): An ImageDraw object to draw.
        image_path (str): The path of the image file.
        accent (bool): Flag indicating whether to include the accent color.
    """

    # Get the color palette from the image
    palette = color_palette(image_path)

    # Draw rectangles for each color on the image
    for i in range(6):

        # Position of the color palette
        x, y = dim.C_PALETTE

        # Starting Position of each colors.
        start, end = 170 * i, 170 * (i + 1)

        # Draw the palette co-ordinate wise.
        draw.rectangle(((x + start, y), (x + end, 1160)), fill=palette[i])

    # Optionally draw a rectangle to highlight the accent color
    if accent:
        draw.rectangle(dim.C_ACCENT, fill=palette[-1])


def square_crop(image_path: str, save_path: str):
    """
    Crops the image to a 1:1 ratio and saves it.

    Args:
        image_path (str): The path to the original image file.
        save_path (str): The path where the cropped image file will be saved.
    """

    # Open the image
    image = Image.open(image_path)

    # It's the chop :3 function
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


def scannable(id: str, dark_mode=False):
    """
    Generates a spotify scannable code based on tracks.

    Args:
        id (str): The ID of the track.
        dark_mode (bool): Flag indicating whether to use dark mode. Defaults to False.
    """

    # Define colors
    transparent = (0, 0, 0, 0)
    white = (255, 255, 255, 255)

    # Determine the color
    color = dim.CL_DARK_MODE if dark_mode else dim.CL_LIGHT_MODE

    # Download the Spotify scan code image
    scan = f"https://scannables.scdn.co/uri/plain/png/101010/white/1280/spotify:track:{id}"
    data = requests.get(scan)

    # Spotify code's path
    assets_path = os.path.realpath("assets")
    spotify_code_path = os.path.join(assets_path, "spotify",
                                     "spotify_code.png")

    with open(spotify_code_path, "wb") as file:
        file.write(data.content)

    with Image.open(spotify_code_path) as scan_code:

        # Convert the image into RGBA mode
        scan_code = scan_code.convert("RGBA")
        pixels = scan_code.load()

        width, height = scan_code.size

        # Iterate through pixels and make white pixels transparent
        for x in range(width):
            for y in range(height):
                if pixels is not None:
                    pixels[x, y] = transparent if pixels[x,
                                                         y] != white else color

        # Save the modified image
        scan_code.save(spotify_code_path)
