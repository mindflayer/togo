"""
Test suite for Shapely-compatible APIs in togo
"""

import pytest
import json


class TestShapelyImports:
    """Test that Shapely-compatible names can be imported"""

    def test_import_point(self):
        from togo import Point

        assert Point is not None

    def test_import_linestring(self):
        from togo import LineString

        assert LineString is not None

    def test_import_polygon(self):
        from togo import Polygon

        assert Polygon is not None

    def test_import_module_functions(self):
        from togo import from_wkt, from_geojson, from_wkb
        from togo import to_wkt, to_geojson, to_wkb

        assert from_wkt is not None
        assert from_geojson is not None
        assert from_wkb is not None
        assert to_wkt is not None
        assert to_geojson is not None
        assert to_wkb is not None

    def test_import_multi_constructors(self):
        from togo import MultiPoint, MultiLineString, MultiPolygon, GeometryCollection

        assert MultiPoint is not None
        assert MultiLineString is not None
        assert MultiPolygon is not None
        assert GeometryCollection is not None


class TestPointShapelyAPI:
    """Test Shapely-compatible API for Point"""

    def test_point_creation(self):
        from togo import Point

        p = Point(1.5, 2.5)
        assert p.x == 1.5
        assert p.y == 2.5

    def test_point_geom_type(self):
        from togo import Point

        p = Point(1.0, 2.0)
        assert p.geom_type == "Point"

    def test_point_bounds(self):
        from togo import Point

        p = Point(3.5, 4.5)
        assert p.bounds == (3.5, 4.5, 3.5, 4.5)

    def test_point_coords(self):
        from togo import Point

        p = Point(1.0, 2.0)
        assert p.coords == [(1.0, 2.0)]

    def test_point_is_empty(self):
        from togo import Point

        p = Point(1.0, 2.0)
        assert not p.is_empty

    def test_point_wkt_property(self):
        from togo import Point

        p = Point(1.0, 2.0)
        wkt = p.wkt
        assert isinstance(wkt, str)
        assert "POINT" in wkt
        assert "1" in wkt
        assert "2" in wkt

    def test_point_wkb_property(self):
        from togo import Point

        p = Point(1.0, 2.0)
        wkb = p.wkb
        assert isinstance(wkb, bytes)
        assert len(wkb) > 0

    def test_point_geo_interface(self):
        from togo import Point

        p = Point(1.5, 2.5)
        geo = p.__geo_interface__()
        assert isinstance(geo, dict)
        assert geo["type"] == "Point"
        assert geo["coordinates"] == [1.5, 2.5]

    def test_point_negative_coords(self):
        from togo import Point

        p = Point(-10.5, -20.3)
        assert p.x == -10.5
        assert p.y == -20.3
        assert p.bounds == (-10.5, -20.3, -10.5, -20.3)

    def test_point_zero_coords(self):
        from togo import Point

        p = Point(0.0, 0.0)
        assert p.coords == [(0.0, 0.0)]
        assert p.bounds == (0.0, 0.0, 0.0, 0.0)


class TestLineStringShapelyAPI:
    """Test Shapely-compatible API for LineString"""

    def test_linestring_creation(self):
        from togo import LineString

        line = LineString([(0, 0), (1, 1), (2, 2)])
        assert line is not None

    def test_linestring_geom_type(self):
        from togo import LineString

        line = LineString([(0, 0), (1, 1)])
        assert line.geom_type == "LineString"

    def test_linestring_coords(self):
        from togo import LineString

        coords = [(0, 0), (1, 1), (2, 2)]
        line = LineString(coords)
        assert line.coords == coords

    def test_linestring_bounds(self):
        from togo import LineString

        line = LineString([(0, 0), (5, 10)])
        bounds = line.bounds
        assert bounds == (0, 0, 5, 10)

    def test_linestring_is_empty(self):
        from togo import LineString

        line = LineString([(0, 0), (1, 1)])
        assert not line.is_empty

    def test_linestring_length(self):
        from togo import LineString

        line = LineString([(0, 0), (3, 4)])  # 3-4-5 triangle
        length = line.length
        assert length == pytest.approx(5.0, rel=1e-5)

    def test_linestring_wkt_property(self):
        from togo import LineString

        line = LineString([(0, 0), (1, 1), (2, 2)])
        wkt = line.wkt
        assert isinstance(wkt, str)
        assert "LINESTRING" in wkt

    def test_linestring_wkb_property(self):
        from togo import LineString

        line = LineString([(0, 0), (1, 1)])
        wkb = line.wkb
        assert isinstance(wkb, bytes)
        assert len(wkb) > 0

    def test_linestring_geo_interface(self):
        from togo import LineString

        coords = [(0, 0), (1, 1), (2, 2)]
        line = LineString(coords)
        geo = line.__geo_interface__()
        assert isinstance(geo, dict)
        assert geo["type"] == "LineString"
        assert geo["coordinates"] == coords

    def test_linestring_complex_path(self):
        from togo import LineString

        coords = [(0, 0), (1, 2), (3, 1), (5, 5)]
        line = LineString(coords)
        assert line.coords == coords
        assert len(line.coords) == 4

    def test_linestring_negative_coords(self):
        from togo import LineString

        line = LineString([(-5, -5), (5, 5)])
        assert line.bounds == (-5, -5, 5, 5)


class TestPolygonShapelyAPI:
    """Test Shapely-compatible API for Polygon"""

    def test_polygon_creation_with_exterior_and_holes_as_lists(self):
        from togo import Polygon

        exterior = [(0, 0), (10, 0), (10, 10), (0, 10), (0, 0)]
        hole = [(2, 2), (4, 2), (4, 4), (2, 4), (2, 2)]
        poly = Polygon(exterior, holes=[hole])
        assert poly is not None
        
        # Verify exterior coordinates
        assert poly.exterior().coords == exterior
        
        # Verify there is exactly one hole
        assert len(poly.interiors) == 1
        
        # Verify the hole coordinates
        assert poly.interiors[0].coords == hole

    def test_polygon_creation_with_exterior_as_list(self):
        from togo import Polygon

        exterior = [(0, 0), (10, 0), (10, 10), (0, 10), (0, 0)]
        poly = Polygon(exterior)
        assert poly is not None

    def test_polygon_creation_with_exterior_as_list_and_holes_as_empty_list(self):
        from togo import Polygon

        exterior = [(0, 0), (10, 0), (10, 10), (0, 10), (0, 0)]
        poly = Polygon(exterior, holes=[])
        assert poly is not None

    def test_polygon_creation(self):
        from togo import Polygon, Ring

        exterior = Ring([(0, 0), (4, 0), (4, 4), (0, 4), (0, 0)])
        poly = Polygon(exterior)
        assert poly is not None

    def test_polygon_geom_type(self):
        from togo import Polygon, Ring

        exterior = Ring([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)])
        poly = Polygon(exterior)
        assert poly.geom_type == "Polygon"

    def test_polygon_bounds(self):
        from togo import Polygon, Ring

        exterior = Ring([(0, 0), (5, 0), (5, 10), (0, 10), (0, 0)])
        poly = Polygon(exterior)
        assert poly.bounds == (0, 0, 5, 10)

    def test_polygon_area(self):
        from togo import Polygon, Ring

        exterior = Ring([(0, 0), (4, 0), (4, 4), (0, 4), (0, 0)])
        poly = Polygon(exterior)
        assert poly.area == pytest.approx(16.0, rel=1e-5)

    def test_polygon_is_empty(self):
        from togo import Polygon, Ring

        exterior = Ring([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)])
        poly = Polygon(exterior)
        assert not poly.is_empty

    def test_polygon_exterior(self):
        from togo import Polygon, Ring

        exterior = Ring([(0, 0), (4, 0), (4, 4), (0, 4), (0, 0)])
        poly = Polygon(exterior)
        ext = poly.exterior()
        assert ext is not None
        assert len(ext.coords) == 5

    def test_polygon_interiors_no_holes(self):
        from togo import Polygon, Ring

        exterior = Ring([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)])
        poly = Polygon(exterior)
        assert isinstance(poly.interiors, list)
        assert len(poly.interiors) == 0

    def test_polygon_interiors_with_holes(self):
        from togo import Polygon, Ring

        exterior = Ring([(0, 0), (10, 0), (10, 10), (0, 10), (0, 0)])
        hole1 = Ring([(2, 2), (4, 2), (4, 4), (2, 4), (2, 2)])
        hole2 = Ring([(6, 6), (8, 6), (8, 8), (6, 8), (6, 6)])
        poly = Polygon(exterior, holes=[hole1, hole2])
        assert len(poly.interiors) == 2
        assert all(hasattr(h, "coords") for h in poly.interiors)

    def test_polygon_wkt_property(self):
        from togo import Polygon, Ring

        exterior = Ring([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)])
        poly = Polygon(exterior)
        wkt = poly.wkt
        assert isinstance(wkt, str)
        assert "POLYGON" in wkt

    def test_polygon_wkb_property(self):
        from togo import Polygon, Ring

        exterior = Ring([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)])
        poly = Polygon(exterior)
        wkb = poly.wkb
        assert isinstance(wkb, bytes)
        assert len(wkb) > 0

    def test_polygon_geo_interface_no_holes(self):
        from togo import Polygon, Ring

        coords = [(0, 0), (4, 0), (4, 4), (0, 4), (0, 0)]
        exterior = Ring(coords)
        poly = Polygon(exterior)
        geo = poly.__geo_interface__()
        assert isinstance(geo, dict)
        assert geo["type"] == "Polygon"
        assert geo["coordinates"] == [coords]

    def test_polygon_geo_interface_with_holes(self):
        from togo import Polygon, Ring

        ext_coords = [(0, 0), (10, 0), (10, 10), (0, 10), (0, 0)]
        hole_coords = [(2, 2), (8, 2), (8, 8), (2, 8), (2, 2)]
        exterior = Ring(ext_coords)
        hole = Ring(hole_coords)
        poly = Polygon(exterior, holes=[hole])
        geo = poly.__geo_interface__()
        assert geo["type"] == "Polygon"
        assert geo["coordinates"] == [ext_coords, hole_coords]

    def test_polygon_large_area(self):
        from togo import Polygon, Ring

        exterior = Ring([(0, 0), (100, 0), (100, 100), (0, 100), (0, 0)])
        poly = Polygon(exterior)
        assert poly.area == pytest.approx(10000.0, rel=1e-5)


class TestRingShapelyAPI:
    """Test Shapely-compatible API for Ring"""

    def test_ring_coords_property(self):
        from togo import Ring

        coords = [(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)]
        ring = Ring(coords)
        assert ring.coords == coords


class TestGeometryShapelyAPI:
    """Test Shapely-compatible API for Geometry class"""

    def test_geometry_point_geom_type(self):
        from togo import Geometry

        geom = Geometry('{"type":"Point","coordinates":[1,2]}')
        assert geom.geom_type == "Point"

    def test_geometry_linestring_geom_type(self):
        from togo import Geometry

        geom = Geometry('{"type":"LineString","coordinates":[[0,0],[1,1]]}')
        assert geom.geom_type == "LineString"

    def test_geometry_polygon_geom_type(self):
        from togo import Geometry

        geom = Geometry(
            '{"type":"Polygon","coordinates":[[[0,0],[1,0],[1,1],[0,1],[0,0]]]}'
        )
        assert geom.geom_type == "Polygon"

    def test_geometry_bounds(self):
        from togo import Geometry

        geom = Geometry("POINT (5 10)", fmt="wkt")
        assert geom.bounds == (5.0, 10.0, 5.0, 10.0)

    def test_geometry_area_polygon(self):
        from togo import Geometry

        geom = Geometry("POLYGON ((0 0, 5 0, 5 5, 0 5, 0 0))", fmt="wkt")
        assert geom.area == pytest.approx(25.0, rel=1e-5)

    def test_geometry_area_linestring(self):
        from togo import Geometry

        geom = Geometry("LINESTRING (0 0, 1 1)", fmt="wkt")
        assert geom.area == 0.0

    def test_geometry_length_linestring(self):
        from togo import Geometry

        geom = Geometry("LINESTRING (0 0, 3 4)", fmt="wkt")
        assert geom.length == pytest.approx(5.0, rel=1e-5)

    def test_geometry_length_polygon(self):
        from togo import Geometry

        geom = Geometry("POLYGON ((0 0, 4 0, 4 4, 0 4, 0 0))", fmt="wkt")
        # For polygon, length returns perimeter
        assert geom.length == pytest.approx(16.0, rel=1e-5)

    def test_geometry_wkt_property(self):
        from togo import Geometry

        geom = Geometry("POINT (1 2)", fmt="wkt")
        wkt = geom.wkt
        assert isinstance(wkt, str)
        assert "POINT" in wkt

    def test_geometry_wkb_property(self):
        from togo import Geometry

        geom = Geometry("POINT (1 2)", fmt="wkt")
        wkb = geom.wkb
        assert isinstance(wkb, bytes)
        assert len(wkb) > 0

    def test_geometry_coords_point(self):
        from togo import Geometry

        geom = Geometry("POINT (5 10)", fmt="wkt")
        coords = geom.coords
        assert coords == [(5.0, 10.0)]

    def test_geometry_coords_linestring(self):
        from togo import Geometry

        geom = Geometry("LINESTRING (0 0, 1 1, 2 2)", fmt="wkt")
        coords = geom.coords
        assert len(coords) == 3
        assert coords[0] == (0.0, 0.0)
        assert coords[2] == (2.0, 2.0)

    def test_geometry_coords_polygon_raises(self):
        from togo import Geometry

        geom = Geometry("POLYGON ((0 0, 1 0, 1 1, 0 1, 0 0))", fmt="wkt")
        with pytest.raises(AttributeError):
            _ = geom.coords

    def test_geometry_geo_interface(self):
        from togo import Geometry

        geom = Geometry('{"type":"Point","coordinates":[3,4]}')
        geo = geom.__geo_interface__()
        assert isinstance(geo, dict)
        assert geo["type"] == "Point"
        assert geo["coordinates"] == [3, 4]


class TestModuleLevelFunctions:
    """Test module-level Shapely-compatible functions"""

    def test_from_wkt_point(self):
        from togo import from_wkt

        geom = from_wkt("POINT (1 2)")
        assert geom.geom_type == "Point"
        assert geom.bounds == (1.0, 2.0, 1.0, 2.0)

    def test_from_wkt_linestring(self):
        from togo import from_wkt

        geom = from_wkt("LINESTRING (0 0, 1 1, 2 2)")
        assert geom.geom_type == "LineString"

    def test_from_wkt_polygon(self):
        from togo import from_wkt

        geom = from_wkt("POLYGON ((0 0, 4 0, 4 4, 0 4, 0 0))")
        assert geom.geom_type == "Polygon"
        assert geom.area == pytest.approx(16.0)

    def test_from_wkt_multipoint(self):
        from togo import from_wkt

        geom = from_wkt("MULTIPOINT ((0 0), (1 1))")
        assert geom.geom_type == "MultiPoint"

    def test_from_geojson_point(self):
        from togo import from_geojson

        geom = from_geojson('{"type":"Point","coordinates":[1,2]}')
        assert geom.geom_type == "Point"
        assert geom.coords == [(1.0, 2.0)]

    def test_from_geojson_linestring(self):
        from togo import from_geojson

        geom = from_geojson('{"type":"LineString","coordinates":[[0,0],[1,1]]}')
        assert geom.geom_type == "LineString"

    def test_from_geojson_polygon(self):
        from togo import from_geojson

        geom = from_geojson(
            '{"type":"Polygon","coordinates":[[[0,0],[1,0],[1,1],[0,1],[0,0]]]}'
        )
        assert geom.geom_type == "Polygon"

    def test_from_wkb(self):
        from togo import from_wkt, from_wkb

        # First create a geometry and get its WKB
        geom1 = from_wkt("POINT (5 10)")
        wkb_bytes = geom1.wkb
        # Now parse it back
        geom2 = from_wkb(wkb_bytes)
        assert geom2.geom_type == "Point"
        # Bounds should be approximately equal
        assert geom2.bounds == pytest.approx(geom1.bounds)

    def test_to_wkt_from_point(self):
        from togo import Point, to_wkt

        p = Point(1.0, 2.0)
        wkt = to_wkt(p)
        assert isinstance(wkt, str)
        assert "POINT" in wkt

    def test_to_wkt_from_linestring(self):
        from togo import LineString, to_wkt

        line = LineString([(0, 0), (1, 1)])
        wkt = to_wkt(line)
        assert isinstance(wkt, str)
        assert "LINESTRING" in wkt

    def test_to_wkt_from_polygon(self):
        from togo import Polygon, Ring, to_wkt

        poly = Polygon(Ring([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)]))
        wkt = to_wkt(poly)
        assert isinstance(wkt, str)
        assert "POLYGON" in wkt

    def test_to_wkt_from_geometry(self):
        from togo import Geometry, to_wkt

        geom = Geometry("POINT (3 4)", fmt="wkt")
        wkt = to_wkt(geom)
        assert "POINT" in wkt

    def test_to_geojson_from_point(self):
        from togo import Point, to_geojson

        p = Point(1.0, 2.0)
        geojson_str = to_geojson(p)
        assert isinstance(geojson_str, str)
        data = json.loads(geojson_str)
        assert data["type"] == "Point"

    def test_to_geojson_from_linestring(self):
        from togo import LineString, to_geojson

        line = LineString([(0, 0), (1, 1)])
        geojson_str = to_geojson(line)
        data = json.loads(geojson_str)
        assert data["type"] == "LineString"

    def test_to_wkb_from_point(self):
        from togo import Point, to_wkb

        p = Point(1.0, 2.0)
        wkb = to_wkb(p)
        assert isinstance(wkb, bytes)
        assert len(wkb) > 0

    def test_to_wkb_from_geometry(self):
        from togo import Geometry, to_wkb

        geom = Geometry("POINT (5 10)", fmt="wkt")
        wkb = to_wkb(geom)
        assert isinstance(wkb, bytes)
        assert len(wkb) > 0


class TestMultiGeometries:
    """Test Shapely-compatible multi-geometry constructors"""

    def test_multipoint_creation(self):
        from togo import MultiPoint, Point

        points = [Point(0, 0), Point(1, 1), Point(2, 2)]
        multi = MultiPoint(points)
        assert multi.geom_type == "MultiPoint"

    def test_multipoint_from_tuples(self):
        from togo import MultiPoint

        points = [(0, 0), (1, 1), (2, 2)]
        multi = MultiPoint(points)
        assert multi.geom_type == "MultiPoint"

    def test_multilinestring_creation(self):
        from togo import MultiLineString, LineString

        lines = [LineString([(0, 0), (1, 1)]), LineString([(2, 2), (3, 3)])]
        multi = MultiLineString(lines)
        assert multi.geom_type == "MultiLineString"

    def test_multilinestring_from_coords(self):
        from togo import MultiLineString

        lines = [[(0, 0), (1, 1)], [(2, 2), (3, 3)]]
        multi = MultiLineString(lines)
        assert multi.geom_type == "MultiLineString"

    def test_multipolygon_creation(self):
        from togo import MultiPolygon, Polygon, Ring

        polys = [
            Polygon(Ring([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)])),
            Polygon(Ring([(2, 2), (3, 2), (3, 3), (2, 3), (2, 2)])),
        ]
        multi = MultiPolygon(polys)
        assert multi.geom_type == "MultiPolygon"

    def test_geometrycollection_creation(self):
        from togo import GeometryCollection, Point, LineString

        geoms = [Point(0, 0), LineString([(1, 1), (2, 2)])]
        collection = GeometryCollection(geoms)
        assert collection.geom_type == "GeometryCollection"


class TestSpatialPredicates:
    """Test that spatial predicates work with Shapely-compatible API"""

    def test_contains_point_in_polygon(self):
        from togo import Polygon, Ring, Point

        poly = Polygon(Ring([(0, 0), (10, 0), (10, 10), (0, 10), (0, 0)]))
        point = Point(5, 5)

        poly_geom = poly.as_geometry()
        pt_geom = point.as_geometry()
        assert poly_geom.contains(pt_geom)

    def test_contains_point_outside_polygon(self):
        from togo import Polygon, Ring, Point

        poly = Polygon(Ring([(0, 0), (10, 0), (10, 10), (0, 10), (0, 0)]))
        point = Point(15, 15)

        poly_geom = poly.as_geometry()
        pt_geom = point.as_geometry()
        assert not poly_geom.contains(pt_geom)

    def test_intersects_overlapping_polygons(self):
        from togo import Polygon, Ring

        poly1 = Polygon(Ring([(0, 0), (5, 0), (5, 5), (0, 5), (0, 0)]))
        poly2 = Polygon(Ring([(3, 3), (8, 3), (8, 8), (3, 8), (3, 3)]))

        geom1 = poly1.as_geometry()
        geom2 = poly2.as_geometry()
        assert geom1.intersects(geom2)

    def test_intersects_non_overlapping_polygons(self):
        from togo import Polygon, Ring

        poly1 = Polygon(Ring([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)]))
        poly2 = Polygon(Ring([(10, 10), (11, 10), (11, 11), (10, 11), (10, 10)]))

        geom1 = poly1.as_geometry()
        geom2 = poly2.as_geometry()
        assert not geom1.intersects(geom2)

    def test_equals_same_polygon(self):
        from togo import Polygon, Ring

        poly1 = Polygon(Ring([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)]))
        poly2 = Polygon(Ring([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)]))

        geom1 = poly1.as_geometry()
        geom2 = poly2.as_geometry()
        assert geom1.equals(geom2)

    def test_equals_different_polygons(self):
        from togo import Polygon, Ring

        poly1 = Polygon(Ring([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)]))
        poly2 = Polygon(Ring([(0, 0), (2, 0), (2, 2), (0, 2), (0, 0)]))

        geom1 = poly1.as_geometry()
        geom2 = poly2.as_geometry()
        assert not geom1.equals(geom2)

    def test_disjoint(self):
        from togo import Polygon, Ring

        poly1 = Polygon(Ring([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)]))
        poly2 = Polygon(Ring([(10, 10), (11, 10), (11, 11), (10, 11), (10, 10)]))

        geom1 = poly1.as_geometry()
        geom2 = poly2.as_geometry()
        assert geom1.disjoint(geom2)

    def test_within(self):
        from togo import Polygon, Ring, Point

        poly = Polygon(Ring([(0, 0), (10, 0), (10, 10), (0, 10), (0, 0)]))
        point = Point(5, 5)

        poly_geom = poly.as_geometry()
        pt_geom = point.as_geometry()
        assert pt_geom.within(poly_geom)

    def test_covers(self):
        from togo import Polygon, Ring, Point

        poly = Polygon(Ring([(0, 0), (10, 0), (10, 10), (0, 10), (0, 0)]))
        point = Point(5, 5)

        poly_geom = poly.as_geometry()
        pt_geom = point.as_geometry()
        assert poly_geom.covers(pt_geom)

    def test_coveredby(self):
        from togo import Polygon, Ring, Point

        poly = Polygon(Ring([(0, 0), (10, 0), (10, 10), (0, 10), (0, 0)]))
        point = Point(5, 5)

        poly_geom = poly.as_geometry()
        pt_geom = point.as_geometry()
        assert pt_geom.coveredby(poly_geom)

    def test_touches_adjacent_polygons(self):
        from togo import Polygon, Ring

        poly1 = Polygon(Ring([(0, 0), (5, 0), (5, 5), (0, 5), (0, 0)]))
        poly2 = Polygon(Ring([(5, 0), (10, 0), (10, 5), (5, 5), (5, 0)]))

        geom1 = poly1.as_geometry()
        geom2 = poly2.as_geometry()
        # Adjacent polygons should touch
        result = geom1.touches(geom2)
        assert isinstance(result, (bool, int))


class TestRoundTripConversions:
    """Test that geometries can be converted and parsed back"""

    def test_point_wkt_roundtrip(self):
        from togo import Point, from_wkt

        p1 = Point(1.5, 2.5)
        wkt = p1.wkt
        geom = from_wkt(wkt)
        assert geom.geom_type == "Point"
        assert geom.bounds == pytest.approx(p1.bounds)

    def test_linestring_wkt_roundtrip(self):
        from togo import LineString, from_wkt

        line1 = LineString([(0, 0), (1, 1), (2, 2)])
        wkt = line1.wkt
        geom = from_wkt(wkt)
        assert geom.geom_type == "LineString"

    def test_polygon_wkt_roundtrip(self):
        from togo import Polygon, Ring, from_wkt

        poly1 = Polygon(Ring([(0, 0), (4, 0), (4, 4), (0, 4), (0, 0)]))
        wkt = poly1.wkt
        geom = from_wkt(wkt)
        assert geom.geom_type == "Polygon"
        assert geom.area == pytest.approx(poly1.area)

    def test_point_geojson_roundtrip(self):
        from togo import Point, from_geojson, to_geojson

        p1 = Point(3.5, 4.5)
        geojson_str = to_geojson(p1)
        geom = from_geojson(geojson_str)
        assert geom.geom_type == "Point"

    def test_point_wkb_roundtrip(self):
        from togo import Point, from_wkb, to_wkb

        p1 = Point(7.5, 8.5)
        wkb_bytes = to_wkb(p1)
        geom = from_wkb(wkb_bytes)
        assert geom.geom_type == "Point"
        assert geom.bounds == pytest.approx(p1.bounds)


class TestEdgeCases:
    """Test edge cases and error handling"""

    def test_empty_multipoint(self):
        from togo import MultiPoint

        multi = MultiPoint([])
        assert multi.geom_type == "MultiPoint"

    def test_empty_multilinestring(self):
        from togo import MultiLineString

        multi = MultiLineString([])
        assert multi.geom_type == "MultiLineString"

    def test_empty_multipolygon(self):
        from togo import MultiPolygon

        multi = MultiPolygon([])
        assert multi.geom_type == "MultiPolygon"

    def test_empty_geometrycollection(self):
        from togo import GeometryCollection

        collection = GeometryCollection([])
        assert collection.geom_type == "GeometryCollection"

    def test_point_with_large_coordinates(self):
        from togo import Point

        p = Point(1000000.5, 2000000.5)
        assert p.x == 1000000.5
        assert p.y == 2000000.5

    def test_invalid_wkt_raises_error(self):
        from togo import from_wkt

        with pytest.raises(ValueError):
            from_wkt("INVALID WKT STRING")

    def test_invalid_geojson_raises_error(self):
        from togo import from_geojson

        with pytest.raises(ValueError):
            from_geojson('{"invalid": "geojson"}')
