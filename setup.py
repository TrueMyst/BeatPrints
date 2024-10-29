import pathlib
from setuptools import setup, find_packages

here = pathlib.Path(__file__).parent.resolve()
desc = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="Beatprints",
    version="1.0.0",
    description="☕️ BeatPrints, a tool designed to create eye-catching, Pinterest-style music posters using Spotify and LRClib API",
    long_description=desc,
    long_description_content_type="text/markdown",
    author="TrueMyst",
    url="https://github.com/TrueMyst/BeatPrints",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.8",
    ],
    python_requires=">=3.8",
    packages=find_packages(include=["BeatPrints"]),
    package_data={"": ["*.ttf", "*.png", "*.jpg"]},
)
