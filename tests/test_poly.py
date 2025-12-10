import pytest
from togo import Poly, Ring, Rect, Geometry


def test_poly_square_no_holes():
    exterior = Ring([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)])
    poly = Poly(exterior)
    assert isinstance(poly.exterior, Ring)
    assert poly.num_holes() == 0
    rect = poly.rect()
    assert isinstance(rect, Rect)
    assert rect.min.as_tuple() == (0, 0)
    assert rect.max.as_tuple() == (1, 1)
    assert poly.is_clockwise() in (True, False)
    # Area and perimeter via exterior ring
    assert poly.exterior.area == pytest.approx(1.0)
    assert poly.exterior.length == pytest.approx(4.0)


def test_poly_with_hole():
    exterior = Ring([(0, 0), (4, 0), (4, 4), (0, 4), (0, 0)])
    hole = Ring([(1, 1), (3, 1), (3, 3), (1, 3), (1, 1)])
    poly = Poly(exterior, holes=[hole])
    assert poly.num_holes() == 1
    h = poly.hole(0)
    assert isinstance(h, Ring)
    assert h.area == pytest.approx(4.0)
    # Exterior area should be larger than hole
    assert poly.exterior.area == pytest.approx(16.0)


def test_poly_multiple_holes():
    exterior = Ring([(0, 0), (5, 0), (5, 5), (0, 5), (0, 0)])
    hole1 = Ring([(1, 1), (2, 1), (2, 2), (1, 2), (1, 1)])
    hole2 = Ring([(3, 3), (4, 3), (4, 4), (3, 4), (3, 3)])
    poly = Poly(exterior, holes=[hole1, hole2])
    assert poly.num_holes() == 2
    assert poly.hole(0).area == pytest.approx(1.0)
    assert poly.hole(1).area == pytest.approx(1.0)
    assert poly.exterior.area == pytest.approx(25.0)


def test_poly_degenerate():
    exterior = Ring([(0, 0), (0, 0), (0, 0)])
    poly = Poly(exterior)
    assert poly.num_holes() == 0
    assert poly.exterior.area == 0
    assert poly.exterior.length == 0
    rect = poly.rect()
    assert rect.min.as_tuple() == (0, 0)
    assert rect.max.as_tuple() == (0, 0)


def test_poly_as_geometry():
    exterior = Ring([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)])
    poly = Poly(exterior)
    g = poly.as_geometry()
    assert isinstance(g, Geometry)
    assert g.type_string() == "Polygon"
    rect = g.bounds
    assert rect == (0.0, 0.0, 1.0, 1.0)
