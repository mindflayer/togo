import os

from setuptools import setup, Extension
from Cython.Build import cythonize


extra_compile_args = [
    "-ffunction-sections",  # Enable function-level sections
    "-fdata-sections",  # Enable data-level sections
]
# Avoid gc-sections when statically linking C++ libs with RTTI/vtables
extra_link_args = [
    # intentionally no --gc-sections
    "-lstdc++",  # Link against C++ standard library
]

# Paths to GEOS headers and libraries
geos_include = os.path.abspath("vendor/geos/include")
geos_lib = os.path.abspath("vendor/geos/lib")

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
                    "-Wl,--whole-archive",  # Link static libraries as whole-archive
                    os.path.join(geos_lib, "libgeos_c.a"),
                    os.path.join(geos_lib, "libgeos.a"),
                    "-Wl,--no-whole-archive",  # End whole-archive linking
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
