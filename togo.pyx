# cython: language_level=3
cdef extern from "tg.h":
    cdef struct tg_geom:
        pass
    cdef struct tg_point:
        double x
        double y
    cdef struct tg_rect:
        tg_point min
        tg_point max

    # Constructors
    tg_geom *tg_geom_clone(const tg_geom *geom)
    tg_geom *tg_geom_copy(const tg_geom *geom)
    tg_geom *tg_parse_wkt(const char *wkt)
    tg_geom *tg_parse_geojson(const char *geojson)
    tg_geom *tg_parse_wkb(const unsigned char *wkb, size_t len)
    tg_geom *tg_parse_hex(const char *hex)
    void tg_geom_free(tg_geom *geom)
    const char *tg_geom_error(const tg_geom *geom)

    # Accessors
    int tg_geom_typeof(const tg_geom *geom)
    const char *tg_geom_type_string(int type)
    tg_rect tg_geom_rect(const tg_geom *geom)
    int tg_geom_is_feature(const tg_geom *geom)
    int tg_geom_is_featurecollection(const tg_geom *geom)
    int tg_geom_is_empty(const tg_geom *geom)
    int tg_geom_dims(const tg_geom *geom)
    int tg_geom_has_z(const tg_geom *geom)
    int tg_geom_has_m(const tg_geom *geom)
    double tg_geom_z(const tg_geom *geom)
    double tg_geom_m(const tg_geom *geom)
    size_t tg_geom_memsize(const tg_geom *geom)
    int tg_geom_num_points(const tg_geom *geom)
    int tg_geom_num_lines(const tg_geom *geom)
    int tg_geom_num_polys(const tg_geom *geom)
    int tg_geom_num_geometries(const tg_geom *geom)

    # Predicates
    int tg_geom_equals(const tg_geom *a, const tg_geom *b)
    int tg_geom_disjoint(const tg_geom *a, const tg_geom *b)
    int tg_geom_contains(const tg_geom *a, const tg_geom *b)
    int tg_geom_within(const tg_geom *a, const tg_geom *b)
    int tg_geom_covers(const tg_geom *a, const tg_geom *b)
    int tg_geom_coveredby(const tg_geom *a, const tg_geom *b)
    int tg_geom_touches(const tg_geom *a, const tg_geom *b)
    int tg_geom_intersects(const tg_geom *a, const tg_geom *b)

    # Writing
    size_t tg_geom_wkt(const tg_geom *geom, char *dst, size_t n)
    size_t tg_geom_geojson(const tg_geom *geom, char *dst, size_t n)
    size_t tg_geom_wkb(const tg_geom *geom, unsigned char *dst, size_t n)
    size_t tg_geom_hex(const tg_geom *geom, char *dst, size_t n)
    size_t tg_geom_geobin(const tg_geom *geom, unsigned char *dst, size_t n)

from libc.stdlib cimport malloc, free
from libc.string cimport memset

cdef class Geometry:
    cdef tg_geom *geom

    def __cinit__(self, data: str = None, fmt: str = "wkt", geom_ptr = None):
        cdef tg_geom *ptr
        if geom_ptr is not None:
            ptr = <tg_geom *>geom_ptr
            self.geom = ptr
            return
        if fmt == "wkt":
            self.geom = tg_parse_wkt(data.encode("utf-8"))
        elif fmt == "geojson":
            self.geom = tg_parse_geojson(data.encode("utf-8"))
        elif fmt == "hex":
            self.geom = tg_parse_hex(data.encode("utf-8"))
        else:
            raise ValueError("Unknown format")
        err = tg_geom_error(self.geom)
        if err != NULL:
            raise ValueError(err.decode("utf-8"))

    def clone(self):
        raise NotImplementedError("Cloning is not supported in this Python wrapper.")

    def copy(self):
        raise NotImplementedError("Copying is not supported in this Python wrapper.")

    def type(self):
        return tg_geom_typeof(self.geom)

    def type_string(self):
        return tg_geom_type_string(tg_geom_typeof(self.geom)).decode("utf-8")

    def rect(self):
        cdef tg_rect r
        r = tg_geom_rect(self.geom)
        return ((r.min.x, r.min.y), (r.max.x, r.max.y))

    def is_feature(self):
        return bool(tg_geom_is_feature(self.geom))

    def is_featurecollection(self):
        return bool(tg_geom_is_featurecollection(self.geom))

    def is_empty(self):
        return bool(tg_geom_is_empty(self.geom))

    def dims(self):
        return tg_geom_dims(self.geom)

    def has_z(self):
        return bool(tg_geom_has_z(self.geom))

    def has_m(self):
        return bool(tg_geom_has_m(self.geom))

    def z(self):
        return tg_geom_z(self.geom)

    def m(self):
        return tg_geom_m(self.geom)

    def memsize(self):
        return tg_geom_memsize(self.geom)

    def num_points(self):
        return tg_geom_num_points(self.geom)

    def num_lines(self):
        return tg_geom_num_lines(self.geom)

    def num_polys(self):
        return tg_geom_num_polys(self.geom)

    def num_geometries(self):
        return tg_geom_num_geometries(self.geom)

    def equals(self, other: Geometry):
        return bool(tg_geom_equals(self.geom, other.geom))

    def disjoint(self, other: Geometry):
        return bool(tg_geom_disjoint(self.geom, other.geom))

    def contains(self, other: Geometry):
        return bool(tg_geom_contains(self.geom, other.geom))

    def within(self, other: Geometry):
        return bool(tg_geom_within(self.geom, other.geom))

    def covers(self, other: Geometry):
        return bool(tg_geom_covers(self.geom, other.geom))

    def coveredby(self, other: Geometry):
        return bool(tg_geom_coveredby(self.geom, other.geom))

    def touches(self, other: Geometry):
        return bool(tg_geom_touches(self.geom, other.geom))

    def intersects(self, other: Geometry):
        return bool(tg_geom_intersects(self.geom, other.geom))

    def to_wkt(self):
        cdef size_t bufsize = 4096
        cdef char *buf = <char *>malloc(bufsize)
        if not buf:
            raise MemoryError("Failed to allocate memory for WKT buffer")
        memset(buf, 0, bufsize)
        n = tg_geom_wkt(self.geom, buf, bufsize)
        result = (<bytes>buf[:n]).decode("utf-8")
        free(buf)
        return result

    def to_geojson(self):
        cdef size_t bufsize = 4096
        cdef char *buf = <char *>malloc(bufsize)
        if not buf:
            raise MemoryError("Failed to allocate memory for GeoJSON buffer")
        memset(buf, 0, bufsize)
        n = tg_geom_geojson(self.geom, buf, bufsize)
        result = (<bytes>buf[:n]).decode("utf-8")
        free(buf)
        return result

    def to_wkb(self):
        cdef size_t bufsize = 4096
        cdef unsigned char *buf = <unsigned char *>malloc(bufsize)
        if not buf:
            raise MemoryError("Failed to allocate memory for WKB buffer")
        memset(buf, 0, bufsize)
        n = tg_geom_wkb(self.geom, buf, bufsize)
        result = bytes(buf[:n])
        free(buf)
        return result

    def to_hex(self):
        cdef size_t bufsize = 4096
        cdef char *buf = <char *>malloc(bufsize)
        if not buf:
            raise MemoryError("Failed to allocate memory for HEX buffer")
        memset(buf, 0, bufsize)
        n = tg_geom_hex(self.geom, buf, bufsize)
        result = (<bytes>buf[:n]).decode("utf-8")
        free(buf)
        return result

    def to_geobin(self):
        cdef size_t bufsize = 4096
        cdef unsigned char *buf = <unsigned char *>malloc(bufsize)
        if not buf:
            raise MemoryError("Failed to allocate memory for Geobin buffer")
        memset(buf, 0, bufsize)
        n = tg_geom_geobin(self.geom, buf, bufsize)
        result = bytes(buf[:n])
        free(buf)
        return result

    def __dealloc__(self):
        if self.geom:
            tg_geom_free(self.geom)
