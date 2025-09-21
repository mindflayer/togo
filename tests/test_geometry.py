from togo import Geometry


def test_geometry_wkt():
    g = Geometry("POINT(1 2)", fmt="wkt")
    assert g.type_string() == "Point"
    assert g.rect() == ((1.0, 2.0), (1.0, 2.0))
    assert g.memsize() == 24
    assert g.num_points() == 0  # FIXME? Points in a Point geometry is considered 0
    assert not g.is_feature()
    assert not g.is_featurecollection()
    assert not g.is_empty()
    assert g.dims() == 2
    assert g.has_z() is False
    assert g.has_m() is False
    assert g.to_wkt() == "POINT(1 2)"


def test_geometry_equals():
    g1 = Geometry("POINT(1 2)", fmt="wkt")
    g2 = Geometry("POINT(1 2)", fmt="wkt")
    g3 = Geometry("POINT(2 3)", fmt="wkt")
    assert g1.equals(g2)
    assert not g1.equals(g3)


def test_geometry_disjoint():
    g1 = Geometry("POINT(1 2)", fmt="wkt")
    g2 = Geometry("POINT(2 3)", fmt="wkt")
    assert g1.disjoint(g2)


def test_geometry_contains():
    g1 = Geometry("POINT(1 2)", fmt="wkt")
    g2 = Geometry("POINT(1 2)", fmt="wkt")
    assert g1.contains(g2)


def test_geometry_to_geojson():
    g = Geometry("POINT(1 2)", fmt="wkt")
    geojson = g.to_geojson()
    assert geojson == '{"type":"Point","coordinates":[1,2]}'


def test_geometry_to_hex():
    g = Geometry("POINT(1 2)", fmt="wkt")
    hexstr = g.to_hex()
    assert hexstr == "0101000000000000000000F03F0000000000000040"


def test_geometry_to_wkb():
    g = Geometry("POINT(1 2)", fmt="wkt")
    wkb = g.to_wkb()
    assert (
        wkb
        == b"\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\xf0?\x00\x00\x00\x00\x00\x00\x00@"
    )


def test_geometry_to_geobin():
    g = Geometry("POINT(1 2)", fmt="wkt")
    geobin = g.to_geobin()
    assert (
        geobin
        == b"\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\xf0?\x00\x00\x00\x00\x00\x00\x00@"
    )


def test_geometry_intersects():
    g1 = Geometry("POLYGON((10 10,20 10,20 20,10 20,10 10))", fmt="wkt")
    g2 = Geometry("POINT(15 15)", fmt="wkt")
    g3 = Geometry("POINT(23 24)", fmt="wkt")
    assert g1.intersects(g2)
    assert not g1.intersects(g3)


def test_equals():
    g1 = Geometry("POINT(1 2)", fmt="wkt")
    g2 = Geometry('{"type":"Point","coordinates":[1,2]}', fmt="geojson")
    g3 = Geometry("POINT(2 3)", fmt="wkt")
    assert g1.equals(g2)
    assert not g1.equals(g3)
