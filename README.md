<h3 align="center">
    <img src="https://i.ibb.co/CWY693F/beatprints-logo.png" width="175"/>
</h3>
<h3 align="center">
    BeatPrints: Quick, stylish posters for your favorite tracks and albums! 🎷☕️
</h3>

<p align="center">Create eye-catching, <b>pinterest-style</b> music posters effortlessly.<br>BeatPrints integrates with <b>Deezer</b> and <b>LRClib API</b> to help you design custom posters for your favorite tracks or albums. 🍀</p>

### **More Languages**  
[English](README.md)  |  [简体中文](README.zh-CN.md)

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

<br>

![examples](https://i.imgur.com/PDcc2Qp.jpeg)

<h3 align="center">📔 Check out the documentation <a href="https://beatprints.readthedocs.io/en/latest/">here!</a></h3>

## 📦 Installation

You can install BeatPrints via:

```bash
# For pip users
pip install BeatPrints

# For poetry users
poetry add BeatPrints
```

Or if you prefer using just the CLI:

```bash
pipx install BeatPrints
```

This will install the CLI, making it ready for you to use.
For more information, check out [pipx](https://github.com/pypa/pipx)

## 🚀 Quick Start

Here's how you can create your first **track / album** poster.

#### 🎵 Track

```python
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
```

#### 💿 Album

```python
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
```

Here's what the posters look like:

|             **Track: Apples by Rocco**             |             **Album: Charm by Clairo**             |
| :------------------------------------------------: | :------------------------------------------------: |
| ![Track Example](https://i.imgur.com/09ExFbx.jpeg) | ![Album Example](https://i.imgur.com/MUkQAb6.jpeg) |

## 🥞 CLI

Here's a short video showing how to generate posters using the CLI. For more information refer to the documentation [here](https://beatprints.readthedocs.io/en/latest/guidebook/cli.html)

https://github.com/user-attachments/assets/3efb7028-c533-4bf4-880b-da3a71f8a3db

## 🎨 Themes

BeatPrints currently offers you **6 additional themes** to use!

<p>
  <img alt="Dark" src="https://img.shields.io/badge/Dark-%23312123?style=for-the-badge">
  <img alt="Catppuccin" src="https://img.shields.io/badge/Catppuccin-%23312123?style=for-the-badge">
  <img alt="Gruvbox" src="https://img.shields.io/badge/Gruvbox-%23312123?style=for-the-badge">
  <img alt="Nord" src="https://img.shields.io/badge/Nord-%23312123?style=for-the-badge">
  <img alt="Rosepine" src="https://img.shields.io/badge/Rosépine-%23312123?style=for-the-badge">
  <img alt="Everforest" src="https://img.shields.io/badge/Everforest-%23312123?style=for-the-badge">
</p>

For more examples, check out the [examples directory](https://github.com/TrueMyst/BeatPrints/tree/main/examples).

## ✨ Features

|     | Feature                        | Description                                                                          |
| --- | ------------------------------ | ------------------------------------------------------------------------------------ |
| 📷  | **Polaroid filter for covers** | Give your track or album covers a vintage Polaroid aesthetic.                        |
| 🌐  | **Multi-language support**     | Supports with Latin, Hindi, Bengali, Russian, Japanese, Chinese, and Korean.         |
| 🖼️  | **Custom cover art**           | Use your own images instead of the default track or album artwork.                   |
| 🎨  | **Theme customization**        | Switch between multiple built-in themes to match your style.                         |

## 🤝 Contributors

Thank you to all contributors for making BeatPrints better!

<p align="center">
 <a href="https://github.com/TrueMyst/BeatPrints/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=TrueMyst/BeatPrints" />
 </a>
</p>

## 💡 Why BeatPrints?

I created this project after finding out that people sell these posters on [Etsy](https://www.etsy.com/market/spotify_poster) at high prices, offering only digital downloads instead of shipping actual posters.

I wanted to make it free for everyone to print themselves, as I believe my posters are simpler, cleaner, and prettier.

## ❤️ Special Thanks

- A big thanks to [Spotify Poster Generator](https://github.com/AnveshakR/poster-generator/) by [@AnveshakR](https://github.com/AnveshakR) for inspiring BeatPrints with amazing ideas!
- Shoutout to [@Magniquick](https://github.com/Magniquick), [@itsnotrin](https://github.com/itsnotrin), [@wenbang24](https://github.com/wenbang24) and [@cherriae](https://github.com/cherriae) for their awesome contributions!

## 📜 License

BeatPrints is distributed under the **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License**:

| Term              | Details                                   |
| ----------------- | ----------------------------------------- |
| **Use**           | Free to share and adapt.                  |
| **Attribution**   | Provide credit and a link to the license. |
| **NonCommercial** | Not for commercial use.                   |
| **ShareAlike**    | Adaptations must follow the same license. |

Read the full license [here](https://github.com/TrueMyst/BeatPrints/blob/main/LICENSE).

<p align="center">
Made with 💜 <br>
elysianmyst, 2026
</p>
