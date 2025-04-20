"""
Module: image.py

Provides essential image functions to generate posters.
"""

import io
import os
import random
from pathlib import Path
from typing import List, Literal, Tuple, Optional
import requests


from Pylette import extract_colors
from PIL import Image, ImageDraw, ImageEnhance
import qrcode
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


def qr_code(
    url: str,
    theme: ThemesSelector.Options = "Light",
) -> Image.Image:
    """
    Generates a QR Code as an alternative to Spotify scannable codes for YouTube Music links.

    Args:
        url (str): The YouTube Music track/album URL.
        theme (ThemesSelector.Options, optional): The theme for the QR Code. Defaults to "Light".
    """

    variant = t.THEMES[theme]
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color=c.WHITE, back_color=variant)

    # Convert to RGBA to support transparency
    img = img.convert("RGBA")

    # Resize the image
    return replace_color_in_image(img, variant, s.QRCODE)


def scannable(
    id: str,
    theme: ThemesSelector.Options = "Light",
    item: Literal["track", "album"] = "track",
) -> Image.Image:
    """
    Generates a Spotify scannable code for a track or album.

    Args:
        id (str): The Spotify track or album ID.
        theme (ThemesSelector.Options, optional): The theme for the scannable code. Defaults to "Light".
        item (Literal["track", "album"], optional): Specifies the type of the scannable code. Defaults to "track".

    Returns:
        Image.Image: The resized scannable code image.
    """

    variant = t.THEMES[theme]

    # URL to fetch the scannable code
    scan_url = f"https://scannables.scdn.co/uri/plain/png/101010/white/1280/spotify:{item}:{id}"

    # Fetch the scannable image data from Spotify
    data = requests.get(scan_url).content
    img_bytes = io.BytesIO(data)

    with Image.open(img_bytes) as scan_code:
        return replace_color_in_image(scan_code, variant, s.SCANCODE)


def replace_color_in_image(
    image: Image.Image, variant: Tuple, size: Tuple, color_to_replace: Tuple = c.WHITE
) -> Image.Image:
    """
    Converts a color in the given image to another color and resizes it.

    Args:
        image (Image.Image): The image to convert the color of
        variant (Tuple): The color to replace to
        size (Tuple): The size to resize the image to.
        color_to_replace (Tuple): The color to replace the selected color to

    Returns:
        Image.Image: The converted and resized image
    """
    # Convert to RGBA to support transparency
    image = image.convert("RGBA")

    pixels = image.load()
    width, height = image.size

    # Iterate over all pixels and replace white pixels with transparency code
    for x in range(width):
        for y in range(height):
            if pixels is not None:
                pixels[x, y] = (
                    c.TRANSPARENT if pixels[x, y] != color_to_replace else variant
                )

    # Resize the image
    return image.resize(size, Image.Resampling.BICUBIC)


def logo(logo_to_draw: dict, theme: ThemesSelector.Options = "Light") -> Image.Image:
    """
    Creates an image for the specified logo.

    Args:
        logo_to_draw (dict): The logo to draw
        theme (ThemesSelector.Options): The theme to draw the logo colors with.
            Defaults to "Light".

    Returns:
        Image.Image: The created logo image
    """

    path_ = Path(logo_to_draw.get("path")).expanduser().resolve()

    if not path_.exists():
        raise FileNotFoundError(f"The specified path '{path_}' does not exist.")

    variant = t.THEMES[theme]

    img = Image.open(path_)
    return replace_color_in_image(img, variant, s.LOGO)


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
