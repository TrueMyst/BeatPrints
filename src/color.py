from PIL import Image
from colorthief import ColorThief


def palette(path: str):
    # Resizes the banner to 1x1 pixel and gets the color
    dominant = Image.open(path).resize((1, 1), Image.NEAREST).getpixel((0, 0))

    color_thief = ColorThief(path)

    palette = color_thief.get_palette(color_count=6)
    palette.append(dominant)

    return palette
