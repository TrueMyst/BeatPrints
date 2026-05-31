import questionary
from rich import print

from cli import conf, exutils, validate
from BeatPrints import lyrics, deez, poster, errors

# Initialize components
dz = deez.Deezer()
ps = poster.Poster(conf.POSTERS_DIR)


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

        result = [
            dz.get_track(track["id"]) for track in dz.search(query, "track", limit)
        ]

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

        result = [
            dz.get_album(album["id"], shuffle)
            for album in dz.search(query, "album", limit)
        ]

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


def handle_lyrics(track: deez.TrackMetadata):
    """
    Get lyrics and let user select lines.

    Args:
        track (TrackMetadata): Track for lyrics.

    Returns:
        str: Selected lyrics portion.
    """

    try:
        ly = lyrics.Lyrics(track).get_lyrics()

        if ly.check_instrumental(track):
            print("🎸 • The track is detected to be an instrumental track")
            return ly.lyrics

        print(exutils.format_lyrics(track.title, track.artists[0], ly.lyrics))

        # Let user pick lyrics lines
        selection_range = questionary.text(
            "• Select 4 of your favorite lines (e.g., 2-5, 7-10):",
            validate=validate.SelectionValidator(ly.lyrics),
            style=exutils.lavish,
            qmark="🎀",
        ).unsafe_ask()

        return ly.select_lines(selection_range)

    except errors.NoLyricsAvailable:
        print("😦 • Couldn't find the lyrics with LRClib.")
        print("╰─ You can try getting them from other sources!")

        # Ask user to paste custom lyrics
        custom_lyrics = questionary.text(
            "• Paste your lyrics here:",
            validate=validate.LineValidator,
            multiline=True,
            style=exutils.lavish,
            qmark="🎀",
        ).unsafe_ask()

        return custom_lyrics


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
        choices=["Track Poster", "Album Poster"],
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
    else:
        album = select_album(conf.SEARCH_LIMIT)

        if album:
            ps.album(*album, accent, theme, image)


def main():
    exutils.clear()

    try:
        create_poster()
    except KeyboardInterrupt:
        exutils.clear()
        print("👋 Alright, no problem! See you next time.")
        exit(1)
