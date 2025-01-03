import os

from rich import box
from rich.table import Table

from questionary import Style
from typing import List, Literal, Union

from BeatPrints import spotify

lavish = Style(
    [
        ("qmark", "fg:ansicyan bold"),
        ("answer", "fg:ansiblue bold"),
        ("pointer", "fg:ansired bold"),
        ("highlighted", "fg:ansigreen bold"),
        ("selected", "fg:ansimagenta bold"),
    ]
)

BEATPRINTS_ASCII = """
██████╗ ███████╗ █████╗ ████████╗██████╗ ██████╗ ██╗███╗   ██╗████████╗███████╗
██╔══██╗██╔════╝██╔══██╗╚══██╔══╝██╔══██╗██╔══██╗██║████╗  ██║╚══██╔══╝██╔════╝
██████╔╝█████╗  ███████║   ██║   ██████╔╝██████╔╝██║██╔██╗ ██║   ██║   ███████╗
██╔══██╗██╔══╝  ██╔══██║   ██║   ██╔═══╝ ██╔══██╗██║██║╚██╗██║   ██║   ╚════██║
██████╔╝███████╗██║  ██║   ██║   ██║     ██║  ██║██║██║ ╚████║   ██║   ███████║
╚═════╝ ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═╝     ╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝

🥰 Create pinterest-style music posters that stand out, for FREE! by @TrueMyst
-------------------------------------------------------------------------------
"""


def clear() -> None:
    """
    Clears the terminal screen.
    """
    os.system("cls" if os.name == "nt" else "clear")
    print(BEATPRINTS_ASCII)


def tablize_items(
    items: List[spotify.TrackMetadata] | List[spotify.AlbumMetadata],
    item_type: Literal["track", "album"],
) -> Table:
    """
    Creates a pretty table for displaying either track or album search results.

    Args:
    """
    table = Table(box=box.ROUNDED)
    table.add_column("*", justify="center", style="magenta")
    table.add_column("Title", style="green")

    if item_type == "track":
        table.add_column("Artist", justify="right", style="blue")
        table.add_column("Album", justify="left", style="cyan")

        for pos, item in enumerate(items, start=1):
            table.add_row(f"{pos}", item.name, item.artist, item.album)

    elif item_type == "album":
        table.add_column("Artist", justify="right", style="blue")
        table.add_column("Year", justify="left", style="cyan")

        for pos, item in enumerate(items, start=1):
            table.add_row(f"{pos}", item.name, item.artist, item.released)

    return table


def format_lyrics(
    name: str, artist: str, lyrics: Union[str, None]
) -> Union[Table, None]:
    """
    Formats the lyrics of a song and returns them in a rich table format.

    Args:
        name (str): The name of the song.
        artist (str): The artist of the song.
        lyrics (str or None): The lyrics of the song.

    Returns:
        Table: A rich table containing the formatted lyrics.
        None: If the lyrics are None.
    """
    if lyrics is not None:
        # Split the lyrics into lines
        lines = lyrics.splitlines()

        # Format the lines
        formatted_lines = [
            f"[bold magenta]{ln:2}[/bold magenta] {line}"
            for ln, line in enumerate(lines, start=1)
        ]

        # Join formatted lines into a single string
        improved_lyrics = "\n".join(formatted_lines)

        # Create and format the table
        table = Table(box=box.ROUNDED)
        table.add_column(f"📜 Lyrics: {name} - {artist}", style="cyan", no_wrap=True)
        table.add_row(improved_lyrics)

        return table

    return None
