"""
Tests for convex_hull property and function implementations in togo
"""

import pytest
from togo import Point, LineString, Polygon, Geometry, MultiPoint, convex_hull


class TestGeometryConvexHull:
    """Test Geometry.convex_hull property"""

    def test_geometry_convex_hull_polygon(self):
        """Test convex hull of a concave polygon"""
        # Create a concave polygon (star-like shape)
        geom = Geometry("POLYGON((0 0, 2 0, 2 2, 1 1, 0 2, 0 0))", fmt="wkt")
        hull = geom.convex_hull
        assert hull is not None
        assert hull.geom_type == "Polygon"
        # Convex hull should contain the original geometry
        assert hull.contains(geom)
        # Convex hull should have greater or equal area
        assert hull.area >= geom.area

    def test_geometry_convex_hull_simple_polygon(self):
        """Test convex hull of an already convex polygon"""
        # Square is already convex
        geom = Geometry("POLYGON((0 0, 4 0, 4 4, 0 4, 0 0))", fmt="wkt")
        hull = geom.convex_hull
        assert hull is not None
        assert hull.geom_type == "Polygon"
        # Convex hull of convex polygon should have same area
        assert abs(hull.area - geom.area) < 0.0001

    def test_geometry_convex_hull_point(self):
        """Test convex hull of a point"""
        geom = Geometry("POINT(1 2)", fmt="wkt")
        hull = geom.convex_hull
        assert hull is not None
        assert hull.geom_type == "Point"
        # Should return the same point
        assert hull.to_wkt() == "POINT(1 2)"

    def test_geometry_convex_hull_linestring(self):
        """Test convex hull of a linestring"""
        geom = Geometry("LINESTRING(0 0, 1 1, 2 0)", fmt="wkt")
        hull = geom.convex_hull
        assert hull is not None
        # Convex hull of 3 non-collinear points should be a polygon (triangle)
        assert hull.geom_type == "Polygon"
        # Hull should have some area (it's a triangle)
        assert hull.area > 0

    def test_geometry_convex_hull_collinear_points(self):
        """Test convex hull of collinear points"""
        geom = Geometry("LINESTRING(0 0, 1 1, 2 2)", fmt="wkt")
        hull = geom.convex_hull
        assert hull is not None
        # Convex hull of collinear points is a line
        assert hull.geom_type == "LineString"

    def test_geometry_convex_hull_multipoint(self):
        """Test convex hull of scattered points"""
        points = [(0, 0), (1, 1), (0, 2), (2, 2), (3, 1), (1, 0)]
        geom = MultiPoint(points)
        hull = geom.convex_hull
        assert hull is not None
        assert hull.geom_type == "Polygon"
        # All original points should be on or inside the hull
        for x, y in points:
            pt = Point(x, y).as_geometry()
            assert hull.contains(pt) or hull.touches(pt)


class TestPointConvexHull:
    """Test Point.convex_hull property"""

    def test_point_convex_hull(self):
        """Test convex hull of a Point"""
        p = Point(3.5, 4.5)
        hull = p.convex_hull
        assert hull is not None
        assert hull.geom_type == "Point"
        # Check WKT representation contains correct coordinates
        wkt = hull.to_wkt()
        assert "3.5" in wkt
        assert "4.5" in wkt


class TestLineStringConvexHull:
    """Test LineString.convex_hull property"""

    def test_linestring_convex_hull_triangle(self):
        """Test convex hull of a triangle-like linestring"""
        line = LineString([(0, 0), (2, 0), (1, 2)])
        hull = line.convex_hull
        assert hull is not None
        assert hull.geom_type == "Polygon"
        # Should form a triangle
        assert hull.area > 0

    def test_linestring_convex_hull_straight(self):
        """Test convex hull of a straight line"""
        line = LineString([(0, 0), (1, 1), (2, 2)])
        hull = line.convex_hull
        assert hull is not None
        # Collinear points result in a linestring
        assert hull.geom_type == "LineString"

    def test_linestring_convex_hull_zigzag(self):
        """Test convex hull of a zigzag line"""
        line = LineString([(0, 0), (1, 1), (2, 0), (3, 1), (4, 0)])
        hull = line.convex_hull
        assert hull is not None
        assert hull.geom_type == "Polygon"
        # Hull should have area greater than zero
        assert hull.area > 0


class TestPolygonConvexHull:
    """Test Polygon.convex_hull property"""

    def test_polygon_convex_hull_concave(self):
        """Test convex hull of a concave polygon"""
        # L-shaped polygon (concave)
        exterior = [(0, 0), (2, 0), (2, 1), (1, 1), (1, 2), (0, 2), (0, 0)]
        poly = Polygon(exterior)
        hull = poly.convex_hull
        assert hull is not None
        assert hull.geom_type == "Polygon"
        # Hull should be larger than original
        assert hull.area >= poly.area
        # Hull should contain original polygon
        assert hull.contains(poly.as_geometry())

    def test_polygon_convex_hull_with_hole(self):
        """Test convex hull of polygon with hole"""
        exterior = [(0, 0), (10, 0), (10, 10), (0, 10), (0, 0)]
        hole = [(2, 2), (8, 2), (8, 8), (2, 8), (2, 2)]
        poly = Polygon(exterior, holes=[hole])
        hull = poly.convex_hull
        assert hull is not None
        assert hull.geom_type == "Polygon"
        # Convex hull should only consider the outer boundary
        # Expected area should be close to 10*10 = 100 (ignoring the hole)
        assert abs(hull.area - 100.0) < 0.1

    def test_polygon_convex_hull_rectangle(self):
        """Test convex hull of a rectangle (already convex)"""
        poly = Polygon([(0, 0), (5, 0), (5, 3), (0, 3), (0, 0)])
        hull = poly.convex_hull
        assert hull is not None
        assert hull.geom_type == "Polygon"
        # Rectangle is already convex, so areas should match
        assert abs(hull.area - poly.area) < 0.0001


class TestModuleLevelConvexHull:
    """Test module-level convex_hull() function"""

    def test_convex_hull_function_polygon(self):
        """Test convex_hull() function with Polygon"""
        poly = Polygon(
            [
                (0, 0),
                (2, 0),
                (
                    2,
                    2,
                ),
                (1, 1),
                (0, 2),
                (0, 0),
            ]
        )
        hull = convex_hull(poly)
        assert hull is not None
        assert hull.geom_type == "Polygon"
        assert hull.contains(poly.as_geometry())

    def test_convex_hull_function_point(self):
        """Test convex_hull() function with Point"""
        p = Point(1.5, 2.5)
        hull = convex_hull(p)
        assert hull is not None
        assert hull.geom_type == "Point"
        wkt = hull.to_wkt()
        assert "1.5" in wkt
        assert "2.5" in wkt

    def test_convex_hull_function_linestring(self):
        """Test convex_hull() function with LineString"""
        line = LineString([(0, 0), (1, 2), (2, 0)])
        hull = convex_hull(line)
        assert hull is not None
        assert hull.geom_type == "Polygon"
        # Hull should have area greater than 0
        assert hull.area > 0

    def test_convex_hull_function_multipoint(self):
        """Test convex_hull() function with MultiPoint"""
        mp = MultiPoint([(0, 0), (1, 0), (1, 1), (0, 1)])
        hull = convex_hull(mp)
        assert hull is not None
        assert hull.geom_type == "Polygon"
        # Should form a square
        assert abs(hull.area - 1.0) < 0.0001

    def test_convex_hull_function_geometry(self):
        """Test convex_hull() function with base Geometry class"""
        geom = Geometry("MULTIPOINT((0 0), (3 0), (3 3), (0 3))", fmt="wkt")
        hull = convex_hull(geom)
        assert hull is not None
        assert hull.geom_type == "Polygon"
        # Should form a square with area 9
        assert abs(hull.area - 9.0) < 0.1

    def test_convex_hull_function_invalid_input(self):
        """Test convex_hull() function with invalid input"""
        with pytest.raises(TypeError):
            convex_hull(None)
        with pytest.raises(TypeError):
            convex_hull("not a geometry")
        with pytest.raises(TypeError):
            convex_hull(42)


class TestConvexHullEdgeCases:
    """Test edge cases for convex hull"""

    def test_convex_hull_two_points(self):
        """Test convex hull of exactly two points"""
        geom = Geometry("LINESTRING(0 0, 1 1)", fmt="wkt")
        hull = geom.convex_hull
        assert hull is not None
        # Two points should result in a linestring
        assert hull.geom_type == "LineString"

    def test_convex_hull_complex_polygon(self):
        """Test convex hull of complex concave polygon"""
        # Star-like polygon
        exterior = [
            (0, 0),
            (1, 0),
            (1.5, -1),
            (2, 0),
            (3, 0),
            (2, 1),
            (2.5, 2),
            (1.5, 1),
            (1, 2),
            (0.5, 1),
            (0, 0),
        ]
        poly = Polygon(exterior)
        hull = poly.convex_hull
        assert hull is not None
        assert hull.geom_type == "Polygon"
        # Hull should contain original polygon
        assert hull.contains(poly.as_geometry())
        # Hull area should be >= original area
        assert hull.area >= poly.area

    def test_convex_hull_preserves_type_for_point(self):
        """Test that convex hull of a single point is still a point"""
        geom = Geometry("POINT(5 5)", fmt="wkt")
        hull = geom.convex_hull
        assert hull.geom_type == "Point"
        # Verify coordinates are preserved
        assert "POINT(5 5)" in hull.to_wkt()
