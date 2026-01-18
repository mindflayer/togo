"""
Tests for intersection() method and function implementations in togo
"""

import pytest
from togo import (
    Point,
    LineString,
    Polygon,
    Ring,
    Geometry,
    MultiPolygon,
    intersection,
)


class TestGeometryIntersection:
    """Test Geometry.intersection method"""

    def test_geometry_intersection_overlapping_polygons(self):
        """Test intersection of two overlapping polygons"""
        poly1 = Geometry("POLYGON((0 0, 2 0, 2 2, 0 2, 0 0))", fmt="wkt")
        poly2 = Geometry("POLYGON((1 1, 3 1, 3 3, 1 3, 1 1))", fmt="wkt")
        result = poly1.intersection(poly2)
        assert result is not None
        assert result.geom_type == "Polygon"
        # Intersection should be a 1x1 square
        assert abs(result.area - 1.0) < 0.0001

    def test_geometry_intersection_non_overlapping_polygons(self):
        """Test intersection of non-overlapping polygons returns empty"""
        poly1 = Geometry("POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))", fmt="wkt")
        poly2 = Geometry("POLYGON((2 2, 3 2, 3 3, 2 3, 2 2))", fmt="wkt")
        result = poly1.intersection(poly2)
        assert result is not None
        # Should be empty or have zero area
        assert result.is_empty or result.area == 0.0

    def test_geometry_intersection_touching_polygons(self):
        """Test intersection of polygons that touch at an edge"""
        poly1 = Geometry("POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))", fmt="wkt")
        poly2 = Geometry("POLYGON((1 0, 2 0, 2 1, 1 1, 1 0))", fmt="wkt")
        result = poly1.intersection(poly2)
        assert result is not None
        # Should be a line (edge)
        assert result.geom_type in ["LineString", "Point"]

    def test_geometry_intersection_point_in_polygon(self):
        """Test intersection of point inside polygon"""
        point = Geometry("POINT(1 1)", fmt="wkt")
        poly = Geometry("POLYGON((0 0, 2 0, 2 2, 0 2, 0 0))", fmt="wkt")
        result = point.intersection(poly)
        assert result is not None
        assert result.geom_type == "Point"
        # Should return the point itself
        assert result.to_wkt() == "POINT(1 1)"

    def test_geometry_intersection_point_outside_polygon(self):
        """Test intersection of point outside polygon"""
        point = Geometry("POINT(5 5)", fmt="wkt")
        poly = Geometry("POLYGON((0 0, 2 0, 2 2, 0 2, 0 0))", fmt="wkt")
        result = point.intersection(poly)
        assert result is not None
        # Should be empty
        assert result.is_empty

    def test_geometry_intersection_line_polygon(self):
        """Test intersection of line crossing polygon"""
        line = Geometry("LINESTRING(0 1, 3 1)", fmt="wkt")
        poly = Geometry("POLYGON((1 0, 2 0, 2 2, 1 2, 1 0))", fmt="wkt")
        result = line.intersection(poly)
        assert result is not None
        assert result.geom_type == "LineString"
        # The intersection should be the segment from (1,1) to (2,1)
        assert abs(result.length - 1.0) < 0.0001

    def test_geometry_intersection_identical_geometries(self):
        """Test intersection of identical geometries"""
        poly = Geometry("POLYGON((0 0, 2 0, 2 2, 0 2, 0 0))", fmt="wkt")
        result = poly.intersection(poly)
        assert result is not None
        assert result.geom_type == "Polygon"
        # Should have same area as original
        assert abs(result.area - poly.area) < 0.0001

    def test_geometry_intersection_none_raises_error(self):
        """Test that intersection with None raises TypeError"""
        geom = Geometry("POINT(0 0)", fmt="wkt")
        with pytest.raises(TypeError):
            geom.intersection(None)

    def test_geometry_intersection_invalid_type_raises_error(self):
        """Test that intersection with invalid type raises TypeError"""
        geom = Geometry("POINT(0 0)", fmt="wkt")
        with pytest.raises(TypeError):
            geom.intersection("not a geometry")


class TestPointIntersection:
    """Test Point.intersection method"""

    def test_point_intersection_with_point_same(self):
        """Test intersection of identical points"""
        p1 = Point(1, 2)
        p2 = Point(1, 2)
        result = p1.intersection(p2)
        assert result is not None
        assert result.geom_type == "Point"

    def test_point_intersection_with_point_different(self):
        """Test intersection of different points"""
        p1 = Point(1, 2)
        p2 = Point(3, 4)
        result = p1.intersection(p2)
        assert result is not None
        assert result.is_empty

    def test_point_intersection_with_polygon_inside(self):
        """Test intersection of point inside polygon"""
        p = Point(1, 1)
        poly = Polygon([(0, 0), (2, 0), (2, 2), (0, 2), (0, 0)])
        result = p.intersection(poly)
        assert result is not None
        assert result.geom_type == "Point"

    def test_point_intersection_with_polygon_outside(self):
        """Test intersection of point outside polygon"""
        p = Point(5, 5)
        poly = Polygon([(0, 0), (2, 0), (2, 2), (0, 2), (0, 0)])
        result = p.intersection(poly)
        assert result is not None
        assert result.is_empty

    def test_point_intersection_with_linestring_on_line(self):
        """Test intersection of point on linestring"""
        p = Point(1, 1)
        line = LineString([(0, 0), (2, 2)])
        result = p.intersection(line)
        assert result is not None
        # Should return the point
        assert result.geom_type == "Point"

    def test_point_intersection_none_raises_error(self):
        """Test that intersection with None raises ValueError"""
        p = Point(0, 0)
        with pytest.raises(ValueError):
            p.intersection(None)


class TestLineStringIntersection:
    """Test LineString.intersection method"""

    def test_linestring_intersection_crossing_lines(self):
        """Test intersection of two crossing lines"""
        line1 = LineString([(0, 0), (2, 2)])
        line2 = LineString([(0, 2), (2, 0)])
        result = line1.intersection(line2)
        assert result is not None
        # Should be a point at (1, 1)
        assert result.geom_type == "Point"

    def test_linestring_intersection_parallel_lines(self):
        """Test intersection of parallel lines"""
        line1 = LineString([(0, 0), (2, 0)])
        line2 = LineString([(0, 1), (2, 1)])
        result = line1.intersection(line2)
        assert result is not None
        assert result.is_empty

    def test_linestring_intersection_overlapping_lines(self):
        """Test intersection of overlapping lines"""
        line1 = LineString([(0, 0), (2, 0)])
        line2 = LineString([(1, 0), (3, 0)])
        result = line1.intersection(line2)
        assert result is not None
        assert result.geom_type == "LineString"
        # Should overlap from (1, 0) to (2, 0)
        assert abs(result.length - 1.0) < 0.0001

    def test_linestring_intersection_with_polygon(self):
        """Test intersection of linestring with polygon"""
        line = LineString([(0, 1), (3, 1)])
        poly = Polygon([(1, 0), (2, 0), (2, 2), (1, 2), (1, 0)])
        result = line.intersection(poly)
        assert result is not None
        assert result.geom_type == "LineString"
        # Should be segment from (1, 1) to (2, 1)
        assert abs(result.length - 1.0) < 0.0001

    def test_linestring_intersection_none_raises_error(self):
        """Test that intersection with None raises ValueError"""
        line = LineString([(0, 0), (1, 1)])
        with pytest.raises(ValueError):
            line.intersection(None)


class TestPolygonIntersection:
    """Test Polygon.intersection method"""

    def test_polygon_intersection_overlapping(self):
        """Test intersection of overlapping polygons"""
        poly1 = Polygon([(0, 0), (2, 0), (2, 2), (0, 2), (0, 0)])
        poly2 = Polygon([(1, 1), (3, 1), (3, 3), (1, 3), (1, 1)])
        result = poly1.intersection(poly2)
        assert result is not None
        assert result.geom_type == "Polygon"
        # Should be 1x1 square
        assert abs(result.area - 1.0) < 0.0001

    def test_polygon_intersection_one_inside_other(self):
        """Test intersection when one polygon is inside another"""
        poly1 = Polygon([(0, 0), (4, 0), (4, 4), (0, 4), (0, 0)])
        poly2 = Polygon([(1, 1), (2, 1), (2, 2), (1, 2), (1, 1)])
        result = poly1.intersection(poly2)
        assert result is not None
        assert result.geom_type == "Polygon"
        # Should be the smaller polygon
        assert abs(result.area - 1.0) < 0.0001

    def test_polygon_intersection_disjoint(self):
        """Test intersection of disjoint polygons"""
        poly1 = Polygon([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)])
        poly2 = Polygon([(5, 5), (6, 5), (6, 6), (5, 6), (5, 5)])
        result = poly1.intersection(poly2)
        assert result is not None
        assert result.is_empty or result.area == 0.0

    def test_polygon_intersection_complex_shape(self):
        """Test intersection resulting in complex shape"""
        # Two overlapping squares at angle
        poly1 = Polygon([(0, 0), (3, 0), (3, 3), (0, 3), (0, 0)])
        poly2 = Polygon([(1, 1), (4, 1), (4, 4), (1, 4), (1, 1)])
        result = poly1.intersection(poly2)
        assert result is not None
        assert result.geom_type == "Polygon"
        # Should be 2x2 square
        assert abs(result.area - 4.0) < 0.0001

    def test_polygon_intersection_with_hole(self):
        """Test intersection preserves holes correctly"""
        # Polygon with hole
        exterior = [(0, 0), (4, 0), (4, 4), (0, 4), (0, 0)]
        hole = [(1, 1), (3, 1), (3, 3), (1, 3), (1, 1)]
        poly1 = Polygon(exterior, holes=[hole])
        # Polygon that overlaps part of the donut
        poly2 = Polygon([(2, 0), (6, 0), (6, 4), (2, 4), (2, 0)])
        result = poly1.intersection(poly2)
        assert result is not None
        # Result should account for the hole
        assert result.area > 0
        assert result.area < 8.0  # Less than full 2x4 rectangle

    def test_polygon_intersection_none_raises_error(self):
        """Test that intersection with None raises ValueError"""
        poly = Polygon([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)])
        with pytest.raises(ValueError):
            poly.intersection(None)


class TestRingIntersection:
    """Test Ring.intersection method"""

    def test_ring_intersection_with_polygon(self):
        """Test intersection of ring with polygon"""
        ring = Ring([(0, 0), (2, 0), (2, 2), (0, 2), (0, 0)])
        poly = Polygon([(1, 1), (3, 1), (3, 3), (1, 3), (1, 1)])
        result = ring.intersection(poly)
        assert result is not None
        assert result.geom_type == "Polygon"
        # Should be 1x1 square
        assert abs(result.area - 1.0) < 0.0001

    def test_ring_intersection_with_point(self):
        """Test intersection of ring with point"""
        ring = Ring([(0, 0), (2, 0), (2, 2), (0, 2), (0, 0)])
        point = Point(1, 1)
        result = ring.intersection(point)
        assert result is not None
        assert result.geom_type == "Point"

    def test_ring_intersection_none_raises_error(self):
        """Test that intersection with None raises ValueError"""
        ring = Ring([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)])
        with pytest.raises(ValueError):
            ring.intersection(None)


class TestModuleLevelIntersection:
    """Test module-level intersection() function"""

    def test_intersection_function_polygons(self):
        """Test module-level intersection with polygons"""
        poly1 = Polygon([(0, 0), (2, 0), (2, 2), (0, 2), (0, 0)])
        poly2 = Polygon([(1, 1), (3, 1), (3, 3), (1, 3), (1, 1)])
        result = intersection(poly1, poly2)
        assert result is not None
        assert result.geom_type == "Polygon"
        assert abs(result.area - 1.0) < 0.0001

    def test_intersection_function_point_polygon(self):
        """Test module-level intersection with point and polygon"""
        point = Point(1, 1)
        poly = Polygon([(0, 0), (2, 0), (2, 2), (0, 2), (0, 0)])
        result = intersection(point, poly)
        assert result is not None
        assert result.geom_type == "Point"

    def test_intersection_function_lines(self):
        """Test module-level intersection with lines"""
        line1 = LineString([(0, 0), (2, 2)])
        line2 = LineString([(0, 2), (2, 0)])
        result = intersection(line1, line2)
        assert result is not None
        assert result.geom_type == "Point"

    def test_intersection_function_with_geometry_objects(self):
        """Test module-level intersection with Geometry objects"""
        geom1 = Geometry("POLYGON((0 0, 2 0, 2 2, 0 2, 0 0))", fmt="wkt")
        geom2 = Geometry("POLYGON((1 1, 3 1, 3 3, 1 3, 1 1))", fmt="wkt")
        result = intersection(geom1, geom2)
        assert result is not None
        assert result.geom_type == "Polygon"
        assert abs(result.area - 1.0) < 0.0001

    def test_intersection_function_mixed_types(self):
        """Test module-level intersection with mixed geometry types"""
        line = LineString([(0, 1), (3, 1)])
        poly = Polygon([(1, 0), (2, 0), (2, 2), (1, 2), (1, 0)])
        result = intersection(line, poly)
        assert result is not None
        assert result.geom_type == "LineString"

    def test_intersection_function_none_raises_error(self):
        """Test that intersection with None raises TypeError"""
        poly = Polygon([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)])
        with pytest.raises(TypeError):
            intersection(None, poly)
        with pytest.raises(TypeError):
            intersection(poly, None)

    def test_intersection_function_invalid_type_raises_error(self):
        """Test that intersection with invalid type raises TypeError"""
        poly = Polygon([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)])
        with pytest.raises(TypeError):
            intersection(poly, "not a geometry")
        with pytest.raises(TypeError):
            intersection("not a geometry", poly)

    def test_intersection_function_empty_result(self):
        """Test intersection that results in empty geometry"""
        poly1 = Polygon([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)])
        poly2 = Polygon([(5, 5), (6, 5), (6, 6), (5, 6), (5, 5)])
        result = intersection(poly1, poly2)
        assert result is not None
        assert result.is_empty or result.area == 0.0


class TestIntersectionEdgeCases:
    """Test edge cases for intersection operations"""

    def test_intersection_multipolygon(self):
        """Test intersection with multipolygon"""
        poly = Polygon([(0, 0), (3, 0), (3, 3), (0, 3), (0, 0)])
        # Create MultiPolygon using proper Polygon objects
        poly1 = Polygon([(1, 1), (2, 1), (2, 2), (1, 2), (1, 1)])
        poly2 = Polygon([(4, 4), (5, 4), (5, 5), (4, 5), (4, 4)])
        multi = MultiPolygon([poly1, poly2])
        # MultiPolygon returns a Geometry object, so use it directly
        result = poly.as_geometry().intersection(multi)
        assert result is not None
        # Should only intersect with first polygon
        assert result.area > 0
        assert result.area <= 1.0

    def test_intersection_very_small_overlap(self):
        """Test intersection with very small overlap"""
        poly1 = Polygon([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)])
        poly2 = Polygon([(0.99, 0.99), (2, 0.99), (2, 2), (0.99, 2), (0.99, 0.99)])
        result = poly1.intersection(poly2)
        assert result is not None
        # Small overlap should still be detected
        assert result.area > 0
        assert result.area < 0.01

    def test_intersection_collinear_lines(self):
        """Test intersection of collinear lines"""
        line1 = LineString([(0, 0), (2, 0)])
        line2 = LineString([(1, 0), (3, 0)])
        result = line1.intersection(line2)
        assert result is not None
        # Should be overlapping segment
        assert result.geom_type == "LineString"

    def test_intersection_line_touches_polygon_vertex(self):
        """Test line that touches polygon at a vertex"""
        line = LineString([(0, 0), (0, 2)])
        poly = Polygon([(0, 0), (2, 0), (2, 2), (0, 2), (0, 0)])
        result = line.intersection(poly)
        assert result is not None
        # Should return the line segment along the edge
        assert result.geom_type == "LineString"
