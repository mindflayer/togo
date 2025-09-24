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
    const tg_line *tg_geom_line(const tg_geom *geom)
    const tg_poly *tg_geom_poly(const tg_geom *geom)
    const tg_geom *tg_geom_geometry_at(const tg_geom *geom, int index)
    const tg_line *tg_geom_line_at(const tg_geom *geom, int index)
    const tg_poly *tg_geom_poly_at(const tg_geom *geom, int index)

from libc.stdlib cimport malloc, free
from libc.string cimport memset

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

    def type(self):
        return tg_geom_typeof(self.geom)

    def type_string(self):
        return tg_geom_type_string(tg_geom_typeof(self.geom)).decode("utf-8")

    def rect(self):
        cdef tg_rect r
        r = tg_geom_rect(self.geom)
        return ((r.min.x, r.min.y), (r.max.x, r.max.y))

    def is_feature(self):
        return tg_geom_is_feature(self.geom) != 0

    def is_featurecollection(self):
        return tg_geom_is_featurecollection(self.geom) != 0

    def is_empty(self):
        return tg_geom_is_empty(self.geom) != 0

    def dims(self):
        return tg_geom_dims(self.geom)

    def has_z(self):
        return tg_geom_has_z(self.geom) != 0

    def has_m(self):
        return tg_geom_has_m(self.geom) != 0

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
        return tg_geom_equals(self.geom, other.geom) != 0

    def disjoint(self, other: Geometry):
        return tg_geom_disjoint(self.geom, other.geom) != 0

    def contains(self, other: Geometry):
        return tg_geom_contains(self.geom, other.geom) != 0

    def within(self, other: Geometry):
        return tg_geom_within(self.geom, other.geom) != 0

    def covers(self, other: Geometry):
        return tg_geom_covers(self.geom, other.geom) != 0

    def coveredby(self, other: Geometry):
        return tg_geom_coveredby(self.geom, other.geom) != 0

    def touches(self, other: Geometry):
        return tg_geom_touches(self.geom, other.geom) != 0

    def intersects(self, other: Geometry):
        return tg_geom_intersects(self.geom, other.geom) != 0

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

    cpdef point(self):
        """Get point from Point geometry"""
        cdef tg_point pt = tg_geom_point(self.geom)
        return Point(pt.x, pt.y)

    cpdef line(self):
        """Get line from LineString geometry"""
        cdef const tg_line *ln = tg_geom_line(self.geom)
        return _line_from_ptr(<tg_line *>ln)

    cpdef poly(self):
        """Get polygon from Polygon geometry"""
        cdef const tg_poly *p = tg_geom_poly(self.geom)
        return Poly._from_c_poly(<tg_poly *>p)  # Cast away const

    def __getitem__(self, idx):
        cdef const tg_geom *g
        t = tg_geom_typeof(self.geom)
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
    def from_linestring(points):
        """Create LineString geometry from points"""
        line = Line(points)
        return _geometry_from_ptr(tg_geom_new_linestring(line._get_c_line()))

    def __dealloc__(self):
        if self.geom:
            tg_geom_free(self.geom)

    # internal accessor for C pointer
    cdef tg_geom *_get_c_geom(self):
        return self.geom

    # --- Factory methods ---
    @staticmethod
    def from_multipoint(points):
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
    def from_multilinestring(lines):
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
    def from_multipolygon(polys):
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
    def from_geometrycollection(geoms):
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


cdef class Point:
    cdef tg_point pt

    def __init__(self, x: float, y: float):
        self.pt.x = x
        self.pt.y = y

    @property
    def x(self):
        return self.pt.x

    @property
    def y(self):
        return self.pt.y

    def as_tuple(self):
        return (self.pt.x, self.pt.y)

    cdef tg_point _get_c_point(self):
        return self.pt

    def as_geometry(self):
        return _geometry_from_ptr(tg_geom_new_point(self.pt))


cdef class Rect:
    cdef tg_rect rect

    def __init__(self, min_pt: Point, max_pt: Point):
        self.rect.min = min_pt.pt
        self.rect.max = max_pt.pt

    @property
    def min(self):
        return Point(self.rect.min.x, self.rect.min.y)

    @property
    def max(self):
        return Point(self.rect.max.x, self.rect.max.y)

    def center(self):
        cdef tg_point c = tg_rect_center(self.rect)
        return Point(c.x, c.y)

    cdef tg_rect _get_c_rect(self):
        return self.rect

    def expand(self, other):
        cdef tg_rect r
        if isinstance(other, Rect):
            r = tg_rect_expand(self.rect, (<Rect>other)._get_c_rect())
            return Rect(Point(r.min.x, r.min.y), Point(r.max.x, r.max.y))
        elif isinstance(other, Point):
            r = tg_rect_expand_point(self.rect, (<Point>other)._get_c_point())
            return Rect(Point(r.min.x, r.min.y), Point(r.max.x, r.max.y))
        else:
            raise TypeError("expand expects Rect or Point")

    def intersects(self, other):
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

    def as_geometry(self):
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

    def __init__(self, points):
        cdef int n = len(points)
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

    @staticmethod
    cdef Ring from_ptr(tg_ring *ptr):
        cdef Ring r = Ring.__new__(Ring)
        r.ring = ptr
        r.owns_pointer = False  # Don't free this pointer
        return r

    cdef tg_ring *_get_c_ring(self):
        return self.ring

    def __dealloc__(self):
        if self.ring and self.owns_pointer:
            tg_ring_free(self.ring)

    def num_points(self):
        return tg_ring_num_points(self.ring)

    def points(self):
        n = tg_ring_num_points(self.ring)
        pts = tg_ring_points(self.ring)
        return [(pts[i].x, pts[i].y) for i in range(n)]

    def area(self):
        return tg_ring_area(self.ring)

    def perimeter(self):
        return tg_ring_perimeter(self.ring)

    def rect(self):
        r = tg_ring_rect(self.ring)
        return Rect(Point(r.min.x, r.min.y), Point(r.max.x, r.max.y))

    def is_convex(self):
        return tg_ring_convex(self.ring)

    def is_clockwise(self):
        return tg_ring_clockwise(self.ring)

    def as_geometry(self):
        # Convert the ring to a Polygon geometry with this ring as exterior
        cdef tg_poly *p = tg_poly_new(self.ring, NULL, 0)
        if not p:
            raise ValueError("Failed to create Poly from Ring")
        cdef tg_geom *g = tg_geom_new_polygon(<const tg_poly *>p)
        tg_poly_free(p)
        if not g:
            raise ValueError("Failed to create Geometry from Ring")
        return _geometry_from_ptr(g)

    def as_poly(self):
        # Build a new Poly object from this Ring
        return Poly(self)


cdef class Line:
    cdef tg_line *line
    cdef bint owns_pointer

    def __init__(self, points):
        cdef int n = len(points)
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

    def __dealloc__(self):
        if self.line and self.owns_pointer:
            tg_line_free(self.line)

    def num_points(self):
        return tg_line_num_points(self.line)

    def points(self):
        n = tg_line_num_points(self.line)
        pts = tg_line_points(self.line)
        return [(pts[i].x, pts[i].y) for i in range(n)]

    def length(self):
        return tg_line_length(self.line)

    def rect(self):
        r = tg_line_rect(self.line)
        return Rect(Point(r.min.x, r.min.y), Point(r.max.x, r.max.y))

    def is_clockwise(self):
        return tg_line_clockwise(self.line)

    def as_geometry(self):
        cdef tg_geom *g = tg_geom_new_linestring(self.line)
        if not g:
            raise ValueError("Failed to create Geometry from LineString")
        return _geometry_from_ptr(g)

    cdef tg_line *_get_c_line(self):
        return self.line

    def __getitem__(self, idx):
        n = self.num_points()
        if not (0 <= idx < n):
            raise IndexError("Line index out of range")
        cdef tg_point pt = tg_line_point_at(self.line, idx)
        return Point(pt.x, pt.y)


cdef class Poly:
    cdef tg_poly *poly
    cdef bint owns_pointer

    def __init__(self, exterior, holes=None):
        cdef int nholes = 0
        cdef tg_ring **hole_ptrs = NULL
        cdef tg_ring **holes_arr = NULL
        cdef tg_ring *ext_ring
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

    def __dealloc__(self):
        if self.poly and self.owns_pointer:
            tg_poly_free(self.poly)

    def exterior(self):
        ext = tg_poly_exterior(self.poly)
        return Ring.from_ptr(<tg_ring *>ext)

    def num_holes(self):
        return tg_poly_num_holes(self.poly)

    @staticmethod
    cdef _from_c_poly(tg_poly *ptr):
        cdef Poly poly = Poly.__new__(Poly)
        poly.poly = ptr
        poly.owns_pointer = False
        return poly

    def hole(self, idx):
        h = tg_poly_hole_at(self.poly, idx)
        return Ring.from_ptr(<tg_ring *>h)

    def rect(self):
        r = tg_poly_rect(self.poly)
        return Rect(Point(r.min.x, r.min.y), Point(r.max.x, r.max.y))

    def is_clockwise(self):
        return tg_poly_clockwise(self.poly)

    def as_geometry(self):
        cdef tg_geom *g = tg_geom_new_polygon(self.poly)
        if not g:
            raise ValueError("Failed to create Geometry from Polygon")
        return _geometry_from_ptr(g)

    cdef tg_poly *_get_c_poly(self):
        return self.poly


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

    def rect(self):
        cdef tg_rect r = tg_segment_rect(self.seg)
        return ((r.min.x, r.min.y), (r.max.x, r.max.y))

    def intersects(self, other):
        if isinstance(other, Segment):
            return tg_segment_intersects_segment(self.seg, other.seg)
        raise TypeError("Expected Segment")

    @property
    def a(self):
        return Point(self.seg.a.x, self.seg.a.y)

    @property
    def b(self):
        return Point(self.seg.b.x, self.seg.b.y)


import enum


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


def set_polygon_indexing_mode(ix: TGIndex):
    """
    Set the polygon indexing mode. Accepts values from TGIndex enum.
    Internally it changes the global tg_index.
    """
    if not isinstance(ix, TGIndex):
        raise TypeError("set_index expects a togo.TGIndex enum value")
    tg_env_set_index(ix)


__all__ = [
    "Geometry", "Point", "Rect", "Ring", "Line", "Poly", "Segment",
    "set_polygon_indexing_mode", "TGIndex"
]
