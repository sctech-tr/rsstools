from setuptools import setup, find_packages

setup(
    name="rsstools",
    version="0.3.0",
    packages=find_packages(),
    url="https://github.com/sctech-tr/rsstools",
    license="GPLv3",
    keywords="rss feed rssfeed xml tool cli rssxml atomrss rssatom news",
    install_requires=[
        "click>=8.0.0",
    ],
    entry_points={
        "console_scripts": [
            "rsstools=rsstools.cli:main",
        ],
    },
)