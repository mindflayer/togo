import os
import shlex
import subprocess
import sys

from setuptools import setup, Extension
from Cython.Build import cythonize


def _platform_id():
    tag = os.environ.get("CIBW_BUILD", "local")
    return tag.split("-", 1)[1] if "-" in tag else tag


extra_compile_args = [
    "-ffunction-sections",  # Enable function-level sections
    "-fdata-sections",  # Enable data-level sections
    "-O2",  # Default optimization for non-ASAN builds
]
# Avoid gc-sections when statically linking C++ libs with RTTI/vtables
extra_link_args = [
    # intentionally no --gc-sections
    "-lstdc++",  # Link against C++ standard library
]

# Enable optional AddressSanitizer build via env var ASAN=1
if os.environ.get("ASAN") == "1":
    # Favor debuggability over speed; replace -O2 with lower optimization.
    extra_compile_args = [
        "-ffunction-sections",
        "-fdata-sections",
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

geos_include = os.path.join(repo_root, "vendor", "geos", plat_id, "include")
geos_lib = os.path.join(repo_root, "vendor", "geos", plat_id, "lib")

geos_c_a = os.path.join(geos_lib, "libgeos_c.a")
geos_a = os.path.join(geos_lib, "libgeos.a")

include_dirs = ["."]
extra_link_args_final = list(extra_link_args)

if os.path.exists(geos_c_a) and os.path.exists(geos_a) and os.path.exists(os.path.join(geos_include, "geos_c.h")):
    include_dirs.append(geos_include)
    if sys.platform == "darwin":
        whole_archive_flags = [
            "-Wl,-force_load," + geos_c_a,
            "-Wl,-force_load," + geos_a,
        ]
    else:
        whole_archive_flags = [
            "-Wl,--whole-archive",
            geos_c_a,
            geos_a,
            "-Wl,--no-whole-archive",
        ]
    extra_link_args_final = whole_archive_flags + extra_link_args_final
else:
    # Fallback for local development when vendored GEOS is not prepared.
    # `geos-config` is provided by system/brew geos installs.
    geos_config = os.environ.get("GEOS_CONFIG", "geos-config")
    try:
        cflags = subprocess.check_output([geos_config, "--cflags"], text=True).strip()
        libs = subprocess.check_output([geos_config, "--clibs"], text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        raise RuntimeError(
            "GEOS not found. Run 'bash tools/prepare_vendor.sh' (requires cmake) "
            "or install geos so 'geos-config' is available."
        )

    for token in shlex.split(cflags):
        if token.startswith("-I") and len(token) > 2:
            include_dirs.append(token[2:])

    extra_link_args_final = shlex.split(libs) + extra_link_args_final

setup(
    ext_modules=cythonize(
        [
            Extension(
                "togo",
                sources=["togo.pyx", "tg.c", "tgx.c"],
                include_dirs=include_dirs,
                # Link static archives as whole-archive to keep all needed RTTI/vtables
                extra_compile_args=extra_compile_args,
                extra_link_args=extra_link_args_final,
            )
        ]
    ),
    # Explicitly disable auto-discovery in flat layout
    packages=[],
    py_modules=[],
    license="MIT",
)
