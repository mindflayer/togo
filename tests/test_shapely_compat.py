"""Tests for Shapely compatibility required by model_based_planner.

Covers:
1. Module-level unary_union(geoms)
2. LineString.project(point)
3. Polygon.intersects(other)
4. Polygon.boundary property
5. Polygon.from_bounds(minx, miny, maxx, maxy)
6. Point.coords and LineString.coords are indexable/sized sequences
7. Operations/predicates accept wrapper geometry objects (Point/LineString/Polygon)
8. MultiPolygon and MultiLineString are real Python classes
9. Geometry equality behaves consistently
10. Difference set-operations are available in method and module forms
11. Wrapper forwarding and Geometry protocol parity regressions
"""

import pytest

import togo
from togo import (
    BaseGeometry,
    Geometry,
    Line,
    LineString,
    MultiLineString,
    MultiPolygon,
    Point,
    Poly,
    Polygon,
    Ring,
    shape,
    unary_union,
)


# ---------------------------------------------------------------------------
# 1. Module-level unary_union
# ---------------------------------------------------------------------------


class TestUnaryUnion:
    def test_unary_union_two_polygons(self):
        """unary_union on a list of two non-overlapping polygons returns a MultiPolygon."""
        p1 = Polygon([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)])
        p2 = Polygon([(2, 0), (3, 0), (3, 1), (2, 1), (2, 0)])
        result = unary_union([p1, p2])
        assert result is not None
        assert not result.is_empty

    def test_unary_union_overlapping_polygons(self):
        """unary_union merges overlapping polygons into a single Polygon."""
        p1 = Polygon([(0, 0), (2, 0), (2, 2), (0, 2), (0, 0)])
        p2 = Polygon([(1, 0), (3, 0), (3, 2), (1, 2), (1, 0)])
        result = unary_union([p1, p2])
        assert result.geom_type in ("Polygon", "MultiPolygon")
        assert result.area > p1.area  # merged area should be larger

    def test_unary_union_single_geometry(self):
        """unary_union on single geometry returns equivalent geometry."""
        p = Polygon([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)])
        result = unary_union([p])
        assert result.geom_type == "Polygon"

    def test_unary_union_accepts_polygon_objects(self):
        """unary_union accepts Polygon wrapper objects (not just Geometry)."""
        polys = [
            Polygon([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)]),
            Polygon([(1, 0), (2, 0), (2, 1), (1, 1), (1, 0)]),
        ]
        result = unary_union(polys)
        assert result is not None
        assert not result.is_empty

    def test_unary_union_empty_raises(self):
        """unary_union on empty list raises ValueError."""
        with pytest.raises(ValueError):
            unary_union([])

    def test_unary_union_is_module_level(self):
        """unary_union is accessible at the togo module level."""
        assert callable(togo.unary_union)

    def test_unary_union_fragment_regression(self):
        """Regression: fragment polygons should not fail TG->GEOS conversion in unary_union."""
        frag1 = togo.from_wkt(
            "POLYGON((-0.04152989791889679 49.96284582619472,-0.05360208037804666 49.99472435266339,-0.0656902329731018 50.026601414028775,-0.07779440359234042 50.05847708901501,-0.08991461246576689 50.09035132352744,-0.10205089834700727 50.12222411693473,-0.11420330012085385 50.15409546618092,-0.12637185679209534 50.1859653682039,-0.05904346830566795 50.19654860260973,-0.04691701001683499 50.164671730344814,-0.034806638272464746 50.13279342311427,-0.022712314198252564 50.10091368395309,-0.010633999039577596 50.06903251589018,0.0014283458601545285 50.03714991943414,0.013474740623997256 50.00526594878062,0.02550520686919014 49.97338059420998,-0.04152989791889679 49.96284582619472))"
        )
        frag2 = togo.from_wkt(
            "POLYGON((-0.0012089070516528855 49.99472435266339,-0.01329705964670802 50.02660141402877,-0.02540123026594665 50.05847708901501,-0.037521439139401536 50.09035132352742,-0.04965772502064192 50.12222411693471,-0.061810126794488496 50.15409546618088,-0.07397868346575842 50.185965368203874,-0.006650294979330146 50.19654860260971,0.005476163309502818 50.16467173034479,0.01758653505390148 50.132793423114265,0.029680859128113662 50.10091368395308,0.04175917428681705 50.06903251589018,0.05382151918654918 50.03714991943415,0.06586791395036348 50.00526594878062,-0.0012089070516528855 49.99472435266339))"
        )

        result = unary_union([frag1, frag2])
        assert result is not None
        assert not result.is_empty
        assert result.geom_type in ("Polygon", "MultiPolygon")


# ---------------------------------------------------------------------------
# 2. LineString.project(point)
# ---------------------------------------------------------------------------


class TestLineStringProject:
    def test_project_start_point(self):
        """Project point at start of line returns 0."""
        line = LineString([(0, 0), (10, 0)])
        pt = Point(0, 0)
        dist = line.project(pt.as_geometry())
        assert dist == pytest.approx(0.0, abs=1e-9)

    def test_project_end_point(self):
        """Project point at end of line returns length of line."""
        line = LineString([(0, 0), (10, 0)])
        pt = Point(10, 0)
        dist = line.project(pt.as_geometry())
        assert dist == pytest.approx(10.0, abs=1e-9)

    def test_project_midpoint(self):
        """Project midpoint returns half the line length."""
        line = LineString([(0, 0), (10, 0)])
        pt = Point(5, 0)
        dist = line.project(pt.as_geometry())
        assert dist == pytest.approx(5.0, abs=1e-9)

    def test_project_perpendicular_point(self):
        """Project point perpendicular to line returns correct distance."""
        line = LineString([(0, 0), (10, 0)])
        # Point is above the midpoint
        pt = Point(5, 3)
        dist = line.project(pt.as_geometry())
        assert dist == pytest.approx(5.0, abs=1e-9)

    def test_project_accepts_point_directly(self):
        """project() accepts a Point wrapper object directly."""
        line = LineString([(0, 0), (10, 0)])
        pt = Point(4, 0)
        dist = line.project(pt)
        assert dist == pytest.approx(4.0, abs=1e-9)

    def test_project_returns_float(self):
        """project() returns a float."""
        line = LineString([(0, 0), (10, 0)])
        pt = Point(3, 0)
        dist = line.project(pt.as_geometry())
        assert isinstance(dist, float)

    def test_project_normalized_midpoint(self):
        """project(normalized=True) returns ~0.5 for the midpoint."""
        line = LineString([(0, 0), (10, 0)])
        pt = Point(5, 0)
        dist = line.project(pt.as_geometry(), normalized=True)
        assert dist == pytest.approx(0.5, abs=1e-9)

    def test_project_normalized_end_point(self):
        """project(normalized=True) returns ~1.0 for the end point."""
        line = LineString([(0, 0), (10, 0)])
        pt = Point(10, 0)
        dist = line.project(pt.as_geometry(), normalized=True)
        assert dist == pytest.approx(1.0, abs=1e-9)

    def test_project_normalized_start_point(self):
        """project(normalized=True) returns ~0.0 for the start point."""
        line = LineString([(0, 0), (10, 0)])
        pt = Point(0, 0)
        dist = line.project(pt.as_geometry(), normalized=True)
        assert dist == pytest.approx(0.0, abs=1e-9)

    def test_project_normalized_zero_length_line(self):
        """project(normalized=True) returns 0.0 for a zero-length line."""
        line = LineString([(5, 5), (5, 5)])
        pt = Point(5, 5)
        dist = line.project(pt.as_geometry(), normalized=True)
        assert dist == pytest.approx(0.0, abs=1e-9)


# ---------------------------------------------------------------------------
# 3. Polygon.intersects(other)
# ---------------------------------------------------------------------------


class TestPolygonIntersects:
    def test_intersects_overlapping_polygons(self):
        """Two overlapping polygons intersect."""
        p1 = Polygon([(0, 0), (2, 0), (2, 2), (0, 2), (0, 0)])
        p2 = Polygon([(1, 1), (3, 1), (3, 3), (1, 3), (1, 1)])
        assert p1.intersects(p2) is True

    def test_intersects_disjoint_polygons(self):
        """Two disjoint polygons do not intersect."""
        p1 = Polygon([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)])
        p2 = Polygon([(5, 5), (6, 5), (6, 6), (5, 6), (5, 5)])
        assert p1.intersects(p2) is False

    def test_intersects_with_geometry_object(self):
        """Polygon.intersects() accepts Geometry objects."""
        p1 = Polygon([(0, 0), (2, 0), (2, 2), (0, 2), (0, 0)])
        p2 = Geometry("POLYGON((1 1, 3 1, 3 3, 1 3, 1 1))", fmt="wkt")
        assert p1.intersects(p2) is True

    def test_intersects_with_polygon_wrapper(self):
        """Polygon.intersects() accepts another Polygon wrapper directly."""
        p1 = Polygon([(0, 0), (2, 0), (2, 2), (0, 2), (0, 0)])
        p2 = Polygon([(1, 1), (3, 1), (3, 3), (1, 3), (1, 1)])
        # Should work without manual as_geometry() conversion
        assert p1.intersects(p2) is True

    def test_intersects_touching_edge(self):
        """Polygons sharing an edge intersect (touch)."""
        p1 = Polygon([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)])
        p2 = Polygon([(1, 0), (2, 0), (2, 1), (1, 1), (1, 0)])
        # Touching at edge - intersects returns True for touching geometries
        assert p1.intersects(p2) is True


# ---------------------------------------------------------------------------
# 4. Polygon.boundary property
# ---------------------------------------------------------------------------


class TestPolygonBoundary:
    def test_boundary_is_linestring(self):
        """Polygon.boundary returns a LineString (Line) object."""
        p = Polygon([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)])
        b = p.boundary
        assert isinstance(b, Line)

    def test_boundary_has_correct_coords(self):
        """Polygon.boundary has the same coordinates as the exterior ring."""
        coords = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0), (0.0, 0.0)]
        p = Polygon(coords)
        b = p.boundary
        assert b.num_points == len(coords)

    def test_boundary_matches_exterior(self):
        """Polygon.boundary coordinates match the exterior ring."""
        coords = [(0.0, 0.0), (2.0, 0.0), (2.0, 3.0), (0.0, 3.0), (0.0, 0.0)]
        p = Polygon(coords)
        b = p.boundary
        b_coords = b.points(as_tuples=True)
        assert b_coords[0] == (0.0, 0.0)
        assert b_coords[1] == (2.0, 0.0)

    def test_boundary_available_on_poly(self):
        """Poly.boundary property also available on the base Poly class."""
        ring = Ring([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)])
        p = Poly(ring)
        assert hasattr(p, "boundary")
        b = p.boundary
        assert isinstance(b, Line)


# ---------------------------------------------------------------------------
# 5. Polygon.from_bounds(minx, miny, maxx, maxy)
# ---------------------------------------------------------------------------


class TestPolygonFromBounds:
    def test_from_bounds_returns_polygon(self):
        """from_bounds returns a Polygon instance."""
        p = Polygon.from_bounds(0, 0, 1, 1)
        assert isinstance(p, Polygon)

    def test_from_bounds_correct_bounds(self):
        """from_bounds creates a polygon with correct bounds."""
        minx, miny, maxx, maxy = 1.0, 2.0, 5.0, 7.0
        p = Polygon.from_bounds(minx, miny, maxx, maxy)
        bounds = p.bounds
        assert bounds[0] == pytest.approx(minx)
        assert bounds[1] == pytest.approx(miny)
        assert bounds[2] == pytest.approx(maxx)
        assert bounds[3] == pytest.approx(maxy)

    def test_from_bounds_correct_area(self):
        """from_bounds creates a polygon with correct area."""
        p = Polygon.from_bounds(0, 0, 4, 3)
        assert p.area == pytest.approx(12.0, rel=1e-6)

    def test_from_bounds_is_rectangle(self):
        """from_bounds creates a rectangular polygon (5 points including close)."""
        p = Polygon.from_bounds(0, 0, 1, 1)
        # Exterior ring should have 5 points (4 corners + closing point)
        assert p.exterior.num_points == 5

    def test_from_bounds_negative_coords(self):
        """from_bounds works with negative coordinates."""
        p = Polygon.from_bounds(-2, -3, 2, 3)
        bounds = p.bounds
        assert bounds[0] == pytest.approx(-2.0)
        assert bounds[1] == pytest.approx(-3.0)
        assert bounds[2] == pytest.approx(2.0)
        assert bounds[3] == pytest.approx(3.0)


# ---------------------------------------------------------------------------
# 6. Point.coords and LineString.coords indexable/sized
# ---------------------------------------------------------------------------


class TestCoordsIndexable:
    def test_point_coords_index_zero(self):
        """Point.coords[0] returns the (x, y) tuple."""
        p = Point(3.0, 4.0)
        assert p.coords[0] == (3.0, 4.0)

    def test_point_coords_len(self):
        """len(Point.coords) returns 1."""
        p = Point(1.0, 2.0)
        assert len(p.coords) == 1

    def test_point_coords_iterable(self):
        """Point.coords can be iterated."""
        p = Point(5.0, 6.0)
        coords_list = list(p.coords)
        assert coords_list == [(5.0, 6.0)]

    def test_linestring_coords_index_zero(self):
        """LineString.coords[0] returns the first coordinate."""
        line = LineString([(1.0, 2.0), (3.0, 4.0), (5.0, 6.0)])
        assert line.coords[0] == (1.0, 2.0)

    def test_linestring_coords_index_last(self):
        """LineString.coords[-1] returns the last coordinate."""
        line = LineString([(1.0, 2.0), (3.0, 4.0), (5.0, 6.0)])
        assert line.coords[-1] == (5.0, 6.0)

    def test_linestring_coords_len(self):
        """len(LineString.coords) returns the correct number of points."""
        line = LineString([(0, 0), (1, 0), (2, 0)])
        assert len(line.coords) == 3

    def test_linestring_coords_indexing(self):
        """LineString.coords supports arbitrary indexing."""
        pts = [(float(i), 0.0) for i in range(5)]
        line = LineString(pts)
        assert line.coords[2] == (2.0, 0.0)


# ---------------------------------------------------------------------------
# 7. Operations/predicates accept wrapper objects without as_geometry()
# ---------------------------------------------------------------------------


class TestPredicatesAcceptWrappers:
    def test_geometry_intersects_polygon_wrapper(self):
        """Geometry.intersects() accepts a Polygon wrapper directly."""
        g = Geometry("POLYGON((0 0, 2 0, 2 2, 0 2, 0 0))", fmt="wkt")
        p = Polygon([(1, 1), (3, 1), (3, 3), (1, 3), (1, 1)])
        assert g.intersects(p) is True

    def test_geometry_contains_point_wrapper(self):
        """Geometry.contains() accepts a Point wrapper directly."""
        g = Geometry("POLYGON((0 0, 4 0, 4 4, 0 4, 0 0))", fmt="wkt")
        pt = Point(2, 2)
        assert g.contains(pt) is True

    def test_geometry_within_polygon_wrapper(self):
        """Geometry.within() accepts a Polygon wrapper directly."""
        pt_geom = Geometry("POINT(2 2)", fmt="wkt")
        p = Polygon([(0, 0), (4, 0), (4, 4), (0, 4), (0, 0)])
        assert pt_geom.within(p) is True

    def test_geometry_touches_polygon_wrapper(self):
        """Geometry.touches() accepts a Polygon wrapper."""
        g = Geometry("POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))", fmt="wkt")
        p = Polygon([(1, 0), (2, 0), (2, 1), (1, 1), (1, 0)])
        # They touch at x=1
        assert g.touches(p) is True

    def test_geometry_disjoint_polygon_wrapper(self):
        """Geometry.disjoint() accepts a Polygon wrapper."""
        g = Geometry("POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))", fmt="wkt")
        p = Polygon([(5, 5), (6, 5), (6, 6), (5, 6), (5, 5)])
        assert g.disjoint(p) is True

    def test_geometry_equals_polygon_wrapper(self):
        """Geometry.equals() accepts a Polygon wrapper."""
        coords = [(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)]
        g = Geometry("POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))", fmt="wkt")
        p = Polygon(coords)
        assert g.equals(p) is True

    def test_geometry_intersection_polygon_wrapper(self):
        """Geometry.intersection() accepts a Polygon wrapper directly."""
        g = Geometry("POLYGON((0 0, 2 0, 2 2, 0 2, 0 0))", fmt="wkt")
        p = Polygon([(1, 1), (3, 1), (3, 3), (1, 3), (1, 1)])
        result = g.intersection(p)
        assert result.geom_type == "Polygon"
        assert result.area == pytest.approx(1.0, rel=1e-6)

    def test_geometry_difference_polygon_wrapper(self):
        """Geometry.difference() accepts a Polygon wrapper directly."""
        g = Geometry("POLYGON((0 0, 2 0, 2 2, 0 2, 0 0))", fmt="wkt")
        p = Polygon([(1, 1), (3, 1), (3, 3), (1, 3), (1, 1)])
        assert hasattr(g, "difference")
        result = getattr(g, "difference")(p)
        assert result.geom_type in ("Polygon", "MultiPolygon")
        assert result.area == pytest.approx(3.0, rel=1e-6)

    def test_module_difference_available(self):
        """difference is accessible at module level and behaves like shapely-style set op."""
        p1 = Polygon([(0, 0), (2, 0), (2, 2), (0, 2), (0, 0)])
        p2 = Polygon([(1, 1), (3, 1), (3, 3), (1, 3), (1, 1)])
        assert hasattr(togo, "difference")
        result = togo.difference(p1, p2)
        assert result.geom_type in ("Polygon", "MultiPolygon")
        assert result.area == pytest.approx(3.0, rel=1e-6)

    def test_polygon_intersects_no_manual_conversion(self):
        """Polygon.intersects() works on another Polygon without as_geometry()."""
        p1 = Polygon([(0, 0), (2, 0), (2, 2), (0, 2), (0, 0)])
        p2 = Polygon([(1, 1), (3, 1), (3, 3), (1, 3), (1, 1)])
        # This must work without any manual as_geometry() call
        result = p1.intersects(p2)
        assert result is True


# ---------------------------------------------------------------------------
# 8. MultiPolygon and MultiLineString are real Python classes
# ---------------------------------------------------------------------------


class TestMultiGeometryClasses:
    def test_multipolygon_is_class(self):
        """MultiPolygon is a real Python class (not a function)."""
        assert isinstance(MultiPolygon, type)

    def test_multilinestring_is_class(self):
        """MultiLineString is a real Python class (not a function)."""
        assert isinstance(MultiLineString, type)

    def test_multipolygon_isinstance(self):
        """isinstance(obj, MultiPolygon) works for MultiPolygon instances."""
        polys = [
            Poly(Ring([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)])),
            Poly(Ring([(2, 0), (3, 0), (3, 1), (2, 1), (2, 0)])),
        ]
        mp = MultiPolygon(polys)
        assert isinstance(mp, MultiPolygon)

    def test_multilinestring_isinstance(self):
        """isinstance(obj, MultiLineString) works for MultiLineString instances."""
        lines = [[(0, 0), (1, 1)], [(2, 2), (3, 3)]]
        mls = MultiLineString(lines)
        assert isinstance(mls, MultiLineString)

    def test_multipolygon_isinstance_geometry(self):
        """MultiPolygon instance is also an instance of Geometry."""
        polys = [Poly(Ring([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)]))]
        mp = MultiPolygon(polys)
        assert isinstance(mp, Geometry)

    def test_multilinestring_isinstance_geometry(self):
        """MultiLineString instance is also an instance of Geometry."""
        lines = [[(0, 0), (1, 1)]]
        mls = MultiLineString(lines)
        assert isinstance(mls, Geometry)

    def test_multipolygon_geom_type(self):
        """MultiPolygon instance has geom_type 'MultiPolygon'."""
        polys = [
            Poly(Ring([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)])),
        ]
        mp = MultiPolygon(polys)
        assert mp.geom_type == "MultiPolygon"

    def test_multilinestring_geom_type(self):
        """MultiLineString instance has geom_type 'MultiLineString'."""
        mls = MultiLineString([[(0, 0), (1, 1)]])
        assert mls.geom_type == "MultiLineString"

    def test_multipolygon_not_isinstance_multilinestring(self):
        """MultiPolygon instance is NOT an instance of MultiLineString."""
        polys = [Poly(Ring([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)]))]
        mp = MultiPolygon(polys)
        assert not isinstance(mp, MultiLineString)

    def test_multipolygon_from_polygons(self):
        """MultiPolygon can be created from Polygon wrapper objects."""
        polys = [
            Polygon([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)]),
            Polygon([(2, 0), (3, 0), (3, 1), (2, 1), (2, 0)]),
        ]
        mp = MultiPolygon(polys)
        assert isinstance(mp, MultiPolygon)
        assert mp.geom_type == "MultiPolygon"

    def test_multipolygon_no_args_is_empty(self):
        """No-arg MultiPolygon initializes to an empty geometry."""
        mp = MultiPolygon()
        assert mp.geom_type == "MultiPolygon"

    def test_multilinestring_no_args_is_empty(self):
        """No-arg MultiLineString initializes to an empty geometry."""
        mls = MultiLineString()
        assert mls.geom_type == "MultiLineString"


# ---------------------------------------------------------------------------
# 9. Geometry equality consistency
# ---------------------------------------------------------------------------


class TestGeometryEquality:
    def test_geometry_eq_same(self):
        """Two identical geometries are equal via ==."""
        g1 = Geometry("POINT(1 2)", fmt="wkt")
        g2 = Geometry("POINT(1 2)", fmt="wkt")
        assert g1 == g2

    def test_geometry_eq_different(self):
        """Two different geometries are not equal via ==."""
        g1 = Geometry("POINT(1 2)", fmt="wkt")
        g2 = Geometry("POINT(3 4)", fmt="wkt")
        assert g1 != g2

    def test_geometry_eq_polygon_wrapper(self):
        """Geometry equals Polygon wrapper with same coordinates."""
        g = Geometry("POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))", fmt="wkt")
        p = Polygon([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)])
        assert g == p

    def test_point_eq_point(self):
        """Two Points with identical coords are equal."""
        p1 = Point(1.0, 2.0)
        p2 = Point(1.0, 2.0)
        assert p1 == p2

    def test_point_neq_different_coords(self):
        """Two Points with different coords are not equal."""
        p1 = Point(1.0, 2.0)
        p2 = Point(3.0, 4.0)
        assert p1 != p2

    def test_point_eq_none(self):
        """Point != None."""
        p = Point(1.0, 2.0)
        assert p != None  # noqa: E711

    def test_geometry_eq_none(self):
        """Geometry != None."""
        g = Geometry("POINT(1 2)", fmt="wkt")
        assert g != None  # noqa: E711

    def test_point_hashable(self):
        """Points can be used as dict keys (are hashable)."""
        p = Point(1.0, 2.0)
        d = {p: "test"}
        assert d[p] == "test"

    def test_geometry_hashable(self):
        """Geometry objects can be used in sets."""
        g1 = Geometry("POINT(1 2)", fmt="wkt")
        g2 = Geometry("POINT(1 2)", fmt="wkt")
        s = {g1, g2}
        assert len(s) == 1  # same geometry, should deduplicate


# ---------------------------------------------------------------------------
# 11. Wrapper forwarding and Geometry protocol parity regressions
# ---------------------------------------------------------------------------


class TestWrapperAndProtocolParity:
    def test_polygon_wrapper_forwards_difference_equals_covers(self):
        left = Polygon([(0, 0), (3, 0), (3, 3), (0, 3), (0, 0)])
        right = Polygon([(2, 2), (4, 2), (4, 4), (2, 4), (2, 2)])

        diff = left.difference(right)
        assert diff.geom_type in {"Polygon", "MultiPolygon"}
        assert left.equals(left) is True
        assert left.covers(Point(1, 1)) is True

    def test_geometry_project_available_on_geometry_linestring(self):
        line_geom = Geometry("LINESTRING(0 0, 10 0)", fmt="wkt")

        distance = line_geom.project(Point(3, 4))
        normalized = line_geom.project(Point(3, 4), normalized=True)

        assert distance == pytest.approx(3.0, rel=1e-9)
        assert normalized == pytest.approx(0.3, rel=1e-9)

    def test_geometry_len_for_collections_and_multi(self):
        multipoly = MultiPolygon(
            [
                ([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)],),
                ([(2, 0), (3, 0), (3, 1), (2, 1), (2, 0)],),
            ]
        )

        assert len(multipoly) == 2
        assert len(multipoly.geoms) == 2

    def test_geometry_len_raises_for_non_collections(self):
        geom = Geometry("POINT(0 0)", fmt="wkt")
        with pytest.raises(TypeError):
            len(geom)

    def test_geometry_truthiness_uses_emptiness_not_len(self):
        non_empty = Geometry("LINESTRING(0 0, 1 1)", fmt="wkt")
        empty = Geometry("GEOMETRYCOLLECTION EMPTY", fmt="wkt")

        assert bool(non_empty) is True
        assert bool(empty) is False

    def test_singleton_geoms_available_for_single_part_results(self):
        line = LineString([(0, 0), (2, 0)])
        clip = Polygon([(1, -1), (3, -1), (3, 1), (1, 1), (1, -1)])

        result = line.intersection(clip)

        assert result.geom_type == "LineString"
        assert isinstance(result.geoms, tuple)
        assert len(result.geoms) == 1
        assert result.geoms[0].geom_type == "LineString"

    def test_polygon_exterior_is_linestring_compatible(self):
        polygon = Polygon([(0, 0), (2, 0), (2, 2), (0, 2), (0, 0)])

        assert isinstance(polygon.exterior, LineString)
        assert polygon.exterior.coords[0] == (0.0, 0.0)

    def test_from_geojson_materializes_multipolygon_class(self):
        geom = togo.from_geojson(
            '{"type":"MultiPolygon","coordinates":[[[[0,0],[1,0],[1,1],[0,1],[0,0]]]]}'
        )
        assert isinstance(geom, MultiPolygon)
        assert geom.geom_type == "MultiPolygon"

    def test_linestring_wrapper_forwards_difference(self):
        line = LineString([(0, 0), (5, 0)])
        clip = Polygon([(2, -1), (3, -1), (3, 1), (2, 1), (2, -1)])

        result = line.difference(clip)
        assert result.geom_type in {
            "LineString",
            "MultiLineString",
            "GeometryCollection",
        }

    def test_base_geometry_isinstance_for_single_geometries(self):
        point = Point(0, 0)
        polygon = Polygon([(0, 0), (1, 0), (1, 1), (0, 0)])

        assert isinstance(point, BaseGeometry)
        assert isinstance(polygon, BaseGeometry)

    def test_shape_materializes_polygon_and_multipolygon_concrete_types(self):
        polygon = shape(
            {
                "type": "Polygon",
                "coordinates": [[(0, 0), (1, 0), (1, 1), (0, 0)]],
            }
        )
        multipolygon = shape(
            {
                "type": "MultiPolygon",
                "coordinates": [
                    [[(0, 0), (1, 0), (1, 1), (0, 0)]],
                    [[(2, 2), (3, 2), (3, 3), (2, 2)]],
                ],
            }
        )

        assert isinstance(polygon, Polygon)
        assert isinstance(multipolygon, MultiPolygon)
        assert isinstance(multipolygon, BaseGeometry)

    def test_centroid_materializes_point_with_xy_accessors(self):
        geom = shape(
            {
                "type": "Polygon",
                "coordinates": [[(0, 0), (1, 0), (1, 1), (0, 0)]],
            }
        )

        centroid = geom.centroid

        assert isinstance(centroid, Point)
        assert hasattr(centroid, "x") and hasattr(centroid, "y")

    def test_line_boundary_geoms_materialize_points(self):
        line = LineString([(1, 2), (5, 2), (8, 9)])
        endpoints = line.boundary.geoms

        assert len(endpoints) == 2
        assert isinstance(endpoints[0], Point)
        assert isinstance(endpoints[1], Point)
        assert (endpoints[0].x, endpoints[0].y) == (1.0, 2.0)
        assert (endpoints[1].x, endpoints[1].y) == (8.0, 9.0)
