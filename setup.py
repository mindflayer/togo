import os

from setuptools import setup, Extension
from Cython.Build import cythonize


def _platform_id():
    tag = os.environ.get("CIBW_BUILD", "local")
    return tag.split("-", 1)[1] if "-" in tag else tag


extra_compile_args = [
    "-ffunction-sections",  # Enable function-level sections
    "-fdata-sections",  # Enable data-level sections
]
# Avoid gc-sections when statically linking C++ libs with RTTI/vtables
extra_link_args = [
    # intentionally no --gc-sections
    "-lstdc++",  # Link against C++ standard library
]

# Enable optional AddressSanitizer build via env var ASAN=1
if os.environ.get("ASAN") == "1":
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

repo_root = os.path.abspath(os.path.dirname(__file__))
plat_id = _platform_id()

# Prefer platform-specific vendor path, fall back to legacy flat layout
cand_include = os.path.join(repo_root, "vendor", "geos", plat_id, "include")
cand_lib = os.path.join(repo_root, "vendor", "geos", plat_id, "lib")
if os.path.isdir(cand_include) and os.path.isdir(cand_lib):
    geos_include = cand_include
    geos_lib = cand_lib
else:
    geos_include = os.path.join(repo_root, "vendor", "geos", "include")
    geos_lib = os.path.join(repo_root, "vendor", "geos", "lib")

setup(
    ext_modules=cythonize(
        [
            Extension(
                "togo",
                sources=["togo.pyx", "tg.c", "tgx.c"],
                include_dirs=[
                    ".",  # For tg.h and tgx.h
                    geos_include,
                ],
                # Link static archives as whole-archive to keep all needed RTTI/vtables
                extra_compile_args=extra_compile_args,
                extra_link_args=[
                    "-Wl,--whole-archive",
                    os.path.join(geos_lib, "libgeos_c.a"),
                    os.path.join(geos_lib, "libgeos.a"),
                    "-Wl,--no-whole-archive",
                ]
                + extra_link_args,
            )
        ]
    ),
    # Explicitly disable auto-discovery in flat layout
    packages=[],
    py_modules=[],
    license="MIT",
)
