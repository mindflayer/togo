import json

import pytest
import togo as tg


def translate(dx, dy):
    def _f(x, y):
        return x + dx, y + dy

    return _f


def scale(sx, sy):
    def _f(x, y):
        return x * sx, y * sy

    return _f


def test_transform_point_translate():
    p = tg.Point(1, 2)
    g = p.as_geometry()
    t = tg.transform(translate(10, -5), g)
    assert t.type_string() == "Point"
    assert t.coords == [(11.0, -3.0)]


def test_transform_linestring_scale():
    line = tg.Line([(0, 0), (1, 2), (3, 4)])
    g = line.as_geometry()
    t = tg.transform(scale(2, 3), g)
    assert t.type_string() == "LineString"
    assert t.coords == [(0.0, 0.0), (2.0, 6.0), (6.0, 12.0)]


def test_transform_polygon_translate_with_holes():
    ext = tg.Ring([(0, 0), (4, 0), (4, 4), (0, 4), (0, 0)])
    hole = tg.Ring([(1, 1), (2, 1), (2, 2), (1, 2), (1, 1)])
    poly = tg.Poly(ext, [hole])
    g = poly.as_geometry()
    t = tg.transform(translate(5, -1), g)
    assert t.type_string() == "Polygon"
    # check exterior first and last points
    pg = t.poly()
    ext2 = pg.exterior.points()
    assert ext2[0] == (5.0, -1.0)
    assert ext2[-1] == (5.0, -1.0)
    # hole preserved
    assert pg.num_holes() == 1
    hole2 = pg.hole(0).points()
    assert hole2[0] == (6.0, 0.0)


def test_transform_multipoint_translate():
    mp = tg.MultiPoint([(0, 0), (1, 1), (2, 2)])
    t = tg.transform(translate(1, 2), mp)
    assert t.type_string() == "MultiPoint"
    # convert to geojson and check coords
    coords = json.loads(t.to_geojson())["coordinates"]
    assert coords == [[1.0, 2.0], [2.0, 3.0], [3.0, 4.0]]


def test_transform_multilinestring_scale():
    mls = tg.MultiLineString([[(0, 0), (1, 0)], [(2, 2), (3, 3), (4, 4)]])
    t = tg.transform(scale(2, 2), mls)
    assert t.type_string() == "MultiLineString"
    # check first line coords
    l0 = t[0].coords
    assert l0 == [(0.0, 0.0), (2.0, 0.0)]


def test_transform_multipolygon_translate():
    p1 = tg.Polygon([(0, 0), (2, 0), (2, 2), (0, 2), (0, 0)])
    p2 = tg.Polygon([(3, 3), (5, 3), (5, 5), (3, 5), (3, 3)])
    mp = tg.MultiPolygon([p1, p2])
    t = tg.transform(translate(-1, -1), mp)
    assert t.type_string() == "MultiPolygon"
    # check first polygon ext first point
    g0 = t[0]
    ext0 = g0.poly().exterior.points()[0]
    assert ext0 == (-1.0, -1.0)


def test_transform_geometrycollection_recursive():
    gc = tg.GeometryCollection(
        [
            tg.Point(0, 0),
            tg.Line([(0, 0), (1, 1)]),
            tg.Polygon([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)]),
        ]
    )
    t = tg.transform(translate(1, 0), gc)
    assert t.type_string() == "GeometryCollection"
    # Validate child types
    assert t[0].type_string() == "Point"
    assert t[1].type_string() == "LineString"
    assert t[2].type_string() == "Polygon"


def test_transform_bad_callable():
    def bad(x, y):
        return None

    with pytest.raises(TypeError):
        tg.transform(bad, tg.Point(1, 2))


def test_transform_empty_multipoint():
    """Test that transforming an empty MultiPoint returns an empty MultiPoint."""
    mp = tg.MultiPoint([])
    t = tg.transform(translate(1, 2), mp)
    assert t.type_string() == "MultiPoint"
    # Convert to geojson and verify it's empty
    coords = json.loads(t.to_geojson())["coordinates"]
    assert coords == []
    assert t.num_points == 0


def test_transform_empty_multilinestring():
    """Test that transforming an empty MultiLineString returns an empty MultiLineString."""
    mls = tg.MultiLineString([])
    t = tg.transform(scale(2, 2), mls)
    assert t.type_string() == "MultiLineString"
    # Verify it has no lines
    assert t.num_lines == 0


def test_transform_empty_multipolygon():
    """Test that transforming an empty MultiPolygon returns an empty MultiPolygon."""
    mp = tg.MultiPolygon([])
    t = tg.transform(translate(-1, -1), mp)
    assert t.type_string() == "MultiPolygon"
    # Verify it has no polygons
    assert t.num_polys == 0


def test_transform_empty_geometrycollection():
    """Test that transforming an empty GeometryCollection returns an empty GeometryCollection."""
    gc = tg.GeometryCollection([])
    t = tg.transform(translate(1, 0), gc)
    assert t.type_string() == "GeometryCollection"
    # Verify it has no child geometries
    assert t.num_geometries == 0
