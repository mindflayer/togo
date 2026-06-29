"""
Tests for auto-closing unclosed rings in the Ring and Polygon constructors.

This test suite ensures that unclosed rings are properly closed automatically,
preventing segmentation faults and memory errors when using operations like
centroid, buffer, etc.
"""

from togo import Ring, Polygon


class TestUnclosedRingAutoClose:
    """Test that unclosed rings are automatically closed."""

    def test_ring_unclosed_square(self):
        """Test that unclosed ring is automatically closed."""
        # Create an unclosed ring
        unclosed = Ring([(0, 0), (4, 0), (4, 4), (0, 4)])

        # The ring should be auto-closed, so it should have 5 points
        # (the closing point added automatically)
        points = unclosed.points(as_tuples=True)
        assert len(points) == 5
        # First and last points should match
        assert points[0] == points[-1]
        # Verify coordinates
        assert points[0] == (0.0, 0.0)
        assert points[1] == (4.0, 0.0)
        assert points[2] == (4.0, 4.0)
        assert points[3] == (0.0, 4.0)
        assert points[4] == (0.0, 0.0)

    def test_ring_unclosed_triangle(self):
        """Test unclosed triangular ring."""
        unclosed = Ring([(0, 0), (10, 0), (5, 10)])
        points = unclosed.points(as_tuples=True)
        assert len(points) == 4
        assert points[0] == points[-1]
        assert points[0] == (0.0, 0.0)

    def test_ring_already_closed(self):
        """Test that already closed rings are not modified."""
        closed = Ring([(0, 0), (4, 0), (4, 4), (0, 4), (0, 0)])
        points = closed.points(as_tuples=True)
        # Should remain with 5 points (not duplicate the closing point)
        assert len(points) == 5
        assert points[0] == points[-1]

    def test_ring_single_point(self):
        """Test ring with single point."""
        single = Ring([(0, 0)])
        points = single.points(as_tuples=True)
        # Single point ring should have 1 or 2 points (depending on auto-close)
        assert len(points) >= 1

    def test_ring_empty(self):
        """Test empty ring."""
        empty = Ring([])
        points = empty.points(as_tuples=True)
        assert len(points) == 0

    def test_ring_unclosed_centroid(self):
        """Test centroid on unclosed ring - reproducer case."""
        # This is the case that previously caused a segmentation fault
        ring = Ring([(12, 10), (12, 0), (0, 0), (0, 10)])

        # Should not segfault
        centroid = ring.centroid
        assert centroid is not None
        assert centroid.geom_type == "Point"
        # Centroid of the rectangle should be near (6, 5)
        wkt = centroid.to_wkt()
        assert "POINT" in wkt

    def test_ring_unclosed_buffer(self):
        """Test buffer on unclosed ring."""
        ring = Ring([(0, 0), (4, 0), (4, 4), (0, 4)])

        # Should not segfault
        buffered = ring.buffer(1.0)
        assert buffered is not None
        assert buffered.geom_type == "Polygon"

    def test_ring_unclosed_convex_hull(self):
        """Test convex hull on unclosed ring."""
        ring = Ring([(0, 0), (4, 0), (4, 4), (0, 4)])

        # Should not segfault
        hull = ring.convex_hull
        assert hull is not None
        assert hull.geom_type == "Polygon"


class TestUnclosedPolygonAutoClose:
    """Test that unclosed polygon rings are automatically closed."""

    def test_polygon_unclosed_exterior(self):
        """Test polygon with unclosed exterior ring."""
        # This is the original reproducer case
        poly = Polygon([(12, 10), (12, 0), (0, 0), (0, 10)])

        # Should not raise an error
        assert poly is not None

        # Exterior should be closed
        exterior_points = poly.exterior.points(as_tuples=True)
        assert exterior_points[0] == exterior_points[-1]

    def test_polygon_unclosed_centroid(self):
        """Test centroid on polygon with unclosed ring - reproducer case."""
        # This previously caused: free(): invalid pointer / Segmentation fault
        poly = Polygon([(12, 10), (12, 0), (0, 0), (0, 10)])

        # Should not segfault
        assert hasattr(poly, "centroid")
        centroid = poly.centroid
        assert centroid is not None
        assert centroid.geom_type == "Point"
        assert centroid.to_wkt() == "POINT(6 5)"

    def test_polygon_unclosed_buffer(self):
        """Test buffer on polygon with unclosed ring."""
        poly = Polygon([(0, 0), (4, 0), (4, 4), (0, 4)])

        # Should not segfault
        buffered = poly.buffer(1.0)
        assert buffered is not None
        assert buffered.geom_type == "Polygon"

    def test_polygon_unclosed_area(self):
        """Test area calculation on polygon with unclosed ring."""
        poly = Polygon([(0, 0), (4, 0), (4, 4), (0, 4)])

        # Should calculate area correctly
        area = poly.area
        assert area == 16.0

    def test_polygon_unclosed_with_holes(self):
        """Test polygon with unclosed exterior and closed holes."""
        exterior = [(0, 0), (10, 0), (10, 10), (0, 10)]
        holes = [Ring([(2, 2), (8, 2), (8, 8), (2, 8), (2, 2)])]

        poly = Polygon(exterior, holes=holes)

        # Should work without segfault
        assert poly is not None
        exterior_points = poly.exterior.points(as_tuples=True)
        assert exterior_points[0] == exterior_points[-1]

    def test_polygon_unclosed_intersection(self):
        """Test intersection with polygon with unclosed ring."""
        poly1 = Polygon([(0, 0), (4, 0), (4, 4), (0, 4)])
        poly2 = Polygon([(2, 2), (6, 2), (6, 6), (2, 6), (2, 2)])

        # Should not segfault
        result = poly1.intersection(poly2)
        assert result is not None


class TestClosingTolerance:
    """Test the floating-point tolerance used for ring closing detection."""

    def test_nearly_closed_ring(self):
        """Test ring that's nearly closed (within tolerance)."""
        # Ring with a very small difference between start and end
        ring = Ring([(0, 0), (4, 0), (4, 4), (0, 4), (0, 1e-15)])

        points = ring.points(as_tuples=True)
        # Should be treated as closed (first and last should match within tolerance)
        # So the ring might not get an extra closing point
        assert points[0][0] == points[-1][0]
        assert abs(points[0][1] - points[-1][1]) < 1e-10

    def test_distinctly_unclosed_ring(self):
        """Test ring that's clearly unclosed."""
        ring = Ring([(0, 0), (4, 0), (4, 4), (0, 4), (0, 0.1)])

        points = ring.points(as_tuples=True)
        # Should be treated as unclosed and auto-closed
        # So the first point should be added at the end
        assert len(points) == 6
        assert points[0] == points[-1]


class TestOperationsOnAutoClosedRings:
    """Test various geometry operations on auto-closed rings."""

    def test_all_operations_unclosed_ring(self):
        """Test that all major operations work on unclosed rings."""
        ring = Ring([(0, 0), (4, 0), (4, 4), (0, 4)])

        # All these operations should work without segfault
        operations = {
            "area": lambda r: r.area,
            "length": lambda r: r.length,
            "rect": lambda r: r.rect(),
            "is_convex": lambda r: r.is_convex,
            "is_clockwise": lambda r: r.is_clockwise,
            "centroid": lambda r: r.centroid,
            "convex_hull": lambda r: r.convex_hull,
            "buffer": lambda r: r.buffer(1.0),
            "simplify": lambda r: r.simplify(0.1),
            "as_geometry": lambda r: r.as_geometry(),
            "points": lambda r: r.points(),
        }

        for op_name, op_func in operations.items():
            try:
                result = op_func(ring)
                assert result is not None, f"Operation {op_name} returned None"
            except Exception as e:
                raise AssertionError(f"Operation {op_name} failed: {e}")
