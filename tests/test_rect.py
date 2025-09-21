from togo import Rect, Point, Geometry


def test_rect_basic():
    min_pt = Point(0, 0)
    max_pt = Point(2, 3)
    rect = Rect(min_pt, max_pt)
    assert rect.min.x == 0
    assert rect.min.y == 0
    assert rect.max.x == 2
    assert rect.max.y == 3
    assert rect.center().as_tuple() == (1.0, 1.5)


def test_rect_expand_with_rect():
    r1 = Rect(Point(0, 0), Point(1, 1))
    r2 = Rect(Point(-1, -1), Point(2, 2))
    expanded = r1.expand(r2)
    assert expanded.min.x == -1
    assert expanded.min.y == -1
    assert expanded.max.x == 2
    assert expanded.max.y == 2


def test_rect_expand_with_point():
    r = Rect(Point(0, 0), Point(1, 1))
    p = Point(2, -1)
    expanded = r.expand(p)
    assert expanded.min.x == 0
    assert expanded.min.y == -1
    assert expanded.max.x == 2
    assert expanded.max.y == 1


def test_rect_intersects_rect():
    r1 = Rect(Point(0, 0), Point(2, 2))
    r2 = Rect(Point(1, 1), Point(3, 3))
    r3 = Rect(Point(3, 3), Point(4, 4))
    assert r1.intersects(r2)
    assert not r1.intersects(r3)


def test_rect_intersects_point():
    r = Rect(Point(0, 0), Point(2, 2))
    p_inside = Point(1, 1)
    p_outside = Point(3, 3)
    assert r.intersects(p_inside)
    assert not r.intersects(p_outside)


def test_rect_zero_area():
    pt = Point(5, 5)
    rect = Rect(pt, pt)
    assert rect.min.as_tuple() == (5, 5)
    assert rect.max.as_tuple() == (5, 5)
    assert rect.center().as_tuple() == (5, 5)


def test_rect_as_geometry():
    rect = Rect(Point(0, 0), Point(2, 3))
    g = rect.as_geometry()
    assert isinstance(g, Geometry)
    assert g.type_string() == "Polygon"
    assert g.rect() == ((0.0, 0.0), (2.0, 3.0))
