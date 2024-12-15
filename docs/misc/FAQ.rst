Frequently Asked Questions
==========================

Can I sell these posters?
-------------------------
No, you cannot sell these posters. The project was created to offer an alternative to overpriced music posters being sold online, especially on platforms like `Etsy <https://www.etsy.com/market/spotify_poster>`_, where digital downloads were sold at high prices. Since the posters use copyrighted song lyrics and album art from Spotify, selling them could lead to legal issues. The tool is intended for personal use and non-commercial sharing only.

Is BeatPrints compatible with other music platforms?
----------------------------------------------------
Currently, BeatPrints is designed to work with Spotify via its API. While it doesn't natively support other music platforms like Apple Music or YouTube, anyone can customize the code to integrate additional platforms if they choose to extend the tool's functionality.

Why isn't "x" language supported in BeatPrints?
-----------------------------------------------
The lack of support for some languages is due to the large size of font files (around 90 MB) required for the tool. Adding more languages would significantly increase the project's size. Since Pillow (the library used for this project) doesn’t support multi-language text natively, the write.py module would need to be rewritten to handle this, which is a time-consuming task. This issue is actively being worked on, but a simple solution hasn't been found yet.

I've got a really interesting idea for a feature for BeatPrints.
----------------------------------------------------------------
I really appreciate that you want to contribute! Feel free to create an issue on the GitHub page. Just keep in mind that I started this project for fun, so actively maintaining it can be tough for me. I’m not always able to dedicate a lot of time, but I truly appreciate all ideas and contributions, and I’ll try my best to work on it when I can. Your suggestions are always welcome!

How do I fix the libraqm error?
-------------------------------

If you encounter this following error:

.. code::

  "KeyError: 'setting text direction, language or font features is not supported without libraqm'"

For Windows Users
~~~~~~~~~~~~~~~~~
You can resolve this by downloading ``fribidi.dll`` from `here <https://www.dllme.com/dll/files/fribidi>`_ and placing it in your Python directory, such as:

.. code::

  C:\Program Files\Python312\

For macOS Users
~~~~~~~~~~~~~~~
If you run into the same issue, fix it by reinstalling Pillow with the correct configuration:

.. code::

  pip uninstall Pillow  
  pip install Pillow --global-option="build_ext" --config-settings="-I=/opt/homebrew/Cellar"
