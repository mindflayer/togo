"""
Tests for buffer() method implementations in togo
"""

import math
import pytest
from togo import Point, LineString, Polygon, Ring, Geometry


class TestGeometryBuffer:
    """Test Geometry.buffer() method"""

    def test_geometry_buffer_linestring(self):
        """Test buffering a LineString geometry"""
        geom = Geometry("LINESTRING(0 0, 5 5)", fmt="wkt")
        buffered = geom.buffer(1.0, resolution=8)
        assert buffered is not None
        assert buffered.geom_type == "Polygon"
        # Buffered geometry should have area
        assert buffered.area > 0
        # Original line should be contained in buffer
        assert buffered.contains(geom)

    def test_geometry_buffer_polygon(self):
        """Test buffering a Polygon geometry"""
        geom = Geometry("POLYGON((0 0, 10 0, 10 10, 0 10, 0 0))", fmt="wkt")
        original_area = geom.area
        buffered = geom.buffer(1.0, resolution=8)
        assert buffered is not None
        assert buffered.geom_type == "Polygon"
        # Positive buffer should increase area
        assert buffered.area > original_area
        # Original polygon should be contained in buffer
        assert buffered.contains(geom)

    def test_geometry_buffer_point(self):
        """Test buffering a Point geometry"""
        geom = Geometry("POINT(0 0)", fmt="wkt")
        buffered = geom.buffer(1.0, resolution=16)
        assert buffered is not None
        assert buffered.geom_type == "Polygon"
        # Buffer of point should approximate circle area: π * r²
        expected_area = math.pi * 1.0 * 1.0
        assert abs(buffered.area - expected_area) < 0.1  # Allow small tolerance
        # Check bounds are symmetric around origin
        minx, miny, maxx, maxy = buffered.bounds()
        assert abs(minx + 1.0) < 0.1
        assert abs(maxx - 1.0) < 0.1
        assert abs(miny + 1.0) < 0.1
        assert abs(maxy - 1.0) < 0.1

    def test_geometry_buffer_with_custom_styles(self):
        """Test buffer with custom cap and join styles"""
        geom = Geometry("LINESTRING(0 0, 10 10)", fmt="wkt")
        buffered = geom.buffer(
            2.0, resolution=16, cap_style=3, join_style=2, mitre_limit=3.0
        )
        assert buffered is not None
        assert buffered.geom_type == "Polygon"
        assert buffered.area > 0
        # Original line should be contained in buffer
        assert buffered.contains(geom)

    def test_geometry_buffer_zero_distance(self):
        """Test buffer with zero distance returns same geometry"""
        geom = Geometry("POINT(0 0)", fmt="wkt")
        buffered = geom.buffer(0.0)
        assert buffered is geom

    def test_geometry_buffer_negative_distance(self):
        """Test buffer with negative distance (shrinking)"""
        geom = Geometry("POLYGON((0 0, 10 0, 10 10, 0 10, 0 0))", fmt="wkt")
        original_area = geom.area
        buffered = geom.buffer(-1.0, resolution=8)
        assert buffered is not None
        # Negative buffer should reduce area
        assert buffered.area < original_area
        # Buffered polygon should be contained in original
        assert geom.contains(buffered)


class TestPointBuffer:
    """Test Point.buffer() method"""

    def test_point_buffer_creates_polygon(self):
        """Test that Point buffer creates a polygon"""
        p = Point(0, 0)
        buffered = p.buffer(1.0, resolution=16)
        assert buffered.geom_type == "Polygon"
        # Buffer should approximate circle: π * r²
        expected_area = math.pi * 1.0 * 1.0
        assert abs(buffered.area - expected_area) < 0.1

    def test_point_buffer_with_resolution(self):
        """Test Point buffer with different resolution"""
        p = Point(5.5, 3.2)
        buffered = p.buffer(2.0, resolution=16)
        assert buffered.geom_type == "Polygon"
        # Check area matches expected circle area
        expected_area = math.pi * 2.0 * 2.0
        assert abs(buffered.area - expected_area) < 0.3
        # Check bounds are centered around the point
        minx, miny, maxx, maxy = buffered.bounds()
        assert abs((minx + maxx) / 2 - 5.5) < 0.1
        assert abs((miny + maxy) / 2 - 3.2) < 0.1


class TestLineStringBuffer:
    """Test LineString (Line) .buffer() method"""

    def test_linestring_buffer_creates_polygon(self):
        """Test that LineString buffer creates a polygon"""
        line = LineString([(0, 0), (10, 10)])
        buffered = line.buffer(1.0, resolution=8)
        assert buffered.geom_type == "Polygon"
        # Buffer should have area
        assert buffered.area > 0
        # Approximate check: buffer of line should be roughly 2*width*length + caps
        line_length = math.sqrt(10**2 + 10**2)  # ~14.14
        min_area = 2 * 1.0 * line_length  # Rectangle portion
        assert buffered.area > min_area

    def test_linestring_buffer_with_cap_styles(self):
        """Test LineString buffer with different cap styles"""
        line = LineString([(0, 0), (10, 0)])
        # Round cap (default)
        buffered1 = line.buffer(1.0, cap_style=1, resolution=16)
        # Square cap
        buffered2 = line.buffer(1.0, cap_style=3)
        assert buffered1.geom_type == "Polygon"
        assert buffered2.geom_type == "Polygon"
        # Both should have positive area
        assert buffered1.area > 0
        assert buffered2.area > 0
        # Square cap should produce larger area than round cap
        assert buffered2.area > buffered1.area


class TestPolygonBuffer:
    """Test Polygon.buffer() method"""

    def test_polygon_buffer_outward(self):
        """Test positive buffer (outward expansion)"""
        ring = Ring([(0, 0), (5, 0), (5, 5), (0, 5), (0, 0)])
        poly = Polygon(ring)
        original_area = poly.area
        buffered = poly.buffer(1.0, resolution=8)
        assert buffered.geom_type == "Polygon"
        # Positive buffer should increase area
        assert buffered.area > original_area
        # Original should be contained in buffered
        assert buffered.contains(poly)

    def test_polygon_buffer_inward(self):
        """Test negative buffer (inward shrinking)"""
        ring = Ring([(0, 0), (10, 0), (10, 10), (0, 10), (0, 0)])
        poly = Polygon(ring)
        original_area = poly.area  # Should be 100
        buffered = poly.buffer(-1.0, resolution=8)
        assert buffered.geom_type == "Polygon"
        # Negative buffer should reduce area
        assert buffered.area < original_area
        # Buffered should be contained in original
        assert poly.contains(buffered)
        # With -1 buffer, should be approximately (10-2)*(10-2) = 64
        assert abs(buffered.area - 64.0) < 5.0

    def test_polygon_buffer_with_holes(self):
        """Test buffering polygon with holes"""
        exterior = Ring([(0, 0), (10, 0), (10, 10), (0, 10), (0, 0)])
        hole = Ring([(2, 2), (4, 2), (4, 4), (2, 4), (2, 2)])
        poly = Polygon(exterior, holes=[hole])
        original_area = poly.area  # 100 - 4 = 96
        buffered = poly.buffer(1.0, resolution=8)
        assert buffered.geom_type == "Polygon"
        # Positive buffer should increase area (and may fill the hole)
        assert buffered.area > original_area


class TestRingBuffer:
    """Test Ring.buffer() method"""

    def test_ring_buffer_creates_polygon(self):
        """Test that Ring buffer creates a polygon"""
        ring = Ring([(0, 0), (5, 0), (5, 5), (0, 5), (0, 0)])
        buffered = ring.buffer(1.0, resolution=8)
        assert buffered.geom_type == "Polygon"
        # Buffer should have positive area
        assert buffered.area > 0
        # Buffer should be larger than original ring's enclosed area (25)
        assert buffered.area > 25.0

    def test_ring_buffer_with_join_styles(self):
        """Test Ring buffer with different join styles"""
        ring = Ring([(0, 0), (5, 0), (5, 5), (0, 5), (0, 0)])
        # Round join (default)
        buffered1 = ring.buffer(1.0, join_style=1, resolution=16)
        # Bevel join
        buffered2 = ring.buffer(1.0, join_style=3)
        assert buffered1.geom_type == "Polygon"
        assert buffered2.geom_type == "Polygon"
        # Both should have positive area
        assert buffered1.area > 0
        assert buffered2.area > 0
        # Areas should be similar but potentially different due to join style
        assert abs(buffered1.area - buffered2.area) < 5.0


class TestBufferParameters:
    """Test buffer parameters and options"""

    def test_buffer_resolution_values(self):
        """Test buffer with various resolution values"""
        geom = Geometry("POINT(0 0)", fmt="wkt")
        areas = []
        for resolution in [4, 8, 16, 32]:
            buffered = geom.buffer(1.0, resolution=resolution)
            assert buffered.geom_type == "Polygon"
            areas.append(buffered.area)
        # Higher resolution should produce area closer to π*r²
        expected = math.pi * 1.0 * 1.0
        # Higher resolution should be more accurate
        assert abs(areas[-1] - expected) < abs(areas[0] - expected)

    def test_buffer_cap_styles(self):
        """Test all cap style values"""
        geom = Geometry("LINESTRING(0 0, 10 0)", fmt="wkt")
        areas = []
        for cap_style in [1, 2, 3]:
            buffered = geom.buffer(1.0, cap_style=cap_style, resolution=16)
            assert buffered.geom_type == "Polygon"
            assert buffered.area > 0
            areas.append(buffered.area)
        # cap_style 2 (flat) should produce smallest area
        # cap_style 3 (square) should produce largest area
        assert areas[1] < areas[0]  # flat < round
        assert areas[0] < areas[2]  # round < square

    def test_buffer_join_styles(self):
        """Test all join style values"""
        geom = Geometry("POLYGON((0 0, 10 0, 10 10, 0 10, 0 0))", fmt="wkt")
        for join_style in [1, 2, 3]:
            buffered = geom.buffer(1.0, join_style=join_style)
            assert buffered.geom_type == "Polygon"
            # All should produce valid polygons with area
            assert buffered.area > 100  # Original was 100


class TestBufferErrorCases:
    """Test buffer error handling and edge cases"""

    def test_buffer_invalid_cap_style_zero(self):
        """Test buffer with invalid cap_style value 0"""
        geom = Geometry("LINESTRING(0 0, 10 0)", fmt="wkt")
        with pytest.raises(RuntimeError):
            geom.buffer(1.0, cap_style=0)

    def test_buffer_invalid_cap_style_negative(self):
        """Test buffer with invalid negative cap_style value"""
        geom = Geometry("LINESTRING(0 0, 10 0)", fmt="wkt")
        with pytest.raises(RuntimeError):
            geom.buffer(1.0, cap_style=-1)

    def test_buffer_invalid_cap_style_too_large(self):
        """Test buffer with invalid cap_style value > 3"""
        geom = Geometry("LINESTRING(0 0, 10 0)", fmt="wkt")
        with pytest.raises(RuntimeError):
            geom.buffer(1.0, cap_style=4)

    def test_buffer_invalid_join_style_zero(self):
        """Test buffer with invalid join_style value 0"""
        geom = Geometry("POLYGON((0 0, 10 0, 10 10, 0 10, 0 0))", fmt="wkt")
        with pytest.raises(RuntimeError):
            geom.buffer(1.0, join_style=0)

    def test_buffer_invalid_join_style_negative(self):
        """Test buffer with invalid negative join_style value"""
        geom = Geometry("POLYGON((0 0, 10 0, 10 10, 0 10, 0 0))", fmt="wkt")
        with pytest.raises(RuntimeError):
            geom.buffer(1.0, join_style=-1)

    def test_buffer_invalid_join_style_too_large(self):
        """Test buffer with invalid join_style value > 3"""
        geom = Geometry("POLYGON((0 0, 10 0, 10 10, 0 10, 0 0))", fmt="wkt")
        with pytest.raises(RuntimeError):
            geom.buffer(1.0, join_style=4)

    def test_buffer_very_large_negative_distance(self):
        """Test buffer with very large negative distance that exceeds geometry size"""
        geom = Geometry("POLYGON((0 0, 10 0, 10 10, 0 10, 0 0))", fmt="wkt")
        # Negative buffer larger than the geometry should produce empty or very small result
        buffered = geom.buffer(-100.0, resolution=8)
        # GEOS should handle this gracefully - result may be empty or None
        assert buffered is not None
        # Area should be 0 or very close to 0
        assert buffered.area < 0.01

    def test_buffer_negative_resolution(self):
        """Test buffer with negative resolution value"""
        geom = Geometry("POINT(0 0)", fmt="wkt")
        # Negative resolution should fail or be handled by GEOS
        with pytest.raises(RuntimeError):
            geom.buffer(1.0, resolution=-1)

    def test_buffer_zero_resolution(self):
        """Test buffer with zero resolution value"""
        geom = Geometry("POINT(0 0)", fmt="wkt")
        # Zero resolution should fail as it's invalid
        with pytest.raises(RuntimeError):
            geom.buffer(1.0, resolution=0)

    def test_buffer_very_small_distance(self):
        """Test buffer with very small distance value"""
        geom = Geometry("POINT(0 0)", fmt="wkt")
        # Very small buffer should still work
        buffered = geom.buffer(0.0001, resolution=8)
        assert buffered.geom_type == "Polygon"
        # Area should be close to π * (0.0001)²
        expected = math.pi * 0.0001 * 0.0001
        assert abs(buffered.area - expected) < expected * 0.5

    def test_buffer_large_positive_distance(self):
        """Test buffer with very large positive distance"""
        geom = Geometry("POINT(0 0)", fmt="wkt")
        # Very large buffer should still work
        buffered = geom.buffer(1000.0, resolution=8)
        assert buffered.geom_type == "Polygon"
        # Area should be approximately π * 1000²
        expected = math.pi * 1000.0 * 1000.0
        assert abs(buffered.area - expected) / expected < 0.1  # Within 10%

    def test_buffer_negative_mitre_limit(self):
        """Test buffer with negative mitre_limit"""
        geom = Geometry("LINESTRING(0 0, 10 0)", fmt="wkt")
        # Negative mitre_limit might be invalid
        with pytest.raises(RuntimeError):
            geom.buffer(1.0, join_style=2, mitre_limit=-1.0)
