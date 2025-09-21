from togo import Point, Geometry


def test_point_basic():
    p = Point(3.5, -7.2)
    assert p.x == 3.5
    assert p.y == -7.2
    assert p.as_tuple() == (3.5, -7.2)


def test_point_zero():
    p = Point(0, 0)
    assert p.x == 0
    assert p.y == 0
    assert p.as_tuple() == (0, 0)


def test_point_negative():
    p = Point(-1.1, 2.2)
    assert p.x == -1.1
    assert p.y == 2.2
    assert p.as_tuple() == (-1.1, 2.2)


def test_point_as_geometry():
    p = Point(3.5, -7.2)
    g = p.as_geometry()
    assert isinstance(g, Geometry)
    assert g.type_string() == "Point"
    assert g.rect() == ((3.5, -7.2), (3.5, -7.2))
