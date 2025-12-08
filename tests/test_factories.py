from togo import Geometry, Point, Line, Ring, Poly


def test_multipoint_from_tuples():
    pts = [(0, 0), (1, 2), (2, -1)]
    mp1 = Geometry.from_multipoint(pts)
    assert mp1.type_string() == "MultiPoint"
    assert mp1.bounds == (0.0, -1.0, 2.0, 2.0)


def test_multipoint_from_points():
    pts_obj = [Point(3, 3), Point(4, 5)]
    mp2 = Geometry.from_multipoint(pts_obj)
    assert mp2.type_string() == "MultiPoint"
    assert mp2.bounds == (3.0, 3.0, 4.0, 5.0)


def test_multilinestring_from_coords():
    ml1 = Geometry.from_multilinestring(
        [
            [(0, 0), (1, 1)],
            [(2, 2), (3, 3), (4, 3)],
        ]
    )
    assert ml1.type_string() == "MultiLineString"
    assert ml1.num_lines == 2
    assert ml1.bounds == (0.0, 0.0, 4.0, 3.0)


def test_multilinestring_from_lines():
    l1 = Line([(10, 10), (11, 12)])
    l2 = Line([(9, 8), (10, 7)])
    ml2 = Geometry.from_multilinestring([l1, l2])
    assert ml2.type_string() == "MultiLineString"
    assert ml2.num_lines == 2


def test_multipolygon_from_polys():
    outer1 = Ring([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)])
    poly1 = Poly(outer1)
    outer2 = Ring([(2, 2), (3, 2), (3, 3), (2, 3), (2, 2)])
    poly2 = Poly(outer2)
    mp = Geometry.from_multipolygon([poly1, poly2])
    assert mp.type_string() == "MultiPolygon"
    assert mp.num_polys == 2
    assert mp.bounds == (0.0, 0.0, 3.0, 3.0)


def test_geometrycollection_mixed_inputs():
    point = Point(1, 2)
    line = Line([(0, 0), (1, 1)])
    ring = Ring([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)])
    poly = Poly(ring)
    geom_point = point.as_geometry()

    gc = Geometry.from_geometrycollection(
        [geom_point, line, ring, poly, (5, 6), Point(7, 8)]
    )
    assert gc.type_string() == "GeometryCollection"
    assert gc.num_geometries == 6
