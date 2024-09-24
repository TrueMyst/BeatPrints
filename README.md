<h3 align="center">
	<img src="https://i.ibb.co/CWY693F/beatprints-logo.png" width="175"/>
</h3>
<h3 align="center">
	BeatPrints: Quick, stylish posters for your favorite tracks! 🎷☕️
</h3>

<p align="center">A tool designed to create eye-catching Pinterest-style music posters that stand out. It provides a straightforward way to generate custom posters using <b>Spotify</b> and <b>LRClib API</b>. 🍀</p>

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

![examples](https://i.ibb.co.com/y0jKqHK/banner.png)

## 📜 Getting Started

### `1.1` Installation

Clone this repository into your preferred directory using Git:

```bash
git clone --depth 1 https://github.com/TrueMyst/BeatPrints.git && cd BeatPrints
```

### `1.2` Dependencies

Install the necessary dependencies using pip:

```bash
$ pip install -r requirements.txt
```

This ensures all required packages are installed to run the project smoothly.

### `1.3` Environment Variables

To run this project, you need to create a `.env` file to set up the required environmental variables. These include:

- **SPOTIFY_CLIENT_ID** and **SPOTIFY_CLIENT_SECRET**, which can be obtained from [Spotify for Developers](https://developer.spotify.com/dashboard/).

> [!NOTE]
> Make sure you select **Web API** as the scope of the application.

You can find an example `.env` file [here](https://github.com/TrueMyst/BeatPrints/tree/main/{example}.env). Rename this file to `.env` and use it as needed.

### `1.4` Generating Posters

Navigate to the [cli](https://github.com/TrueMyst/BeatPrints/tree/main/cli/) directory and execute the following command:

```bash
$ python3 prompt.py
```

> [!IMPORTANT]
>
> ```bash
> KeyError: 'setting text direction, language or font features is not supported without libraqm'.
> ```
>
> If you're on Windows, you may encounter this problem. You can resolve this issue, by installing `fribidi.dll` for Pillow to handle complicated texts. Download the required file from [here](https://www.dllme.com/dll/files/fribidi) and place it in the following directory: `C:\Program Files\Python312\`
>
> If you're on macOS, you can fix this issue by running these commands:
> ```bash
> pip3 uninstall Pillow
> pip3 install Pillow --global-option="build_ext" --config-settings="-I = /opt/homebrew/Cellar"
> ```

### `1.5` Current Features

For now BeatPrints offers these such features:

- [x] **Polaroid Filter**: Enhance cover pictures with a classic look.
- [x] **Multi-language Support**: English, Hindi, Russian, Japanese, Chinese, Korean.
- [x] **Custom Image**: Personalize with your own cover image.
- [x] **Themes**: Choose between Dark mode and Light mode.
- [x] **Song Selection**: Highlight your favorite track.
- [x] **Lyrics Selection**: Feature meaningful lyrics.

More features are yet to come :)

### `1.6` We got more samples!

If you're looking for more samples, no worries—we've got you covered. Head to the [examples](https://github.com/TrueMyst/BeatPrints/tree/main/examples/) directory to find additional posters available for viewing.

## 🤝 Contributing

Contributions to BeatPrints are welcome. Feel free to submit your suggestions via pull requests. Your contributions are invaluable in enhancing this tool for everyone.

## 💡 Inspiration & Gratitude

I created this project after finding out that people sell these posters on [Etsy](https://www.etsy.com/market/spotify_poster) at high prices, offering only digital downloads instead of shipping actual posters. I wanted to make it free for everyone to print themselves, and I believe my posters are simpler, cleaner, and prettier.

- Thanks to [Spotify Poster Generator](https://github.com/AnveshakR/poster-generator/) by [@AnveshakR](https://github.com/AnveshakR) for a good amount of ideas!
- A big shoutout to [@Magniquick](https://github.com/Magniquick) & @[Krishna-Gunjan](https://github.com/Krishna-Gunjan) for their big contributions!
- And a heartfelt thank you to [@T-Dynamos](https://github.com/T-Dynamos) and [@cherriae](https://github.com/cherriae) for their significant improvements to BeatPrints.

## 📋 About License

**BeatPrints** is released under the **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License**, which grants the following permissions:

- **Use:** Copy, share, and adapt the material.
- **Attribution:** Provide appropriate credit to the owner and a link to the license.
- **NonCommercial:** Don't use it for commercial purposes.
- **ShareAlike:** Share adaptations under the same license.
- **No Additional Restrictions:** Don't impose extra legal or technological limitations.

For more detailed information, please check out the [LICENSE](https://github.com/TrueMyst/BeatPrints/blob/main/LICENSE)

<br>

<p align="center">
Made with 💜<br>
elysianmyst, 2024
</p>
