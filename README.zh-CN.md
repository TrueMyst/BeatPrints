<h3 align="center">
    <img src="https://i.ibb.co/CWY693F/beatprints-logo.png" width="175"/>
</h3>

<h3 align="center">
    <b>BeatPrints:</b>为您喜欢的歌曲或专辑高效地生成时髦的海报🎷☕️
</h3>

<p align="center">创造吸睛的Pinterest风音乐海报，不费吹灰之力<br>BeatPrints整合了<b>Spotify</b>和<b>LRClib API</b>来帮助你为你喜爱的专辑或单曲设计定制海报🍀</p>

### **更多语言**  
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


![examples](https://i.imgur.com/tQdIeIU.png)

<h3 align="center">
📔 点击 <a href="https://beatprints.readthedocs.io/en/latest/">此处</a> 查看帮助文档！
</h3>

## 📦 安装

<b>可以从以下方法安装:</b>

```bash
# For pip users
pip install BeatPrints

# For poetry users
poetry add BeatPrints
```

<b>面向CLI用户:</b>

```bash
pipx install BeatPrints
```

此操作将安装 CLI，  
更多信息请查看 [pipx](https://github.com/pypa/pipx)

## 🚀 快速开始

### 🌱 配置环境变量

开始使用BeatPrints, 你需要准备一个包含以下内容的```.env```文件：

```env
SPOTIFY_CLIENT_ID = "<your-client-id>"
SPOTIFY_CLIENT_SECRET = "<your-client-secret>"
```

你可以在 [Spotify开发者控制台](https://developer.spotify.com/dashboard/) 创建一个作用域为Web API的新应用来获取以上信息

### 🎀 创建你的第一份海报
以下是创建第一份海报的方法：

```python
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

# Search for the track and fetch metadata
search = sp.get_track("Saturn - SZA", limit=1)

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
```

## 🥞 CLI 命令行工具

下面是一个简短的视频展示如何使用CLI创建海报  
更多信息请参照 [文档](https://beatprints.readthedocs.io/en/latest/guidebook/cli.html)

https://github.com/user-attachments/assets/3efb7028-c533-4bf4-880b-da3a71f8a3db

## 🖼️ 示例

|**单曲: Saturn by SZA**|**专辑: Charm by Clairo**|
|---|---|
| ![Track Example](https://i.imgur.com/wWUbdK1.png)| ![Album Example](https://i.imgur.com/9vlD94t.png)|


## 🎨 主题
BeatPrints目前为您提供 **5种不同的** 附加主题来使用！
- Catppuccin
- Gruvbox
- Nord
- Rosepine
- Everforest

更多例图请查看[examples directory](https://github.com/TrueMyst/BeatPrints/tree/main/examples).


## ✨ 特征

- **宝丽来封面滤镜**: 为您的曲目和专辑提供复古的宝丽来外观.  
- **多语言支持**: 支持英文，印地语, 俄语, 日语, 中文, 韩语.  
- **自定义封面图像**: 支持使用自己的图片制作个性化海报.  
- **主题定制**: 在不同主体之间切换.
- **单曲/专辑 选择**: 展示你最喜欢的曲目或整个专辑 
- **歌词高亮**: 直接在海报上突出显示你最喜欢的歌词


## 🤝 贡献者

Thank you to all contributors for making BeatPrints better!  
感谢所有贡献者让 BeatPrints 变得更好！

<p align="center">
 <a href="https://github.com/TrueMyst/BeatPrints/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=TrueMyst/BeatPrints" />
 </a>
</p>


## 💡 为什么创作 BeatPrints?

我发现有人在 [Etsy](https://www.etsy.com/market/spotify_poster) 上高价售卖这些海报，只提供数字版下载而不是邮寄实体海报，所以只做了这个项目。

我想让每个人都可以免费自行打印，因为我相信我的海报更简洁干净和漂亮。


## ❤️  特别感谢

- 十分感谢[@AnveshakR](https://github.com/AnveshakR)的[Spotify Poster Generator](https://github.com/AnveshakR/poster-generator/) 为BeatPrints提供了绝妙的创意!  
- 感谢[@Magniquick](https://github.com/Magniquick), [@itsnotrin](https://github.com/itsnotrin), [@wenbang24](https://github.com/wenbang24) 与 [@cherriae](https://github.com/cherriae) 的精彩共享!


## 📜 License 许可证

BeatPrints 遵循 **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License** 分发:

- **Use**: Free to share and adapt.<br>
使用：免费分享和改编 
- **Attribution**: Provide credit and a link to the license. <br>
署名：辨明出书并链接到许可协议
- **NonCommercial**: Not for commercial use.  
非商业性：禁止用于商业用途
- **ShareAlike**: Adaptations must follow the same license.  
相同方式共享：改编作品必须使用相同许可协议

点击查看[完整许可证](https://github.com/TrueMyst/BeatPrints/blob/main/LICENSE).  


<p align="center">
Made with 💜 <br>
elysianmyst, 2025
</p>
