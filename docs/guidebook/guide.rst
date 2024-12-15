Generate Posters
================

This is a quick guide on how you can generate posters using *BeatPrints*.

🎷 Track Posters
^^^^^^^^^^^^^^^^^

To generate a track poster, follow the steps below.

.. code-block:: python

   import os, dotenv
   from BeatPrints import lyrics, poster, spotify

   dotenv.load_dotenv()

   # Spotify credentials
   CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
   CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

   # Initialize components
   ly = lyrics.Lyrics()
   ps = poster.Poster("./")
   sp = spotify.Spotify(CLIENT_ID, CLIENT_SECRET)

   # Search for a track
   search = sp.get_track("Saturn by SZA", limit=1)

   # Get the track's metadata and lyrics
   metadata = search[0]
   lyrics = ly.get_lyrics(metadata)
   highlighted_lyrics = ly.select_lines(lyrics, "5-9")

   # Generate the track poster
   ps.track(metadata, highlighted_lyrics)

💿️ Album Posters 
^^^^^^^^^^^^^^^^^

Like tracks, you can also create an album poster, follow these steps below.

.. code-block:: python

   import os, dotenv
   from BeatPrints import poster, spotify

   dotenv.load_dotenv()

   # Spotify credentials
   CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
   CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

   # Initialize components
   ps = poster.Poster("./")
   sp = spotify.Spotify(CLIENT_ID, CLIENT_SECRET)

   # Search for an album
   search = sp.get_album("Charm by Clairo", limit=1)

   # Get the album's metadata
   metadata = search[0]

   # Generate the album poster
   ps.album(metadata)

.. seealso::

  For more details, see the :ref:`reference` section on using BeatPrints.
