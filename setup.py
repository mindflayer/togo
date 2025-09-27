import os
import urllib.request
from urllib.parse import urlparse

from setuptools import setup, Extension
from Cython.Build import cythonize


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
                sources=["togo.pyx", "tg.c", "tgx.c"],
                include_dirs=[
                    ".",
                    "./vendor/geos/include",
                ],
                library_dirs=[
                    "./vendor/geos/lib",
                ],
                libraries=["geos_c"],
                extra_compile_args=extra_compile_args,
            )
        ]
    ),
    # Explicitly disable auto-discovery in flat layout
    packages=[],
    py_modules=[],
    license="MIT",
)
