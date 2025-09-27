#!/usr/bin/env bash
set -e

make install-deps

# Ensure vendor directories exist
mkdir -p vendor/geos/lib

# Remove any existing files in vendor/geos/lib to avoid conflicts
find vendor/geos/lib -type f -delete
find vendor/geos/lib -type l -delete

# Find Shapely's GEOS libraries and header using Python
GEOS_LIB_DIR=.venv/lib/python3.*/site-packages/shapely.libs

VENDOR_DIR=vendor/geos/lib

cp ${GEOS_LIB_DIR}/libgeos-*.so.* ${VENDOR_DIR}/
cp ${GEOS_LIB_DIR}/libgeos_c-*.so.* ${VENDOR_DIR}/
cd ${VENDOR_DIR}
ln -sf libgeos-*.so.* libgeos.so
ln -sf libgeos_c-*.so.* libgeos_c.so
cd -

touch vendor/geos/include/geos_c.h

echo "Shapely GEOS libraries and header have been copied to vendor/geos/lib."
