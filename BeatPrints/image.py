"""
Module: image.py

Provides essential image functions to generate posters.
"""

import random
import requests

from io import BytesIO
from pathlib import Path
from typing import List, Tuple, Optional

from Pylette import extract_colors
from PIL import Image, ImageDraw, ImageEnhance

from .consts import *


def get_palette(image: Image.Image) -> List[Tuple]:
    """
    Extracts the dominant color palette from an image.

    Args:
        image (Image.Image): The image to extract the palette from.

    Returns:
        List[Tuple]: A list of RGB tuples representing the dominant colors.
    """
    with BytesIO() as byte_stream:
        # Save image to in-memory byte stream
        image.save(byte_stream, format="PNG")

        # Get byte data of the image
        img_bytes = byte_stream.getvalue()

    # Extract the dominant colors from the image
    colors = extract_colors(image=img_bytes, palette_size=6, sort_mode="luminance")
    return [tuple(color.rgb) for color in colors]


def draw_palette(
    draw: ImageDraw.ImageDraw, image: Image.Image, accent: bool = False
) -> None:
    """
    Draws a color palette on the image.

    Args:
        draw (ImageDraw.ImageDraw): The drawing context.
        image (Image.Image): The image to draw on.
        accent (bool): If True, adds an accent color at the bottom. Defaults to False.
    """
    palette = get_palette(image)

    # Draw each color in the palette as a box
    for i in range(6):
        x, y = C_PALETTE
        start, end = PL_BOX_WIDTH * i, PL_BOX_WIDTH * (i + 1)

        # Draw the box for the current color
        draw.rectangle(((x + start, y), (x + end, PL_BOX_HEIGHT)), fill=palette[i])

    # If accent is True, draw the accent color at the bottom
    if accent:
        draw.rectangle(C_ACCENT, fill=palette[random.randint(0, 2)])


def crop(path: Path) -> Image.Image:
    """
    Crops an image to a square aspect ratio.

    Args:
        path (Path): The path to the image file.

    Returns:
        Image.Image: The cropped square image.

    Raises:
        FileNotFoundError: If the file path does not exist.
    """

    def chop(image: Image.Image) -> Image.Image:
        width, height = image.size

        # Get the smaller dimension for square cropping
        min_dim = min(width, height)

        # Define cropping box to center and crop the image to a square
        left = (width - min_dim) / 2
        top = (height - min_dim) / 2
        right = (width + min_dim) / 2
        bottom = (height + min_dim) / 2

        return image.crop((left, top, right, bottom))

    with Image.open(path) as img:
        return chop(img)


def magicify(image: Image.Image) -> Image.Image:
    """
    Adjusts the brightness and contrast of an image.

    Args:
        image (Image.Image): The image to adjust.

    Returns:
        Image.Image: The adjusted image.
    """

    # Reduce brightness by 10%
    brightness = ImageEnhance.Brightness(image)
    magic = brightness.enhance(0.9)

    # Reduce contrast by 20%
    contrast = ImageEnhance.Contrast(magic)
    return contrast.enhance(0.8)


def scannable(
    id: str, theme: THEME_OPTS = "Light", is_album: bool = False
) -> Image.Image:
    """
    Generates a Spotify scannable code for a track or album.

    Args:
        id (str): The Spotify track or album ID.
        theme (str): The theme for the scannable code. Defaults to "Light".
        is_album (bool): If True, generates for an album. Defaults to False.

    Returns:
        Image.Image: The resized scannable code image.
    """

    color = THEMES[theme]
    item_type = "album" if is_album else "track"

    # Construct the URL to fetch the scannable code from Spotify
    scan_url = f"https://scannables.scdn.co/uri/plain/png/101010/white/1280/spotify:{item_type}:{id}"

    # Fetch the scannable image data from Spotify
    data = requests.get(scan_url).content
    img_bytes = BytesIO(data)

    with Image.open(img_bytes) as scan_code:
        # Convert to RGBA to support transparency
        scan_code = scan_code.convert("RGBA")

        pixels = scan_code.load()
        width, height = scan_code.size

        # Iterate through all pixels to replace white pixels with transparency
        for x in range(width):
            for y in range(height):
                if pixels is not None:
                    pixels[x, y] = CL_TRANSPARENT if pixels[x, y] != CL_WHITE else color

        # Resize the image to a specific size
        return scan_code.resize(S_SPOTIFY_CODE, Image.Resampling.BICUBIC)


def cover(image_url: str, image_path: Optional[str]) -> Image.Image:
    """
    Fetches and processes an image from a URL or local path.

    Args:
        image_url (str): The image URL.
        image_path (Optional[str]): The local image path.

    Returns:
        Image.Image: The processed image.

    Raises:
        FileNotFoundError: If the local image path does not exist.
    """

    if image_path:
        path = Path(image_path).expanduser().resolve()

        if not path.exists():
            raise FileNotFoundError(f"The specified path '{path}' does not exist.")

        img = crop(path)

    else:
        img = Image.open(BytesIO(requests.get(image_url).content))

    # Apply the magic filter and resize the image for the cover
    return magicify(img.resize(S_COVER))


def get_theme(theme: THEME_OPTS = "Light") -> Tuple[tuple, str]:
    """
    Returns theme-related properties based on the selected theme.

    Args:
        theme (str): The selected theme. Default is "Light".

    Returns:
        Tuple[tuple, str]: A tuple containing the theme color and the template path.
    """

    color = THEMES[theme]
    template_path = os.path.join(P_TEMPLATES, f"{theme.lower()}.png")

    return color, template_path
