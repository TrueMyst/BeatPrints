"""
Modules:
    PIL: Open and resize image
    colorthief: extract color palette from image
"""
from PIL import Image
from colorthief import ColorThief


def get_color_palette(path: str):
    """
    Function to resize image and get color palette.
    
    Args:
        path (str): The path of the image file.

    Returns:
        list: A list containing the color palette extracted from the image.
    """

    # Resizes the banner to 1x1 pixel and gets the color
    dominant_color = Image.open(path).resize((1, 1), Image.NEAREST).getpixel((0, 0))

    color_thief = ColorThief(path)

    #Extract color palette with 6 additional colors from the image
    color_palette = color_thief.get_palette(color_count=6)

    #Appends the dominant color to the palette
    color_palette.append(dominant_color)

    #Returns the color palette
    return color_palette
