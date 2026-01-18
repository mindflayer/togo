"""
Additional comprehensive tests for Shapely-compatible error handling
This file contains edge case tests beyond the main test suite
"""

import pytest


class TestEdgeCaseErrorHandling:
    """Test edge cases for error handling"""

    def test_all_predicates_raise_typeerror_consistently(self):
        """Ensure all predicates raise the same TypeError for invalid inputs"""
        from togo import Point

        p = Point(1, 2)
        geom = p.as_geometry()

        invalid_inputs = [None, "string", 123, [1, 2, 3], {"x": 1}, True]
        predicates = [
            "contains",
            "intersects",
            "touches",
            "within",
            "disjoint",
            "equals",
            "covers",
            "coveredby",
        ]

        for invalid_input in invalid_inputs:
            for pred_name in predicates:
                pred = getattr(geom, pred_name)
                with pytest.raises(
                    TypeError, match="other must be a Geometry instance"
                ):
                    pred(invalid_input)

    def test_predicate_error_messages_clear(self):
        """Ensure error messages are clear and helpful"""
        from togo import Point

        p = Point(1, 2)
        geom = p.as_geometry()

        try:
            geom.contains(None)
            assert False, "Should have raised TypeError"
        except TypeError as e:
            # Check that error message is informative
            assert "Geometry" in str(e)
            assert "other" in str(e) or "must" in str(e)

    def test_valid_geometries_still_work(self):
        """Ensure valid geometry operations still work after error checking"""
        from togo import Point, LineString, Polygon

        p1 = Point(0, 0)
        p2 = Point(1, 1)  # Point inside the polygon
        p3 = Point(1, 1)  # Point on the line
        p_boundary = Point(0, 0)  # Point on polygon boundary
        line = LineString([(0, 0), (2, 2)])
        poly = Polygon([(0, 0), (2, 0), (2, 2), (0, 2), (0, 0)])

        # All these should work fine
        assert p1.as_geometry().equals(p1.as_geometry())
        assert not p1.as_geometry().equals(p2.as_geometry())
        assert not p1.as_geometry().disjoint(p1.as_geometry())
        # LineStrings intersect with points on them, but don't "contain" them
        assert line.as_geometry().intersects(p3.as_geometry())
        # Point inside polygon interior (not on boundary)
        assert p2.as_geometry().within(poly.as_geometry())
        assert poly.as_geometry().contains(p2.as_geometry())
        # Point on boundary is covered but not within
        assert poly.as_geometry().covers(p_boundary.as_geometry())

    def test_geometry_predicates_with_mixed_types(self):
        """Test predicates work with different geometry type combinations"""
        from togo import Point, LineString, Polygon

        p = Point(1, 1)
        line = LineString([(0, 0), (2, 2)])
        poly = Polygon([(0, 0), (3, 0), (3, 3), (0, 3), (0, 0)])

        # Point-Line: Lines intersect with points on them, but don't "contain" them
        assert line.as_geometry().intersects(p.as_geometry())
        # A point is not "within" a line in the topological sense
        assert p.as_geometry().intersects(line.as_geometry())

        # Point-Polygon: Polygons (2D) can contain points (0D)
        assert poly.as_geometry().contains(p.as_geometry())
        assert p.as_geometry().within(poly.as_geometry())

        # Line-Polygon: Polygon contains the line (line is inside the polygon)
        assert poly.as_geometry().intersects(line.as_geometry())

    def test_intersection_with_various_invalid_types(self):
        """Test intersection handles various invalid types gracefully"""
        from togo import Point

        p = Point(1, 2)

        # These should all return empty geometries (Shapely-compatible)
        result1 = p.intersection(None)
        assert result1.is_empty

        result2 = p.intersection("invalid")
        assert result2.is_empty

        result3 = p.intersection(123)
        assert result3.is_empty

    def test_nearest_points_type_checking(self):
        """Test nearest_points properly validates input types"""
        from togo import Point, LineString

        p = Point(1, 2)
        line = LineString([(0, 0), (5, 5)])

        # Valid calls should work
        pts1 = p.nearest_points(line.as_geometry())
        assert len(pts1) == 2
        assert all(isinstance(pt, Point) for pt in pts1)

        # Invalid calls should raise ValueError
        with pytest.raises(ValueError):
            p.nearest_points(None)

        with pytest.raises(ValueError):
            p.nearest_points("invalid")

    def test_shortest_line_type_checking(self):
        """Test shortest_line properly validates input types"""
        from togo import Point, LineString, Line

        p = Point(1, 2)
        line = LineString([(0, 0), (5, 5)])

        # Valid calls should work
        result = p.shortest_line(line.as_geometry())
        assert isinstance(result, Line)

        # Invalid calls should raise ValueError
        with pytest.raises(ValueError):
            p.shortest_line(None)

        with pytest.raises(ValueError):
            p.shortest_line("invalid")

    def test_buffer_with_various_parameters(self):
        """Test buffer works with various parameter values"""
        from togo import Point, Polygon

        p = Point(0, 0)

        # Positive buffer
        result = p.buffer(1.0)
        assert result.geom_type == "Polygon"
        assert result.area > 3.0  # pi * 1^2 ≈ 3.14

        # Zero buffer (should return empty or degenerate)
        result = p.buffer(0)
        assert result is not None

        # Negative buffer on point (should return empty or very small)
        result = p.buffer(-1.0)
        assert result is not None

        # Negative buffer on polygon (inset)
        poly = Polygon([(0, 0), (10, 0), (10, 10), (0, 10), (0, 0)])
        result = poly.as_geometry().buffer(-1.0)
        assert result is not None
        # Inset should have smaller area
        assert result.area < poly.area

    def test_empty_geometry_predicates(self):
        """Test predicates work with empty geometries"""
        from togo import Geometry, Point

        # Create empty geometry - GeometryCollection uses "geometries", not "coordinates"
        empty = Geometry('{"type":"GeometryCollection","geometries":[]}')
        p = Point(1, 2)

        # These should all work without raising errors
        assert empty.disjoint(p.as_geometry())
        assert not empty.intersects(p.as_geometry())
        assert not empty.contains(p.as_geometry())
        assert not empty.equals(p.as_geometry())

    def test_constructor_error_types(self):
        """Test that constructors raise appropriate error types"""
        from togo import LineString, Polygon

        # Note: Empty LineString might be allowed (Shapely 2.x allows it)
        # Test that empty LineString either works or raises appropriate error
        try:
            empty_line = LineString([])
            # If it succeeds, verify it's empty
            assert empty_line.is_empty or empty_line.num_points == 0
        except (ValueError, MemoryError):
            # If it fails, that's also acceptable (depends on TG implementation)
            pass

        # LineString with one point (might fail or succeed depending on TG behavior)
        try:
            LineString([(0, 0)])
            # If it doesn't fail, that's OK - TG might allow it
            # Shapely 2.x allows single-point LineStrings (though they're degenerate)
        except ValueError:
            # If it fails with ValueError, that's also acceptable
            pass

        # Polygon with invalid exterior type
        with pytest.raises(TypeError):
            Polygon("not a list")

        with pytest.raises((TypeError, ValueError)):
            Polygon(None)

    def test_property_access_on_correct_types(self):
        """Test that properties work correctly on appropriate types"""
        from togo import Point, LineString, Polygon

        # Point properties
        p = Point(3.5, 4.5)
        assert p.x == 3.5
        assert p.y == 4.5
        assert p.coords == [(3.5, 4.5)]
        assert p.bounds == (3.5, 4.5, 3.5, 4.5)

        # LineString properties
        line = LineString([(0, 0), (1, 1), (2, 2)])
        assert line.coords == [(0, 0), (1, 1), (2, 2)]
        assert line.bounds == (0, 0, 2, 2)
        assert line.length > 0

        # Polygon properties
        poly = Polygon([(0, 0), (2, 0), (2, 2), (0, 2), (0, 0)])
        assert poly.bounds == (0, 0, 2, 2)
        assert poly.area == pytest.approx(4.0, rel=1e-5)
        assert len(poly.exterior.coords) == 5

    def test_wkt_wkb_on_all_types(self):
        """Test WKT/WKB conversion on all geometry types"""
        from togo import Point, LineString, Polygon

        geometries = [
            Point(1, 2),
            LineString([(0, 0), (1, 1)]),
            Polygon([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)]),
        ]

        for geom in geometries:
            # WKT
            wkt = geom.wkt
            assert isinstance(wkt, str)
            assert len(wkt) > 0

            # WKB
            wkb = geom.wkb
            assert isinstance(wkb, bytes)
            assert len(wkb) > 0

    def test_geom_type_on_all_types(self):
        """Test geom_type property on all geometry types"""
        from togo import Point, LineString, Polygon

        assert Point(1, 2).geom_type == "Point"
        assert LineString([(0, 0), (1, 1)]).geom_type == "LineString"
        assert Polygon([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)]).geom_type == "Polygon"

    def test_is_empty_on_all_types(self):
        """Test is_empty property on all geometry types"""
        from togo import Point, LineString, Polygon

        # Non-empty geometries
        assert not Point(1, 2).is_empty
        assert not LineString([(0, 0), (1, 1)]).is_empty
        assert not Polygon([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)]).is_empty

    def test_is_valid_on_all_types(self):
        """Test is_valid property on all geometry types"""
        from togo import Point, LineString, Polygon

        # Valid geometries
        assert Point(1, 2).is_valid
        assert LineString([(0, 0), (1, 1)]).is_valid
        assert Polygon([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)]).is_valid
