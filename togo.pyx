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
    cdef struct tg_ring:
        pass
    cdef struct tg_poly:
        pass
    cdef struct tg_segment:
        tg_point a
        tg_point b
    cdef struct tg_line:
        pass
    ctypedef int bool

    # Enum for tg_index
    cdef enum tg_index:
        TG_DEFAULT
        TG_NONE
        TG_NATURAL
        TG_YSTRIPES

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

    # --- Point functions ---
    tg_rect tg_point_rect(tg_point point)
    bint tg_point_intersects_rect(tg_point a, tg_rect b)

    # --- Segment functions ---
    tg_rect tg_segment_rect(tg_segment s)
    bint tg_segment_intersects_segment(tg_segment a, tg_segment b)

    # --- Rect functions ---
    tg_rect tg_rect_expand(tg_rect rect, tg_rect other)
    tg_rect tg_rect_expand_point(tg_rect rect, tg_point point)
    tg_point tg_rect_center(tg_rect rect)
    bint tg_rect_intersects_rect(tg_rect a, tg_rect b)
    bint tg_rect_intersects_point(tg_rect a, tg_point b)

    # --- Ring functions ---
    tg_ring *tg_ring_new(const tg_point *points, int npoints)
    tg_ring *tg_ring_new_ix(const tg_point *points, int npoints, tg_index ix)
    void tg_ring_free(tg_ring *ring)
    tg_ring *tg_ring_clone(const tg_ring *ring)
    tg_ring *tg_ring_copy(const tg_ring *ring)
    size_t tg_ring_memsize(const tg_ring *ring)
    tg_rect tg_ring_rect(const tg_ring *ring)
    int tg_ring_num_points(const tg_ring *ring)
    tg_point tg_ring_point_at(const tg_ring *ring, int index)
    const tg_point *tg_ring_points(const tg_ring *ring)
    int tg_ring_num_segments(const tg_ring *ring)
    tg_segment tg_ring_segment_at(const tg_ring *ring, int index)
    bint tg_ring_convex(const tg_ring *ring)
    bint tg_ring_clockwise(const tg_ring *ring)
    int tg_ring_index_spread(const tg_ring *ring)
    int tg_ring_index_num_levels(const tg_ring *ring)
    int tg_ring_index_level_num_rects(const tg_ring *ring, int levelidx)
    tg_rect tg_ring_index_level_rect(const tg_ring *ring, int levelidx, int rectidx)
    bint tg_ring_nearest_segment(
        const tg_ring *ring,
        double (*rect_dist)(tg_rect rect, int *more, void *udata),
        double (*seg_dist)(tg_segment seg, int *more, void *udata),
        bint (*iter)(tg_segment seg, double dist, int index, void *udata),
        void *udata
    )
    void tg_ring_line_search(
        const tg_ring *a, const tg_line *b,
        bint (*iter)(tg_segment aseg, int aidx, tg_segment bseg, int bidx, void *udata),
        void *udata
    )
    void tg_ring_ring_search(
        const tg_ring *a, const tg_ring *b,
        bint (*iter)(tg_segment aseg, int aidx, tg_segment bseg, int bidx, void *udata),
        void *udata
    )
    double tg_ring_area(const tg_ring *ring)
    double tg_ring_perimeter(const tg_ring *ring)

    # --- Line functions ---
    tg_line *tg_line_new(const tg_point *points, int npoints)
    tg_line *tg_line_new_ix(const tg_point *points, int npoints, tg_index ix)
    void tg_line_free(tg_line *line)
    tg_line *tg_line_clone(const tg_line *line)
    tg_line *tg_line_copy(const tg_line *line)
    size_t tg_line_memsize(const tg_line *line)
    tg_rect tg_line_rect(const tg_line *line)
    int tg_line_num_points(const tg_line *line)
    const tg_point *tg_line_points(const tg_line *line)
    tg_point tg_line_point_at(const tg_line *line, int index)
    int tg_line_num_segments(const tg_line *line)
    tg_segment tg_line_segment_at(const tg_line *line, int index)
    bint tg_line_clockwise(const tg_line *line)
    int tg_line_index_spread(const tg_line *line)
    int tg_line_index_num_levels(const tg_line *line)
    int tg_line_index_level_num_rects(const tg_line *line, int levelidx)
    tg_rect tg_line_index_level_rect(const tg_line *line, int levelidx, int rectidx)
    bint tg_line_nearest_segment(
        const tg_line *line,
        double (*rect_dist)(tg_rect rect, int *more, void *udata),
        double (*seg_dist)(tg_segment seg, int *more, void *udata),
        bint (*iter)(tg_segment seg, double dist, int index, void *udata),
        void *udata
    )
    void tg_line_line_search(
        const tg_line *a, const tg_line *b,
        bint (*iter)(tg_segment aseg, int aidx, tg_segment bseg, int bidx, void *udata),
        void *udata
    )
    double tg_line_length(const tg_line *line)

    # --- Poly functions ---
    tg_poly *tg_poly_new(
        const tg_ring *exterior, const tg_ring *const holes[], int nholes
    )
    void tg_poly_free(tg_poly *poly)
    tg_poly *tg_poly_clone(const tg_poly *poly)
    tg_poly *tg_poly_copy(const tg_poly *poly)
    size_t tg_poly_memsize(const tg_poly *poly)
    const tg_ring *tg_poly_exterior(const tg_poly *poly)
    int tg_poly_num_holes(const tg_poly *poly)
    const tg_ring *tg_poly_hole_at(const tg_poly *poly, int index)
    tg_rect tg_poly_rect(const tg_poly *poly)
    bint tg_poly_clockwise(const tg_poly *poly)

    # --- Global environment functions ---
    void tg_env_set_allocator(
        void *(*malloc)(size_t), void *(*realloc)(void*, size_t), void (*free)(void*)
    )
    void tg_env_set_index(tg_index ix)
    void tg_env_set_index_spread(int spread)
    void tg_env_set_print_fixed_floats(bint print)

    tg_geom *tg_geom_new_point(tg_point point)
    tg_geom *tg_geom_new_polygon(const tg_poly *poly)
    # New multi-geometry constructors
    tg_geom *tg_geom_new_multipoint(const tg_point *points, int npoints)
    tg_geom *tg_geom_new_multilinestring(const tg_line *const lines[], int nlines)
    tg_geom *tg_geom_new_multipolygon(const tg_poly *const polys[], int npolys)
    tg_geom *tg_geom_new_geometrycollection(const tg_geom *const geoms[], int ngeoms)
    tg_geom *tg_geom_new_multipoint_empty()
    tg_geom *tg_geom_new_multilinestring_empty()
    tg_geom *tg_geom_new_multipolygon_empty()
    tg_geom *tg_geom_new_geometrycollection_empty()
    tg_geom *tg_geom_new_linestring(const tg_line *line)
    tg_point tg_geom_point(const tg_geom *geom)
    tg_point tg_geom_point_at(const tg_geom *geom, int index)
    const tg_line *tg_geom_line(const tg_geom *geom)
    const tg_poly *tg_geom_poly(const tg_geom *geom)
    const tg_geom *tg_geom_geometry_at(const tg_geom *geom, int index)
    const tg_line *tg_geom_line_at(const tg_geom *geom, int index)
    const tg_poly *tg_geom_poly_at(const tg_geom *geom, int index)

cdef extern from "geos_c.h":
    ctypedef void *GEOSContextHandle_t
    ctypedef void *GEOSGeometry
    ctypedef void *GEOSCoordSequence
    GEOSContextHandle_t GEOS_init_r()
    void GEOS_finish_r(GEOSContextHandle_t handle)
    void GEOSGeom_destroy_r(GEOSContextHandle_t handle, GEOSGeometry *g)
    void GEOSCoordSeq_destroy_r(GEOSContextHandle_t handle, GEOSCoordSequence *seq)
    GEOSGeometry *GEOSUnaryUnion(const GEOSGeometry *g)
    GEOSGeometry *GEOSUnaryUnion_r(GEOSContextHandle_t handle, const GEOSGeometry *g)
    GEOSGeometry *GEOSBufferWithStyle_r(
        GEOSContextHandle_t handle, const GEOSGeometry *g, double width,
        int quadSegs, int endCapStyle, int joinStyle, double mitreLimit
    )
    char GEOSisValid_r(GEOSContextHandle_t handle, const GEOSGeometry *g)
    GEOSGeometry *GEOSSimplify_r(
        GEOSContextHandle_t handle, const GEOSGeometry *g, double tolerance
    )
    GEOSGeometry *GEOSTopologyPreserveSimplify_r(
        GEOSContextHandle_t handle, const GEOSGeometry *g, double tolerance
    )
    GEOSCoordSequence *GEOSNearestPoints_r(
        GEOSContextHandle_t handle, const GEOSGeometry *g1, const GEOSGeometry *g2
    )
    int GEOSCoordSeq_getSize_r(
        GEOSContextHandle_t handle, const GEOSCoordSequence *seq, unsigned int *size
    )
    int GEOSCoordSeq_getXY_r(
        GEOSContextHandle_t handle, const GEOSCoordSequence *seq, unsigned int i,
        double *x, double *y
    )
    GEOSGeometry *GEOSGetCentroid_r(
        GEOSContextHandle_t handle, const GEOSGeometry *g
    )
    GEOSGeometry *GEOSConvexHull_r(
        GEOSContextHandle_t handle, const GEOSGeometry *g
    )
    GEOSGeometry *GEOSIntersection_r(
        GEOSContextHandle_t handle, const GEOSGeometry *g1, const GEOSGeometry *g2
    )

cdef extern from "tgx.h":
    GEOSGeometry *tg_geom_to_geos(GEOSContextHandle_t handle, const tg_geom *geom)
    tg_geom *tg_geom_from_geos(GEOSContextHandle_t handle, GEOSGeometry *geom)
    tg_geom *tg_geom_to_meters_grid(const tg_geom *geom, tg_point origin)
    tg_geom *tg_geom_from_meters_grid(const tg_geom *geom, tg_point origin)


from libc.stdlib cimport malloc, free


cdef Geometry _geometry_from_ptr(tg_geom *ptr):
    cdef Geometry g = Geometry.__new__(Geometry)
    g.geom = ptr
    return g


cdef Line _line_from_ptr(tg_line *ptr):
    cdef Line line_obj = Line.__new__(Line)
    line_obj.line = ptr
    line_obj.owns_pointer = False
    return line_obj


cdef class Geometry:
    cdef tg_geom *geom

    def __cinit__(self, data: str = None, fmt: str = "geojson"):
        if self.geom is not NULL:
            return
        if data is not None:
            if fmt == "geojson":
                self.geom = tg_parse_geojson(data.encode("utf-8"))
            elif fmt == "wkt":
                self.geom = tg_parse_wkt(data.encode("utf-8"))
            elif fmt == "hex":
                self.geom = tg_parse_hex(data.encode("utf-8"))
            else:
                raise ValueError("Unknown format")
            err = tg_geom_error(self.geom)
            if err != NULL:
                raise ValueError(err.decode("utf-8"))
            return
        # If data is None, this might be an object created from a C pointer
        # The pointer will be set after __cinit__ in _geometry_from_ptr
        # So we just leave geom as NULL for now

    def __str__(self):
        if self.geom == NULL:
            return "Geometry(NULL)"
        # Prefer WKT for a concise, standard representation
        try:
            return self.to_wkt()
        except Exception:
            # Fallback to type string with bounds if WKT fails
            try:
                t = self.type_string()
            except Exception:
                t = "?"
            try:
                r = self.bounds
            except Exception:
                r = None
            return f"Geometry(type={t}, bounds={r})"

    def __repr__(self):
        return self.__str__()

    def type(self) -> int:
        return tg_geom_typeof(self.geom)

    def type_string(self) -> str:
        return tg_geom_type_string(tg_geom_typeof(self.geom)).decode("utf-8")

    @property
    def bounds(self):
        """Returns (minx, miny, maxx, maxy) for Shapely compatibility"""
        cdef tg_rect r
        r = tg_geom_rect(self.geom)
        return (r.min.x, r.min.y, r.max.x, r.max.y)

    def is_feature(self) -> bool:
        return tg_geom_is_feature(self.geom) != 0

    def is_featurecollection(self) -> bool:
        return tg_geom_is_featurecollection(self.geom) != 0

    @property
    def is_empty(self):
        return tg_geom_is_empty(self.geom) != 0

    @property
    def is_valid(self):
        """Check if the geometry is valid using GEOS.

        A geometry is valid if it satisfies geometric constraints.
        For example, polygons must have proper ring orientation and no self-intersections.
        """
        if self.geom == NULL:
            return False

        cdef GEOSContextHandle_t ctx = GEOS_init_r()
        if ctx == NULL:
            raise RuntimeError("Failed to initialize GEOS context")

        cdef GEOSGeometry *g_geos = tg_geom_to_geos(ctx, self.geom)
        if g_geos == NULL:
            GEOS_finish_r(ctx)
            raise RuntimeError("Failed to convert TG geometry to GEOS")

        cdef char result = GEOSisValid_r(ctx, g_geos)
        GEOSGeom_destroy_r(ctx, g_geos)
        GEOS_finish_r(ctx)

        return result == 1

    @property
    def dims(self) -> int:
        return tg_geom_dims(self.geom)

    @property
    def has_z(self) -> bool:
        return tg_geom_has_z(self.geom) != 0

    @property
    def has_m(self) -> bool:
        return tg_geom_has_m(self.geom) != 0

    @property
    def z(self) -> float:
        return tg_geom_z(self.geom)

    @property
    def m(self) -> float:
        return tg_geom_m(self.geom)

    @property
    def memsize(self) -> int:
        return tg_geom_memsize(self.geom)

    @property
    def num_points(self) -> int:
        return tg_geom_num_points(self.geom)

    @property
    def num_lines(self) -> int:
        return tg_geom_num_lines(self.geom)

    @property
    def num_polys(self) -> int:
        return tg_geom_num_polys(self.geom)

    @property
    def num_geometries(self) -> int:
        return tg_geom_num_geometries(self.geom)

    def equals(self, other) -> bool:
        if other is None or not isinstance(other, Geometry):
            raise TypeError("other must be a Geometry instance")
        return tg_geom_equals(self.geom, (<Geometry>other).geom) != 0

    def disjoint(self, other) -> bool:
        if other is None or not isinstance(other, Geometry):
            raise TypeError("other must be a Geometry instance")
        return tg_geom_disjoint(self.geom, (<Geometry>other).geom) != 0

    def contains(self, other) -> bool:
        if other is None or not isinstance(other, Geometry):
            raise TypeError("other must be a Geometry instance")
        return tg_geom_contains(self.geom, (<Geometry>other).geom) != 0

    def within(self, other) -> bool:
        if other is None or not isinstance(other, Geometry):
            raise TypeError("other must be a Geometry instance")
        return tg_geom_within(self.geom, (<Geometry>other).geom) != 0

    def covers(self, other) -> bool:
        if other is None or not isinstance(other, Geometry):
            raise TypeError("other must be a Geometry instance")
        return tg_geom_covers(self.geom, (<Geometry>other).geom) != 0

    def coveredby(self, other) -> bool:
        if other is None or not isinstance(other, Geometry):
            raise TypeError("other must be a Geometry instance")
        return tg_geom_coveredby(self.geom, (<Geometry>other).geom) != 0

    def touches(self, other) -> bool:
        if other is None or not isinstance(other, Geometry):
            raise TypeError("other must be a Geometry instance")
        return tg_geom_touches(self.geom, (<Geometry>other).geom) != 0

    def intersects(self, other) -> bool:
        if other is None or not isinstance(other, Geometry):
            raise TypeError("other must be a Geometry instance")
        return tg_geom_intersects(self.geom, (<Geometry>other).geom) != 0

    cdef str _to_string(
        self, size_t (*writer_func)(const tg_geom*, char*, size_t), str format_name
    ):
        # First call to get the required buffer size
        cdef size_t required_size = writer_func(self.geom, NULL, 0)
        if required_size == 0:
            return ""

        # Allocate buffer with an extra byte for the null terminator
        cdef char *buf = <char *>malloc(required_size + 1)
        if not buf:
            raise MemoryError(
                f"Failed to allocate memory for {format_name} buffer"
            )

        # Second call to actually write the data
        cdef size_t n = writer_func(self.geom, buf, required_size + 1)
        # Convert to bytes and remove any trailing null terminators
        result = (<bytes>buf[:n]).rstrip(b"\x00").decode("utf-8")
        free(buf)
        return result

    def to_wkt(self) -> str:
        return self._to_string(tg_geom_wkt, "WKT")

    def to_geojson(self) -> str:
        return self._to_string(tg_geom_geojson, "GeoJSON")

    cdef bytes _to_binary(
        self,
        size_t (*writer_func)(const tg_geom*, unsigned char*, size_t),
        str format_name
    ):
        # First call to get the required buffer size
        cdef size_t required_size = writer_func(self.geom, NULL, 0)
        if required_size == 0:
            return b""

        # Allocate buffer with the exact required size
        cdef unsigned char *buf = <unsigned char *>malloc(required_size)
        if not buf:
            raise MemoryError(
                f"Failed to allocate memory for {format_name} buffer"
            )

        # Second call to actually write the data
        cdef size_t n = writer_func(self.geom, buf, required_size)
        # Ensure we don't read beyond the allocated buffer
        cdef size_t actual_len = min(n, required_size)
        result = bytes(buf[:actual_len])
        free(buf)
        return result

    def to_wkb(self) -> bytes:
        return self._to_binary(tg_geom_wkb, "WKB")

    def to_hex(self) -> str:
        return self._to_string(tg_geom_hex, "HEX")

    def to_geobin(self) -> bytes:
        return self._to_binary(tg_geom_geobin, "Geobin")

    def to_meters_grid(self, origin: Point) -> Geometry:
        """Convert geometry to meters grid using tgx."""
        cdef tg_geom *g2 = tg_geom_to_meters_grid(self.geom, origin._get_c_point())
        if not g2:
            raise ValueError("tgx meters grid conversion failed")
        return _geometry_from_ptr(g2)

    def from_meters_grid(self, origin: Point) -> Geometry:
        """Convert geometry from meters grid using tgx."""
        cdef tg_geom *g2 = tg_geom_from_meters_grid(self.geom, origin._get_c_point())
        if not g2:
            raise ValueError("tgx from meters grid conversion failed")
        return _geometry_from_ptr(g2)

    cpdef Point point(self):
        """Get point from Point geometry"""
        cdef tg_point pt = tg_geom_point(self.geom)
        return Point(pt.x, pt.y)

    cpdef Line line(self):
        """Get line from LineString geometry"""
        cdef const tg_line *ln = tg_geom_line(self.geom)
        return _line_from_ptr(<tg_line *>ln)

    cpdef Poly poly(self):
        """Get polygon from Polygon geometry"""
        cdef const tg_poly *p = tg_geom_poly(self.geom)
        return Poly._from_c_poly(<tg_poly *>p)  # Cast away const

    def __getitem__(self, idx: int) -> Geometry:
        cdef const tg_geom *g
        cdef int t = tg_geom_typeof(self.geom)
        cdef int n
        cdef const tg_line *ln
        cdef const tg_poly *poly
        # 1: Point, 2: LineString, 3: Polygon, 4: MultiPoint,
        # 5: MultiLineString, 6: MultiPolygon, 7: GeometryCollection
        if t == 5:  # MultiLineString
            n = tg_geom_num_lines(self.geom)
            if not (0 <= idx < n):
                raise IndexError("MultiLineString index out of range")
            ln = tg_geom_line_at(self.geom, idx)
            return _geometry_from_ptr(tg_geom_new_linestring(<tg_line *>ln))
        elif t == 6:  # MultiPolygon
            n = tg_geom_num_polys(self.geom)
            if not (0 <= idx < n):
                raise IndexError("MultiPolygon index out of range")
            poly = tg_geom_poly_at(self.geom, idx)
            return _geometry_from_ptr(tg_geom_new_polygon(<tg_poly *>poly))
        elif t == 7:  # GeometryCollection
            g = tg_geom_geometry_at(self.geom, idx)
            if g == NULL:
                raise IndexError("GeometryCollection index out of range")
            return _geometry_from_ptr(tg_geom_clone(g))
        else:
            raise IndexError("Indexing not supported for this geometry type")

    @staticmethod
    def from_linestring(points) -> Geometry:
        """Create LineString geometry from points"""
        line = Line(points)
        return _geometry_from_ptr(tg_geom_new_linestring(line._get_c_line()))

    def __dealloc__(self):
        if self.geom:
            tg_geom_free(self.geom)

    # internal accessor for C pointer
    cdef tg_geom *_get_c_geom(self) noexcept:
        return self.geom

    # Shapely-compatible properties
    @property
    def geom_type(self):
        """Returns geometry type string for Shapely compatibility"""
        return self.type_string()

    @property
    def bounds(self):
        """Returns (minx, miny, maxx, maxy) for Shapely compatibility"""
        cdef tg_rect r = tg_geom_rect(self.geom)
        return (r.min.x, r.min.y, r.max.x, r.max.y)

    @property
    def area(self) -> float:
        """Returns area for Polygon geometries"""
        cdef int t = tg_geom_typeof(self.geom)
        cdef const tg_poly *poly
        cdef double total
        cdef int n, i
        if t == 3:  # Polygon
            poly = tg_geom_poly(self.geom)
            return tg_ring_area(tg_poly_exterior(poly))
        elif t == 6:  # MultiPolygon
            total = 0.0
            n = tg_geom_num_polys(self.geom)
            for i in range(n):
                poly = tg_geom_poly_at(self.geom, i)
                total += tg_ring_area(tg_poly_exterior(poly))
            return total
        return 0.0

    @property
    def length(self) -> float:
        """Returns length for LineString geometries"""
        cdef int t = tg_geom_typeof(self.geom)
        cdef const tg_line *line
        cdef const tg_poly *poly
        cdef double total
        cdef int n, i
        if t == 2:  # LineString
            line = tg_geom_line(self.geom)
            return tg_line_length(line)
        elif t == 5:  # MultiLineString
            total = 0.0
            n = tg_geom_num_lines(self.geom)
            for i in range(n):
                line = tg_geom_line_at(self.geom, i)
                total += tg_line_length(line)
            return total
        elif t == 3:  # Polygon - return perimeter
            poly = tg_geom_poly(self.geom)
            return tg_ring_perimeter(tg_poly_exterior(poly))
        return 0.0

    @property
    def wkt(self) -> str:
        """Returns WKT representation"""
        return self.to_wkt()

    @property
    def wkb(self) -> bytes:
        """Returns WKB representation"""
        return self.to_wkb()

    @property
    def coords(self) -> list:
        """Returns coordinate sequence for Point/LineString geometries"""
        cdef int t = tg_geom_typeof(self.geom)
        cdef tg_point pt
        cdef const tg_line *line
        cdef int n, i
        cdef const tg_point *pts
        if t == 1:  # Point
            pt = tg_geom_point(self.geom)
            return [(pt.x, pt.y)]
        elif t == 2:  # LineString
            line = tg_geom_line(self.geom)
            n = tg_line_num_points(line)
            pts = tg_line_points(line)
            return [(pts[i].x, pts[i].y) for i in range(n)]
        else:
            raise AttributeError(f"coords not available for {self.type_string()}")

    @property
    def __geo_interface__(self) -> dict:
        """Returns GeoJSON-like dict for Shapely compatibility"""
        import json
        geojson_str = self.to_geojson()
        return json.loads(geojson_str)

    # --- Factory methods ---
    @staticmethod
    def from_multipoint(points) -> Geometry:
        """
        Create a MultiPoint geometry from an iterable of Point or (x, y) tuples.
        """
        cdef int n = len(points)
        cdef tg_geom *gptr
        if n == 0:
            gptr = tg_geom_new_multipoint_empty()
            if not gptr:
                raise ValueError("Failed to create empty MultiPoint")
            return _geometry_from_ptr(gptr)
        cdef tg_point *pts = <tg_point *>malloc(n * sizeof(tg_point))
        if not pts:
            raise MemoryError("Failed to allocate points for MultiPoint")
        cdef int i
        for i in range(n):
            obj = points[i]
            if isinstance(obj, Point):
                pts[i] = (<Point>obj)._get_c_point()
            else:
                # assume (x, y)
                pts[i].x = float(obj[0])
                pts[i].y = float(obj[1])
        gptr = tg_geom_new_multipoint(pts, n)
        free(pts)
        if not gptr:
            raise ValueError("Failed to create MultiPoint")
        return _geometry_from_ptr(gptr)

    @staticmethod
    def from_multilinestring(lines) -> Geometry:
        """
        Create a MultiLineString from an iterable of Line or sequences of (x,y).
        """
        cdef int n = len(lines)
        cdef tg_geom *gptr
        if n == 0:
            gptr = tg_geom_new_multilinestring_empty()
            if not gptr:
                raise ValueError("Failed to create empty MultiLineString")
            return _geometry_from_ptr(gptr)
        cdef const tg_line **arr = <const tg_line **>malloc(n * sizeof(tg_line *))
        if not arr:
            raise MemoryError("Failed to allocate lines array for MultiLineString")
        cdef int i
        temp_created = []  # keep refs to any temporary Line we create
        for i in range(n):
            obj = lines[i]
            if isinstance(obj, Line):
                arr[i] = (<Line>obj)._get_c_line()
            else:
                # assume it's an iterable of (x, y) tuples
                tmp = Line(obj)
                temp_created.append(tmp)
                arr[i] = tmp._get_c_line()
        gptr = tg_geom_new_multilinestring(arr, n)
        free(arr)
        if not gptr:
            raise ValueError("Failed to create MultiLineString")
        return _geometry_from_ptr(gptr)

    @staticmethod
    def from_multipolygon(polys) -> Geometry:
        """Create a MultiPolygon from an iterable of Poly objects."""
        cdef int n = len(polys)
        cdef tg_geom *gptr
        if n == 0:
            gptr = tg_geom_new_multipolygon_empty()
            if not gptr:
                raise ValueError("Failed to create empty MultiPolygon")
            return _geometry_from_ptr(gptr)
        cdef const tg_poly **arr = <const tg_poly **>malloc(n * sizeof(tg_poly *))
        if not arr:
            raise MemoryError("Failed to allocate polys array for MultiPolygon")
        cdef int i
        for i in range(n):
            obj = polys[i]
            if not isinstance(obj, Poly):
                free(arr)
                raise TypeError("multipolygon expects a sequence of Poly")
            arr[i] = (<Poly>obj)._get_c_poly()
        gptr = tg_geom_new_multipolygon(arr, n)
        free(arr)
        if not gptr:
            raise ValueError("Failed to create MultiPolygon")
        return _geometry_from_ptr(gptr)

    @staticmethod
    def from_geometrycollection(geoms) -> Geometry:
        """
        Create a GeometryCollection from an iterable of Geometry, Point, Line,
        Ring, or Poly. For Point or (x,y) input, temporary tg_geom objects are
        created and freed after cloning.
        """
        cdef int n = len(geoms)
        cdef tg_geom *gptr
        if n == 0:
            gptr = tg_geom_new_geometrycollection_empty()
            if not gptr:
                raise ValueError("Failed to create empty GeometryCollection")
            return _geometry_from_ptr(gptr)
        cdef const tg_geom **arr = <const tg_geom **>malloc(n * sizeof(tg_geom *))
        if not arr:
            raise MemoryError("Failed to allocate geoms array for GeometryCollection")
        cdef tg_geom **temp_to_free = NULL
        cdef int temp_count = 0
        cdef int i
        cdef int j
        cdef tg_geom *tmpg = NULL
        cdef tg_poly *tmp_poly = NULL
        cdef tg_point tmppt
        # two-pass allocation for temporary geoms created
        # from Points/tuples/Line/Ring/Poly
        for i in range(n):
            obj = geoms[i]
            if isinstance(obj, Geometry):
                continue
            elif isinstance(obj, (Point, Line, Ring, Poly)):
                temp_count += 1
            else:
                # try tuple-like point
                try:
                    _x, _y = float(obj[0]), float(obj[1])
                    temp_count += 1
                except Exception:
                    free(arr)
                    raise TypeError(
                        "geometrycollection expects Geometry, Point/(x,y), "
                        "Line, Ring, or Poly"
                    )
        if temp_count > 0:
            temp_to_free = <tg_geom **>malloc(temp_count * sizeof(tg_geom *))
            if not temp_to_free:
                free(arr)
                raise MemoryError(
                    "Failed to allocate temporary geoms for GeometryCollection"
                )
        temp_count = 0
        for i in range(n):
            obj = geoms[i]
            if isinstance(obj, Geometry):
                arr[i] = (<Geometry>obj)._get_c_geom()
            elif isinstance(obj, Point):
                tmpg = tg_geom_new_point((<Point>obj)._get_c_point())
                if not tmpg:
                    if temp_to_free != NULL:
                        for j in range(temp_count):
                            if temp_to_free[j] != NULL:
                                tg_geom_free(temp_to_free[j])
                        free(temp_to_free)
                    free(arr)
                    raise ValueError(
                        "Failed to create temporary Point geometry"
                    )
                temp_to_free[temp_count] = tmpg
                temp_count += 1
                arr[i] = tmpg
            elif isinstance(obj, Line):
                tmpg = tg_geom_new_linestring((<Line>obj)._get_c_line())
                if not tmpg:
                    if temp_to_free != NULL:
                        for j in range(temp_count):
                            if temp_to_free[j] != NULL:
                                tg_geom_free(temp_to_free[j])
                        free(temp_to_free)
                    free(arr)
                    raise ValueError(
                        "Failed to create temporary LineString geometry"
                    )
                temp_to_free[temp_count] = tmpg
                temp_count += 1
                arr[i] = tmpg
            elif isinstance(obj, Ring):
                # Convert ring to a temporary polygon geometry
                tmp_poly = tg_poly_new((<Ring>obj)._get_c_ring(), NULL, 0)
                if not tmp_poly:
                    if temp_to_free != NULL:
                        for j in range(temp_count):
                            if temp_to_free[j] != NULL:
                                tg_geom_free(temp_to_free[j])
                        free(temp_to_free)
                    free(arr)
                    raise ValueError("Failed to create temporary Poly from Ring")
                tmpg = tg_geom_new_polygon(<const tg_poly *>tmp_poly)
                tg_poly_free(tmp_poly)
                if not tmpg:
                    if temp_to_free != NULL:
                        for j in range(temp_count):
                            if temp_to_free[j] != NULL:
                                tg_geom_free(temp_to_free[j])
                        free(temp_to_free)
                    free(arr)
                    raise ValueError(
                        "Failed to create temporary Polygon geometry from Ring"
                    )
                temp_to_free[temp_count] = tmpg
                temp_count += 1
                arr[i] = tmpg
            elif isinstance(obj, Poly):
                tmpg = tg_geom_new_polygon((<Poly>obj)._get_c_poly())
                if not tmpg:
                    if temp_to_free != NULL:
                        for j in range(temp_count):
                            if temp_to_free[j] != NULL:
                                tg_geom_free(temp_to_free[j])
                        free(temp_to_free)
                    free(arr)
                    raise ValueError(
                        "Failed to create temporary Polygon geometry"
                    )
                temp_to_free[temp_count] = tmpg
                temp_count += 1
                arr[i] = tmpg
            else:
                # assume tuple-like point already validated
                tmppt = tg_point(x=float(obj[0]), y=float(obj[1]))
                tmpg2 = tg_geom_new_point(tmppt)
                if not tmpg2:
                    if temp_to_free != NULL:
                        for j in range(temp_count):
                            if temp_to_free[j] != NULL:
                                tg_geom_free(temp_to_free[j])
                        free(temp_to_free)
                    free(arr)
                    raise ValueError(
                        "Failed to create temporary Point geometry"
                    )
                temp_to_free[temp_count] = tmpg2
                temp_count += 1
                arr[i] = tmpg2
        gptr = tg_geom_new_geometrycollection(arr, n)
        # free temporaries
        if temp_to_free != NULL:
            for i in range(temp_count):
                if temp_to_free[i] != NULL:
                    tg_geom_free(temp_to_free[i])
            free(temp_to_free)
        free(arr)
        if not gptr:
            raise ValueError("Failed to create GeometryCollection")
        return _geometry_from_ptr(gptr)

    @staticmethod
    def unary_union(geoms) -> Geometry:
        """Return the unary union of a sequence of geometries using GEOS."""
        cdef int n = len(geoms)
        if n == 0:
            raise ValueError("unary_union requires at least one geometry")
        cdef const tg_geom **arr = <const tg_geom **>malloc(n * sizeof(tg_geom *))
        if not arr:
            raise MemoryError("Failed to allocate geometry array for unary_union")
        cdef tg_geom **temp_to_free = NULL
        cdef int temp_count = 0
        cdef int i, j
        cdef tg_geom *tmpg = NULL
        cdef tg_poly *tmp_poly = NULL
        cdef tg_point tmppt
        # Count temporaries needed
        for i in range(n):
            obj = geoms[i]
            if isinstance(obj, Geometry):
                continue
            elif isinstance(obj, (Point, Line, Ring, Poly)):
                temp_count += 1
            else:
                try:
                    _x, _y = float(obj[0]), float(obj[1])
                    temp_count += 1
                except Exception:
                    free(arr)
                    raise TypeError(
                        "unary_union expects Geometry, Point/(x,y), Line, Ring, or Poly"
                    )
        if temp_count > 0:
            temp_to_free = <tg_geom **>malloc(temp_count * sizeof(tg_geom *))
            if not temp_to_free:
                free(arr)
                raise MemoryError(
                    "Failed to allocate temporary geoms for unary_union"
                )
        temp_count = 0
        for i in range(n):
            obj = geoms[i]
            if isinstance(obj, Geometry):
                arr[i] = (<Geometry>obj)._get_c_geom()
            elif isinstance(obj, Point):
                tmpg = tg_geom_new_point((<Point>obj)._get_c_point())
                if not tmpg:
                    if temp_to_free != NULL:
                        for j in range(temp_count):
                            if temp_to_free[j] != NULL:
                                tg_geom_free(temp_to_free[j])
                        free(temp_to_free)
                    free(arr)
                    raise ValueError("Failed to create temporary Point geometry")
                temp_to_free[temp_count] = tmpg
                temp_count += 1
                arr[i] = tmpg
            elif isinstance(obj, Line):
                tmpg = tg_geom_new_linestring((<Line>obj)._get_c_line())
                if not tmpg:
                    if temp_to_free != NULL:
                        for j in range(temp_count):
                            if temp_to_free[j] != NULL:
                                tg_geom_free(temp_to_free[j])
                        free(temp_to_free)
                    free(arr)
                    raise ValueError("Failed to create temporary LineString geometry")
                temp_to_free[temp_count] = tmpg
                temp_count += 1
                arr[i] = tmpg
            elif isinstance(obj, Ring):
                tmp_poly = tg_poly_new((<Ring>obj)._get_c_ring(), NULL, 0)
                if not tmp_poly:
                    if temp_to_free != NULL:
                        for j in range(temp_count):
                            if temp_to_free[j] != NULL:
                                tg_geom_free(temp_to_free[j])
                        free(temp_to_free)
                    free(arr)
                    raise ValueError("Failed to create temporary Poly from Ring")
                tmpg = tg_geom_new_polygon(<const tg_poly *>tmp_poly)
                tg_poly_free(tmp_poly)
                if not tmpg:
                    if temp_to_free != NULL:
                        for j in range(temp_count):
                            if temp_to_free[j] != NULL:
                                tg_geom_free(temp_to_free[j])
                        free(temp_to_free)
                    free(arr)
                    raise ValueError("Failed to create temporary Polygon geometry from Ring")
                temp_to_free[temp_count] = tmpg
                temp_count += 1
                arr[i] = tmpg
            elif isinstance(obj, Poly):
                tmpg = tg_geom_new_polygon((<Poly>obj)._get_c_poly())
                if not tmpg:
                    if temp_to_free != NULL:
                        for j in range(temp_count):
                            if temp_to_free[j] != NULL:
                                tg_geom_free(temp_to_free[j])
                        free(temp_to_free)
                    free(arr)
                    raise ValueError("Failed to create temporary Polygon geometry")
                temp_to_free[temp_count] = tmpg
                temp_count += 1
                arr[i] = tmpg
            else:
                tmppt = tg_point(x=float(obj[0]), y=float(obj[1]))
                tmpg2 = tg_geom_new_point(tmppt)
                if not tmpg2:
                    if temp_to_free != NULL:
                        for j in range(temp_count):
                            if temp_to_free[j] != NULL:
                                tg_geom_free(temp_to_free[j])
                        free(temp_to_free)
                    free(arr)
                    raise ValueError("Failed to create temporary Point geometry")
                temp_to_free[temp_count] = tmpg2
                temp_count += 1
                arr[i] = tmpg2
        gptr = tg_geom_new_geometrycollection(arr, n)
        if temp_to_free != NULL:
            for i in range(temp_count):
                if temp_to_free[i] != NULL:
                    tg_geom_free(temp_to_free[i])
            free(temp_to_free)
        free(arr)
        if not gptr:
            raise ValueError("Failed to create GeometryCollection for unary_union")
        cdef GEOSContextHandle_t ctx = GEOS_init_r()
        if ctx == NULL:
            tg_geom_free(gptr)
            raise RuntimeError("Failed to initialize GEOS context")
        cdef GEOSGeometry *g_geos = tg_geom_to_geos(ctx, gptr)
        if g_geos == NULL:
            GEOS_finish_r(ctx)
            tg_geom_free(gptr)
            raise RuntimeError("Failed to convert TG geometry to GEOS")
        cdef GEOSGeometry *g_union = GEOSUnaryUnion_r(ctx, g_geos)
        if g_union == NULL:
            GEOS_finish_r(ctx)
            tg_geom_free(gptr)
            raise RuntimeError("GEOSUnaryUnion failed")
        cdef tg_geom *g_tg = tg_geom_from_geos(ctx, g_union)
        GEOS_finish_r(ctx)
        tg_geom_free(gptr)
        if g_tg == NULL:
            raise RuntimeError("Failed to convert GEOS geometry to TG")
        return _geometry_from_ptr(g_tg)

    def buffer(self, distance: float, quad_segs: int = 16,
               cap_style: int = 1, join_style: int = 1,
               mitre_limit: float = 5.0) -> Geometry:
        """
        Return a geometry that is the input geometry buffered by the given distance.

        Parameters:
        -----------
        distance : float
            The buffer distance in the geometry's units
        quad_segs : int
            Number of segments per quadrant (default: 16). Higher values = smoother buffer.
        cap_style : int
            End cap style: 1=round (default), 2=flat, 3=square
        join_style : int
            Join style: 1=round (default), 2=mitre, 3=bevel
        mitre_limit : float
            Mitre ratio limit for joins (default: 5.0)

        Returns:
        --------
        Geometry
            A new Geometry representing the buffered shape
        """
        if distance == 0:
            return self

        if not (0 < cap_style < 4):
            raise ValueError("cap_style must be 1 (round), 2 (flat), or 3 (square)")

        if not (0 < join_style < 4):
            raise ValueError("join_style must be 1 (round), 2 (flat), or 3 (bevel)")

        if quad_segs < 1:
            raise ValueError("quad_segs must be >= 1")

        if not mitre_limit > 0.0:
            raise ValueError("mitre_limit must be > 0.0")

        cdef GEOSContextHandle_t ctx = GEOS_init_r()
        if ctx == NULL:
            raise RuntimeError("Failed to initialize GEOS context")

        cdef GEOSGeometry *g_geos = tg_geom_to_geos(ctx, self.geom)
        if g_geos == NULL:
            GEOS_finish_r(ctx)
            raise RuntimeError("Failed to convert TG geometry to GEOS")

        cdef GEOSGeometry *g_buffered = GEOSBufferWithStyle_r(
            ctx, g_geos, distance, quad_segs, cap_style, join_style, mitre_limit
        )
        if g_buffered == NULL:
            GEOSGeom_destroy_r(ctx, g_geos)
            GEOS_finish_r(ctx)
            raise RuntimeError(f"GEOSBuffer failed with distance {distance}")

        cdef tg_geom *g_tg = tg_geom_from_geos(ctx, g_buffered)
        if g_tg == NULL:
            GEOSGeom_destroy_r(ctx, g_buffered)
            GEOSGeom_destroy_r(ctx, g_geos)
            GEOS_finish_r(ctx)
            raise RuntimeError("Failed to convert GEOS geometry to TG")

        GEOSGeom_destroy_r(ctx, g_buffered)
        GEOSGeom_destroy_r(ctx, g_geos)
        GEOS_finish_r(ctx)

        return _geometry_from_ptr(g_tg)

    def simplify(self, tolerance: float, preserve_topology: bool = True) -> Geometry:
        """
        Return a simplified geometry produced by the Douglas-Peucker algorithm.

        Parameters:
        -----------
        tolerance : float
            The tolerance distance. Coordinates of the simplified geometry will be no more
            than the tolerance distance from the original.
        preserve_topology : bool
            If True (default), use topology-preserving simplification which is more
            computationally expensive but prevents self-intersections and invalid geometries.
            If False, use the standard Douglas-Peucker algorithm which may produce
            self-intersecting geometries but is faster.

        Returns:
        --------
        Geometry
            A new Geometry representing the simplified shape
        """
        if tolerance < 0:
            raise ValueError("tolerance must be >= 0")

        cdef GEOSContextHandle_t ctx = GEOS_init_r()
        if ctx == NULL:
            raise RuntimeError("Failed to initialize GEOS context")

        cdef GEOSGeometry *g_geos = tg_geom_to_geos(ctx, self.geom)
        if g_geos == NULL:
            GEOS_finish_r(ctx)
            raise RuntimeError("Failed to convert TG geometry to GEOS")

        cdef GEOSGeometry *g_simplified
        if preserve_topology:
            g_simplified = GEOSTopologyPreserveSimplify_r(ctx, g_geos, tolerance)
        else:
            g_simplified = GEOSSimplify_r(ctx, g_geos, tolerance)

        if g_simplified == NULL:
            GEOSGeom_destroy_r(ctx, g_geos)
            GEOS_finish_r(ctx)
            raise RuntimeError(
                f"Simplification failed with tolerance {tolerance}"
                f" (preserve_topology={preserve_topology})"
            )

        cdef tg_geom *g_tg = tg_geom_from_geos(ctx, g_simplified)
        if g_tg == NULL:
            GEOSGeom_destroy_r(ctx, g_simplified)
            GEOSGeom_destroy_r(ctx, g_geos)
            GEOS_finish_r(ctx)
            raise RuntimeError("Failed to convert GEOS geometry to TG")

        GEOSGeom_destroy_r(ctx, g_simplified)
        GEOSGeom_destroy_r(ctx, g_geos)
        GEOS_finish_r(ctx)

        return _geometry_from_ptr(g_tg)

    @property
    def centroid(self) -> Geometry:
        """
        Return the centroid of the geometry.

        The centroid is the geometric center of mass of the geometry.
        For polygons, this may lie outside the polygon.

        Returns:
        --------
        Geometry
            A Point geometry representing the centroid

        Raises:
        -------
        RuntimeError
            If the centroid calculation fails
        """
        cdef GEOSContextHandle_t ctx = GEOS_init_r()
        if ctx == NULL:
            raise RuntimeError("Failed to initialize GEOS context")

        cdef GEOSGeometry *g_geos = tg_geom_to_geos(ctx, self.geom)
        if g_geos == NULL:
            GEOS_finish_r(ctx)
            raise RuntimeError("Failed to convert TG geometry to GEOS")

        cdef GEOSGeometry *g_centroid = GEOSGetCentroid_r(ctx, g_geos)
        if g_centroid == NULL:
            GEOSGeom_destroy_r(ctx, g_geos)
            GEOS_finish_r(ctx)
            raise RuntimeError("GEOSGetCentroid failed")

        cdef tg_geom *g_tg = tg_geom_from_geos(ctx, g_centroid)
        if g_tg == NULL:
            GEOSGeom_destroy_r(ctx, g_centroid)
            GEOSGeom_destroy_r(ctx, g_geos)
            GEOS_finish_r(ctx)
            raise RuntimeError("Failed to convert GEOS geometry to TG")

        GEOSGeom_destroy_r(ctx, g_centroid)
        GEOSGeom_destroy_r(ctx, g_geos)
        GEOS_finish_r(ctx)

        return _geometry_from_ptr(g_tg)

    @property
    def convex_hull(self) -> Geometry:
        """
        Return the convex hull of the geometry.

        The convex hull is the smallest convex geometry that encloses all points
        in the input geometry. It is equivalent to the geometry you would get by
        stretching a rubber band around the points.

        Returns:
        --------
        Geometry
            A Polygon (or Point/LineString for degenerate cases) representing
            the convex hull

        Raises:
        -------
        RuntimeError
            If the convex hull calculation fails

        Examples:
        ---------
        >>> from togo import Polygon
        >>> poly = Polygon([(0, 0), (2, 0), (2, 2), (1, 1), (0, 2), (0, 0)])
        >>> hull = poly.convex_hull
        >>> print(hull.to_wkt())
        POLYGON((0 0,2 0,2 2,0 2,0 0))
        """
        cdef GEOSContextHandle_t ctx = GEOS_init_r()
        if ctx == NULL:
            raise RuntimeError("Failed to initialize GEOS context")

        cdef GEOSGeometry *g_geos = tg_geom_to_geos(ctx, self.geom)
        if g_geos == NULL:
            GEOS_finish_r(ctx)
            raise RuntimeError("Failed to convert TG geometry to GEOS")

        cdef GEOSGeometry *g_hull = GEOSConvexHull_r(ctx, g_geos)
        if g_hull == NULL:
            GEOSGeom_destroy_r(ctx, g_geos)
            GEOS_finish_r(ctx)
            raise RuntimeError("GEOSConvexHull failed")

        cdef tg_geom *g_tg = tg_geom_from_geos(ctx, g_hull)
        if g_tg == NULL:
            GEOSGeom_destroy_r(ctx, g_hull)
            GEOSGeom_destroy_r(ctx, g_geos)
            GEOS_finish_r(ctx)
            raise RuntimeError("Failed to convert GEOS geometry to TG")

        GEOSGeom_destroy_r(ctx, g_hull)
        GEOSGeom_destroy_r(ctx, g_geos)
        GEOS_finish_r(ctx)

        return _geometry_from_ptr(g_tg)

    def intersection(self, other) -> Geometry:
        """
        Return the geometric intersection of this geometry with another.

        The intersection is the set of points common to both geometries.
        This method is compatible with Shapely's intersection.

        Parameters:
        -----------
        other : Geometry
            The other geometry to compute the intersection with

        Returns:
        --------
        Geometry
            A Geometry representing the intersection. The result type depends
            on the input geometries and their spatial relationship:
            - Point-Point: Point (if they overlap) or empty
            - Line-Line: Point, LineString, or MultiLineString
            - Polygon-Polygon: Point, LineString, Polygon, or MultiPolygon
            - Empty if geometries do not intersect

        Raises:
        -------
        RuntimeError
            If the intersection calculation fails

        Examples:
        ---------
        >>> from togo import Geometry
        >>> poly1 = Geometry("POLYGON((0 0, 2 0, 2 2, 0 2, 0 0))", fmt="wkt")
        >>> poly2 = Geometry("POLYGON((1 1, 3 1, 3 3, 1 3, 1 1))", fmt="wkt")
        >>> result = poly1.intersection(poly2)
        >>> print(result.geom_type)
        Polygon
        """
        cdef GEOSContextHandle_t ctx
        cdef GEOSGeometry *g1_geos
        cdef GEOSGeometry *g2_geos
        cdef GEOSGeometry *g_intersection
        cdef tg_geom *g_tg
        cdef tg_geom *empty
        cdef Geometry other_geom

        # Return empty geometry for None or non-Geometry objects (Shapely-compatible behavior)
        if other is None or not isinstance(other, Geometry):
            # Return empty geometry collection
            empty = tg_geom_new_geometrycollection_empty()
            return _geometry_from_ptr(empty)

        # Cast to Geometry for safe access to .geom attribute
        other_geom = <Geometry>other

        ctx = GEOS_init_r()
        if ctx == NULL:
            raise RuntimeError("Failed to initialize GEOS context")

        g1_geos = tg_geom_to_geos(ctx, self.geom)
        if g1_geos == NULL:
            GEOS_finish_r(ctx)
            raise RuntimeError("Failed to convert first geometry to GEOS")

        g2_geos = tg_geom_to_geos(ctx, other_geom.geom)
        if g2_geos == NULL:
            GEOSGeom_destroy_r(ctx, g1_geos)
            GEOS_finish_r(ctx)
            raise RuntimeError("Failed to convert second geometry to GEOS")

        g_intersection = GEOSIntersection_r(ctx, g1_geos, g2_geos)
        if g_intersection == NULL:
            GEOSGeom_destroy_r(ctx, g2_geos)
            GEOSGeom_destroy_r(ctx, g1_geos)
            GEOS_finish_r(ctx)
            raise RuntimeError("GEOSIntersection failed")

        g_tg = tg_geom_from_geos(ctx, g_intersection)
        if g_tg == NULL:
            GEOSGeom_destroy_r(ctx, g_intersection)
            GEOSGeom_destroy_r(ctx, g2_geos)
            GEOSGeom_destroy_r(ctx, g1_geos)
            GEOS_finish_r(ctx)
            raise RuntimeError("Failed to convert GEOS geometry to TG")

        GEOSGeom_destroy_r(ctx, g_intersection)
        GEOSGeom_destroy_r(ctx, g2_geos)
        GEOSGeom_destroy_r(ctx, g1_geos)
        GEOS_finish_r(ctx)

        return _geometry_from_ptr(g_tg)

    cdef tuple _get_nearest_point_coords(self, Geometry other):
        """
        Private helper method to extract nearest point coordinates using GEOS.

        Returns a tuple of (x1, y1, x2, y2) representing the two nearest points
        between this geometry and the other geometry.

        This method handles all GEOS initialization, conversion, calculation,
        and cleanup, reducing code duplication between nearest_points() and
        shortest_line().

        Parameters:
        -----------
        other : Geometry
            The other geometry to find the nearest points to

        Returns:
        --------
        tuple
            A tuple of (x1, y1, x2, y2) representing coordinates of the two
            nearest points

        Raises:
        -------
        RuntimeError
            If GEOS operations fail
        """
        cdef GEOSContextHandle_t ctx = GEOS_init_r()
        if ctx == NULL:
            raise RuntimeError("Failed to initialize GEOS context")

        cdef GEOSGeometry *g1_geos = tg_geom_to_geos(ctx, self.geom)
        if g1_geos == NULL:
            GEOS_finish_r(ctx)
            raise RuntimeError("Failed to convert first TG geometry to GEOS")

        cdef GEOSGeometry *g2_geos = tg_geom_to_geos(ctx, other.geom)
        if g2_geos == NULL:
            GEOSGeom_destroy_r(ctx, g1_geos)
            GEOS_finish_r(ctx)
            raise RuntimeError("Failed to convert second TG geometry to GEOS")

        cdef GEOSCoordSequence *coords = GEOSNearestPoints_r(ctx, g1_geos, g2_geos)
        if coords == NULL:
            GEOSGeom_destroy_r(ctx, g2_geos)
            GEOSGeom_destroy_r(ctx, g1_geos)
            GEOS_finish_r(ctx)
            raise RuntimeError("GEOSNearestPoints failed")

        # Extract the two coordinates directly (GEOS always returns exactly 2 points)
        cdef double x1, y1, x2, y2
        cdef int ret = GEOSCoordSeq_getXY_r(ctx, coords, 0, &x1, &y1)
        if ret == -1:
            GEOSCoordSeq_destroy_r(ctx, coords)
            GEOSGeom_destroy_r(ctx, g2_geos)
            GEOSGeom_destroy_r(ctx, g1_geos)
            GEOS_finish_r(ctx)
            raise RuntimeError("Failed to get first coordinate")

        ret = GEOSCoordSeq_getXY_r(ctx, coords, 1, &x2, &y2)
        if ret == -1:
            GEOSCoordSeq_destroy_r(ctx, coords)
            GEOSGeom_destroy_r(ctx, g2_geos)
            GEOSGeom_destroy_r(ctx, g1_geos)
            GEOS_finish_r(ctx)
            raise RuntimeError("Failed to get second coordinate")

        # Clean up GEOS resources
        GEOSCoordSeq_destroy_r(ctx, coords)
        GEOSGeom_destroy_r(ctx, g2_geos)
        GEOSGeom_destroy_r(ctx, g1_geos)
        GEOS_finish_r(ctx)

        return (x1, y1, x2, y2)

    def nearest_points(self, other) -> tuple:
        """
        Return a tuple of the nearest points between two geometries.

        Returns a tuple of two Point objects: (point_from_self, point_from_other).
        The first point is the nearest point in this geometry to the other geometry,
        and the second point is the nearest point in the other geometry to this geometry.

        This method is compatible with Shapely's nearest_points function.

        Parameters:
        -----------
        other : Geometry
            The other geometry to find the nearest point to

        Returns:
        --------
        tuple
            A tuple of (Point, Point) representing the nearest points between the two geometries

        Raises:
        -------
        ValueError
            If the operation fails
        """
        if other is None or not isinstance(other, Geometry):
            raise ValueError("other must be a Geometry object")

        # Use helper method to get coordinates
        cdef double x1, y1, x2, y2
        x1, y1, x2, y2 = self._get_nearest_point_coords(<Geometry>other)

        # Create Point objects efficiently using __new__ to avoid __init__ overhead
        cdef Point pt1 = Point.__new__(Point)
        pt1.pt.x = x1
        pt1.pt.y = y1

        cdef Point pt2 = Point.__new__(Point)
        pt2.pt.x = x2
        pt2.pt.y = y2

        return (pt1, pt2)

    def shortest_line(self, other):
        """
        Return the shortest LineString connecting two geometries.

        This is the line connecting the nearest points between two geometries.
        This method is compatible with Shapely v2's shortest_line.

        Parameters:
        -----------
        other : Geometry
            The other geometry to find the shortest line to

        Returns:
        --------
        Line
            A LineString (Line) connecting the two nearest points

        Raises:
        -------
        ValueError
            If the operation fails
        """
        if other is None or not isinstance(other, Geometry):
            raise ValueError("other must be a Geometry object")

        # Use helper method to get coordinates
        cdef double x1, y1, x2, y2
        x1, y1, x2, y2 = self._get_nearest_point_coords(<Geometry>other)

        # Create Line directly from coordinates using tg_line_new
        cdef tg_point *pts = <tg_point *>malloc(2 * sizeof(tg_point))
        if not pts:
            raise MemoryError("Failed to allocate points for Line")

        pts[0].x = x1
        pts[0].y = y1
        pts[1].x = x2
        pts[1].y = y2

        cdef tg_line *line_ptr = tg_line_new(pts, 2)
        free(pts)

        if not line_ptr:
            raise ValueError("Failed to create Line")

        # Create Line object and set ownership
        cdef Line result = Line.__new__(Line)
        result.line = line_ptr
        result.owns_pointer = True
        return result


cdef class Point:
    cdef tg_point pt
    cdef object _cached_geometry

    def __init__(self, x: float, y: float):
        self.pt.x = x
        self.pt.y = y
        self._cached_geometry = None

    def __str__(self):
        return f"Point({self.pt.x}, {self.pt.y})"

    def __repr__(self):
        return self.__str__()

    @property
    def x(self) -> float:
        return self.pt.x

    @property
    def y(self) -> float:
        return self.pt.y

    def as_tuple(self) -> tuple:
        return (self.pt.x, self.pt.y)

    cdef tg_point _get_c_point(self) noexcept:
        return self.pt

    def as_geometry(self) -> Geometry:
        # Cache geometry result since Point is immutable
        if self._cached_geometry is None:
            self._cached_geometry = self._as_geometry()
        return self._cached_geometry

    cdef Geometry _as_geometry(self):
        return _geometry_from_ptr(tg_geom_new_point(self.pt))

    # Shapely-compatible properties
    @property
    def geom_type(self) -> str:
        """Returns 'Point' for Shapely compatibility"""
        return "Point"

    @property
    def coords(self) -> list:
        """Returns coordinate sequence for Shapely compatibility"""
        return [(self.pt.x, self.pt.y)]

    @property
    def bounds(self) -> tuple:
        """Returns (minx, miny, maxx, maxy) for Shapely compatibility"""
        return (self.pt.x, self.pt.y, self.pt.x, self.pt.y)

    @property
    def is_empty(self) -> bool:
        """Always False for non-null Point"""
        return False

    @property
    def is_valid(self) -> bool:
        """A Point is always valid."""
        return True

    @property
    def wkt(self) -> str:
        """Returns WKT representation"""
        return self.as_geometry().to_wkt()

    @property
    def wkb(self) -> bytes:
        """Returns WKB representation"""
        return self.as_geometry().to_wkb()

    @property
    def __geo_interface__(self) -> dict:
        """Returns GeoJSON-like dict for Shapely compatibility"""
        return {"type": "Point", "coordinates": [self.pt.x, self.pt.y]}

    def buffer(self, distance: float, quad_segs: int = 16,
               cap_style: int = 1, join_style: int = 1,
               mitre_limit: float = 5.0) -> Geometry:
        """
        Return a geometry that is this Point buffered by the given distance.
        This creates a circular polygon around the point.

        Parameters:
        -----------
        distance : float
            The buffer distance (radius) in the geometry's units
        quad_segs : int
            Number of segments per quadrant (default: 16). Higher values = smoother circle.
        cap_style : int
            End cap style: 1=round (default), 2=flat, 3=square
        join_style : int
            Join style: 1=round (default), 2=mitre, 3=bevel
        mitre_limit : float
            Mitre ratio limit for joins (default: 5.0)

        Returns:
        --------
        Geometry
            A new Geometry representing the buffered point (as a polygon)
        """
        return self.as_geometry().buffer(distance, quad_segs, cap_style, join_style, mitre_limit)

    def simplify(self, tolerance: float, preserve_topology: bool = True) -> Geometry:
        """
        Return a simplified geometry produced by the Douglas-Peucker algorithm.

        Parameters:
        -----------
        tolerance : float
            The tolerance distance. Coordinates of the simplified geometry will be no more
            than the tolerance distance from the original.
        preserve_topology : bool
            If True (default), use topology-preserving simplification.
            If False, use the standard Douglas-Peucker algorithm.

        Returns:
        --------
        Geometry
            A new Geometry representing the simplified shape
        """
        return self.as_geometry().simplify(tolerance, preserve_topology)

    def nearest_points(self, other) -> tuple:
        """
        Return a tuple of the nearest points between this point and another geometry.

        Returns a tuple of two Point objects: (point_from_self, point_from_other).

        Parameters:
        -----------
        other : Geometry, Point, LineString, Polygon, or other geometry
            The other geometry to find the nearest point to

        Returns:
        --------
        tuple
            A tuple of (Point, Point) representing the nearest points between the two geometries

        Raises:
        -------
        ValueError
            If other is None or not a valid geometry
        """
        if other is None:
            raise ValueError("other must be a Geometry object, not None")

        if isinstance(other, Geometry):
            return self.as_geometry().nearest_points(other)
        elif hasattr(other, "as_geometry"):
            # Assume it's another geometry type with as_geometry method
            return self.as_geometry().nearest_points(other.as_geometry())
        raise ValueError(f"other must be a Geometry object, got {type(other)}")

    def shortest_line(self, other):
        """
        Return the shortest LineString connecting this point to another geometry.

        This is the line connecting the nearest points between two geometries.
        This method is compatible with Shapely v2's shortest_line.

        Parameters:
        -----------
        other : Geometry, Point, LineString, Polygon, or other geometry
            The other geometry to find the shortest line to

        Returns:
        --------
        Line
            A LineString (Line) connecting the two nearest points

        Raises:
        -------
        ValueError
            If other is None or not a valid geometry
        """
        if other is None:
            raise ValueError("other must be a Geometry object, not None")

        if isinstance(other, Geometry):
            return self.as_geometry().shortest_line(other)
        elif hasattr(other, "as_geometry"):
            return self.as_geometry().shortest_line(other.as_geometry())
        raise ValueError(f"other must be a Geometry object, got {type(other)}")

    @property
    def centroid(self) -> Geometry:
        """
        Return the centroid of the point (which is the point itself).

        Returns:
        --------
        Geometry
            A Point geometry representing the centroid
        """
        return self.as_geometry().centroid

    @property
    def convex_hull(self) -> Geometry:
        """
        Return the convex hull of the point (which is the point itself).

        Returns:
        --------
        Geometry
            A Point geometry representing the convex hull
        """
        return self.as_geometry().convex_hull

    def intersection(self, other) -> Geometry:
        """
        Return the geometric intersection of this point with another geometry.

        The intersection is the set of points common to both geometries.
        This method is compatible with Shapely's intersection.

        Parameters:
        -----------
        other : Geometry, Point, LineString, Polygon, or other geometry
            The other geometry to compute the intersection with

        Returns:
        --------
        Geometry
            A Geometry representing the intersection. May be empty if geometries
            do not intersect.

        Examples:
        ---------
        >>> from togo import Point, LineString
        >>> p = Point(1, 1)
        >>> line = LineString([(1, 1), (2, 2)])
        >>> result = p.intersection(line)
        >>> print(result.geom_type)
        Point
        """
        cdef tg_geom *empty

        if other is None:
            # Return empty geometry (Shapely-compatible)
            empty = tg_geom_new_geometrycollection_empty()
            return _geometry_from_ptr(empty)

        if isinstance(other, Geometry):
            return self.as_geometry().intersection(other)
        elif hasattr(other, "as_geometry"):
            return self.as_geometry().intersection(other.as_geometry())

        # Return empty for unrecognized types (Shapely-compatible)
        empty = tg_geom_new_geometrycollection_empty()
        return _geometry_from_ptr(empty)


cdef class Rect:
    cdef tg_rect rect
    cdef object _cached_geometry

    def __init__(self, min_pt: Point, max_pt: Point):
        self.rect.min = min_pt.pt
        self.rect.max = max_pt.pt
        self._cached_geometry = None

    def __str__(self):
        return (
            f"Rect(min=({self.rect.min.x}, {self.rect.min.y}), "
            f"max=({self.rect.max.x}, {self.rect.max.y}))"
        )

    def __repr__(self):
        return self.__str__()

    @property
    def min(self) -> Point:
        return Point(self.rect.min.x, self.rect.min.y)

    @property
    def max(self) -> Point:
        return Point(self.rect.max.x, self.rect.max.y)

    def center(self) -> Point:
        cdef tg_point c = tg_rect_center(self.rect)
        return Point(c.x, c.y)

    cdef tg_rect _get_c_rect(self) noexcept:
        return self.rect

    def expand(self, other) -> Rect:
        cdef tg_rect r
        if isinstance(other, Rect):
            r = tg_rect_expand(self.rect, (<Rect>other)._get_c_rect())
            return Rect(Point(r.min.x, r.min.y), Point(r.max.x, r.max.y))
        elif isinstance(other, Point):
            r = tg_rect_expand_point(self.rect, (<Point>other)._get_c_point())
            return Rect(Point(r.min.x, r.min.y), Point(r.max.x, r.max.y))
        else:
            raise TypeError("expand expects Rect or Point")

    def intersects(self, other) -> bool:
        if isinstance(other, Rect):
            return tg_rect_intersects_rect(
                self.rect, (<Rect>other)._get_c_rect()
            )
        elif isinstance(other, Point):
            return tg_rect_intersects_point(
                self.rect, (<Point>other)._get_c_point()
            )
        else:
            raise TypeError("intersects expects Rect or Point")

    def as_geometry(self) -> Geometry:
        # Cache geometry result since Rect is immutable
        if self._cached_geometry is None:
            self._cached_geometry = self._as_geometry()
        return self._cached_geometry

    cdef Geometry _as_geometry(self):
        minx, miny = self.rect.min.x, self.rect.min.y
        maxx, maxy = self.rect.max.x, self.rect.max.y
        corners = [
            (minx, miny),
            (maxx, miny),
            (maxx, maxy),
            (minx, maxy),
            (minx, miny)
        ]
        ring = Ring(corners)
        poly = Poly(ring)
        return _geometry_from_ptr(tg_geom_new_polygon(poly.poly))


cdef class Ring:
    cdef tg_ring *ring
    cdef bint owns_pointer
    cdef object _cached_geometry

    def __init__(self, points):
        cdef int n = len(points)
        cdef int i
        cdef tg_point *pts = <tg_point *>malloc(n * sizeof(tg_point))
        if not pts:
            raise MemoryError("Failed to allocate points for Ring")
        for i in range(n):
            pts[i].x = points[i][0]
            pts[i].y = points[i][1]
        self.ring = tg_ring_new(pts, n)
        free(pts)
        if not self.ring:
            raise ValueError("Failed to create Ring")
        self.owns_pointer = True
        self._cached_geometry = None

    def __str__(self):
        try:
            n = tg_ring_num_points(self.ring)
            pts = tg_ring_points(self.ring)
            pypts = [(pts[i].x, pts[i].y) for i in range(n)]
            return f"Ring(n={n}, points={pypts})"
        except Exception:
            return "Ring(<unavailable>)"

    def __repr__(self):
        return self.__str__()

    @staticmethod
    cdef Ring from_ptr(tg_ring *ptr):
        cdef Ring r = Ring.__new__(Ring)
        r.ring = ptr
        r.owns_pointer = False  # Don't free this pointer
        return r

    cdef tg_ring *_get_c_ring(self) noexcept:
        return self.ring

    def __dealloc__(self):
        if self.ring and self.owns_pointer:
            tg_ring_free(self.ring)

    @property
    def num_points(self) -> int:
        return tg_ring_num_points(self.ring)

    def points(self, as_tuples=False) -> list[tuple] | list[Point]:
        cdef int n = tg_ring_num_points(self.ring)
        cdef const tg_point *pts = tg_ring_points(self.ring)
        if as_tuples:
            return [(pts[i].x, pts[i].y) for i in range(n)]
        else:
            return [Point(pts[i].x, pts[i].y) for i in range(n)]

    @property
    def area(self) -> float:
        return tg_ring_area(self.ring)

    @property
    def length(self) -> float:
        return tg_ring_perimeter(self.ring)

    def rect(self) -> Rect:
        cdef tg_rect r = tg_ring_rect(self.ring)
        return Rect(Point(r.min.x, r.min.y), Point(r.max.x, r.max.y))

    @property
    def is_convex(self) -> bool:
        return tg_ring_convex(self.ring)

    @property
    def is_clockwise(self) -> bool:
        return tg_ring_clockwise(self.ring)

    def as_geometry(self) -> Geometry:
        # Cache geometry result since Ring is immutable
        if self._cached_geometry is None:
            self._cached_geometry = self._as_geometry()
        return self._cached_geometry

    cdef Geometry _as_geometry(self):
        cdef tg_poly *p = tg_poly_new(self.ring, NULL, 0)
        if not p:
            raise ValueError("Failed to create Poly from Ring")
        cdef tg_geom *g = tg_geom_new_polygon(<const tg_poly *>p)
        tg_poly_free(p)
        if not g:
            raise ValueError("Failed to create Geometry from Ring")
        return _geometry_from_ptr(g)

    def as_poly(self) -> Poly:
        # Build a new Poly object from this Ring
        return Poly(self)

    # Shapely-compatible properties
    @property
    def coords(self):
        """Returns coordinate sequence for Shapely compatibility"""
        return self.points(as_tuples=True)

    @property
    def is_empty(self):
        """Check if Ring is empty"""
        return tg_ring_num_points(self.ring) == 0

    @property
    def is_valid(self):
        """A Ring is always valid."""
        return True

    def buffer(self, distance: float, quad_segs: int = 16,
               cap_style: int = 1, join_style: int = 1,
               mitre_limit: float = 5.0) -> Geometry:
        """
        Return a geometry that is this Ring buffered by the given distance.

        Parameters:
        -----------
        distance : float
            The buffer distance in the geometry's units. Positive = outward, negative = inward
        quad_segs : int
            Number of segments per quadrant (default: 16). Higher values = smoother buffer.
        cap_style : int
            End cap style: 1=round (default), 2=flat, 3=square
        join_style : int
            Join style: 1=round (default), 2=mitre, 3=bevel
        mitre_limit : float
            Mitre ratio limit for joins (default: 5.0)

        Returns:
        --------
        Geometry
            A new Geometry representing the buffered ring
        """
        return self.as_geometry().buffer(distance, quad_segs, cap_style, join_style, mitre_limit)

    def simplify(self, tolerance: float, preserve_topology: bool = True) -> Geometry:
        """
        Return a simplified geometry produced by the Douglas-Peucker algorithm.

        Parameters:
        -----------
        tolerance : float
            The tolerance distance. Coordinates of the simplified geometry will be no more
            than the tolerance distance from the original.
        preserve_topology : bool
            If True (default), use topology-preserving simplification.
            If False, use the standard Douglas-Peucker algorithm.

        Returns:
        --------
        Geometry
            A new Geometry representing the simplified shape
        """
        return self.as_geometry().simplify(tolerance, preserve_topology)

    def nearest_points(self, other) -> tuple:
        """
        Return a tuple of the nearest points between this ring and another geometry.

        Returns a tuple of two Point objects: (point_from_self, point_from_other).

        Parameters:
        -----------
        other : Geometry, Point, LineString, Polygon, or other geometry
            The other geometry to find the nearest point to

        Returns:
        --------
        tuple
            A tuple of (Point, Point) representing the nearest points between the two
            geometries

        Raises:
        -------
        ValueError
            If other is None or not a valid geometry
        """
        if other is None:
            raise ValueError("other must be a Geometry object, not None")

        if isinstance(other, Geometry):
            return self.as_geometry().nearest_points(other)
        elif hasattr(other, "as_geometry"):
            # Assume it's another geometry type with as_geometry method
            return self.as_geometry().nearest_points(other.as_geometry())
        else:
            raise ValueError(f"other must be a Geometry object, got {type(other)}")

    def shortest_line(self, other):
        """
        Return the shortest LineString connecting this ring to another geometry.

        This is the line connecting the nearest points between two geometries.
        This method is compatible with Shapely v2's shortest_line.

        Parameters:
        -----------
        other : Geometry, Point, LineString, Polygon, or other geometry
            The other geometry to find the shortest line to

        Returns:
        --------
        Line
            A LineString (Line) connecting the two nearest points

        Raises:
        -------
        ValueError
            If other is None or not a valid geometry
        """
        if other is None:
            raise ValueError("other must be a Geometry object, not None")

        if isinstance(other, Geometry):
            return self.as_geometry().shortest_line(other)
        elif hasattr(other, "as_geometry"):
            return self.as_geometry().shortest_line(other.as_geometry())
        else:
            raise ValueError(f"other must be a Geometry object, got {type(other)}")

    @property
    def centroid(self) -> Geometry:
        """
        Return the centroid of the ring.

        Returns:
        --------
        Geometry
            A Point geometry representing the centroid
        """
        return self.as_geometry().centroid

    @property
    def convex_hull(self) -> Geometry:
        """
        Return the convex hull of the ring.

        Returns:
        --------
        Geometry
            A Polygon geometry representing the convex hull
        """
        return self.as_geometry().convex_hull

    def intersection(self, other) -> Geometry:
        """
        Return the geometric intersection of this ring with another geometry.

        The intersection is the set of points common to both geometries.
        This method is compatible with Shapely's intersection.

        Parameters:
        -----------
        other : Geometry, Point, Line, Ring, Poly, or other geometry
            The other geometry to compute the intersection with

        Returns:
        --------
        Geometry
            A Geometry representing the intersection. May be empty if geometries
            do not intersect.

        Examples:
        ---------
        >>> from togo import Ring, Point
        >>> ring = Ring([(0, 0), (4, 0), (4, 4), (0, 4), (0, 0)])
        >>> point = Point(2, 2)
        >>> result = ring.intersection(point.as_geometry())
        >>> print(result.geom_type)
        Point
        """
        cdef tg_geom *empty

        if other is None:
            # Return empty geometry (Shapely-compatible)
            empty = tg_geom_new_geometrycollection_empty()
            return _geometry_from_ptr(empty)

        if isinstance(other, Geometry):
            return self.as_geometry().intersection(other)
        elif hasattr(other, "as_geometry"):
            return self.as_geometry().intersection(other.as_geometry())

        # Return empty for unrecognized types (Shapely-compatible)
        empty = tg_geom_new_geometrycollection_empty()
        return _geometry_from_ptr(empty)


cdef class Line:
    cdef tg_line *line
    cdef bint owns_pointer
    cdef object _cached_geometry

    def __init__(self, points):
        cdef int n = len(points)
        cdef int i
        cdef tg_point *pts = <tg_point *>malloc(n * sizeof(tg_point))
        if not pts:
            raise MemoryError("Failed to allocate points for Line")
        for i in range(n):
            pts[i].x = points[i][0]
            pts[i].y = points[i][1]
        self.line = tg_line_new(pts, n)
        free(pts)
        if not self.line:
            raise ValueError("Failed to create Line")
        self.owns_pointer = True
        self._cached_geometry = None

    def __dealloc__(self):
        if self.line and self.owns_pointer:
            tg_line_free(self.line)

    def __str__(self):
        try:
            n = tg_line_num_points(self.line)
            pts = tg_line_points(self.line)
            pypts = [(pts[i].x, pts[i].y) for i in range(n)]
            return f"Line(n={n}, points={pypts})"
        except Exception:
            return "Line(<unavailable>)"

    def __repr__(self):
        return self.__str__()

    @property
    def num_points(self) -> int:
        return tg_line_num_points(self.line)

    def points(self, as_tuples=False) -> list[tuple] | list[Point]:
        cdef int n = tg_line_num_points(self.line)
        cdef const tg_point *pts = tg_line_points(self.line)
        if as_tuples:
            return [(pts[i].x, pts[i].y) for i in range(n)]
        else:
            return [Point(pts[i].x, pts[i].y) for i in range(n)]

    @property
    def length(self) -> float:
        return tg_line_length(self.line)

    def rect(self) -> Rect:
        cdef tg_rect r = tg_line_rect(self.line)
        return Rect(Point(r.min.x, r.min.y), Point(r.max.x, r.max.y))

    def is_clockwise(self) -> bool:
        return tg_line_clockwise(self.line)

    def as_geometry(self) -> Geometry:
        # Cache geometry result since Line is immutable
        if self._cached_geometry is None:
            self._cached_geometry = self._as_geometry()
        return self._cached_geometry

    cdef Geometry _as_geometry(self):
        cdef tg_geom *g = tg_geom_new_linestring(self.line)
        if not g:
            raise ValueError("Failed to create Geometry from LineString")
        return _geometry_from_ptr(g)

    cdef tg_line *_get_c_line(self) noexcept:
        return self.line

    def __getitem__(self, idx: int) -> Point:
        n = self.num_points
        if not (0 <= idx < n):
            raise IndexError("Line index out of range")
        cdef tg_point pt = tg_line_point_at(self.line, idx)
        return Point(pt.x, pt.y)

    # Shapely-compatible properties
    @property
    def geom_type(self) -> str:
        """Returns 'LineString' for Shapely compatibility"""
        return "LineString"

    @property
    def coords(self) -> list:
        """Returns coordinate sequence for Shapely compatibility"""
        return self.points(as_tuples=True)

    @property
    def bounds(self) -> tuple:
        """Returns (minx, miny, maxx, maxy) for Shapely compatibility"""
        cdef tg_rect r = tg_line_rect(self.line)
        return (r.min.x, r.min.y, r.max.x, r.max.y)

    @property
    def is_empty(self) -> bool:
        """Check if LineString is empty"""
        return tg_line_num_points(self.line) == 0

    @property
    def is_valid(self) -> bool:
        """A LineString is always valid."""
        return True

    @property
    def wkt(self) -> str:
        """Returns WKT representation"""
        return self.as_geometry().to_wkt()

    @property
    def wkb(self) -> bytes:
        """Returns WKB representation"""
        return self.as_geometry().to_wkb()

    @property
    def __geo_interface__(self) -> dict:
        """Returns GeoJSON-like dict for Shapely compatibility"""
        return {"type": "LineString", "coordinates": self.points(as_tuples=True)}

    def buffer(self, distance: float, quad_segs: int = 16,
               cap_style: int = 1, join_style: int = 1,
               mitre_limit: float = 5.0) -> Geometry:
        """
        Return a geometry that is this LineString buffered by the given distance.

        Parameters:
        -----------
        distance : float
            The buffer distance in the geometry's units
        quad_segs : int
            Number of segments per quadrant (default: 16). Higher values = smoother buffer.
        cap_style : int
            End cap style: 1=round (default), 2=flat, 3=square
        join_style : int
            Join style: 1=round (default), 2=mitre, 3=bevel
        mitre_limit : float
            Mitre ratio limit for joins (default: 5.0)

        Returns:
        --------
        Geometry
            A new Geometry representing the buffered line
        """
        return self.as_geometry().buffer(distance, quad_segs, cap_style, join_style, mitre_limit)

    def simplify(self, tolerance: float, preserve_topology: bool = True) -> Geometry:
        """
        Return a simplified geometry produced by the Douglas-Peucker algorithm.

        Parameters:
        -----------
        tolerance : float
            The tolerance distance. Coordinates of the simplified geometry will be no more
            than the tolerance distance from the original.
        preserve_topology : bool
            If True (default), use topology-preserving simplification.
            If False, use the standard Douglas-Peucker algorithm.

        Returns:
        --------
        Geometry
            A new Geometry representing the simplified shape
        """
        return self.as_geometry().simplify(tolerance, preserve_topology)

    def nearest_points(self, other) -> tuple:
        """
        Return a tuple of the nearest points between this line and another geometry.

        Returns a tuple of two Point objects: (point_from_self, point_from_other).

        Parameters:
        -----------
        other : Geometry, Point, Line, Ring, Poly, or other geometry
            The other geometry to find the nearest point to

        Returns:
        --------
        tuple
            A tuple of (Point, Point) representing the nearest points between the two geometries

        Raises:
        -------
        ValueError
            If other is None or not a valid geometry
        """
        if other is None:
            raise ValueError("other must be a Geometry object, not None")

        if isinstance(other, Geometry):
            return self.as_geometry().nearest_points(other)
        elif hasattr(other, "as_geometry"):
            return self.as_geometry().nearest_points(other.as_geometry())
        raise ValueError(f"other must be a Geometry object, got {type(other)}")

    def shortest_line(self, other):
        """
        Return the shortest LineString connecting this line to another geometry.

        This is the line connecting the nearest points between two geometries.
        This method is compatible with Shapely v2's shortest_line.

        Parameters:
        -----------
        other : Geometry, Point, Line, Ring, Poly, or other geometry
            The other geometry to find the shortest line to

        Returns:
        --------
        Line
            A LineString (Line) connecting the two nearest points

        Raises:
        -------
        ValueError
            If other is None or not a valid geometry
        """
        if other is None:
            raise ValueError("other must be a Geometry object, not None")

        if isinstance(other, Geometry):
            return self.as_geometry().shortest_line(other)
        elif hasattr(other, "as_geometry"):
            return self.as_geometry().shortest_line(other.as_geometry())
        else:
            raise ValueError(f"other must be a Geometry object, got {type(other)}")

    @property
    def centroid(self) -> Geometry:
        """
        Return the centroid of the linestring.

        Returns:
        --------
        Geometry
            A Point geometry representing the centroid
        """
        return self.as_geometry().centroid

    @property
    def convex_hull(self) -> Geometry:
        """
        Return the convex hull of the linestring.

        Returns:
        --------
        Geometry
            A Polygon (or LineString for collinear points) representing the convex hull
        """
        return self.as_geometry().convex_hull

    def intersection(self, other) -> Geometry:
        """
        Return the geometric intersection of this linestring with another geometry.

        The intersection is the set of points common to both geometries.
        This method is compatible with Shapely's intersection.

        Parameters:
        -----------
        other : Geometry, Point, Line, Ring, Poly, or other geometry
            The other geometry to compute the intersection with

        Returns:
        --------
        Geometry
            A Geometry representing the intersection. May be empty if geometries
            do not intersect.

        Examples:
        ---------
        >>> from togo import LineString, Polygon
        >>> line = LineString([(0, 0), (2, 2)])
        >>> poly = Polygon([(1, 0), (3, 0), (3, 2), (1, 2), (1, 0)])
        >>> result = line.intersection(poly)
        >>> print(result.geom_type)
        LineString
        """
        cdef tg_geom *empty

        if other is None:
            # Return empty geometry (Shapely-compatible)
            empty = tg_geom_new_geometrycollection_empty()
            return _geometry_from_ptr(empty)

        if isinstance(other, Geometry):
            return self.as_geometry().intersection(other)
        elif hasattr(other, "as_geometry"):
            return self.as_geometry().intersection(other.as_geometry())

        # Return empty for unrecognized types (Shapely-compatible)
        empty = tg_geom_new_geometrycollection_empty()
        return _geometry_from_ptr(empty)


cdef class Poly:
    cdef tg_poly *poly
    cdef bint owns_pointer
    cdef object _cached_geometry

    def __init__(self, exterior, holes=None):
        cdef int nholes = 0
        cdef int i
        cdef tg_ring **hole_ptrs = NULL
        cdef tg_ring **holes_arr = NULL
        cdef tg_ring *ext_ring
        cdef tg_ring *hole_ptr
        if not isinstance(exterior, Ring):
            raise TypeError("exterior must be a Ring")
        ext_ring = (<Ring>exterior)._get_c_ring()
        if ext_ring == NULL:
            raise ValueError("exterior Ring is not initialized")
        # Handle holes
        if holes is None or len(holes) == 0:
            nholes = 0
            holes_arr = NULL
        else:
            nholes = len(holes)
            hole_ptrs = <tg_ring **>malloc(nholes * sizeof(tg_ring *))
            if not hole_ptrs:
                raise MemoryError("Failed to allocate holes array")
            for i in range(nholes):
                if not isinstance(holes[i], Ring):
                    free(hole_ptrs)
                    raise TypeError("holes must be a list of Ring")
                hole_ptr = (<Ring>holes[i])._get_c_ring()
                if hole_ptr == NULL:
                    free(hole_ptrs)
                    raise ValueError(f"hole {i} Ring is not initialized")
                hole_ptrs[i] = hole_ptr
            holes_arr = hole_ptrs
        self.poly = tg_poly_new(ext_ring, <const tg_ring * const *>holes_arr, nholes)
        if hole_ptrs != NULL:
            free(hole_ptrs)
        if not self.poly:
            raise ValueError("Failed to create Poly")
        self.owns_pointer = True
        self._cached_geometry = None

    def __dealloc__(self):
        if self.poly and self.owns_pointer:
            tg_poly_free(self.poly)

    def __str__(self):
        try:
            ext_n = tg_poly_num_holes(self.poly)  # temporarily store holes count
            # rect
            r = tg_poly_rect(self.poly)
            rect_str = f"(({r.min.x}, {r.min.y}), ({r.max.x}, {r.max.y}))"
            holes_n = ext_n
            return f"Poly(holes={holes_n}, rect={rect_str})"
        except Exception:
            return "Poly(<unavailable>)"

    def __repr__(self):
        return self.__str__()

    @property
    def exterior(self) -> Ring:
        cdef const tg_ring *ext = tg_poly_exterior(self.poly)
        return Ring.from_ptr(<tg_ring *>ext)

    def num_holes(self) -> int:
        return tg_poly_num_holes(self.poly)

    @staticmethod
    cdef Poly _from_c_poly(tg_poly *ptr):
        cdef Poly poly = Poly.__new__(Poly)
        poly.poly = ptr
        poly.owns_pointer = False
        return poly

    def hole(self, idx: int) -> Ring:
        cdef const tg_ring *h = tg_poly_hole_at(self.poly, idx)
        return Ring.from_ptr(<tg_ring *>h)

    def rect(self) -> Rect:
        cdef tg_rect r = tg_poly_rect(self.poly)
        return Rect(Point(r.min.x, r.min.y), Point(r.max.x, r.max.y))

    def is_clockwise(self) -> bool:
        return tg_poly_clockwise(self.poly)

    def as_geometry(self) -> Geometry:
        # Cache geometry result since Poly is immutable
        if self._cached_geometry is None:
            self._cached_geometry = self._as_geometry()
        return self._cached_geometry

    cdef Geometry _as_geometry(self):
        cdef tg_geom *g = tg_geom_new_polygon(self.poly)
        if not g:
            raise ValueError("Failed to create Geometry from Polygon")
        return _geometry_from_ptr(g)

    cdef tg_poly *_get_c_poly(self) noexcept:
        return self.poly

    # Shapely-compatible properties
    @property
    def geom_type(self) -> str:
        """Returns 'Polygon' for Shapely compatibility"""
        return "Polygon"

    @property
    def bounds(self) -> tuple:
        """Returns (minx, miny, maxx, maxy) for Shapely compatibility"""
        cdef tg_rect r = tg_poly_rect(self.poly)
        return (r.min.x, r.min.y, r.max.x, r.max.y)

    @property
    def area(self) -> float:
        """Returns the area of the polygon"""
        return tg_ring_area(tg_poly_exterior(self.poly))

    @property
    def length(self) -> float:
        """Returns the perimeter (length of exterior ring) for Shapely compatibility"""
        return tg_ring_perimeter(tg_poly_exterior(self.poly))

    @property
    def is_empty(self) -> bool:
        """Check if Polygon is empty"""
        cdef const tg_ring *ext = tg_poly_exterior(self.poly)
        return tg_ring_num_points(ext) == 0

    @property
    def is_valid(self) -> bool:
        """Check if the polygon is valid using GEOS.

        A polygon is valid if it satisfies geometric constraints,
        such as proper ring orientation and no self-intersections.
        """
        cdef GEOSContextHandle_t ctx = GEOS_init_r()
        if ctx == NULL:
            raise RuntimeError("Failed to initialize GEOS context")

        cdef tg_geom *g_tg = tg_geom_new_polygon(self.poly)
        if not g_tg:
            GEOS_finish_r(ctx)
            raise RuntimeError("Failed to create geometry from polygon")

        cdef GEOSGeometry *g_geos = tg_geom_to_geos(ctx, g_tg)
        tg_geom_free(g_tg)
        if g_geos == NULL:
            GEOS_finish_r(ctx)
            raise RuntimeError("Failed to convert TG geometry to GEOS")

        cdef char result = GEOSisValid_r(ctx, g_geos)
        GEOSGeom_destroy_r(ctx, g_geos)
        GEOS_finish_r(ctx)

        return result == 1

    @property
    def wkt(self) -> str:
        """Returns WKT representation"""
        return self.as_geometry().to_wkt()

    @property
    def wkb(self) -> bytes:
        """Returns WKB representation"""
        return self.as_geometry().to_wkb()

    @property
    def interiors(self) -> list:
        """Returns list of holes for Shapely compatibility"""
        return [self.hole(i) for i in range(self.num_holes())]

    @property
    def __geo_interface__(self) -> dict:
        """Returns GeoJSON-like dict for Shapely compatibility"""
        ext_coords = self.exterior.points(as_tuples=True)
        if self.num_holes() == 0:
            return {"type": "Polygon", "coordinates": [ext_coords]}
        else:
            hole_coords = [self.hole(i).points(as_tuples=True) for i in range(self.num_holes())]
            return {"type": "Polygon", "coordinates": [ext_coords] + hole_coords}

    def buffer(self, distance: float, quad_segs: int = 16,
               cap_style: int = 1, join_style: int = 1,
               mitre_limit: float = 5.0) -> Geometry:
        """
        Return a geometry that is this Polygon buffered by the given distance.

        Parameters:
        -----------
        distance : float
            The buffer distance in the geometry's units. Positive = outward, negative = inward
        quad_segs : int
            Number of segments per quadrant (default: 16). Higher values = smoother buffer.
        cap_style : int
            End cap style: 1=round (default), 2=flat, 3=square
        join_style : int
            Join style: 1=round (default), 2=mitre, 3=bevel
        mitre_limit : float
            Mitre ratio limit for joins (default: 5.0)

        Returns:
        --------
        Geometry
            A new Geometry representing the buffered polygon
        """
        return self.as_geometry().buffer(distance, quad_segs, cap_style, join_style, mitre_limit)

    def simplify(self, tolerance: float, preserve_topology: bool = True) -> Geometry:
        """
        Return a simplified geometry produced by the Douglas-Peucker algorithm.

        Parameters:
        -----------
        tolerance : float
            The tolerance distance. Coordinates of the simplified geometry will be no more
            than the tolerance distance from the original.
        preserve_topology : bool
            If True (default), use topology-preserving simplification.
            If False, use the standard Douglas-Peucker algorithm.

        Returns:
        --------
        Geometry
            A new Geometry representing the simplified shape
        """
        return self.as_geometry().simplify(tolerance, preserve_topology)

    def nearest_points(self, other) -> tuple:
        """
        Return a tuple of the nearest points between this polygon and another geometry.

        Returns a tuple of two Point objects: (point_from_self, point_from_other).

        Parameters:
        -----------
        other : Geometry, Point, LineString, Polygon, or other geometry
            The other geometry to find the nearest point to

        Returns:
        --------
        tuple
            A tuple of (Point, Point) representing the nearest points between the two geometries

        Raises:
        -------
        ValueError
            If other is None or not a valid geometry
        """
        if other is None:
            raise ValueError("other must be a Geometry object, not None")

        if isinstance(other, Geometry):
            return self.as_geometry().nearest_points(other)
        elif hasattr(other, "as_geometry"):
            # Assume it's another geometry type with as_geometry method
            return self.as_geometry().nearest_points(other.as_geometry())
        else:
            raise ValueError(f"other must be a Geometry object, got {type(other)}")

    def shortest_line(self, other):
        """
        Return the shortest LineString connecting this polygon to another geometry.

        This is the line connecting the nearest points between two geometries.
        This method is compatible with Shapely v2's shortest_line.

        Parameters:
        -----------
        other : Geometry, Point, LineString, Polygon, or other geometry
            The other geometry to find the shortest line to

        Returns:
        --------
        Line
            A LineString (Line) connecting the two nearest points

        Raises:
        -------
        ValueError
            If other is None or not a valid geometry
        """
        if other is None:
            raise ValueError("other must be a Geometry object, not None")

        if isinstance(other, Geometry):
            return self.as_geometry().shortest_line(other)
        elif hasattr(other, "as_geometry"):
            return self.as_geometry().shortest_line(other.as_geometry())
        else:
            raise ValueError(f"other must be a Geometry object, got {type(other)}")

    @property
    def centroid(self) -> Geometry:
        """
        Return the centroid of the polygon.

        The centroid is the geometric center of mass of the polygon.
        For polygons, this may lie outside the polygon if it is concave.

        Returns:
        --------
        Geometry
            A Point geometry representing the centroid
        """
        return self.as_geometry().centroid

    @property
    def convex_hull(self) -> Geometry:
        """
        Return the convex hull of the polygon.

        The convex hull is the smallest convex geometry that encloses all points
        in the polygon.

        Returns:
        --------
        Geometry
            A Polygon geometry representing the convex hull
        """
        return self.as_geometry().convex_hull

    def intersection(self, other) -> Geometry:
        """
        Return the geometric intersection of this polygon with another geometry.

        The intersection is the set of points common to both geometries.
        This method is compatible with Shapely's intersection.

        Parameters:
        -----------
        other : Geometry, Point, Line, Ring, Poly, or other geometry
            The other geometry to compute the intersection with

        Returns:
        --------
        Geometry
            A Geometry representing the intersection. May be empty if geometries
            do not intersect.

        Examples:
        ---------
        >>> from togo import Polygon
        >>> poly1 = Polygon([(0, 0), (2, 0), (2, 2), (0, 2), (0, 0)])
        >>> poly2 = Polygon([(1, 1), (3, 1), (3, 3), (1, 3), (1, 1)])
        >>> result = poly1.intersection(poly2)
        >>> print(result.geom_type)
        Polygon
        """
        cdef tg_geom *empty

        if other is None:
            # Return empty geometry (Shapely-compatible)
            empty = tg_geom_new_geometrycollection_empty()
            return _geometry_from_ptr(empty)

        if isinstance(other, Geometry):
            return self.as_geometry().intersection(other)
        elif hasattr(other, "as_geometry"):
            return self.as_geometry().intersection(other.as_geometry())

        # Return empty for unrecognized types (Shapely-compatible)
        empty = tg_geom_new_geometrycollection_empty()
        return _geometry_from_ptr(empty)


cdef class Segment:
    cdef public tg_segment seg

    def __init__(self, a, b):
        if isinstance(a, Point):
            self.seg.a.x = a.x
            self.seg.a.y = a.y
        else:
            self.seg.a.x = a[0]
            self.seg.a.y = a[1]
        if isinstance(b, Point):
            self.seg.b.x = b.x
            self.seg.b.y = b.y
        else:
            self.seg.b.x = b[0]
            self.seg.b.y = b[1]

    def __str__(self):
        return (
            f"Segment(a=({self.seg.a.x}, {self.seg.a.y}), "
            f"b=({self.seg.b.x}, {self.seg.b.y}))"
        )

    def __repr__(self):
        return self.__str__()

    def rect(self) -> tuple:
        cdef tg_rect r = tg_segment_rect(self.seg)
        return ((r.min.x, r.min.y), (r.max.x, r.max.y))

    def intersects(self, other) -> bool:
        if isinstance(other, Segment):
            return tg_segment_intersects_segment(self.seg, other.seg)
        raise TypeError("Expected Segment")

    @property
    def a(self) -> Point:
        return Point(self.seg.a.x, self.seg.a.y)

    @property
    def b(self) -> Point:
        return Point(self.seg.b.x, self.seg.b.y)


import enum
from typing import Optional, Union, Sequence


class TGIndex(enum.IntEnum):
    """
    Used for setting the polygon indexing default mode.
    DEFAULT: Use the library default indexing strategy. Currently NATURAL.
    NONE: No indexing.
    NATURAL: see
        https://github.com/tidwall/tg/blob/main/docs/POLYGON_INDEXING.md#natural
    YSTRIPES: see
        https://github.com/tidwall/tg/blob/main/docs/POLYGON_INDEXING.md#ystripes
    """

    DEFAULT = TG_DEFAULT
    NONE = TG_NONE
    NATURAL = TG_NATURAL
    YSTRIPES = TG_YSTRIPES


def set_polygon_indexing_mode(ix: TGIndex) -> None:
    """
    Set the polygon indexing mode. Accepts values from TGIndex enum.
    Internally it changes the global tg_index.
    """
    if not isinstance(ix, TGIndex):
        raise TypeError("set_index expects a togo.TGIndex enum value")
    tg_env_set_index(ix)


# Shapely-compatible aliases
LineString = Line


class Polygon(Poly):
    """Shapely-compatible Polygon class that extends Poly.

    Create a Polygon geometry from an exterior ring (list of coordinates or Ring object)
    and optional holes (list of lists of coordinates or Ring objects).
    """

    def __init__(
        self,
        exterior: Union[Ring, Sequence[Tuple[float, float]]],
        holes: Optional[Sequence[Union[Ring, Sequence[Tuple[float, float]]]]] = None
    ) -> None:
        """Initialize Polygon from exterior ring and optional holes.

        Parameters:
        -----------
        exterior : Ring or list of coordinates
            The exterior ring. If a list, will be converted to Ring.
        holes : list of Ring or list of coordinate lists, optional
            List of hole rings. Each hole will be converted to Ring if needed.
        """
        # Convert exterior to Ring if needed
        if not isinstance(exterior, Ring):
            exterior = Ring(exterior)

        # Convert holes to Ring objects if needed
        if holes:
            holes = [Ring(h) if not isinstance(h, Ring) else h for h in holes]

        # Call parent Poly.__init__
        super().__init__(exterior, holes)


def MultiPoint(points) -> Geometry:
    """Create a MultiPoint geometry from a list of points"""
    return Geometry.from_multipoint(points)


def MultiLineString(lines) -> Geometry:
    """Create a MultiLineString geometry from a list of lines"""
    return Geometry.from_multilinestring(lines)


def MultiPolygon(polys) -> Geometry:
    """Create a MultiPolygon geometry from a list of polygons"""
    return Geometry.from_multipolygon(polys)


def GeometryCollection(geoms) -> Geometry:
    """Create a GeometryCollection from a list of geometries"""
    return Geometry.from_geometrycollection(geoms)


# Shapely-compatible module-level functions
def from_wkt(wkt_string: str) -> Geometry:
    """Create a Geometry from a WKT string (Shapely-compatible)"""
    return Geometry(wkt_string, fmt="wkt")


def from_geojson(geojson_string: str) -> Geometry:
    """Create a Geometry from a GeoJSON string (Shapely-compatible)"""
    return Geometry(geojson_string, fmt="geojson")


def from_wkb(wkb_bytes: bytes) -> Geometry:
    """Create a Geometry from WKB bytes (Shapely-compatible)"""
    import binascii
    hex_string = binascii.hexlify(wkb_bytes).decode("ascii")
    return Geometry(hex_string, fmt="hex")


def to_wkt(geom) -> str:
    """Convert a geometry to WKT (Shapely-compatible)"""
    if hasattr(geom, "as_geometry"):
        return geom.as_geometry().to_wkt()
    elif isinstance(geom, Geometry):
        return geom.to_wkt()
    else:
        raise TypeError("Object must be a togo geometry")


def to_geojson(geom) -> str:
    """Convert a geometry to GeoJSON (Shapely-compatible)"""
    if hasattr(geom, "as_geometry"):
        return geom.as_geometry().to_geojson()
    elif isinstance(geom, Geometry):
        return geom.to_geojson()
    else:
        raise TypeError("Object must be a togo geometry")


def to_wkb(geom) -> bytes:
    """Convert a geometry to WKB (Shapely-compatible)"""
    if hasattr(geom, "as_geometry"):
        return geom.as_geometry().to_wkb()
    elif isinstance(geom, Geometry):
        return geom.to_wkb()
    else:
        raise TypeError("Object must be a togo geometry")


def transform(func, geometry) -> Geometry:
    """
    Apply a transformation function to all coordinates in a geometry.

    Similar to shapely.ops.transform, applies a callable to every coordinate
    in the geometry, recursively handling multi-geometries and geometry collections.

    Parameters:
    -----------
    func : callable
        A function that takes (x, y) and returns a tuple (x', y').
        Must return a tuple of two numbers.
    geometry : Geometry, Point, Line, Ring, Poly, or other geometry type
        The geometry to transform. If it has an as_geometry() method,
        that will be called to get the base Geometry.

    Returns:
    --------
    Geometry
        A new transformed Geometry

    Raises:
    -------
    TypeError
        If func doesn't return a valid (x, y) tuple or if geometry is invalid.

    Examples:
    ---------
    >>> def translate(x, y):
    ...     return x + 1, y + 2
    >>> point = Point(0, 0)
    >>> transformed = transform(translate, point)
    """
    # Convert to Geometry if needed
    if hasattr(geometry, "as_geometry"):
        geom = geometry.as_geometry()
    elif isinstance(geometry, Geometry):
        geom = geometry
    else:
        raise TypeError("geometry must be a togo geometry type")

    return _transform_recursive(func, geom)


cdef tuple _validate_transform_result(object result):
    """
    Validate and convert the result from a transform function.

    Args:
        result: The return value from the transform function

    Returns:
        A tuple of (x, y) as floats

    Raises:
        TypeError: If the result is not a valid tuple of two numbers
    """
    if result is None or not isinstance(result, (tuple, list)) or len(result) != 2:
        raise TypeError("Transform function must return a tuple of (x, y)")
    try:
        x_new = float(result[0])
        y_new = float(result[1])
    except (TypeError, ValueError):
        raise TypeError("Transform function must return a tuple of two numbers")
    return (x_new, y_new)


cdef Geometry _transform_recursive(object func, Geometry geom):
    """Internal recursive function to transform a geometry"""
    cdef int geom_type = tg_geom_typeof(geom.geom)
    cdef int i, n, j, nholes, line_num_pts
    cdef tg_point transformed_pt
    cdef list transformed_coords
    cdef list transformed_lines
    cdef list transformed_polys
    cdef list transformed_geoms
    cdef const tg_line *line
    cdef const tg_poly *poly
    cdef const tg_geom *child_geom
    cdef tg_point pt
    cdef const tg_point *pts
    cdef const tg_point *line_pts

    # Point (type 1)
    if geom_type == 1:
        pt = tg_geom_point(geom.geom)
        result = func(pt.x, pt.y)
        x_new, y_new = _validate_transform_result(result)
        transformed_pt.x = x_new
        transformed_pt.y = y_new
        return _geometry_from_ptr(tg_geom_new_point(transformed_pt))

    # LineString (type 2)
    elif geom_type == 2:
        line = tg_geom_line(geom.geom)
        n = tg_line_num_points(line)
        pts = tg_line_points(line)
        transformed_coords = []
        for i in range(n):
            result = func(pts[i].x, pts[i].y)
            x_new, y_new = _validate_transform_result(result)
            transformed_coords.append((x_new, y_new))
        return _geometry_from_ptr(tg_geom_new_linestring(
            (<Line>Line(transformed_coords))._get_c_line())
        )

    # Polygon (type 3)
    elif geom_type == 3:
        poly = tg_geom_poly(geom.geom)
        # Transform exterior ring
        ext_ring = Ring.from_ptr(<tg_ring *>tg_poly_exterior(poly))
        transformed_ext_coords = _transform_ring_coords(func, ext_ring)
        transformed_ext = Ring(transformed_ext_coords)

        # Transform holes
        n = tg_poly_num_holes(poly)
        transformed_holes = []
        for i in range(n):
            hole_ring = Ring.from_ptr(<tg_ring *>tg_poly_hole_at(poly, i))
            transformed_hole_coords = _transform_ring_coords(func, hole_ring)
            transformed_holes.append(Ring(transformed_hole_coords))

        transformed_poly = Poly(transformed_ext, transformed_holes if transformed_holes else None)
        return _geometry_from_ptr(tg_geom_new_polygon(transformed_poly._get_c_poly()))

    # MultiPoint (type 4)
    elif geom_type == 4:
        n = tg_geom_num_points(geom.geom)
        transformed_coords = []
        for i in range(n):
            pt = tg_geom_point_at(geom.geom, i)
            result = func(pt.x, pt.y)
            x_new, y_new = _validate_transform_result(result)
            transformed_coords.append((x_new, y_new))
        return Geometry.from_multipoint(transformed_coords)

    # MultiLineString (type 5)
    elif geom_type == 5:
        n = tg_geom_num_lines(geom.geom)
        transformed_lines = []
        for i in range(n):
            line = tg_geom_line_at(geom.geom, i)
            line_num_pts = tg_line_num_points(line)
            line_pts = tg_line_points(line)
            transformed_coords = []
            for j in range(line_num_pts):
                result = func(line_pts[j].x, line_pts[j].y)
                x_new, y_new = _validate_transform_result(result)
                transformed_coords.append((x_new, y_new))
            transformed_lines.append(transformed_coords)
        return Geometry.from_multilinestring(transformed_lines)

    # MultiPolygon (type 6)
    elif geom_type == 6:
        n = tg_geom_num_polys(geom.geom)
        transformed_polys = []
        for i in range(n):
            poly = tg_geom_poly_at(geom.geom, i)
            # Transform exterior ring
            ext_ring = Ring.from_ptr(<tg_ring *>tg_poly_exterior(poly))
            transformed_ext_coords = _transform_ring_coords(func, ext_ring)
            transformed_ext = Ring(transformed_ext_coords)

            # Transform holes
            nholes = tg_poly_num_holes(poly)
            transformed_holes = []
            for j in range(nholes):
                hole_ring = Ring.from_ptr(<tg_ring *>tg_poly_hole_at(poly, j))
                transformed_hole_coords = _transform_ring_coords(func, hole_ring)
                transformed_holes.append(Ring(transformed_hole_coords))

            transformed_polys.append(
                Poly(transformed_ext, transformed_holes if transformed_holes else None)
            )
        return Geometry.from_multipolygon(transformed_polys)

    # GeometryCollection (type 7)
    elif geom_type == 7:
        n = tg_geom_num_geometries(geom.geom)
        transformed_geoms = []
        for i in range(n):
            child_geom = tg_geom_geometry_at(geom.geom, i)
            child_geom_obj = _geometry_from_ptr(tg_geom_clone(child_geom))
            transformed_child = _transform_recursive(func, child_geom_obj)
            transformed_geoms.append(transformed_child)
        return Geometry.from_geometrycollection(transformed_geoms)

    else:
        raise ValueError(f"Unknown geometry type: {geom_type}")


cdef list _transform_ring_coords(object func, Ring ring):
    """Helper function to transform all coordinates in a ring"""
    cdef int n = tg_ring_num_points(ring.ring)
    cdef const tg_point *pts = tg_ring_points(ring.ring)
    cdef list transformed_coords = []
    cdef int i

    for i in range(n):
        result = func(pts[i].x, pts[i].y)
        x_new, y_new = _validate_transform_result(result)
        transformed_coords.append((x_new, y_new))

    return transformed_coords


def nearest_points(geom1, geom2) -> tuple:
    """
    Return a tuple of the nearest points between two geometries.

    This is a module-level function compatible with Shapely's nearest_points.
    Returns a tuple of two Point objects: (point_from_geom1, point_from_geom2).

    Parameters:
    -----------
    geom1 : Geometry, Point, Line, Ring, Poly, or other geometry type
        The first geometry
    geom2 : Geometry, Point, Line, Ring, Poly, or other geometry type
        The second geometry

    Returns:
    --------
    tuple
        A tuple of (Point, Point) representing the nearest points between the two geometries

    Raises:
    -------
    TypeError
        If either geometry is None or invalid

    Examples:
    ---------
    >>> from togo import nearest_points, Point, LineString
    >>> p = Point(0, 0)
    >>> line = LineString([(10, 0), (10, 10)])
    >>> pt1, pt2 = nearest_points(p, line)
    >>> print(f"Distance: {((pt2.x - pt1.x)**2 + (pt2.y - pt1.y)**2)**0.5:.1f}")
    10.0
    """
    # Convert to Geometry if needed
    if hasattr(geom1, "as_geometry"):
        g1 = geom1.as_geometry()
    elif isinstance(geom1, Geometry):
        g1 = geom1
    else:
        raise TypeError("geom1 must be a togo geometry type")

    if hasattr(geom2, "as_geometry"):
        g2 = geom2.as_geometry()
    elif isinstance(geom2, Geometry):
        g2 = geom2
    else:
        raise TypeError("geom2 must be a togo geometry type")

    # Use the Geometry.nearest_points method
    return g1.nearest_points(g2)


def shortest_line(geom1, geom2):
    """
    Return the shortest LineString connecting two geometries.

    This is a module-level function compatible with Shapely v2's shortest_line.
    Returns a LineString connecting the nearest points between the two geometries.

    Parameters:
    -----------
    geom1 : Geometry, Point, Line, Ring, Poly, or other geometry type
        The first geometry
    geom2 : Geometry, Point, Line, Ring, Poly, or other geometry type
        The second geometry

    Returns:
    --------
    Line
        A LineString (Line) connecting the two nearest points

    Raises:
    -------
    ValueError
        If either geometry is None or invalid

    Examples:
    ---------
    >>> from togo import shortest_line, Point, LineString
    >>> p = Point(0, 0)
    >>> line = LineString([(10, 0), (10, 10)])
    >>> connecting = shortest_line(p, line)
    >>> print(connecting.length)
    10.0
    """
    # Convert to Geometry if needed
    if hasattr(geom1, "as_geometry"):
        g1 = geom1.as_geometry()
    elif isinstance(geom1, Geometry):
        g1 = geom1
    else:
        raise TypeError("geom1 must be a togo geometry type")

    if hasattr(geom2, "as_geometry"):
        g2 = geom2.as_geometry()
    elif isinstance(geom2, Geometry):
        g2 = geom2
    else:
        raise TypeError("geom2 must be a togo geometry type")

    # Use the Geometry.shortest_line method
    return g1.shortest_line(g2)


def intersection(geom1, geom2) -> Geometry:
    """
    Return the geometric intersection of two geometries.

    This is a module-level function compatible with Shapely's intersection.
    Returns the set of points common to both geometries.

    Parameters:
    -----------
    geom1 : Geometry, Point, Line, Ring, Poly, or other geometry type
        The first geometry
    geom2 : Geometry, Point, Line, Ring, Poly, or other geometry type
        The second geometry

    Returns:
    --------
    Geometry
        A Geometry representing the intersection. The result type depends
        on the input geometries and their spatial relationship:
        - Point-Point: Point (if they overlap) or empty
        - Line-Line: Point, LineString, or MultiLineString
        - Polygon-Polygon: Point, LineString, Polygon, or MultiPolygon
        - Empty if geometries do not intersect

    Raises:
    -------
    RuntimeError
        If the intersection calculation fails

    Examples:
    ---------
    >>> from togo import intersection, Polygon
    >>> poly1 = Polygon([(0, 0), (2, 0), (2, 2), (0, 2), (0, 0)])
    >>> poly2 = Polygon([(1, 1), (3, 1), (3, 3), (1, 3), (1, 1)])
    >>> result = intersection(poly1, poly2)
    >>> print(result.geom_type)
    Polygon
    >>> print(f"{result.area:.1f}")
    1.0
    """
    cdef tg_geom *empty

    # Convert to Geometry if needed, return empty for None/invalid (Shapely-compatible)
    if geom1 is None:
        empty = tg_geom_new_geometrycollection_empty()
        return _geometry_from_ptr(empty)

    if hasattr(geom1, "as_geometry"):
        g1 = geom1.as_geometry()
    elif isinstance(geom1, Geometry):
        g1 = geom1
    else:
        # Return empty for invalid type (Shapely-compatible)
        empty = tg_geom_new_geometrycollection_empty()
        return _geometry_from_ptr(empty)

    if geom2 is None:
        empty = tg_geom_new_geometrycollection_empty()
        return _geometry_from_ptr(empty)

    if hasattr(geom2, "as_geometry"):
        g2 = geom2.as_geometry()
    elif isinstance(geom2, Geometry):
        g2 = geom2
    else:
        # Return empty for invalid type (Shapely-compatible)
        empty = tg_geom_new_geometrycollection_empty()
        return _geometry_from_ptr(empty)

    # Use the Geometry.intersection method
    return g1.intersection(g2)


def convex_hull(geom):
    """
    Return the convex hull of a geometry.

    This is a module-level function compatible with Shapely's convex_hull.
    The convex hull is the smallest convex geometry that encloses all points
    in the input geometry.

    Parameters:
    -----------
    geom : Geometry, Point, Line, Ring, Poly, or other geometry type
        The geometry to compute the convex hull for

    Returns:
    --------
    Geometry
        A Polygon (or Point/LineString for degenerate cases) representing
        the convex hull

    Raises:
    -------
    TypeError
        If the geometry is None or invalid

    Examples:
    ---------
    >>> from togo import convex_hull, MultiPoint
    >>> points = MultiPoint([(0, 0), (1, 1), (0, 2), (2, 2), (3, 1), (1, 0)])
    >>> hull = convex_hull(points)
    >>> print(hull.geom_type)
    Polygon
    """
    # Convert to Geometry if needed
    if hasattr(geom, "as_geometry"):
        g = geom.as_geometry()
    elif isinstance(geom, Geometry):
        g = geom
    else:
        raise TypeError("geom must be a togo geometry type")

    # Use the Geometry.convex_hull property
    return g.convex_hull


__all__ = [
    "Geometry", "Point", "Rect", "Ring", "Line", "Poly", "Segment",
    "LineString", "Polygon",
    "MultiPoint", "MultiLineString", "MultiPolygon", "GeometryCollection",
    "from_wkt", "from_geojson", "from_wkb",
    "to_wkt", "to_geojson", "to_wkb",
    "nearest_points", "shortest_line", "convex_hull", "transform",
    "set_polygon_indexing_mode", "TGIndex"
]
