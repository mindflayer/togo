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

# Enable optional AddressSanitizer build via env var ASAN=1
asan_enabled = os.environ.get("ASAN") == "1"
extra_compile_args = []
extra_link_args = []
if asan_enabled:
    # Favor debuggability over speed
    extra_compile_args += [
        "-O1",
        "-g",
        "-fno-omit-frame-pointer",
        "-fsanitize=address",
    ]
    extra_link_args += [
        "-fsanitize=address",
    ]

setup(
    ext_modules=cythonize(
        [
            Extension(
                "togo",
                sources=["togo.pyx", TG_SOURCE_FILENAME],
                include_dirs=["."],
                extra_compile_args=extra_compile_args,
                extra_link_args=extra_link_args,
            )
        ]
    ),
    # Explicitly disable auto-discovery in flat layout
    packages=[],
    py_modules=[],
    license="MIT",
)
