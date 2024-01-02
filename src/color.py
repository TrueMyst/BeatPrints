from colorthief import ColorThief


def palette(path: str):
    color_thief = ColorThief(path)
    palette = color_thief.get_palette(color_count=6)
    return palette
