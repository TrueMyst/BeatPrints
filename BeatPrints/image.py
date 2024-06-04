"""
Module: image.py

Imports:
    - dim: Cords & Sizes
    - requests: HTTP requests
    - PIL: Image Processing
    - colorthief: Extract color palette
"""

import dim
import requests

from PIL import Image
from PIL import ImageDraw
from colorthief import ColorThief


def color_palette(path: str) -> list:
    """
    Extract the color palette from an image.

    Args:
        path (str): The path of the image file.

    Returns:
        list: A list containing the colors extracted from the image.
    """

    # Resizes the image to 1x1 pixel to get the dominant color of the image.
    dominant_color = Image.open(path).resize(
        (1, 1), Image.Resampling.BICUBIC).getpixel((0, 0))

    ct = ColorThief(path)
    palette = ct.get_palette(color_count=6)

    # Append the dominant color to the palette
    palette.append(dominant_color)

    # Returns the color palette
    return palette


def draw_palette(draw: ImageDraw.ImageDraw, image_path: str, accent: bool):
    """
    Uses Pillow to draw the color palette on a image.

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

        # Starting Position of the colors.
        start, end = 170 * i, 170 * (i + 1)

        # Draw the palette co-ordinate wise.
        draw.rectangle(((x + start, y), (x + end, 1160)), fill=palette[i])

    # Optionally draw a rectangle to highlight the accent color
    if accent:
        draw.rectangle(dim.C_ACCENT, fill=palette[-1])


def square_crop(image_path: str, save_path: str):
    """
    Crops the image to a square aspect ratio and saves it.

    Args:
        image_path (str): The path of the original image file.
        save_path (str): The path where the cropped image will be saved.
    """

    # Open the image
    image = Image.open(image_path)

    # Crop the image to a square aspect ratio
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
    Downloads the Spotify scan code for a particular song and removes white pixels from it.

    Args:
        id (str): The ID of the track.
        dark_mode (bool): Whether to use dark mode colors. Default is False.
    """

    # Define colors
    transparent = (0, 0, 0, 0)
    white = (255, 255, 255, 255)

    # Determine the color
    color = dim.CL_DARK_MODE if dark_mode else dim.CL_LIGHT_MODE

    # Download the Spotify scan code image
    main = f"https://scannables.scdn.co/uri/plain/png/101010/white/1280/spotify:track:{id}"
    data = requests.get(main)

    with open("./assets/spotify/spotify_code.png", "wb") as file:
        file.write(data.content)

    with Image.open("./assets/spotify/spotify_code.png") as scan_code:
        # Convert the image into RGBA mode
        scan_code = scan_code.convert("RGBA")

        pixels = scan_code.load()
        width, height = scan_code.size

        # Iterate through pixels and make white pixels transparent
        for x in range(width):
            for y in range(height):
                pixels[x, y] = transparent if pixels[x, y] != white else color

        # Save the modified image
        scan_code.save("./assets/spotify/spotify_code.png")
