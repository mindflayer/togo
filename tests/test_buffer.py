"""
Tests for buffer() method implementations in togo
"""

from togo import Point, LineString, Polygon, Ring, Geometry


class TestGeometryBuffer:
    """Test Geometry.buffer() method"""

    def test_geometry_buffer_linestring(self):
        """Test buffering a LineString geometry"""
        geom = Geometry("LINESTRING(0 0, 5 5)", fmt="wkt")
        buffered = geom.buffer(1.0, resolution=8)
        assert buffered is not None
        assert buffered.geom_type == "Polygon"

    def test_geometry_buffer_polygon(self):
        """Test buffering a Polygon geometry"""
        geom = Geometry("POLYGON((0 0, 10 0, 10 10, 0 10, 0 0))", fmt="wkt")
        buffered = geom.buffer(1.0, resolution=8)
        assert buffered is not None
        assert buffered.geom_type == "Polygon"

    def test_geometry_buffer_point(self):
        """Test buffering a Point geometry"""
        geom = Geometry("POINT(0 0)", fmt="wkt")
        buffered = geom.buffer(1.0, resolution=8)
        assert buffered is not None
        assert buffered.geom_type == "Polygon"

    def test_geometry_buffer_with_custom_styles(self):
        """Test buffer with custom cap and join styles"""
        geom = Geometry("LINESTRING(0 0, 10 10)", fmt="wkt")
        buffered = geom.buffer(
            2.0, resolution=16, cap_style=3, join_style=2, mitre_limit=3.0
        )
        assert buffered is not None
        assert buffered.geom_type == "Polygon"

    def test_geometry_buffer_zero_distance(self):
        """Test buffer with zero distance returns same geometry"""
        geom = Geometry("POINT(0 0)", fmt="wkt")
        buffered = geom.buffer(0.0)
        assert buffered is geom

    def test_geometry_buffer_negative_distance(self):
        """Test buffer with negative distance (shrinking)"""
        geom = Geometry("POLYGON((0 0, 10 0, 10 10, 0 10, 0 0))", fmt="wkt")
        buffered = geom.buffer(-1.0, resolution=8)
        assert buffered is not None


class TestPointBuffer:
    """Test Point.buffer() method"""

    def test_point_buffer_creates_polygon(self):
        """Test that Point buffer creates a polygon"""
        p = Point(0, 0)
        buffered = p.buffer(1.0, resolution=8)
        assert buffered.geom_type == "Polygon"

    def test_point_buffer_with_resolution(self):
        """Test Point buffer with different resolution"""
        p = Point(5.5, 3.2)
        buffered = p.buffer(2.0, resolution=16)
        assert buffered.geom_type == "Polygon"


class TestLineStringBuffer:
    """Test LineString (Line) .buffer() method"""

    def test_linestring_buffer_creates_polygon(self):
        """Test that LineString buffer creates a polygon"""
        line = LineString([(0, 0), (10, 10)])
        buffered = line.buffer(1.0, resolution=8)
        assert buffered.geom_type == "Polygon"

    def test_linestring_buffer_with_cap_styles(self):
        """Test LineString buffer with different cap styles"""
        line = LineString([(0, 0), (10, 0)])
        # Round cap (default)
        buffered1 = line.buffer(1.0, cap_style=1)
        # Square cap
        buffered2 = line.buffer(1.0, cap_style=3)
        assert buffered1.geom_type == "Polygon"
        assert buffered2.geom_type == "Polygon"


class TestPolygonBuffer:
    """Test Polygon.buffer() method"""

    def test_polygon_buffer_outward(self):
        """Test positive buffer (outward expansion)"""
        ring = Ring([(0, 0), (5, 0), (5, 5), (0, 5), (0, 0)])
        poly = Polygon(ring)
        buffered = poly.buffer(1.0, resolution=8)
        assert buffered.geom_type == "Polygon"

    def test_polygon_buffer_inward(self):
        """Test negative buffer (inward shrinking)"""
        ring = Ring([(0, 0), (10, 0), (10, 10), (0, 10), (0, 0)])
        poly = Polygon(ring)
        buffered = poly.buffer(-1.0, resolution=8)
        assert buffered.geom_type == "Polygon"

    def test_polygon_buffer_with_holes(self):
        """Test buffering polygon with holes"""
        exterior = Ring([(0, 0), (10, 0), (10, 10), (0, 10), (0, 0)])
        hole = Ring([(2, 2), (4, 2), (4, 4), (2, 4), (2, 2)])
        poly = Polygon(exterior, holes=[hole])
        buffered = poly.buffer(1.0, resolution=8)
        assert buffered.geom_type == "Polygon"


class TestRingBuffer:
    """Test Ring.buffer() method"""

    def test_ring_buffer_creates_polygon(self):
        """Test that Ring buffer creates a polygon"""
        ring = Ring([(0, 0), (5, 0), (5, 5), (0, 5), (0, 0)])
        buffered = ring.buffer(1.0, resolution=8)
        assert buffered.geom_type == "Polygon"

    def test_ring_buffer_with_join_styles(self):
        """Test Ring buffer with different join styles"""
        ring = Ring([(0, 0), (5, 0), (5, 5), (0, 5), (0, 0)])
        # Round join (default)
        buffered1 = ring.buffer(1.0, join_style=1)
        # Bevel join
        buffered2 = ring.buffer(1.0, join_style=3)
        assert buffered1.geom_type == "Polygon"
        assert buffered2.geom_type == "Polygon"


class TestBufferParameters:
    """Test buffer parameters and options"""

    def test_buffer_resolution_values(self):
        """Test buffer with various resolution values"""
        geom = Geometry("POINT(0 0)", fmt="wkt")
        for resolution in [4, 8, 16, 32]:
            buffered = geom.buffer(1.0, resolution=resolution)
            assert buffered.geom_type == "Polygon"

    def test_buffer_cap_styles(self):
        """Test all cap style values"""
        geom = Geometry("LINESTRING(0 0, 10 0)", fmt="wkt")
        for cap_style in [1, 2, 3]:
            buffered = geom.buffer(1.0, cap_style=cap_style)
            assert buffered.geom_type == "Polygon"

    def test_buffer_join_styles(self):
        """Test all join style values"""
        geom = Geometry("POLYGON((0 0, 10 0, 10 10, 0 10, 0 0))", fmt="wkt")
        for join_style in [1, 2, 3]:
            buffered = geom.buffer(1.0, join_style=join_style)
            assert buffered.geom_type == "Polygon"
