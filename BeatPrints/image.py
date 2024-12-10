"""
Module: image.py

Provides essential image functions to generate posters.
"""

import random
import requests

from io import BytesIO
from typing import List, Tuple, Optional

from Pylette import extract_colors
from PIL import Image, ImageDraw, ImageEnhance

from .consts import *
from .errors import PathNotFoundError


def get_palette(image: Image.Image) -> List[Tuple]:
    """
    Extracts a color palette from an image.

    Args:
        image (Image.Image): The image from which the color palette will be extracted.

    Returns:
        List[Tuple]: A list of RGB tuples representing the dominant colors in the image.
    """

    # Save the image to an in-memory byte stream in PNG format
    with BytesIO() as byte_stream:
        image.save(byte_stream, format="PNG")

        # Get the byte data
        img_bytes = byte_stream.getvalue()

    # Extract the color palette
    colors = extract_colors(image=img_bytes, palette_size=6, sort_mode="luminance")

    # Return the color palette
    return [tuple(color.rgb) for color in colors]


def draw_palette(
    draw: ImageDraw.ImageDraw, image: Image.Image, accent: bool = False
) -> None:
    """
    Draws a color palette on the given image using Pillow.

    Args:
        draw (ImageDraw.ImageDraw): The drawing context for the image.
        image (Image.Image): The image on which to draw the palette.
        accent (bool): If True, highlights an accent color in the palette.
    """

    palette = get_palette(image)

    # Draw the palette as rectangles on the image
    for i in range(6):

        # Calculate the position and size for each color rectangle
        x, y = C_PALETTE
        start, end = 170 * i, 170 * (i + 1)

        # Draw the color rectangle
        draw.rectangle(((x + start, y), (x + end, 1160)), fill=palette[i])

    # Optionally draw the accent color at the bottom
    if accent:
        draw.rectangle(C_ACCENT, fill=palette[random.randint(0, 2)])


def crop(path: str) -> Image.Image:
    """
    Crops an image to a square (1:1) aspect ratio.

    Args:
        path (str): The path to the image file.

    Returns:
        Image.Image: The cropped image with a 1:1 aspect ratio.

    Raises:
        PathNotFoundError: If the path to the image file doesn't exists
    """

    def chop(image: Image.Image) -> Image.Image:
        # Get the dimensions of the image
        width, height = image.size
        min_dim = min(width, height)

        # Calculate the cropping box to make the image square
        left = (width - min_dim) / 2
        top = (height - min_dim) / 2
        right = (width + min_dim) / 2
        bottom = (height + min_dim) / 2

        # Crop and return the image
        return image.crop((left, top, right, bottom))

    if os.path.exists(path):
        with Image.open(path) as img:
            return chop(img)
    else:
        raise PathNotFoundError


def magicify(image: Image.Image) -> Image.Image:
    """
    Adjusts the brightness and contrast of the image.

    Args:
        image (Image.Image): The image to be adjusted.

    Returns:
        Image.Image: The adjusted image with modified brightness and contrast.
    """

    # Reduce brightness by 10%
    brightness = ImageEnhance.Brightness(image)
    image_brightness = brightness.enhance(0.9)

    # Reduce contrast by 20%
    contrast = ImageEnhance.Contrast(image_brightness)
    image_contrast = contrast.enhance(0.8)

    return image_contrast


def scannable(id: str, darktheme: bool = False, is_album: bool = False) -> Image.Image:
    """
    Generates a Spotify scannable code (QR code) for a track or album.

    Args:
        id (str): The ID of the track or album on Spotify.
        darktheme (bool): Flag to indicate whether to use a dark theme (default is False).
        is_album (bool): Flag to indicate if the ID is for an album (default is False).

    Returns:
        Image.Image: A resized and transparent Spotify scannable code image.
    """

    # Set the color based on the theme
    color = CL_FONT_DARK_MODE if darktheme else CL_FONT_LIGHT_MODE

    # Build the URL for the Spotify scannable code
    item_type = "album" if is_album else "track"
    scan_url = f"https://scannables.scdn.co/uri/plain/png/101010/white/1280/spotify:{item_type}:{id}"

    # Download the scannable image data
    data = requests.get(scan_url).content
    img_bytes = BytesIO(data)

    # Process the image to make white pixels transparent
    with Image.open(img_bytes) as scan_code:

        # Convert the image to RGBA mode to support transparency
        scan_code = scan_code.convert("RGBA")
        width, height = scan_code.size
        pixels = scan_code.load()

        # Replace white pixels with transparency, others with the selected color
        for x in range(width):
            for y in range(height):
                if pixels is not None:
                    pixels[x, y] = CL_TRANSPARENT if pixels[x, y] != CL_WHITE else color

        # Resize the image to specific size
        resized = scan_code.resize(S_SPOTIFY_CODE, Image.Resampling.BICUBIC)

    return resized


def cover(image_url: str, path: Optional[str]) -> Image.Image:
    """
    Fetches and processes an image from a URL or a local path.

    Args:
        image_url (str): The URL to fetch the image from.
        path (Optional[str]): Local path to the custom image.

    Returns:
        Image.Image: The processed image.
    """

    # Load image from a path or fetch from URL
    img = crop(path) if path else Image.open(BytesIO(requests.get(image_url).content))

    # Apply magic filter  and resize
    return magicify(img.resize(S_COVER))


def get_theme(dark_theme: bool):
    """
    Determines theme-related properties.

    Args:
        dark_theme (bool): Whether to use a dark theme.

    Returns:
        Tuple containing theme color, template path
    """
    color, template = (
        (CL_FONT_DARK_MODE, "banner_dark.png")
        if dark_theme
        else (CL_FONT_LIGHT_MODE, "banner_light.png")
    )
    template_path = os.path.join(P_TEMPLATES, template)
    return color, template_path
