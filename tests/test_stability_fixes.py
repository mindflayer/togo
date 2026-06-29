"""
Regression tests for native-layer stability fixes.

Covers:
- tg_geom_error propagation after tg_geom_from_geos in all overlay methods
- Correct GEOSCoordSeq_getXY_r return-value semantics (was checking -1, should be != 1)
- 2D dimensionality guard in unary_union
- tg_geom_error propagation after tg_geom_to/from_meters_grid
- Explicit temporary Line lifetime in _transform_recursive
"""

import pytest


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _poly(coords):
    from togo import Polygon

    return Polygon(coords)


def _simple_square(offset=0):
    o = offset
    return _poly([(o, o), (o + 2, o), (o + 2, o + 2), (o, o + 2), (o, o)])


# ---------------------------------------------------------------------------
# 1. GEOS overlay operations must not silently use error geometries
# ---------------------------------------------------------------------------


class TestOverlayReturnSanity:
    """All overlay operations should return a valid, accessible Geometry."""

    def test_buffer_result_is_accessible(self):
        from togo import Point

        g = Point(0, 0).buffer(1.0)
        assert g.geom_type == "Polygon"
        assert g.area > 0

    def test_simplify_result_is_accessible(self):
        poly = _simple_square()
        result = poly.simplify(0.01)
        assert result.geom_type in {"Polygon", "MultiPolygon", "GeometryCollection"}

    def test_centroid_result_is_accessible(self):
        from togo import Geometry

        poly = Geometry("POLYGON((0 0,4 0,4 4,0 4,0 0))", fmt="wkt")
        c = poly.centroid
        assert c.geom_type == "Point"
        # centroid of axis-aligned square at (0,0)–(4,4) is (2,2)
        assert abs(c.bounds[0] - 2.0) < 1e-9
        assert abs(c.bounds[1] - 2.0) < 1e-9

    def test_convex_hull_result_is_accessible(self):
        from togo import MultiPoint

        pts = MultiPoint([(0, 0), (2, 0), (1, 2)])
        hull = pts.convex_hull
        assert hull.geom_type in {"Polygon", "LineString", "Point"}

    def test_intersection_result_is_accessible(self):
        p1 = _simple_square(0)
        p2 = _simple_square(1)
        result = p1.intersection(p2)
        # overlapping squares produce a polygon
        assert result.geom_type in {"Polygon", "MultiPolygon", "GeometryCollection"}
        assert result.area == pytest.approx(1.0)

    def test_union_result_is_accessible(self):
        p1 = _simple_square(0)
        p2 = _simple_square(1)
        result = p1.union(p2)
        assert result.geom_type in {"Polygon", "MultiPolygon"}
        assert result.area == pytest.approx(7.0)

    def test_unary_union_result_is_accessible(self):
        from togo import Geometry

        polys = [_simple_square(i) for i in range(3)]
        result = Geometry.unary_union(polys)
        assert not result.is_empty
        # three touching squares give a merged polygon
        assert result.geom_type in {"Polygon", "MultiPolygon"}

    def test_intersection_disjoint_returns_empty(self):
        p1 = _simple_square(0)
        p2 = _simple_square(10)  # far away, no overlap
        result = p1.intersection(p2)
        assert result.is_empty

    def test_module_level_intersection_result_is_accessible(self):
        from togo import intersection

        p1 = _simple_square(0)
        p2 = _simple_square(1)
        result = intersection(p1, p2)
        assert result.area == pytest.approx(1.0)

    def test_module_level_union_result_is_accessible(self):
        from togo import union

        p1 = _simple_square(0)
        p2 = _simple_square(1)
        result = union(p1, p2)
        assert result.area == pytest.approx(7.0)


# ---------------------------------------------------------------------------
# 2. unary_union 2D dimensionality guard
# ---------------------------------------------------------------------------


class TestUnaryUnion2DGuard:
    """unary_union should normalize 3D inputs to 2D for topology operations."""

    def test_unary_union_2d_list_succeeds(self):
        from togo import Geometry

        polys = [_simple_square(i * 3) for i in range(4)]
        result = Geometry.unary_union(polys)
        assert not result.is_empty

    def test_unary_union_normalizes_3d_geometry_to_2d(self):
        from togo import Geometry

        # Parse a 3D polygon (has Z coordinate)
        g3d = Geometry("POLYGON Z ((0 0 1, 2 0 1, 2 2 1, 0 2 1, 0 0 1))", fmt="wkt")
        assert g3d.has_z, "test precondition: geometry should be 3D"

        result = Geometry.unary_union([g3d])

        assert result.geom_type == "Polygon"
        assert result.has_z is False
        assert result.area == pytest.approx(4.0)

    def test_module_level_unary_union_2d_succeeds(self):
        from togo import unary_union

        polys = [_simple_square(0), _simple_square(3)]
        result = unary_union(polys)
        assert not result.is_empty

    def test_unary_union_empty_list_raises(self):
        from togo import Geometry

        with pytest.raises(ValueError):
            Geometry.unary_union([])


# ---------------------------------------------------------------------------
# 3. Nearest-points coordinate extraction (GEOSCoordSeq_getXY_r return check)
# ---------------------------------------------------------------------------


class TestNearestPointsCoordExtraction:
    """Nearest-points extraction must not silently swallow GEOS failures."""

    def test_nearest_points_returns_correct_coordinates(self):
        from togo import Point, LineString

        p = Point(0, 0)
        line = LineString([(3, 4), (10, 4)])
        pt_from_p, pt_from_line = p.nearest_points(line)
        # Nearest point on line to origin is (3, 4)
        assert pt_from_p.x == pytest.approx(0.0)
        assert pt_from_p.y == pytest.approx(0.0)
        assert pt_from_line.x == pytest.approx(3.0)
        assert pt_from_line.y == pytest.approx(4.0)

    def test_nearest_points_between_polygons(self):
        from togo import nearest_points

        p1 = _simple_square(0)  # (0,0)-(2,2)
        p2 = _simple_square(5)  # (5,5)-(7,7)
        pt1, pt2 = nearest_points(p1, p2)
        # nearest corners are (2,2) and (5,5)
        assert pt1.x == pytest.approx(2.0)
        assert pt1.y == pytest.approx(2.0)
        assert pt2.x == pytest.approx(5.0)
        assert pt2.y == pytest.approx(5.0)

    def test_shortest_line_length_is_correct(self):
        from togo import shortest_line, Point
        import math

        p = Point(0, 0)
        line_geom = _simple_square(3).as_geometry()  # shifted square
        sl = shortest_line(p, line_geom)
        # distance from origin to nearest corner (3,3) ≈ 4.2426
        expected = math.sqrt(3**2 + 3**2)
        assert sl.length == pytest.approx(expected, abs=1e-6)


# ---------------------------------------------------------------------------
# 4. transform recursive – LineString temporary lifetime
# ---------------------------------------------------------------------------


class TestTransformLineStringLifetime:
    """transform() must keep its temporary Line alive until tg copies the data."""

    def test_transform_linestring(self):
        from togo import transform, LineString

        line = LineString([(0, 0), (1, 0), (2, 0)])
        shifted = transform(lambda x, y: (x + 10, y + 5), line)
        assert shifted.geom_type == "LineString"
        coords = shifted.coords
        assert len(coords) == 3
        assert coords[0] == pytest.approx((10.0, 5.0))
        assert coords[1] == pytest.approx((11.0, 5.0))
        assert coords[2] == pytest.approx((12.0, 5.0))

    def test_transform_linestring_many_points(self):
        """Stress test with many coordinates to stress the temporary object path."""
        from togo import transform, LineString

        pts = [(float(i), float(i) * 2) for i in range(1000)]
        line = LineString(pts)
        result = transform(lambda x, y: (x * 2, y * 2), line)
        assert result.geom_type == "LineString"
        result_coords = result.coords
        assert len(result_coords) == 1000
        assert result_coords[0] == pytest.approx((0.0, 0.0))
        assert result_coords[999] == pytest.approx((1998.0, 3996.0))

    def test_transform_multilinestring(self):
        from togo import transform, Geometry

        mls = Geometry.from_multilinestring([[(0, 0), (1, 1)], [(2, 2), (3, 3)]])
        result = transform(lambda x, y: (x + 1, y + 1), mls)
        assert result.geom_type == "MultiLineString"

    def test_transform_polygon(self):
        from togo import transform

        poly = _simple_square(0)
        result = transform(lambda x, y: (x + 1, y + 1), poly)
        assert result.geom_type == "Polygon"
        assert result.area == pytest.approx(4.0)

    def test_transform_multipolygon(self):
        from togo import transform, Geometry

        mp = Geometry.from_multipolygon(
            [
                _simple_square(0).as_geometry().poly(),
                _simple_square(5).as_geometry().poly(),
            ]
        )
        result = transform(lambda x, y: (x * 2, y * 2), mp)
        assert result.geom_type == "MultiPolygon"

    def test_transform_collection(self):
        from togo import transform, Geometry, Point

        gc = Geometry.from_geometrycollection(
            [
                Point(1, 1).as_geometry(),
                _simple_square(0).as_geometry(),
            ]
        )
        result = transform(lambda x, y: (x - 1, y - 1), gc)
        assert result.geom_type == "GeometryCollection"


# ---------------------------------------------------------------------------
# 5. meters_grid conversion error propagation
# ---------------------------------------------------------------------------


class TestMetersGridErrorPropagation:
    """to_meters_grid / from_meters_grid must not silently use error geometries."""

    def test_to_meters_grid_point_roundtrip(self):
        from togo import Geometry, Point

        g = Geometry("POINT(1 1)", fmt="wkt")
        origin = Point(0, 0)
        converted = g.to_meters_grid(origin)
        # should return a valid (non-empty) geometry
        assert not converted.is_empty
        back = converted.from_meters_grid(origin)
        assert back.geom_type == "Point"

    def test_from_meters_grid_polygon_roundtrip(self):
        from togo import Geometry, Point

        poly = Geometry("POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))", fmt="wkt")
        origin = Point(0.5, 0.5)
        converted = poly.to_meters_grid(origin)
        assert not converted.is_empty
        back = converted.from_meters_grid(origin)
        assert back.geom_type == "Polygon"

    def test_to_meters_grid_empty_returns_empty(self):
        """Empty geometry should survive meters_grid round-trip without crashing."""
        from togo import Geometry, Point

        empty = Geometry('{"type":"GeometryCollection","geometries":[]}')
        assert empty.is_empty
        origin = Point(0, 0)
        # Should not crash; empty geometry clones are returned early.
        converted = empty.to_meters_grid(origin)
        assert converted.is_empty


# ---------------------------------------------------------------------------
# 6. Operation-chain stress – unary_union -> intersection -> buffer chain
# ---------------------------------------------------------------------------


class TestOperationChainSafety:
    """Simulate the area-slicer workflow: union -> intersection -> buffer."""

    def test_union_then_intersection(self):
        from togo import Geometry

        # Build two overlapping polygon groups
        group_a = [_simple_square(i) for i in [0, 1, 2]]
        group_b = [_simple_square(i) for i in [1, 2, 3]]
        union_a = Geometry.unary_union(group_a)
        union_b = Geometry.unary_union(group_b)
        ix = union_a.intersection(union_b)
        assert not ix.is_empty
        # Intersection should be smaller than either union
        assert ix.area < union_a.area
        assert ix.area < union_b.area
        # Intersection must be at least as large as a single shared square (area=4)
        assert ix.area >= 4.0

    def test_unary_union_then_buffer(self):
        from togo import Geometry

        polys = [_simple_square(i * 3) for i in range(3)]
        merged = Geometry.unary_union(polys)
        buffered = merged.buffer(0.1)
        assert buffered.area > merged.area

    def test_intersection_chain_is_stable(self):
        """Repeatedly intersect progressively smaller regions."""
        from togo import Geometry

        current = Geometry("POLYGON((0 0, 10 0, 10 10, 0 10, 0 0))", fmt="wkt")
        for step in range(5):
            clip = Geometry(
                f"POLYGON(({step} {step}, 10 {step}, 10 10, {step} 10, {step} {step}))",
                fmt="wkt",
            )
            current = current.intersection(clip)
            assert not current.is_empty

    def test_unary_union_with_shapely_like_objects(self):
        """Objects with .wkb attribute (Shapely-style) should work without crashing."""
        from togo import Geometry

        class FakeShapelyGeom:
            """Minimal Shapely-like shim with .wkb."""

            def __init__(self, wkb_bytes):
                self.wkb = wkb_bytes

        poly = _simple_square(0)
        wkb_bytes = poly.as_geometry().to_wkb()
        fake = FakeShapelyGeom(wkb_bytes)

        result = Geometry.unary_union([poly.as_geometry(), fake])
        assert not result.is_empty
