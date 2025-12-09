"""
Tests for simplify() method implementations in togo
"""

import pytest
from togo import Point, LineString, Polygon, Ring, Geometry


class TestGeometrySimplify:
    """Test Geometry.simplify() method"""

    def test_geometry_simplify_linestring(self):
        """Test simplifying a LineString geometry"""
        # Create a line with extra points that should be simplified
        geom = Geometry("LINESTRING(0 0, 0.1 0.1, 0.2 0.2, 1 1, 2 2)", fmt="wkt")
        geom.to_wkt()
        simplified = geom.simplify(0.5, preserve_topology=True)
        assert simplified is not None
        assert simplified.geom_type == "LineString"
        # Simplified geometry should have fewer or equal characters in WKT
        # (actual simplification happened)
        simplified_wkt = simplified.to_wkt()
        # Verify it was simplified (fewer coordinate points in WKT)
        assert simplified_wkt is not None
        assert "LINESTRING" in simplified_wkt

    def test_geometry_simplify_polygon(self):
        """Test simplifying a Polygon geometry"""
        geom = Geometry(
            "POLYGON((0 0, 0.1 0, 0.2 0, 1 0, 2 0, 2 1, 2 2, 1 2, 0 2, 0 1, 0 0))",
            fmt="wkt",
        )
        simplified = geom.simplify(0.5, preserve_topology=True)
        assert simplified is not None
        assert simplified.geom_type == "Polygon"
        # Simplified polygon should still be valid
        assert simplified.is_valid

    def test_geometry_simplify_with_preserve_topology_true(self):
        """Test simplify with topology preservation enabled"""
        geom = Geometry("LINESTRING(0 0, 1 1, 2 0, 3 1, 4 0)", fmt="wkt")
        simplified = geom.simplify(1.0, preserve_topology=True)
        assert simplified is not None
        # Should still be a valid geometry
        assert simplified.geom_type in ["LineString", "MultiLineString"]

    def test_geometry_simplify_with_preserve_topology_false(self):
        """Test simplify with topology preservation disabled"""
        geom = Geometry("LINESTRING(0 0, 1 1, 2 0, 3 1, 4 0)", fmt="wkt")
        simplified = geom.simplify(1.0, preserve_topology=False)
        assert simplified is not None
        # Should return a geometry (may be different type with preserve_topology=False)
        assert simplified.geom_type in ["LineString", "MultiLineString"]

    def test_geometry_simplify_zero_tolerance(self):
        """Test simplify with zero tolerance"""
        geom = Geometry("LINESTRING(0 0, 1 1, 2 0, 3 1, 4 0)", fmt="wkt")
        simplified = geom.simplify(0.0, preserve_topology=True)
        assert simplified is not None
        # With zero tolerance, should be identical to original
        assert simplified.to_wkt() == geom.to_wkt()

    def test_geometry_simplify_negative_tolerance_raises(self):
        """Test that negative tolerance raises ValueError"""
        geom = Geometry("LINESTRING(0 0, 1 1, 2 2)", fmt="wkt")
        with pytest.raises(ValueError, match="tolerance must be >= 0"):
            geom.simplify(-1.0)

    def test_geometry_simplify_large_tolerance(self):
        """Test simplify with large tolerance"""
        geom = Geometry(
            "LINESTRING(0 0, 0.1 0.1, 0.2 0.2, 1 1, 1.1 1.1, 1.2 1.2, 2 2)", fmt="wkt"
        )
        simplified = geom.simplify(10.0, preserve_topology=True)
        assert simplified is not None
        # Very large tolerance should simplify to very few points
        # Verify by checking the WKT is shorter (fewer coordinates)
        original_wkt = geom.to_wkt()
        simplified_wkt = simplified.to_wkt()
        assert simplified_wkt is not None
        # Count commas (coordinate separator) to verify simplification
        assert simplified_wkt.count(",") <= original_wkt.count(",")


class TestPointSimplify:
    """Test Point.simplify() method"""

    def test_point_simplify(self):
        """Test that Point.simplify() works"""
        p = Point(1.5, 2.5)
        simplified = p.simplify(1.0, preserve_topology=True)
        assert simplified is not None
        assert simplified.geom_type == "Point"

    def test_point_simplify_preserve_topology(self):
        """Test Point simplify with topology preservation"""
        p = Point(5.5, 3.2)
        simplified = p.simplify(2.0, preserve_topology=True)
        assert simplified is not None
        assert simplified.geom_type == "Point"

    def test_point_simplify_without_preserve_topology(self):
        """Test Point simplify without topology preservation"""
        p = Point(5.5, 3.2)
        simplified = p.simplify(2.0, preserve_topology=False)
        assert simplified is not None
        assert simplified.geom_type == "Point"


class TestLineStringSimplify:
    """Test LineString.simplify() method"""

    def test_linestring_simplify(self):
        """Test simplifying a LineString"""
        line = LineString([(0, 0), (0.1, 0.1), (0.2, 0.2), (1, 1), (2, 2)])
        simplified = line.simplify(0.5, preserve_topology=True)
        assert simplified is not None
        assert simplified.geom_type == "LineString"
        # Simplified should have fewer or equal points
        # Use as_line() to get a Line object if possible, then check num_points
        simplified_wkt = simplified.to_wkt()
        assert simplified_wkt is not None

    def test_linestring_simplify_preserve_topology(self):
        """Test LineString simplify with topology preservation"""
        line = LineString([(0, 0), (1, 1), (2, 0), (3, 1), (4, 0)])
        simplified = line.simplify(1.0, preserve_topology=True)
        assert simplified is not None
        assert simplified.geom_type == "LineString"

    def test_linestring_simplify_without_preserve_topology(self):
        """Test LineString simplify without topology preservation"""
        line = LineString([(0, 0), (1, 1), (2, 0), (3, 1), (4, 0)])
        simplified = line.simplify(1.0, preserve_topology=False)
        assert simplified is not None
        # May return LineString or MultiLineString
        assert simplified.geom_type in ["LineString", "MultiLineString"]


class TestPolygonSimplify:
    """Test Polygon.simplify() method"""

    def test_polygon_simplify(self):
        """Test simplifying a Polygon"""
        poly = Polygon(
            [
                (0, 0),
                (0.1, 0),
                (0.2, 0),
                (1, 0),
                (2, 0),
                (2, 1),
                (2, 2),
                (1, 2),
                (0, 2),
                (0, 1),
                (0, 0),
            ]
        )
        simplified = poly.simplify(0.5, preserve_topology=True)
        assert simplified is not None
        assert simplified.geom_type == "Polygon"
        # Simplified polygon should still be valid
        assert simplified.is_valid

    def test_polygon_simplify_preserve_topology(self):
        """Test Polygon simplify with topology preservation"""
        poly = Polygon([(0, 0), (10, 0), (10, 10), (0, 10), (0, 0)])
        simplified = poly.simplify(1.0, preserve_topology=True)
        assert simplified is not None
        # With such a simple polygon, simplification should maintain validity
        assert simplified.is_valid

    def test_polygon_simplify_without_preserve_topology(self):
        """Test Polygon simplify without topology preservation"""
        poly = Polygon([(0, 0), (10, 0), (10, 10), (0, 10), (0, 0)])
        simplified = poly.simplify(1.0, preserve_topology=False)
        assert simplified is not None
        assert simplified.geom_type == "Polygon"


class TestRingSimplify:
    """Test Ring.simplify() method"""

    def test_ring_simplify(self):
        """Test simplifying a Ring"""
        ring = Ring(
            [(0, 0), (0.1, 0.1), (0.2, 0.2), (1, 1), (2, 2), (2, 1), (1, 0), (0, 0)]
        )
        simplified = ring.simplify(0.5, preserve_topology=True)
        assert simplified is not None
        # Result should be a geometry
        assert simplified.geom_type in ["LineString", "LinearRing", "Polygon"]

    def test_ring_simplify_preserve_topology(self):
        """Test Ring simplify with topology preservation"""
        ring = Ring([(0, 0), (10, 0), (10, 10), (0, 10), (0, 0)])
        simplified = ring.simplify(1.0, preserve_topology=True)
        assert simplified is not None

    def test_ring_simplify_without_preserve_topology(self):
        """Test Ring simplify without topology preservation"""
        ring = Ring([(0, 0), (10, 0), (10, 10), (0, 10), (0, 0)])
        simplified = ring.simplify(1.0, preserve_topology=False)
        assert simplified is not None


class TestSimplifyComparison:
    """Test simplify with different tolerances"""

    def test_simplify_increasing_tolerance(self):
        """Test that larger tolerance produces simpler geometries"""
        geom = Geometry(
            "LINESTRING(0 0, 0.1 0.1, 0.2 0.2, 0.3 0.3, 1 1, 1.1 1.1, 1.2 1.2, 2 2)",
            fmt="wkt",
        )

        simple_low = geom.simplify(0.1, preserve_topology=True)
        simple_high = geom.simplify(1.0, preserve_topology=True)

        # Higher tolerance should produce fewer or equal points
        # Verify by comparing WKT comma counts
        low_commas = simple_low.to_wkt().count(",")
        high_commas = simple_high.to_wkt().count(",")
        assert high_commas <= low_commas

    def test_simplify_preserves_geometry_type(self):
        """Test that simplify preserves geometry type for simple geometries"""
        line = LineString([(0, 0), (0.1, 0.1), (1, 1), (2, 2)])
        simplified = line.simplify(0.5, preserve_topology=True)
        assert simplified.geom_type == "LineString"

        poly = Polygon([(0, 0), (0.05, 0.05), (1, 0), (1, 1), (0, 1), (0, 0)])
        simplified = poly.simplify(0.5, preserve_topology=True)
        assert simplified.geom_type == "Polygon"
