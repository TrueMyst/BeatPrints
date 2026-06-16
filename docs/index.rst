☕️ BeatPrints
==============

.. raw:: html

  <h3 align="center">
      <img src="https://i.ibb.co/CWY693F/beatprints-logo.png" width="175"/>
  </h3>

  <h3 align="center">
      BeatPrints: Quick, stylish posters for your favorite tracks and albums! 🎷☕️
  </h3>

  <p align="center">Create eye-catching, <b>pinterest-style</b> music posters effortlessly.<br>
      BeatPrints integrates with <b>Deezer</b> and <b>LRClib API</b> to help you design custom posters for your favorite tracks or albums. 🍀
  </p>

  <p align="center">
    <a href="https://gitHub.com/TrueMyst/BeatPrints/graphs/commit-activity">
      <img alt="Maintenance" src="https://img.shields.io/badge/Maintained%3F-Yes-%23c4b9a6?style=for-the-badge&logo=Undertale&logoColor=%23b5a790&labelColor=%23312123"></a>

    <a href="https://github.com/TrueMyst/BeatPrints/stargazers">
      <img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/TrueMyst/BeatPrints?style=for-the-badge&logo=Apache%20Spark&logoColor=%23b5a790&labelColor=%23312123&color=%23c4b9a6"></a>

    <a href="https://pepy.tech/projects/BeatPrints">
      <img alt="Downloads" src="https://img.shields.io/pepy/dt/BeatPrints?style=for-the-badge&logo=pypi&logoColor=%23C4B9A6&labelColor=%23312123&color=%23C4B9A6"></a>

    <a href="https://github.com/psf/black">
      <img alt="Code Formatter" src="https://img.shields.io/badge/Code_Style-black-%23c4b9a6?style=for-the-badge&logo=CodeFactor&logoColor=%23b5a790&labelColor=%23312123"></a>

    <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/">
      <img alt="Static Badge" src="https://img.shields.io/badge/License-CC_BY--NC--SA_4.0-%23c4b9a6?style=for-the-badge&logo=Pinboard&logoColor=%23b5a790&labelColor=%23312123"></a>
  </p>

.. image:: https://i.imgur.com/PDcc2Qp.jpeg
   :alt: examples

.. centered:: 📔 Check out the `documentation <https://beatprints.readthedocs.io/en/latest/>`_!


📦 Installation
---------------

You can install BeatPrints via:

.. code-block:: bash

   # For pip users
   pip install BeatPrints

   # For poetry users
   poetry add BeatPrints

Or if you prefer using just the CLI:

.. code-block:: bash

   pipx install BeatPrints

This will install the CLI, making it ready for you to use.
For more information, check out `pipx <https://github.com/pypa/pipx>`_.


🚀 Quick Start
--------------

Here's how you can create your first **track / album** poster.

🎵 Track
~~~~~~~~~

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

💿 Album
~~~~~~~~~

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

Here's what the posters look like:

.. list-table::
   :widths: 50 50
   :header-rows: 1

   * - **Track: Apples by Rocco**
     - **Album: Charm by Clairo**
   * - .. image:: https://i.imgur.com/09ExFbx.jpeg
          :alt: Track Example
     - .. image:: https://i.imgur.com/MUkQAb6.jpeg
          :alt: Album Example


🥞 CLI
------

Here's a short video showing how to generate posters using the CLI.
For more information refer to the `documentation <https://beatprints.readthedocs.io/en/latest/guidebook/cli.html>`_.

.. video:: https://github.com/user-attachments/assets/3efb7028-c533-4bf4-880b-da3a71f8a3db
   :width: 700


🎨 Themes
---------

BeatPrints currently offers you **6 additional themes** to use!

.. raw:: html

   <p>
     <img alt="Dark" src="https://img.shields.io/badge/Dark-%23312123?style=for-the-badge">
     <img alt="Catppuccin" src="https://img.shields.io/badge/Catppuccin-%23312123?style=for-the-badge">
     <img alt="Gruvbox" src="https://img.shields.io/badge/Gruvbox-%23312123?style=for-the-badge">
     <img alt="Nord" src="https://img.shields.io/badge/Nord-%23312123?style=for-the-badge">
     <img alt="Rosépine" src="https://img.shields.io/badge/Ros%C3%A9pine-%23312123?style=for-the-badge">
     <img alt="Everforest" src="https://img.shields.io/badge/Everforest-%23312123?style=for-the-badge">
   </p>

For more examples, check out the `examples directory <https://github.com/TrueMyst/BeatPrints/tree/main/examples>`_.


✨ Features
-----------

.. list-table::
   :widths: 5 30 65
   :header-rows: 1

   * -
     - Feature
     - Description
   * - 📷
     - **Polaroid filter for covers**
     - Give your track or album covers a vintage Polaroid aesthetic.
   * - 🌐
     - **Multi-language support**
     - Supports Latin, Hindi, Bengali, Russian, Japanese, Chinese, and Korean.
   * - 🖼️
     - **Custom cover art**
     - Use your own images instead of the default track or album artwork.
   * - 🎨
     - **Theme customization**
     - Switch between multiple built-in themes to match your style.


🤝 Contributors
---------------

Thank you to all contributors for making BeatPrints better!

.. raw:: html

   <p align="center">
     <a href="https://github.com/TrueMyst/BeatPrints/graphs/contributors">
       <img src="https://contrib.rocks/image?repo=TrueMyst/BeatPrints" />
     </a>
   </p>


💡 Why BeatPrints?
------------------

I created this project after finding out that people sell these posters on
`Etsy <https://www.etsy.com/market/spotify_poster>`_ at high prices, offering only
digital downloads instead of shipping actual posters.

I wanted to make it free for everyone to print themselves, as I believe my posters
are simpler, cleaner, and prettier.


❤️ Special Thanks
-----------------

- A big thanks to `Spotify Poster Generator <https://github.com/AnveshakR/poster-generator/>`_ by
  `@AnveshakR <https://github.com/AnveshakR>`_ for inspiring BeatPrints with amazing ideas!
- Shoutout to `@Magniquick <https://github.com/Magniquick>`_,
  `@itsnotrin <https://github.com/itsnotrin>`_,
  `@wenbang24 <https://github.com/wenbang24>`_ and
  `@cherriae <https://github.com/cherriae>`_ for their awesome contributions!


📜 License
----------

BeatPrints is distributed under the **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License**:

.. list-table::
   :widths: 25 75
   :header-rows: 1

   * - Term
     - Details
   * - **Use**
     - Free to share and adapt.
   * - **Attribution**
     - Provide credit and a link to the license.
   * - **NonCommercial**
     - Not for commercial use.
   * - **ShareAlike**
     - Adaptations must follow the same license.

Read the full license `here <https://github.com/TrueMyst/BeatPrints/blob/main/LICENSE>`_.


.. centered:: Made with 💜
.. centered:: elysianmyst, 2026

📋️ Table
---------
.. toctree::
   :maxdepth: 1
  
   guidebook/index
   reference/index
   misc/index
