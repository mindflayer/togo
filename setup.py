import os
import urllib.request
from urllib.parse import urlparse

from setuptools import setup, Extension
from Cython.Build import cythonize

TG_SOURCE_URL = "https://raw.githubusercontent.com/tidwall/tg/main/tg.c"
TG_SOURCE_FILENAME = os.path.basename(urlparse(TG_SOURCE_URL).path)

if not os.path.exists(TG_SOURCE_FILENAME):
    urllib.request.urlretrieve(TG_SOURCE_URL, TG_SOURCE_FILENAME)

TG_HEADER_URL = "https://raw.githubusercontent.com/tidwall/tg/main/tg.h"
TG_HEADER_FILENAME = os.path.basename(urlparse(TG_HEADER_URL).path)

if not os.path.exists(TG_HEADER_FILENAME):
    urllib.request.urlretrieve(TG_HEADER_URL, TG_HEADER_FILENAME)

# Package metadata
NAME = "togo"
VERSION = "0.1.0"
DESCRIPTION = "Lightweight Python bindings for the TG geometry library"
LONG_DESCRIPTION = ""
LONG_DESCRIPTION_CONTENT_TYPE = "text/markdown"
if os.path.exists("README.md"):
    with open("README.md", "r", encoding="utf-8") as f:
        LONG_DESCRIPTION = f.read()

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESCRIPTION_CONTENT_TYPE,
    license="MIT",
    ext_modules=cythonize(
        [
            Extension(
                "togo",
                sources=["togo.pyx", TG_SOURCE_FILENAME],
                include_dirs=["."],
            )
        ]
    ),
    python_requires=">=3.8",
)
