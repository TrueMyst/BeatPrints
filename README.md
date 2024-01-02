<h3 align="center">
	<img src="https://i.imgur.com/IR6xU7d.png" width="150"/>
	<br><br>
	BeatPrints, a tool that generates eye-catching pinterest-style music posters ☕
</h3>

<p align="center">
  <a href="https://gitHub.com/TrueMyst/BeatPrints/graphs/commit-activity">
    <img src="https://img.shields.io/badge/Maintained%3F-Yes-%23c4b9a6?style=for-the-badge&logo=Undertale&logoColor=%23b5a790&labelColor=%23312123" alt="Maintenance"></a>
    <a href="https://github.com/TrueMyst/BeatPrints/stargazers"><img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/TrueMyst/BeatPrints?style=for-the-badge&logo=Apache%20Spark&logoColor=%23b5a790&labelColor=%23312123&color=%23c4b9a6"></a>
  <a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/Code_Style-black-%23c4b9a6?style=for-the-badge&logo=CodeFactor&logoColor=%23b5a790&labelColor=%23312123" alt="Code Formatter"></a>
  <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Static Badge" src="https://img.shields.io/badge/License-CC_BY--NC--SA_4.0-%23c4b9a6?style=for-the-badge&logo=Pinboard&labelColor=%23312123"></a>
  </p>

![examples](https://i.imgur.com/Sy7gsv6.png)

<p align ="center"><b>BeatPrints</b> is a tool designed to create eye-catching music posters that stand out. It provides a straightforward way to generate custom posters using <b>Spotify</b> and <b>MusixMatch API.</b> 🍀</p>

## 📜 Getting Started

### `1.1` Installation

Clone this repository into your preferred directory using Git:

```bash
git clone https://github.com/TrueMyst/BeatPrints.git
```

### `1.2` Environment Variables

To run this project, set up the required environment variables in the [`.env`](https://github.com/TrueMyst/BeatPrints/tree/main/src/EXAMPLE.env) file located in the [`./src`](https://github.com/TrueMyst/BeatPrints/tree/main/src) directory. These variables include:

- **`MUSIXMATCH_API`** from [MusixMatch for Developers](https://developer.musixmatch.com/)
- **`SPOTIFY_CLIENT_ID`** and **`SPOTIFY_CLIENT_SECRET`** from [Spotify for Developers](https://developer.spotify.com/dashboard/)

### `1.3` Dependencies

Install the necessary dependencies using pip:

```bash
$ pip install -r requirements.txt
```

This ensures all required packages are installed to run the project smoothly.

### `1.4` Generating Posters

Navigate to the [`./src`](https://github.com/TrueMyst/BeatPrints/tree/main/src) directory and execute the following command:

```bash
$ python3 main.py
```

For now BeatPrints offers these such features:

- Custom Image Banner: Add a personalized touch with your own image.
- Song Selection: Highlight your favorite track.
- Lyrics Selection: Feature lyrics that resonate with you

More features are yet to come :)

### `1.5` We got more samples!

If you're looking for more samples, no worries—we've got you covered. Head to the [examples directory](https://github.com/TrueMyst/BeatPrints/tree/main/examples) to find additional posters available for viewing.

## 🤝 Contributing

Contributions to BeatPrints are welcome. Feel free to submit your suggestions via pull requests. Your contributions are invaluable in enhancing this tool for everyone.

## 💡 Inspiration & Gratitude

I stumbled upon incredible music posters on Pinterest and was amazed by their uniqueness. Not finding a platform to create similarly diverse and appealing designs, I set out to develop a program that simplifies the process with just a few clicks and inputs. Surprisingly, the result exceeded my expectations, resulting in BeatPrints!

- Thanks to [Spotify Poster Generator](https://github.com/AnveshakR/poster-generator/) by [@AnveshakR](https://github.com/AnveshakR) for a good amount of ideas!

## 📋 About License

**BeatPrints** is released under the **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License license**, which grants the following permissions:

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
