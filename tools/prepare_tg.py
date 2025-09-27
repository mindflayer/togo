import os
import urllib.request
from urllib.parse import urlparse


# Download the tg and tgx source and header files if not already present
NEEDED_FILES = [
    "https://raw.githubusercontent.com/tidwall/tg/main/tg.c",
    "https://raw.githubusercontent.com/tidwall/tg/main/tg.h",
    "https://raw.githubusercontent.com/tidwall/tgx/main/tgx.c",
    "https://raw.githubusercontent.com/tidwall/tgx/main/tgx.h",
]


def download_if_missing(url: str, filename: str):
    if not os.path.exists(filename):
        print(f"Downloading {filename}...")
        urllib.request.urlretrieve(url, filename)


for url in NEEDED_FILES:
    filename = os.path.basename(urlparse(url).path)
    download_if_missing(url, filename)
