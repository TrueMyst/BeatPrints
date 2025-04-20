☕️ BeatPrints
=============

.. raw:: html

  <h3 align="center">
      <img src="https://i.ibb.co/CWY693F/beatprints-logo.png" width="175"/>
  </h3>
  <h3 align="center">
      BeatPrints: Quick, stylish posters for your favorite tracks! 🎷☕️
  </h3>

  <p align="center">Create eye-catching, Pinterest-style music posters effortlessly. BeatPrints integrates with <b>Spotify</b> and <b>LRClib API</b> to help you design custom posters for your favorite tracks or albums. 🍀</p>

  <p align="center">
    <a href="https://gitHub.com/TrueMyst/BeatPrints/graphs/commit-activity">
      <img src="https://img.shields.io/badge/Maintained%3F-Yes-%23c4b9a6?style=for-the-badge&logo=Undertale&logoColor=%23b5a790&labelColor=%23312123" alt="Maintenance"></a>
    <a href="https://github.com/TrueMyst/BeatPrints/stargazers">
      <img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/TrueMyst/BeatPrints?style=for-the-badge&logo=Apache%20Spark&logoColor=%23b5a790&labelColor=%23312123&color=%23c4b9a6"></a>
    <a href="https://github.com/psf/black">
      <img src="https://img.shields.io/badge/Code_Style-black-%23c4b9a6?style=for-the-badge&logo=CodeFactor&logoColor=%23b5a790&labelColor=%23312123" alt="Code Formatter"></a>
    <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/">
      <img alt="Static Badge" src="https://img.shields.io/badge/License-CC_BY--NC--SA_4.0-%23c4b9a6?style=for-the-badge&logo=Pinboard&logoColor=%23b5a790&labelColor=%23312123"></a>
  </p>

.. image:: https://i.ibb.co.com/y0jKqHK/banner.png
   :alt: examples

📦 Installation
---------------

You can install BeatPrints via:

.. code:: python

   # For pip users
   pip install BeatPrints

   # For poetry users
   poetry add BeatPrints

Or if you prefer using just the CLI:

.. code:: python

   pipx install BeatPrints

This will install the CLI, making it ready for you to use.
For more more infomation, check out `pipx <https://github.com/pypa/pipx>`_


🚀 Quick Start
--------------

🌱 Environment Variables
^^^^^^^^^^^^^^^^^^^^^^^^

🎷 Spotify
**********

If you want to use the Spotify API, you’ll need a ``.env`` file with these
keys:

.. code:: python

  SPOTIFY_CLIENT_ID = "<your-client-id>"
  SPOTIFY_CLIENT_SECRET = "<your-client-secret>"

You can get these from the `Spotify Developer Dashboard <https://developer.spotify.com/dashboard/>`_ by creating a new app with **Web API** as the scope.


🎀 Creating your FIRST Poster
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Here’s how you can create your first poster:

.. code:: python

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

🥞 CLI
------

Here’s a short video showing how to generate posters using the CLI. For more information refer to the documentation `here <https://beatprints.readthedocs.io/en/latest/guidebook/cli.html>`_

.. video:: https://github.com/user-attachments/assets/3efb7028-c533-4bf4-880b-da3a71f8a3db
   :width: 700

🖼️ Examples
-----------

======================== ==========================
**Track: Saturn by SZA** **Album: Charm by Clairo**
======================== ==========================
|Track Example|          |Album Example|
======================== ==========================

.. |Track Example| image:: https://i.ibb.co.com/q5v8J9R/saturn-by-sza-1e3.png
.. |Album Example| image:: https://i.ibb.co.com/TcrKKXV/charm-by-clairo-f8a.png


🎨 Themes
---------

BeatPrints currently offers you **5 additional themes**  to use!

-  Catppuccin
-  Gruvbox
-  Nord
-  Rosepine
-  Everforest

For more examples, check out the `examples directory <https://github.com/TrueMyst/BeatPrints/tree/main/examples>`_.

✨ Features
-----------

-  **Polaroid Filter for Covers**: Give your track or album covers a
   vintage Polaroid look.
-  **Multi-language Support**: Supports English, Hindi, Russian,
   Japanese, Chinese, and Korean.
-  **Custom Cover Images**: Personalize posters with your own images.
-  **Theme Customization**: Switch between different other themes.
-  **Track & Album Selection**: Highlight your favorite track or entire
   album.
-  **Lyrics Highlighting**: Feature impactful lyrics directly on your
   poster.


💡 Why BeatPrints?
------------------

I created this project after finding out that people sell these posters on `Etsy <https://www.etsy.com/market/spotify_poster>`_ at high prices, offering only digital downloads instead of shipping actual posters.

I wanted to make it free for everyone to print themselves, as I believe my posters are simpler, cleaner, and prettier.


📜 License
----------

BeatPrints is distributed under the **Creative Commons
Attribution-NonCommercial-ShareAlike 4.0 International License**:

-  **Use**: Free to share and adapt.
-  **Attribution**: Provide credit and a link to the license.
-  **NonCommercial**: Not for commercial use.
-  **ShareAlike**: Adaptations must follow the same license.

📋️ Table
---------
.. toctree::
   :maxdepth: 1
  
   guidebook/index
   reference/index
   misc/index
