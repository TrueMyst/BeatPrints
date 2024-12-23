import os

from rich import box
from rich.table import Table
from questionary import Style
from typing import List, Union

from BeatPrints import spotify

default = Style(
    [
        ("qmark", "fg:ansicyan bold"),
        ("answer", "fg:ansiblue bold"),
        ("pointer", "fg:ansired bold"),
    ]
)

BEATPRINTS_ANSI = """

██████╗ ███████╗ █████╗ ████████╗██████╗ ██████╗ ██╗███╗   ██╗████████╗███████╗
██╔══██╗██╔════╝██╔══██╗╚══██╔══╝██╔══██╗██╔══██╗██║████╗  ██║╚══██╔══╝██╔════╝
██████╔╝█████╗  ███████║   ██║   ██████╔╝██████╔╝██║██╔██╗ ██║   ██║   ███████╗
██╔══██╗██╔══╝  ██╔══██║   ██║   ██╔═══╝ ██╔══██╗██║██║╚██╗██║   ██║   ╚════██║
██████╔╝███████╗██║  ██║   ██║   ██║     ██║  ██║██║██║ ╚████║   ██║   ███████║
╚═════╝ ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═╝     ╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝

🍀 Create eye-catching music posters that stand out, for FREE! by @TrueMyst
───────────────────────────────────────────────────────────────────────────────
"""


def clear() -> None:
    """
    Clears the terminal screen.
    """
    os.system("cls" if os.name == "nt" else "clear")
    print(BEATPRINTS_ANSI)


def tablize_track(tracks: List[spotify.TrackMetadata]):
    """
    Creates a pretty table for displaying track search results.
    """
    table = Table(box=box.ROUNDED)

    table.add_column("*", justify="center", style="cyan")
    table.add_column("Title", style="magenta")
    table.add_column("Artist", justify="right", style="blue")
    table.add_column("Album", justify="left", style="white")

    for pos, track in enumerate(tracks, start=1):
        name, artist, album = track.name, track.artist, track.album
        table.add_row(f"{pos}", name, artist, album)

    return table


def tablize_albums(albums: List[spotify.AlbumMetadata]) -> Table:
    """
    Creates a pretty table for displaying album search results.
    """
    table = Table(box=box.ROUNDED)

    table.add_column("*", justify="center", style="cyan")
    table.add_column("Title", style="magenta")
    table.add_column("Artist", justify="right", style="blue")
    table.add_column("Year", justify="left", style="white")

    for pos, track in enumerate(albums, start=1):
        name, artist, album = track.name, track.artist, track.released
        table.add_row(f"{pos}", name, artist, album)

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
