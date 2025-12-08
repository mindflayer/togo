"""Tests for the is_valid property on various geometry types."""

from togo import (
    Point,
    LineString,
    Polygon,
    Ring,
    from_wkt,
    from_geojson,
    from_wkb,
    to_wkb,
)


class TestGeometryIsValid:
    """Test is_valid property on Geometry class."""

    def test_geometry_valid_point(self):
        """Test is_valid on a valid Point geometry."""
        geom = from_wkt("POINT (1 2)")
        assert geom.is_valid is True

    def test_geometry_valid_linestring(self):
        """Test is_valid on a valid LineString geometry."""
        geom = from_wkt("LINESTRING (0 0, 1 1, 2 2)")
        assert geom.is_valid is True

    def test_geometry_valid_polygon(self):
        """Test is_valid on a valid Polygon geometry."""
        geom = from_wkt("POLYGON ((0 0, 4 0, 4 4, 0 4, 0 0))")
        assert geom.is_valid is True

    def test_geometry_valid_multipoint(self):
        """Test is_valid on a valid MultiPoint geometry."""
        geom = from_wkt("MULTIPOINT ((0 0), (1 1), (2 2))")
        assert geom.is_valid is True

    def test_geometry_valid_multilinestring(self):
        """Test is_valid on a valid MultiLineString geometry."""
        geom = from_wkt("MULTILINESTRING ((0 0, 1 1), (2 2, 3 3))")
        assert geom.is_valid is True

    def test_geometry_valid_multipolygon(self):
        """Test is_valid on a valid MultiPolygon geometry."""
        geom = from_wkt(
            "MULTIPOLYGON (((0 0, 1 0, 1 1, 0 1, 0 0)), ((2 2, 3 2, 3 3, 2 3, 2 2)))"
        )
        assert geom.is_valid is True

    def test_geometry_valid_geojson(self):
        """Test is_valid on geometry parsed from GeoJSON."""
        geom = from_geojson('{"type":"Point","coordinates":[1,2]}')
        assert geom.is_valid is True

    def test_geometry_valid_wkb(self):
        """Test is_valid on geometry parsed from WKB."""
        point = from_wkt("POINT (1 2)")
        wkb = to_wkb(point)
        geom = from_wkb(wkb)
        assert geom.is_valid is True


class TestPointIsValid:
    """Test is_valid property on Point class."""

    def test_point_is_valid(self):
        """Test that constructed points are always valid."""
        p = Point(1.5, 2.5)
        assert p.is_valid is True

    def test_point_zero_coords_is_valid(self):
        """Test that point at origin is valid."""
        p = Point(0, 0)
        assert p.is_valid is True

    def test_point_negative_coords_is_valid(self):
        """Test that point with negative coords is valid."""
        p = Point(-1.5, -2.5)
        assert p.is_valid is True

    def test_point_large_coords_is_valid(self):
        """Test that point with large coords is valid."""
        p = Point(1e10, -1e10)
        assert p.is_valid is True


class TestLineIsValid:
    """Test is_valid property on Line class."""

    def test_linestring_is_valid(self):
        """Test that constructed linestrings are always valid."""
        line = LineString([(0, 0), (1, 1), (2, 2)])
        assert line.is_valid is True

    def test_linestring_two_points_is_valid(self):
        """Test that linestring with two points is valid."""
        line = LineString([(0, 0), (1, 1)])
        assert line.is_valid is True

    def test_linestring_many_points_is_valid(self):
        """Test that linestring with many points is valid."""
        coords = [(i, i) for i in range(100)]
        line = LineString(coords)
        assert line.is_valid is True

    def test_linestring_closed_is_valid(self):
        """Test that closed linestring is valid."""
        line = LineString([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)])
        assert line.is_valid is True


class TestRingIsValid:
    """Test is_valid property on Ring class."""

    def test_ring_is_valid(self):
        """Test that constructed rings are always valid."""
        ring = Ring([(0, 0), (4, 0), (4, 4), (0, 4), (0, 0)])
        assert ring.is_valid is True

    def test_ring_triangle_is_valid(self):
        """Test that triangle ring is valid."""
        ring = Ring([(0, 0), (1, 0), (0.5, 1), (0, 0)])
        assert ring.is_valid is True

    def test_ring_with_many_points_is_valid(self):
        """Test that ring with many points is valid."""
        import math

        # Create a circle with many points
        points = [
            (math.cos(2 * math.pi * i / 100), math.sin(2 * math.pi * i / 100))
            for i in range(100)
        ]
        points.append(points[0])  # Close the ring
        ring = Ring(points)
        assert ring.is_valid is True


class TestPolyIsValid:
    """Test is_valid property on Poly class."""

    def test_polygon_is_valid(self):
        """Test that constructed polygons are always valid."""
        poly = Polygon([(0, 0), (4, 0), (4, 4), (0, 4), (0, 0)])
        assert poly.is_valid is True

    def test_polygon_with_hole_is_valid(self):
        """Test that polygon with hole is valid."""
        exterior = [(0, 0), (4, 0), (4, 4), (0, 4), (0, 0)]
        hole = [(1, 1), (3, 1), (3, 3), (1, 3), (1, 1)]
        poly = Polygon(exterior, holes=[hole])
        assert poly.is_valid is True

    def test_polygon_with_multiple_holes_is_valid(self):
        """Test that polygon with multiple holes is valid."""
        exterior = [(0, 0), (10, 0), (10, 10), (0, 10), (0, 0)]
        hole1 = [(1, 1), (3, 1), (3, 3), (1, 3), (1, 1)]
        hole2 = [(6, 6), (8, 6), (8, 8), (6, 8), (6, 6)]
        poly = Polygon(exterior, holes=[hole1, hole2])
        assert poly.is_valid is True

    def test_polygon_triangle_is_valid(self):
        """Test that triangle polygon is valid."""
        poly = Polygon([(0, 0), (1, 0), (0.5, 1), (0, 0)])
        assert poly.is_valid is True


class TestGeometryIsInvalid:
    """Test is_valid property for geometrically invalid geometries."""

    def test_polygon_self_intersecting(self):
        """Test that self-intersecting polygon is detected as invalid."""
        # Create a self-intersecting polygon (bowtie/figure-8)
        # Vertices: (0,0), (2,2), (2,0), (0,2), (0,0)
        # This creates two triangles crossing each other
        geom = from_wkt("POLYGON ((0 0, 2 2, 2 0, 0 2, 0 0))")
        assert geom.is_valid is False

    def test_polygon_inner_ring_outside_outer_ring(self):
        """Test that polygon with hole outside exterior is invalid."""
        # Create polygon where hole is outside the exterior ring
        exterior_wkt = (
            "POLYGON ((0 0, 4 0, 4 4, 0 4, 0 0), (10 10, 12 10, 12 12, 10 12, 10 10))"
        )
        geom = from_wkt(exterior_wkt)
        assert geom.is_valid is False

    def test_valid_simple_polygon(self):
        """Test that simple valid polygon is valid."""
        geom = from_wkt("POLYGON ((0 0, 4 0, 4 4, 0 4, 0 0))")
        assert geom.is_valid is True

    def test_valid_polygon_with_hole(self):
        """Test that valid polygon with hole is valid."""
        geom = from_wkt(
            "POLYGON ((0 0, 10 0, 10 10, 0 10, 0 0), (2 2, 8 2, 8 8, 2 8, 2 2))"
        )
        assert geom.is_valid is True

    def test_invalid_ring_self_intersecting(self):
        """Test that self-intersecting ring results in invalid polygon."""
        # Create a ring that crosses itself
        geom = from_wkt("POLYGON ((0 0, 4 4, 4 0, 0 4, 0 0))")
        assert geom.is_valid is False

    def test_valid_linestring_is_valid(self):
        """Test that valid linestring is valid."""
        geom = from_wkt("LINESTRING (0 0, 1 1, 2 2, 3 3)")
        assert geom.is_valid is True

    def test_valid_point_is_valid(self):
        """Test that point is always valid."""
        geom = from_wkt("POINT (1 2)")
        assert geom.is_valid is True

    def test_valid_multipoint_is_valid(self):
        """Test that multipoint is valid."""
        geom = from_wkt("MULTIPOINT ((0 0), (1 1), (2 2))")
        assert geom.is_valid is True

    def test_valid_multilinestring_is_valid(self):
        """Test that multilinestring is valid."""
        geom = from_wkt("MULTILINESTRING ((0 0, 1 1), (2 2, 3 3))")
        assert geom.is_valid is True

    def test_valid_multipolygon_is_valid(self):
        """Test that valid multipolygon is valid."""
        geom = from_wkt(
            "MULTIPOLYGON (((0 0, 1 0, 1 1, 0 1, 0 0)), ((2 2, 3 2, 3 3, 2 3, 2 2)))"
        )
        assert geom.is_valid is True
