"""Tests for shortest_line method"""

import pytest
from togo import Point, LineString, Polygon, Ring, Geometry, from_wkt, shortest_line


class TestShortestLine:
    """Test shortest_line functionality"""

    def test_shortest_line_point_to_point(self):
        """Test shortest_line between two points"""
        p1 = Point(0, 0)
        p2 = Point(3, 4)

        line = p1.shortest_line(p2)

        assert line is not None
        assert line.geom_type == "LineString"
        assert line.num_points == 2

        coords = line.coords
        assert coords[0] == (0.0, 0.0)
        assert coords[1] == (3.0, 4.0)

        # Length should be 5 (3-4-5 triangle)
        assert abs(line.length - 5.0) < 1e-10

    def test_shortest_line_point_to_line(self):
        """Test shortest_line from point to line"""
        point = Point(0, 0)
        line_geom = LineString([(10, 0), (10, 10)])

        result = point.shortest_line(line_geom)

        assert result is not None
        assert result.geom_type == "LineString"
        assert result.num_points == 2

        coords = result.coords
        # First point should be from the point (0, 0)
        assert coords[0] == (0.0, 0.0)
        # Second point should be on the line at (10, 0)
        assert coords[1] == (10.0, 0.0)

        # Length should be 10
        assert abs(result.length - 10.0) < 1e-10

    def test_shortest_line_point_to_polygon(self):
        """Test shortest_line from point to polygon"""
        point = Point(0, 0)
        exterior = Ring([(10, 0), (15, 0), (15, 5), (10, 5), (10, 0)])
        poly = Polygon(exterior)

        result = point.shortest_line(poly)

        assert result is not None
        assert result.geom_type == "LineString"
        assert result.num_points == 2

        coords = result.coords
        # First point should be from the point
        assert coords[0] == (0.0, 0.0)
        # Second point should be nearest point on polygon (10, 0)
        assert coords[1] == (10.0, 0.0)

        # Length should be 10
        assert abs(result.length - 10.0) < 1e-10

    def test_shortest_line_line_to_line(self):
        """Test shortest_line between two lines"""
        line1 = LineString([(0, 0), (0, 10)])
        line2 = LineString([(10, 0), (10, 10)])

        result = line1.shortest_line(line2)

        assert result is not None
        assert result.geom_type == "LineString"
        assert result.num_points == 2

        coords = result.coords
        # The shortest distance between parallel lines at x=0 and x=10
        # Should be a horizontal line at some y
        assert coords[0][0] == 0.0
        assert coords[1][0] == 10.0

        # Length should be 10
        assert abs(result.length - 10.0) < 1e-10

    def test_shortest_line_polygon_to_polygon(self):
        """Test shortest_line between two polygons"""
        exterior1 = Ring([(0, 0), (5, 0), (5, 5), (0, 5), (0, 0)])
        poly1 = Polygon(exterior1)

        exterior2 = Ring([(10, 0), (15, 0), (15, 5), (10, 5), (10, 0)])
        poly2 = Polygon(exterior2)

        result = poly1.shortest_line(poly2)

        assert result is not None
        assert result.geom_type == "LineString"
        assert result.num_points == 2

        # Should connect the nearest corners/edges
        # Distance should be 5 (from x=5 to x=10)
        assert abs(result.length - 5.0) < 1e-10

    def test_shortest_line_intersecting_geometries(self):
        """Test shortest_line with intersecting geometries (distance = 0)"""
        line1 = LineString([(0, 0), (10, 10)])
        line2 = LineString([(0, 10), (10, 0)])

        result = line1.shortest_line(line2)

        assert result is not None
        assert result.geom_type == "LineString"
        assert result.num_points == 2

        # Lines intersect at (5, 5), so shortest line should have length 0
        assert result.length < 1e-10

        coords = result.coords
        # Both points should be at or very near the intersection
        assert abs(coords[0][0] - coords[1][0]) < 1e-10
        assert abs(coords[0][1] - coords[1][1]) < 1e-10

    def test_shortest_line_with_geometry_class(self):
        """Test shortest_line with Geometry class objects"""
        g1 = Geometry("POINT(0 0)", fmt="wkt")
        g2 = Geometry("POINT(3 4)", fmt="wkt")

        result = g1.shortest_line(g2)

        assert result is not None
        assert result.geom_type == "LineString"
        assert result.num_points == 2

        # Length should be 5 (3-4-5 triangle)
        assert abs(result.length - 5.0) < 1e-10

    def test_shortest_line_from_wkt(self):
        """Test shortest_line with geometries created from WKT"""
        g1 = from_wkt("POINT(0 0)")
        g2 = from_wkt("LINESTRING(10 0, 10 10)")

        result = g1.shortest_line(g2)

        assert result is not None
        coords = result.coords
        assert coords[0] == (0.0, 0.0)
        assert coords[1] == (10.0, 0.0)
        assert abs(result.length - 10.0) < 1e-10

    def test_shortest_line_invalid_other(self):
        """Test that shortest_line raises error with invalid geometry"""
        point = Point(0, 0)

        with pytest.raises(ValueError):
            point.shortest_line(None)

        with pytest.raises(ValueError):
            point.shortest_line("not a geometry")

    def test_shortest_line_ring_to_point(self):
        """Test shortest_line from ring to point"""
        ring = Ring([(0, 0), (10, 0), (10, 10), (0, 10), (0, 0)])
        point = Point(15, 5)

        result = ring.shortest_line(point)

        assert result is not None
        assert result.geom_type == "LineString"
        assert result.num_points == 2

        coords = result.coords
        # Should connect from ring edge at (10, 5) to point at (15, 5)
        assert coords[0] == (10.0, 5.0)
        assert coords[1] == (15.0, 5.0)
        assert abs(result.length - 5.0) < 1e-10

    def test_shortest_line_symmetry(self):
        """Test that shortest_line is symmetric (same length both ways)"""
        p1 = Point(0, 0)
        p2 = Point(3, 4)

        line1 = p1.shortest_line(p2)
        line2 = p2.shortest_line(p1)

        # Both should have the same length
        assert abs(line1.length - line2.length) < 1e-10

        # The lines should connect the same points (just reversed)
        coords1 = line1.coords
        coords2 = line2.coords

        assert coords1[0] == coords2[1]
        assert coords1[1] == coords2[0]

    def test_shortest_line_module_level_function(self):
        """Test module-level shortest_line function (Shapely v2 API)"""
        p1 = Point(0, 0)
        p2 = Point(3, 4)

        # Module-level function
        line = shortest_line(p1, p2)
        assert line is not None
        assert line.geom_type == "LineString"
        assert abs(line.length - 5.0) < 1e-10

        # Should give same result as method
        line_method = p1.shortest_line(p2)
        assert abs(line.length - line_method.length) < 1e-10

    def test_shortest_line_module_level_with_wkt(self):
        """Test module-level shortest_line with WKT geometries"""
        g1 = from_wkt("POINT(0 0)")
        g2 = from_wkt("LINESTRING(10 0, 10 10)")

        line = shortest_line(g1, g2)
        assert line is not None
        assert abs(line.length - 10.0) < 1e-10
