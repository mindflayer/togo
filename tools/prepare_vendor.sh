#!/usr/bin/env bash
set -e

VENDOR_GEOS_DIR="vendor/geos"
GEOS_VERSION=3.14.0
GEOS_DIR=geos-${GEOS_VERSION}

# download and unpack GEOS
wget https://github.com/libgeos/geos/archive/refs/tags/${GEOS_VERSION}.tar.gz
tar -xzf ${GEOS_VERSION}.tar.gz
cd ${GEOS_DIR}
# build GEOS as static libraries
mkdir build
cd build
cmake .. -DBUILD_SHARED_LIBS=OFF -DCMAKE_BUILD_TYPE=Release -DCMAKE_POSITION_INDEPENDENT_CODE=ON
make -j$(nproc)
cd ../..

# Prepare vendor directory
mkdir -p ${VENDOR_GEOS_DIR}/lib
mkdir -p ${VENDOR_GEOS_DIR}/include/geos
cp ${GEOS_DIR}/build/lib/libgeos.a ${VENDOR_GEOS_DIR}/lib/
cp ${GEOS_DIR}/build/lib/libgeos_c.a ${VENDOR_GEOS_DIR}/lib/
cp ${GEOS_DIR}/build/capi/geos_c.h ${VENDOR_GEOS_DIR}/include/
cp ${GEOS_DIR}/include/geos/export.h ${VENDOR_GEOS_DIR}/include/geos/

rm -rf ${GEOS_DIR}
rm ${GEOS_VERSION}.tar.gz

echo "Shapely GEOS static libraries and header have been built and copied to ${VENDOR_GEOS_DIR}."
tree vendor/geos
