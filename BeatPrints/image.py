"""
Module: image.py

Provides essential image functions to generate posters.
"""

import os
import random
import requests

from .consts import *

from typing import List, Tuple
from Pylette import extract_colors
from PIL import Image, ImageDraw, ImageEnhance


def c_palette(image_path: str) -> List[Tuple]:
    """
    Extracts a color palette from an image.

    Args:
        image_path (str): The path to the image file.

    Returns:
        palette (List[Tuple]): A list of RGB tuples representing the color palette.
    """
    extract = extract_colors(image=image_path, palette_size=6, sort_mode="luminance")
    palette = [tuple(color.rgb) for color in extract]

    return palette


def draw_palette(draw: ImageDraw.ImageDraw, image_path: str, accent: bool) -> None:
    """
    Uses Pillow to draw the color palette on the image.

    Args:
        draw (ImageDraw.ImageDraw): An ImageDraw object to draw.
        image_path (str): The path to the image file.
        accent (bool): Flag indicating whether to include the accent color.
    """

    palette = c_palette(image_path)

    # Draw rectangles for each color on the image
    for n in range(6):

        # Position of the current color in the palette
        x, y = C_PALETTE

        # Starting Position of each color
        start, end = 170 * n, 170 * (n + 1)

        # Draw the palette coordinate-wise
        draw.rectangle(((x + start, y), (x + end, 1160)), fill=palette[n])

    # Optionally draw a rectangle to highlight the accent color
    if accent:
        draw.rectangle(C_ACCENT, fill=palette[random.randint(0, 2)])


def crop(image_path: str, output_path: str) -> None:
    """
    Crops an image to a 1:1 aspect ratio.

    Args:
        image_path (str): The path to the image file.
        output_path (str): The path to save the cropped image.
    """

    def chop(image):
        width, height = image.size
        min_dimension = min(width, height)
        left = (width - min_dimension) / 2
        top = (height - min_dimension) / 2
        right = (width + min_dimension) / 2
        bottom = (height + min_dimension) / 2
        return image.crop((left, top, right, bottom))

    # Crop to 1:1 ratio
    with Image.open(image_path) as img:
        img_cropped = chop(img)
        img_cropped.save(output_path)


def magicify(image_path: str) -> None:
    """
    Adjusts the brightness and the contrast of the image.

    Args:
        image_path (str): The path to the image file.
    """
    with Image.open(image_path) as img:

        # Adjust brightness by -10%
        brightness_enhancer = ImageEnhance.Brightness(img)
        img_brightness = brightness_enhancer.enhance(0.9)

        # Adjust contrast by -20%
        contrast_enhancer = ImageEnhance.Contrast(img_brightness)
        img_contrast = contrast_enhancer.enhance(0.8)

        # Save the modified image
        img_contrast.save(image_path)


def scannable(
    id: str, save_path: str, darktheme: bool = False, is_album: bool = False
) -> str:
    """
    Generates a Spotify scannable code based on a track or album.

    Args:
        id (str): The ID of the track or album.
        save_path (str): The path to save the scannable code.
        darktheme (bool): Flag indicating whether to use dark theme. Defaults to False.
        is_album (bool): Flag indicating if the ID is for an album. Defaults to False.

    Returns:
        scannable_path (str): The path where the scannable code will be saved.
    """

    # Determine the color
    color = CL_DARK_MODE if darktheme else CL_LIGHT_MODE

    # Download the Spotify scan code image
    item_type = "album" if is_album else "track"
    scan = f"https://scannables.scdn.co/uri/plain/png/101010/white/1280/spotify:{item_type}:{id}"
    data = requests.get(scan)

    # Spotify code's path
    scannable_path = os.path.join(save_path, "scannable.png")

    # Save the scannable code
    with open(scannable_path, "wb") as file:
        file.write(data.content)

    # Turn it into a transparent code
    with Image.open(scannable_path) as scan_code:
        scan_code = scan_code.convert("RGBA")
        pixels = scan_code.load()

        width, height = scan_code.size

        # Iterate through pixels and make white pixels transparent
        for x in range(width):
            for y in range(height):
                if pixels is not None:
                    pixels[x, y] = CL_TRANSPARENT if pixels[x, y] != CL_WHITE else color

        # Save the modified image
        scan_code.save(scannable_path)

    return scannable_path
