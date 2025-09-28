#!/usr/bin/env bash
set -euo pipefail

# Repo root (works both locally and inside cibuildwheel containers)
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")"/.. && pwd)"
VENDOR_DIR="${REPO_ROOT}/vendor/geos"

# GEOS version to build (allow override from environment)
GEOS_VERSION="${GEOS_VERSION:-3.14.0}"
GEOS_DIR="geos-${GEOS_VERSION}"
TARBALL="${GEOS_VERSION}.tar.gz"
TARBALL_URL="https://github.com/libgeos/geos/archive/refs/tags/${GEOS_VERSION}.tar.gz"

# Derive a platform identifier:
#  - in cibuildwheel, CIBW_BUILD looks like cp311-manylinux_x86_64; we keep the part after first '-'
#  - locally, fall back to 'local'
CIBW_BUILD_TAG=${CIBW_BUILD:-local}
if [[ "${CIBW_BUILD_TAG}" == *-* ]]; then
  PLATFORM_ID="${CIBW_BUILD_TAG#*-}"
else
  PLATFORM_ID="${CIBW_BUILD_TAG}"
fi

INSTALL_PREFIX="${VENDOR_DIR}/${PLATFORM_ID}"
INCLUDE_DIR="${INSTALL_PREFIX}/include"
LIB_DIR="${INSTALL_PREFIX}/lib"

# Short-circuit if we already have the libraries for this platform
if [[ -f "${LIB_DIR}/libgeos.a" && -f "${LIB_DIR}/libgeos_c.a" && -f "${INCLUDE_DIR}/geos_c.h" ]]; then
  echo "GEOS already prepared for platform '${PLATFORM_ID}' at ${INSTALL_PREFIX}. Skipping build."
  exit 0
fi

echo "Preparing GEOS ${GEOS_VERSION} for platform '${PLATFORM_ID}'..."
mkdir -p "${INCLUDE_DIR}" "${LIB_DIR}"

# Download and unpack
rm -rf "${GEOS_DIR}" "${TARBALL}"
curl -fsSL -o "${TARBALL}" "${TARBALL_URL}"
tar -xzf "${TARBALL}"

# Build static libs
pushd "${GEOS_DIR}" >/dev/null
mkdir -p build
pushd build >/dev/null
cmake .. -DBUILD_SHARED_LIBS=OFF -DCMAKE_BUILD_TYPE=Release -DCMAKE_POSITION_INDEPENDENT_CODE=ON
make -j"$(nproc)"
popd >/dev/null

# Copy artifacts
cp "build/lib/libgeos.a" "${LIB_DIR}/"
cp "build/lib/libgeos_c.a" "${LIB_DIR}/"
cp "build/capi/geos_c.h" "${INCLUDE_DIR}/"
mkdir -p "${INCLUDE_DIR}/geos"
cp "include/geos/export.h" "${INCLUDE_DIR}/geos/"

popd >/dev/null

# Cleanup
rm -rf "${GEOS_DIR}" "${TARBALL}"

echo "GEOS prepared at: ${INSTALL_PREFIX}"
# Print a lightweight tree using find to avoid tree dependency
find "${INSTALL_PREFIX}" -maxdepth 2 -type f -printf "%P\n" | sed "s#^#vendor/geos/${PLATFORM_ID}/#"
