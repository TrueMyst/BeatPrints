import questionary

from rich import print

from cli import conf, exutils, validate
from BeatPrints import lyrics, spotify, poster, errors, wallpaper  
import os 

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
            validate=validate.LineValidator,
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


def create_poster(return_image=False):
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

    generated_image = None

    # Generate posters
    if poster_type == "Track Poster":
        track = select_track(conf.SEARCH_LIMIT)

        if track:
            lyrics = handle_lyrics(track)

            exutils.clear()
            generated_image = ps.track(track, lyrics, accent, theme, image, return_image=return_image)
    else:
        album = select_album(conf.SEARCH_LIMIT)

        if album:
            generated_image = ps.album(*album, accent, theme, image, return_image=return_image)

    return generated_image


def main():
    exutils.clear()

    try:
        creation_type = questionary.select(
            "• What would you like to create?",
            choices=["Poster", "Wallpaper"],
            style=exutils.lavish,
            qmark="✨",
        ).unsafe_ask()

        if creation_type == "Poster":
            create_poster()
        elif creation_type == "Wallpaper":
            num_posters = questionary.text(
                "• How many posters (1-10) would you like in your wallpaper?",
                validate=validate.NumericValidator(limit=10),
                style=exutils.lavish,
                qmark="🖼️",
            ).unsafe_ask()
            num_posters = int(num_posters)

            if 1 <= num_posters <= 10:
                poster_images = []
                temp_poster_paths = []
                for i in range(num_posters):
                    print(f"\nCreating poster {i+1} for the wallpaper:")
                    poster_image = create_poster(return_image=True)
                    if poster_image:
                        poster_images.append(poster_image)
                        # Optionally save to temporary files if memory becomes an issue
                        temp_path = f"temp_poster_{i+1}.png"
                        poster_image.save(temp_path)
                        temp_poster_paths.append(temp_path)
                    else:
                        print("Error creating a poster. Wallpaper creation aborted.")
                        # Clean up any created temporary files
                        for path in temp_poster_paths:
                            try:
                                os.remove(path)
                            except FileNotFoundError:
                                pass
                        return

                wallpaper_width = questionary.text(
                    "• Enter the desired wallpaper width:",
                    validate=validate.NumericValidator(limit=9999),
                    style=exutils.lavish,
                    qmark="📏",
                ).unsafe_ask()
                wallpaper_height = questionary.text(
                    "• Enter the desired wallpaper height:",
                    validate=validate.NumericValidator(limit=9999),
                    style=exutils.lavish,
                    qmark="📐",
                ).unsafe_ask()
                wallpaper_resolution = (int(wallpaper_width), int(wallpaper_height))
                wallpaper_bg_color = questionary.text(
                    "• Enter the background color for the wallpaper (e.g., slategrey, #RRGGBB):",
                    style=exutils.lavish,
                    qmark="🎨",
                ).unsafe_ask()

                try:
                    wallpaper_image = wallpaper.generate_wallpaper(
                        wallpaper_resolution,
                        temp_poster_paths,  # Pass the list of temporary file paths
                        wallpaper_bg_color
                    )
                    # Need to come up with a scheme for naming generated files
                    wallpaper_save_path = os.path.join(conf.POSTERS_DIR, "generated_wallpaper.png")
                    wallpaper_image.save(wallpaper_save_path)
                    print(f"\nWallpaper created successfully and saved as {wallpaper_save_path}")

                    # Clean up temporary poster files
                    for path in temp_poster_paths:
                        try:
                            os.remove(path)
                        except FileNotFoundError:
                            pass

                except ValueError as e:
                    print(f"Error during wallpaper generation: {e}")
                except Exception as e:
                    print(f"An unexpected error occurred: {e}")
            else:
                print("Invalid number of posters.")
        else:
            print("Invalid choice.")

    except KeyboardInterrupt:
        exutils.clear()
        print("👋 Alright, no problem! See you next time.")
        exit(1)
