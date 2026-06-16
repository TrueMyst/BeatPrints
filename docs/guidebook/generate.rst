🎨 Code Examples
===================

This is a quick guide on how to create track / album posters using **BeatPrints**.

🎷 Track Posters
^^^^^^^^^^^^^^^^^

.. code-block:: python

  from BeatPrints import deez, lyrics, poster

  # Initialize components
  dz = deez.Deezer()
  ps = poster.Poster("./")  # Save the poster in the current directory

  # Search for the track and fetch metadata
  search = dz.search(query="Apples - Rocco", stype="track", limit=1)

  # Grab the Track ID from the first result
  id = search[0]["id"]

  # Fetch full track metadata
  metadata = dz.get_track(id)

  # Get lyrics and check if the track is instrumental
  lrc = lyrics.Lyrics(metadata).get_lyrics()

  # Use a placeholder for instrumentals; otherwise pick specific lines
  lyrics = (
      "It's an instrumental track :>"
      if lrc.check_instrumental(metadata)
      else lrc.select_lines("11-14")
  )

  # Generate and save the poster
  ps.track(metadata=metadata, lyrics=lyrics, accent=False, theme="Light")

.. tip::

  You can create a **helper function** to display lyrics with line numbers in a nice format using `rich <https://github.com/Textualize/rich/>`_. 
  This is just a **basic way** to generate the poster. The sky's the limit!

💿️ Album Posters 
^^^^^^^^^^^^^^^^^

.. code-block:: python

  from BeatPrints import poster, deez

  # Initialize components
  dz = deez.Deezer()
  ps = poster.Poster("./")  # Save the poster in the current directory

  # Search for the album and fetch metadata
  search = dz.search(query="Charm - Clairo", stype="album", limit=1)

  # Grab the Album ID from the first result
  id = search[0]["id"]

  # Fetch full album metadata
  metadata = dz.get_album(id)

  # Generate and save the poster
  ps.album(metadata=metadata, indexing=False, accent=True, theme="Light")

This is a basic guide on generating your posters. You can always extend the functionality of the program to suit your needs. 

.. tip::

  Use a hyphen (-) between the track/album and the artist for more accurate results.

.. seealso::

  For more details, see the :ref:`reference` section on using BeatPrints.
