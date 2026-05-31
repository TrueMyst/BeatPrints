"""
Module: image.py

Provides essential image functions to generate posters.
"""

import io
import os
import random
import requests

from pathlib import Path
from typing import List, Tuple, Optional

from Pylette import extract_colors
from PIL import Image, ImageDraw, ImageEnhance
from BeatPrints.consts import Size, Position, Color, ThemesSelector, FilePath

# Initialize the components
s = Size()
c = Color()
p = Position()
f = FilePath()
t = ThemesSelector()


def get_palette(image: Image.Image) -> List[Tuple]:
    """
    Extracts the dominant color palette from an image.

    Args:
        image (Image.Image): The image from which to extract the color palette.

    Returns:
        List[Tuple[int, int, int]]: A list of RGB tuples representing the dominant colors.
    """
    with io.BytesIO() as byte_stream:
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
    Draws a color palette on the given image.

    Args:
        draw (ImageDraw.ImageDraw): The drawing context used to render on the image.
        image (Image.Image): The image to which the color palette will be drawn.
        accent (bool, optional): If True, an accent color is added at the bottom. Defaults to False.
    """
    palette = get_palette(image)

    # Render each color from the palette as a rectangle
    for index in range(6):
        x, y = p.PALETTE
        start, end = s.PL_WIDTH * index, s.PL_WIDTH * (index + 1)

        # Render the rectangle for the current color
        draw.rectangle(((x + start, y), (x + end, s.PL_HEIGHT)), fill=palette[index])

    # Add the accent at the bottom of the poster, if True
    if accent:
        draw.rectangle(p.ACCENT, fill=palette[random.randint(0, 2)])


def crop(path: Path) -> Image.Image:
    """
    Crops an image to a square aspect ratio.

    Args:
        path (Path): The file system path to the image file.

    Returns:
        Image.Image: The cropped square image.

    Raises:
        FileNotFoundError: If the provided file path does not exist.
    """

    def chop(image: Image.Image) -> Image.Image:
        width, height = image.size

        # Retrieve the minimum length of the image
        min_size = min(width, height)

        # Calculate the center of the image and crop it to a square
        left = (width - min_size) / 2
        top = (height - min_size) / 2
        right = (width + min_size) / 2
        bottom = (height + min_size) / 2

        return image.crop((left, top, right, bottom))

    with Image.open(path) as img:
        return chop(img)


def magicify(image: Image.Image) -> Image.Image:
    """
    Adjusts the brightness and contrast of an image.

    Args:
        image (Image.Image): The image to be adjusted.

    Returns:
        Image.Image: The image with modified brightness and contrast.
    """

    # Reduce brightness by 10%
    brightness = ImageEnhance.Brightness(image)
    magic = brightness.enhance(0.9)

    # Reduce contrast by 20%
    contrast = ImageEnhance.Contrast(magic)
    return contrast.enhance(0.8)


def scannable(
    theme: ThemesSelector.Options = "Light",
) -> Image.Image:
    """
    Prepares the deezer's logo based on the theme selected.

    Args:
        theme (ThemesSelector.Options, optional): The theme for the scannable code. Defaults to "Light".

    Returns:
        Image.Image: The resized scannable code image.
    """

    color = t.THEMES[theme]

    # Recolor the image
    image = Image.open(f.IMAGES + "/deezer.png")
    image = image.convert("RGBA")

    alpha = image.getchannel("A")

    colored = Image.new("RGBA", image.size, color + (255,))
    colored.putalpha(alpha)

    # Resize the image
    return colored.resize(s.SCANCODE, Image.Resampling.BICUBIC)


def cover(url: str, path: Optional[str]) -> Image.Image:
    """
    Fetches and processes an image from a URL or local path.

    Args:
        url (str): The URL of the image.
        path (Optional[str]): The local path of the image. If provided, the image will be loaded
                              from this path; otherwise, it will be fetched from the URL.

    Returns:
        Image.Image: The processed image.

    Raises:
        FileNotFoundError: If the provided local image path does not exist.
    """

    if path:
        path_ = Path(path).expanduser().resolve()

        if not path_.exists():
            raise FileNotFoundError(f"The specified path '{path_}' does not exist.")

        img = crop(path_)

    else:
        img = Image.open(io.BytesIO(requests.get(url).content))

    # Apply the magic filter and resize the image
    return magicify(img.resize(s.COVER))


def get_theme(theme: ThemesSelector.Options = "Light") -> Tuple[tuple, str]:
    """
    Returns theme-related properties based on the selected theme.

    Args:
        theme (ThemesSelector.Options, optional): The selected theme. Defaults to "Light".

    Returns:
        Tuple[tuple, str]: A tuple containing the theme color and the template path.
    """

    variant = t.THEMES[theme]
    template = os.path.join(f.TEMPLATES, f"{theme.lower()}.png")

    return variant, template
