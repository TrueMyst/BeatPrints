🥞 CLI Setup
------------

To get started with the BeatPrints CLI, you'll need to set up a configuration file.

Windows
~~~~~~~

1. Create a folder named ``BeatPrints`` in the following directory:

.. code:: python

  C:\Users\<YourUsername>\AppData\Roaming\

2. Inside this folder, create a file called ``config.toml`` with the
   following contents:

.. code:: toml

   [general]
   search_limit = 7
   output_directory = "<path-to-save-your-posters>"

   [credentials]
   # Spotify API credentials - the Spotify API will be use if these are set
   client_id = "<your-client-id>"
   client_secret = "<your-client-secret>"

Replace ``<path-to-save-your-posters>`` with the path where you'd like to save the generated posters, and fill in the ``client_id`` and ``client_secret`` with your Spotify credentials.


.. important::

  If you're using **Windows**, please ensure you use **double backslashes** (``\\``) rather than a single backslash when specifying your output path. For example:

  .. code:: python

    output_directory = "C:\\Users\\<YourUsername>\\Downloads\\Posters"

Linux or macOS
~~~~~~~~~~~~~~

1. Create a folder named ``BeatPrints`` in your ``~/.config/`` directory:

.. code:: python

   ~/.config/BeatPrints/

2. Inside this folder, create a file called ``config.toml`` with the same contents as mentioned above.

Running the CLI
~~~~~~~~~~~~~~~

Once the config file is set up, you can run the BeatPrints CLI:

1. Open your terminal.
2. Type ``beatprints`` and press Enter.

Your poster will be saved in the output directory you specified in the ``config.toml`` file.
