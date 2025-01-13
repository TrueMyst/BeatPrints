import questionary
import re

from rich import print

from cli import conf, exutils, validate
from BeatPrints import lyrics, spotify, poster, errors

# Initialize components
ly = lyrics.Lyrics()
ps = poster.Poster(conf.POSTERS_DIR)
sp = spotify.Spotify(conf.CLIENT_ID, conf.CLIENT_SECRET)


def select_track(limit: int):
    """
    Prompt user to search and select a track.

    Args:
        limit (int): Max search results.

    Returns:
        TrackMetadata: The selected track.
    """
    repeat = True

    while repeat:
        query = questionary.text(
            "• Type the track you love most:",
            validate=validate.LengthValidator,
            style=exutils.lavish,
            qmark="🎺",
        ).unsafe_ask()

        result = sp.get_track(query, limit=limit)

        # Clear the screen
        exutils.clear()

        # Show results
        print(f'{len(result)} results found for "{query}"!')
        print(exutils.tablize_items(result, "track"))

        # Repeat search if needed
        repeat = questionary.confirm(
            "• Not what you wanted? Search again?",
            default=True,
            style=exutils.lavish,
            qmark="🤷",
        ).unsafe_ask()

        # Select track
        if not repeat:
            choice = questionary.text(
                f"• Select the track you like:",
                validate=validate.NumericValidator(limit=len(result)),
                style=exutils.lavish,
                qmark="🍀",
            ).unsafe_ask()

            exutils.clear()
            return result[int(choice) - 1]


def select_album(limit: int):
    """
    Prompt user to search and select an album.

    Args:
        limit (int): Max search results.

    Returns:
        AlbumMetadata: The selected album.
    """
    repeat = True

    # Options for track numbering and shuffling
    index = questionary.confirm(
        "• Number the tracks?", style=exutils.lavish, qmark="🍙"
    ).unsafe_ask()

    shuffle = questionary.confirm(
        "• Shuffle the tracks?", style=exutils.lavish, qmark="🚀"
    ).unsafe_ask()

    while repeat:
        query = questionary.text(
            "• Type the album you love most:",
            validate=validate.LengthValidator,
            style=exutils.lavish,
            qmark="💿️",
        ).unsafe_ask()

        result = sp.get_album(query, limit, shuffle)

        # Clear the screen
        exutils.clear()

        # Show results
        print(f'{len(result)} results found for "{query}"!')
        print(exutils.tablize_items(result, "album"))

        # Repeat search if needed
        repeat = questionary.confirm(
            "• Not what you wanted? Search again?",
            default=True,
            style=exutils.lavish,
            qmark="🤷",
        ).unsafe_ask()

        # Select album
        if not repeat:
            choice = questionary.text(
                f"• Select the album you like:",
                validate=validate.NumericValidator(limit=len(result)),
                style=exutils.lavish,
                qmark="🍀",
            ).unsafe_ask()

            exutils.clear()
            return result[int(choice) - 1], index


def parse_spotify_url(url: str) -> tuple:
    """
    Parses a Spotify URL to extract the type and ID.

    Args:
        url (str): The Spotify URL to be parsed.

    Returns:
        tuple: A tuple containing two elements:
            - The type of the Spotify URL (e.g., "track", "album").
            - The ID of the Spotify URL.
    """

    # Extract the type and ID from the Spotify URL
    match = re.match(r"https://open.spotify.com/(track|album)/(\w+)", url)

    if match:
        return match.groups()

    return None, None


def select_from_spotify_url():
    """
    Prompt user to input url.

    Returns:
        TrackMetadata or AlbumMetadata.
    """
    url = questionary.text(
        "• Type the spotify url:",
        validate=validate.SpotifyURLValidator,
        style=exutils.lavish,
        qmark="🎺",
    ).unsafe_ask()

    type, id = parse_spotify_url(url)
    result = sp.get_from_id(type, id)
    return result


def handle_lyrics(track: spotify.TrackMetadata):
    """
    Get lyrics and let user select lines.

    Args:
        track (TrackMetadata): Track for lyrics.

    Returns:
        str: Selected lyrics portion.
    """
    try:
        # Fetch lyrics and print it in a pretty table
        lyrics = ly.get_lyrics(track)

        if ly.check_instrumental(track):
            print("🎸 • The track is detected to be an instrumental track")
            return lyrics

        print(exutils.format_lyrics(track.name, track.artist, lyrics))

        # Let user pick lyrics lines
        selection_range = questionary.text(
            "• Select 4 of your favorite lines (e.g., 2-5, 7-10):",
            validate=validate.SelectionValidator(lyrics),
            style=exutils.lavish,
            qmark="🎀",
        ).unsafe_ask()

        return ly.select_lines(lyrics, selection_range)

    except errors.NoLyricsAvailable:
        print("😦 • Couldn't find the lyrics with LRClib.")
        print("╰─ You can try getting them from other sources!")

        # Ask user to paste custom lyrics
        lyrics = questionary.text(
            "• Paste your lyrics here:",
            validate=validate.LineCountValidator,
            multiline=True,
            style=exutils.lavish,
            qmark="🎀",
        ).unsafe_ask()

        return lyrics


def poster_features():
    """
    Ask for poster customization options.

    Returns:
        tuple: theme, accent color, and image path.
    """
    features = questionary.form(
        theme=questionary.select(
            "• Which theme do you prefer?",
            choices=[
                "Light",
                "Dark",
                "Catppuccin",
                "Gruvbox",
                "Nord",
                "RosePine",
                "Everforest",
            ],
            default="Light",
            style=exutils.lavish,
            qmark="💫",
        ),
        accent=questionary.confirm(
            "• Add a colored accent to the bottom?",
            default=False,
            style=exutils.lavish,
            qmark="🌈",
        ),
        image=questionary.confirm(
            "• Use a custom image as the poster's cover art?",
            default=False,
            style=exutils.lavish,
            qmark="🥐",
        ),
    ).unsafe_ask()

    theme, accent, image = features.values()

    # Get the image path if custom image is selected
    image_path = (
        questionary.path(
            "• Provide the file path to the image:",
            validate=validate.ImagePathValidator,
            style=exutils.lavish,
            qmark="╰─",
        )
        .skip_if(not image, default=None)
        .unsafe_ask()
    )

    return theme, accent, image_path


def create_poster():
    """
    Create a poster based on user input.
    """
    poster_type = questionary.select(
        "• What do you want to create?",
        choices=["Track Poster", "Album Poster", "From Spotify URL"],
        style=exutils.lavish,
        qmark="🎨",
    ).unsafe_ask()

    theme, accent, image = poster_features()

    # Clear the screen
    exutils.clear()

    # Generate posters
    if poster_type == "Track Poster":
        track = select_track(conf.SEARCH_LIMIT)

        if track:
            lyrics = handle_lyrics(track)

            exutils.clear()
            ps.track(track, lyrics, accent, theme, image)
    elif poster_type == "Album Poster":
        album = select_album(conf.SEARCH_LIMIT)

        if album:
            ps.album(*album, accent, theme, image)
    else:
        result = select_from_spotify_url()

        if isinstance(result, spotify.TrackMetadata):
            lyrics = handle_lyrics(result)
            exutils.clear()
            ps.track(result, lyrics, accent, theme, image)
        elif isinstance(result, spotify.AlbumMetadata):
            ps.album(result, False, accent, theme, image)

def main():
    exutils.clear()

    try:
        create_poster()
    except KeyboardInterrupt:
        exutils.clear()
        print("👋 Alright, no problem! See you next time.")
        exit(1)
