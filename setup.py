import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


requirements = []
with open('requirements.txt') as f:
    requirements = f.read().splitlines()


setup(
    name = "Beatprints",
    version = "0.0.1",
    author = "TrueMyst",
    author_email = "urEmailHere@gmail.com",
    url='https://github.com/TrueMyst/BeatPrints',
    project_urls={
        'Issue tracker': 'https://github.com/TrueMyst/BeatPrints/issues',
    },
    description = "A tool that generates eye-catching pinterest-style music posters ",
    license = "Creative Commons Attribution-NonCommercial-ShareAlike 4.0. https://creativecommons.org/licenses/by-nc-sa/4.0/",
    keywords = "music posters",
    url = "http://packages.python.org/an_example_pypi_project",
    packages=requirements,
    long_description=read('README.md'),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: Creative Commons Attribution-NonCommercial-ShareAlike 4.0',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
        'Typing :: Typed',
    ],
)