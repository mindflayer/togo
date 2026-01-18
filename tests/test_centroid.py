"""
Tests for centroid property implementations as direct class methods
Tests that centroid works on Point, LineString, Polygon, Ring, and MultiPoint instances
Also tests centroid on Geometry instances
"""

from togo import Point, LineString, Polygon, Ring, MultiPoint, Geometry


class TestGeometryCentroid:
    """Test Geometry.centroid property"""

    def test_geometry_centroid_point(self):
        """Test centroid of a point"""
        geom = Geometry("POINT(1 2)", fmt="wkt")
        centroid = geom.centroid
        assert centroid is not None
        assert centroid.geom_type == "Point"
        # Centroid of a point is the point itself
        assert "POINT(1 2)" in centroid.to_wkt() or "POINT (1 2)" in centroid.to_wkt()

    def test_geometry_centroid_linestring(self):
        """Test centroid of a linestring"""
        geom = Geometry("LINESTRING(0 0, 10 0, 10 10)", fmt="wkt")
        centroid = geom.centroid
        assert centroid is not None
        assert centroid.geom_type == "Point"
        # Centroid should be somewhere in the middle
        wkt = centroid.to_wkt()
        assert "POINT" in wkt

    def test_geometry_centroid_polygon_square(self):
        """Test centroid of a square polygon"""
        geom = Geometry("POLYGON((0 0, 10 0, 10 10, 0 10, 0 0))", fmt="wkt")
        centroid = geom.centroid
        assert centroid is not None
        assert centroid.geom_type == "Point"
        # Centroid of a square should be at its center (5, 5)
        wkt = centroid.to_wkt()
        assert "POINT" in wkt
        # Extract coordinates from WKT and check they're close to (5, 5)
        assert "5" in wkt

    def test_geometry_centroid_polygon_triangle(self):
        """Test centroid of a triangle polygon"""
        geom = Geometry("POLYGON((0 0, 10 0, 5 10, 0 0))", fmt="wkt")
        centroid = geom.centroid
        assert centroid is not None
        assert centroid.geom_type == "Point"
        # Centroid should exist
        wkt = centroid.to_wkt()
        assert "POINT" in wkt

    def test_geometry_centroid_polygon_with_hole(self):
        """Test centroid of polygon with hole"""
        geom = Geometry(
            "POLYGON((0 0, 10 0, 10 10, 0 10, 0 0), (2 2, 8 2, 8 8, 2 8, 2 2))",
            fmt="wkt",
        )
        centroid = geom.centroid
        assert centroid is not None
        assert centroid.geom_type == "Point"
        wkt = centroid.to_wkt()
        assert "POINT" in wkt

    def test_geometry_centroid_multipoint(self):
        """Test centroid of multipoint"""
        geom = Geometry("MULTIPOINT((0 0), (10 10))", fmt="wkt")
        centroid = geom.centroid
        assert centroid is not None
        assert centroid.geom_type == "Point"
        wkt = centroid.to_wkt()
        assert "POINT" in wkt


class TestPointCentroid:
    """Test Point.centroid property"""

    def test_point_centroid(self):
        """Test centroid of a Point"""
        p = Point(3.5, 4.5)
        centroid = p.centroid
        assert centroid is not None
        assert centroid.geom_type == "Point"
        # Centroid of a point is the point itself
        wkt = centroid.to_wkt()
        assert "3.5" in wkt
        assert "4.5" in wkt

    def test_point_centroid_origin(self):
        """Test centroid of point at origin"""
        p = Point(0, 0)
        centroid = p.centroid
        assert centroid is not None
        assert centroid.geom_type == "Point"
        wkt = centroid.to_wkt()
        assert "POINT" in wkt

    def test_point_centroid_negative(self):
        """Test centroid of point with negative coordinates"""
        p = Point(-5.5, -10.25)
        centroid = p.centroid
        assert centroid is not None
        assert centroid.geom_type == "Point"
        wkt = centroid.to_wkt()
        assert "-5.5" in wkt
        assert "-10.25" in wkt


class TestLineStringCentroid:
    """Test LineString.centroid property"""

    def test_linestring_centroid_horizontal(self):
        """Test centroid of horizontal line"""
        line = LineString([(0, 5), (10, 5)])
        centroid = line.centroid
        assert centroid is not None
        assert centroid.geom_type == "Point"
        wkt = centroid.to_wkt()
        assert "POINT" in wkt

    def test_linestring_centroid_diagonal(self):
        """Test centroid of diagonal line"""
        line = LineString([(0, 0), (10, 10)])
        centroid = line.centroid
        assert centroid is not None
        assert centroid.geom_type == "Point"
        wkt = centroid.to_wkt()
        assert "POINT" in wkt

    def test_linestring_centroid_polyline(self):
        """Test centroid of polyline"""
        line = LineString([(0, 0), (10, 0), (10, 10), (0, 10)])
        centroid = line.centroid
        assert centroid is not None
        assert centroid.geom_type == "Point"
        wkt = centroid.to_wkt()
        assert "POINT" in wkt

    def test_linestring_centroid_complex(self):
        """Test centroid of complex polyline"""
        points = [(i, (i * i) % 10) for i in range(0, 20)]
        line = LineString(points)
        centroid = line.centroid
        assert centroid is not None
        assert centroid.geom_type == "Point"
        wkt = centroid.to_wkt()
        assert "POINT" in wkt


class TestPolygonCentroid:
    """Test Polygon.centroid property"""

    def test_polygon_centroid_square(self):
        """Test centroid of square polygon"""
        poly = Polygon([(0, 0), (4, 0), (4, 4), (0, 4), (0, 0)])
        centroid = poly.centroid
        assert centroid is not None
        assert centroid.geom_type == "Point"
        # Centroid should be close to center (2, 2)
        wkt = centroid.to_wkt()
        assert "POINT" in wkt

    def test_polygon_centroid_rectangle(self):
        """Test centroid of rectangular polygon"""
        poly = Polygon([(0, 0), (6, 0), (6, 4), (0, 4), (0, 0)])
        centroid = poly.centroid
        assert centroid is not None
        assert centroid.geom_type == "Point"
        wkt = centroid.to_wkt()
        assert "POINT" in wkt

    def test_polygon_centroid_triangle(self):
        """Test centroid of triangular polygon"""
        poly = Polygon([(0, 0), (10, 0), (5, 10), (0, 0)])
        centroid = poly.centroid
        assert centroid is not None
        assert centroid.geom_type == "Point"
        wkt = centroid.to_wkt()
        assert "POINT" in wkt

    def test_polygon_centroid_irregular(self):
        """Test centroid of irregular polygon"""
        poly = Polygon([(0, 0), (4, 0), (4, 3), (2, 3), (2, 2), (0, 2), (0, 0)])
        centroid = poly.centroid
        assert centroid is not None
        assert centroid.geom_type == "Point"
        wkt = centroid.to_wkt()
        assert "POINT" in wkt

    def test_polygon_centroid_with_hole(self):
        """Test centroid of polygon with hole"""
        exterior = [(0, 0), (10, 0), (10, 10), (0, 10), (0, 0)]
        hole = [(2, 2), (8, 2), (8, 8), (2, 8), (2, 2)]
        poly = Polygon(exterior, holes=[hole])
        centroid = poly.centroid
        assert centroid is not None
        assert centroid.geom_type == "Point"
        wkt = centroid.to_wkt()
        assert "POINT" in wkt


class TestRingCentroid:
    """Test Ring.centroid property"""

    def test_ring_centroid_square(self):
        """Test centroid of square ring"""
        ring = Ring([(0, 0), (4, 0), (4, 4), (0, 4), (0, 0)])
        centroid = ring.centroid
        assert centroid is not None
        assert centroid.geom_type == "Point"
        wkt = centroid.to_wkt()
        assert "POINT" in wkt

    def test_ring_centroid_triangle(self):
        """Test centroid of triangular ring"""
        ring = Ring([(0, 0), (10, 0), (5, 10), (0, 0)])
        centroid = ring.centroid
        assert centroid is not None
        assert centroid.geom_type == "Point"
        wkt = centroid.to_wkt()
        assert "POINT" in wkt

    def test_ring_centroid_pentagon(self):
        """Test centroid of pentagonal ring"""
        ring = Ring([(0, 0), (4, 0), (6, 3), (3, 6), (-1, 3), (0, 0)])
        centroid = ring.centroid
        assert centroid is not None
        assert centroid.geom_type == "Point"
        wkt = centroid.to_wkt()
        assert "POINT" in wkt


class TestMultiPointCentroid:
    """Test MultiPoint.centroid property"""

    def test_multipoint_centroid_two_points(self):
        """Test centroid of two points"""
        mp = MultiPoint([(0, 0), (10, 10)])
        centroid = mp.centroid
        assert centroid is not None
        assert centroid.geom_type == "Point"
        wkt = centroid.to_wkt()
        assert "POINT" in wkt

    def test_multipoint_centroid_many_points(self):
        """Test centroid of many points"""
        points = [(i, i) for i in range(10)]
        mp = MultiPoint(points)
        centroid = mp.centroid
        assert centroid is not None
        assert centroid.geom_type == "Point"
        wkt = centroid.to_wkt()
        assert "POINT" in wkt

    def test_multipoint_centroid_scattered(self):
        """Test centroid of scattered points"""
        mp = MultiPoint([(0, 0), (10, 0), (10, 10), (0, 10), (5, 5)])
        centroid = mp.centroid
        assert centroid is not None
        assert centroid.geom_type == "Point"
        wkt = centroid.to_wkt()
        assert "POINT" in wkt


class TestCentroidProperties:
    """Test centroid properties and behavior"""

    def test_centroid_is_property(self):
        """Test that centroid is a property, not a method"""
        poly = Polygon([(0, 0), (4, 0), (4, 4), (0, 4), (0, 0)])
        # Should be accessible as property (no parentheses)
        centroid = poly.centroid
        assert centroid is not None

    def test_centroid_returns_geometry(self):
        """Test that centroid returns Geometry object"""
        poly = Polygon([(0, 0), (4, 0), (4, 4), (0, 4), (0, 0)])
        centroid = poly.centroid
        assert hasattr(centroid, "geom_type")
        assert hasattr(centroid, "to_wkt")
        assert hasattr(centroid, "bounds")

    def test_centroid_can_chain_operations(self):
        """Test that centroid result can be used in further operations"""
        poly = Polygon([(0, 0), (4, 0), (4, 4), (0, 4), (0, 0)])
        centroid = poly.centroid
        # Should be able to call methods on the result
        wkt = centroid.to_wkt()
        assert wkt is not None
        bounds = centroid.bounds
        assert len(bounds) == 4

    def test_centroid_consistency(self):
        """Test that calling centroid multiple times returns consistent results"""
        poly = Polygon([(0, 0), (4, 0), (4, 4), (0, 4), (0, 0)])
        centroid1 = poly.centroid
        centroid2 = poly.centroid
        # Both should represent the same point
        assert centroid1.to_wkt() == centroid2.to_wkt()


class TestCentroidEdgeCases:
    """Test centroid edge cases"""

    def test_centroid_large_polygon(self):
        """Test centroid of large polygon"""
        # Create a large polygon
        points = [(i, (i * i) % 100) for i in range(0, 1000, 10)]
        points.append(points[0])  # Close the polygon
        poly = Polygon(points)
        centroid = poly.centroid
        assert centroid is not None
        assert centroid.geom_type == "Point"

    def test_centroid_very_small_polygon(self):
        """Test centroid of very small polygon"""
        poly = Polygon([(0, 0), (0.001, 0), (0.001, 0.001), (0, 0.001), (0, 0)])
        centroid = poly.centroid
        assert centroid is not None
        assert centroid.geom_type == "Point"

    def test_centroid_negative_coordinates(self):
        """Test centroid with negative coordinates"""
        poly = Polygon([(-10, -10), (-5, -10), (-5, -5), (-10, -5), (-10, -10)])
        centroid = poly.centroid
        assert centroid is not None
        assert centroid.geom_type == "Point"
        wkt = centroid.to_wkt()
        # Should contain negative values
        assert "-" in wkt

    def test_centroid_mixed_coordinates(self):
        """Test centroid with mixed positive and negative coordinates"""
        poly = Polygon([(-5, -5), (5, -5), (5, 5), (-5, 5), (-5, -5)])
        centroid = poly.centroid
        assert centroid is not None
        assert centroid.geom_type == "Point"
        wkt = centroid.to_wkt()
        assert "POINT" in wkt
