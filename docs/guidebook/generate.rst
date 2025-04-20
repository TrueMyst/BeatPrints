🎨 Code Examples
===================

This is a quick guide on how to generate posters using **BeatPrints** through code.

.. note::

   It is important for you to have the ``.env`` file in the same directory.

🎷 Track Posters
^^^^^^^^^^^^^^^^^

To generate a track poster, follow the steps below.


.. code-block:: python

  import os, dotenv
  from BeatPrints import lyrics, poster
  from BeatPrints.api import api_client

  dotenv.load_dotenv()

  # Spotify credentials
  CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
  CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

  # Initialize components
  ly = lyrics.Lyrics()
  ps = poster.Poster("./")
  cl = api_client.ApiClient()

  # If you want to use the Spotify API
  cl.setSpotifyClient(CLIENT_ID, CLIENT_SECRET)

  # If you want to use the YT Music API (default)
  cl.setYtMusicClient()

  # Search for the track and fetch metadata
  search = cl.get_track("Saturn - SZA", limit=1)

  # Pick the first result
  metadata = search[0]

  # Get lyrics and determine if the track is instrumental
  lyrics = ly.get_lyrics(metadata)

  # Use the placeholder for instrumental tracks; otherwise, select specific lines
  highlighted_lyrics = (
      lyrics if ly.check_instrumental(metadata) else ly.select_lines(lyrics, "5-9")
  )

  # Generate the track poster
  ps.track(metadata, highlighted_lyrics)

.. tip::

  You can create a **helper function** to display lyrics with line numbers in a nice format using `rich <https://github.com/Textualize/rich/>`_. 
  This is just a **basic way** to generate the poster. The sky's the limit!

💿️ Album Posters 
^^^^^^^^^^^^^^^^^

Like tracks, you can also create an album poster, follow these steps below.

.. code-block:: python

  import os, dotenv
  from BeatPrints import poster
  from BeatPrints.api import api_client

  dotenv.load_dotenv()

  # Spotify credentials
  CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
  CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

  # Initialize components
  ps = poster.Poster("./")
  cl = api_client.ApiClient()

  # If you want to use the Spotify API
  cl.setSpotifyClient(CLIENT_ID, CLIENT_SECRET)

  # If you want to use the YT Music API (default)
  cl.setYtMusicClient()

  # Search for an album
  search = cl.get_album("Charm - Clairo", limit=1)

  # Get the album's metadata
  metadata = search[0]

  # Generate the album poster
  ps.album(metadata)

This is a basic guide on generating your posters. You can extend it by creating your own functions to make them more useful.

.. tip::

  Use a hyphen (-) between the track/album and the artist for more accurate results.

.. seealso::

  For more details, see the :ref:`reference` section on using BeatPrints.
