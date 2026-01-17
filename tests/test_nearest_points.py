"""
Test suite for nearest_points method
"""

import pytest
from togo import Geometry, Point, LineString, Polygon


class TestNearestPoints:
    """Test nearest_points method"""

    def test_nearest_points_point_to_point(self):
        """Test nearest_points between two points"""
        p1 = Point(0, 0)
        p2 = Point(3, 4)

        np = p1.nearest_points(p2)

        assert isinstance(np, tuple)
        assert len(np) == 2
        assert np[0].x == 0.0
        assert np[0].y == 0.0
        assert np[1].x == 3.0
        assert np[1].y == 4.0

    def test_nearest_points_point_to_point_same(self):
        """Test nearest_points between the same point"""
        p = Point(1.5, 2.5)

        np = p.nearest_points(p)

        assert np[0].x == p.x
        assert np[0].y == p.y
        assert np[1].x == p.x
        assert np[1].y == p.y

    def test_nearest_points_point_to_line(self):
        """Test nearest_points between a point and a line"""
        point = Point(0, 0)
        line = LineString([(1, 1), (2, 2), (3, 3)])

        np = point.nearest_points(line)

        # The nearest point on the line to (0, 0) should be (1, 1)
        assert np[0].x == 0.0
        assert np[0].y == 0.0
        # The nearest point should be close to (1, 1)
        assert abs(np[1].x - 1.0) < 0.01
        assert abs(np[1].y - 1.0) < 0.01

    def test_nearest_points_point_to_polygon(self):
        """Test nearest_points between a point and a polygon"""
        point = Point(0, 0)
        poly = Polygon([(1, 1), (3, 1), (3, 3), (1, 3), (1, 1)])

        np = point.nearest_points(poly)

        # The nearest point on the polygon to (0, 0) should be (1, 1)
        assert np[0].x == 0.0
        assert np[0].y == 0.0
        assert abs(np[1].x - 1.0) < 0.01
        assert abs(np[1].y - 1.0) < 0.01

    def test_nearest_points_line_to_line(self):
        """Test nearest_points between two lines"""
        line1 = LineString([(0, 0), (1, 1)])
        line2 = LineString([(2, 0), (2, 1)])

        np = line1.nearest_points(line2)

        # One point should be on line1, the other on line2
        assert isinstance(np[0], Point)
        assert isinstance(np[1], Point)

    def test_nearest_points_geometry_from_wkt(self):
        """Test nearest_points with geometries created from WKT"""
        g1 = Geometry("POINT(0 0)", fmt="wkt")
        g2 = Geometry("POINT(3 4)", fmt="wkt")

        np = g1.nearest_points(g2)

        assert len(np) == 2
        assert np[0].x == 0.0
        assert np[0].y == 0.0
        assert np[1].x == 3.0
        assert np[1].y == 4.0

    def test_nearest_points_invalid_other(self):
        """Test that nearest_points raises error with invalid geometry"""
        point = Point(0, 0)

        with pytest.raises(ValueError):
            point.nearest_points(None)

        with pytest.raises(ValueError):
            point.nearest_points("not a geometry")

    def test_nearest_points_polygon_to_polygon(self):
        """Test nearest_points between two polygons"""
        poly1 = Polygon([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)])
        poly2 = Polygon([(2, 0), (3, 0), (3, 1), (2, 1), (2, 0)])

        np = poly1.nearest_points(poly2)

        # Should have two points
        assert len(np) == 2
        assert isinstance(np[0], Point)
        assert isinstance(np[1], Point)
        # The nearest points should be on the edges facing each other
        # (1, 0) to (2, 0) or similar
        assert np[0].x <= 1.0 or abs(np[0].x - 1.0) < 0.01
        assert np[1].x >= 2.0 or abs(np[1].x - 2.0) < 0.01

    def test_nearest_points_symmetric(self):
        """Test that nearest_points is symmetric"""
        g1 = Geometry("POINT(0 0)", fmt="wkt")
        g2 = Geometry("POINT(3 4)", fmt="wkt")

        np1 = g1.nearest_points(g2)
        np2 = g2.nearest_points(g1)

        # The points should be swapped but coordinates should match
        assert abs(np1[0].x - np2[1].x) < 1e-10
        assert abs(np1[0].y - np2[1].y) < 1e-10
        assert abs(np1[1].x - np2[0].x) < 1e-10
        assert abs(np1[1].y - np2[0].y) < 1e-10

    def test_nearest_points_overlapping_geometries(self):
        """Test nearest_points with overlapping geometries"""
        poly1 = Polygon([(0, 0), (2, 0), (2, 2), (0, 2), (0, 0)])
        poly2 = Polygon([(1, 1), (3, 1), (3, 3), (1, 3), (1, 1)])

        np = poly1.nearest_points(poly2)

        # Should have two points
        assert len(np) == 2
        assert isinstance(np[0], Point)
        assert isinstance(np[1], Point)

    def test_nearest_points_point_inside_polygon(self):
        """Test nearest_points with a point inside a polygon"""
        point = Point(1.5, 1.5)
        poly = Polygon([(0, 0), (3, 0), (3, 3), (0, 3), (0, 0)])

        np = point.nearest_points(poly)

        # The nearest point on the polygon to an interior point should be on the boundary
        assert isinstance(np[0], Point)
        assert isinstance(np[1], Point)
