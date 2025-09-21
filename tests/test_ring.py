import pytest
from togo import Ring, Rect


def test_ring_triangle():
    points = [(0, 0), (1, 0), (0, 1), (0, 0)]
    ring = Ring(points)
    assert ring.num_points() == 4
    assert ring.points() == points
    assert ring.area() > 0
    assert ring.perimeter() > 0
    rect = ring.rect()
    assert isinstance(rect, Rect)
    assert rect.min.as_tuple() == (0, 0)
    assert rect.max.as_tuple() == (1, 1)
    assert ring.is_convex() in (True, False)
    assert ring.is_clockwise() in (True, False)


def test_ring_square():
    points = [(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)]
    ring = Ring(points)
    assert ring.num_points() == 5
    assert ring.points() == points
    assert ring.area() == pytest.approx(1.0)
    assert ring.perimeter() == pytest.approx(4.0)
    rect = ring.rect()
    assert rect.min.as_tuple() == (0, 0)
    assert rect.max.as_tuple() == (1, 1)
    assert ring.is_convex() is True


def test_ring_degenerate():
    points = [(0, 0), (0, 0), (0, 0)]
    ring = Ring(points)
    assert ring.num_points() == 3
    assert ring.area() == 0
    assert ring.perimeter() == 0
    rect = ring.rect()
    assert rect.min.as_tuple() == (0, 0)
    assert rect.max.as_tuple() == (0, 0)


def test_ring_nonconvex():
    points = [(0, 0), (2, 0), (1, 1), (2, 2), (0, 2), (0, 0)]
    ring = Ring(points)
    assert ring.num_points() == 6
    assert ring.points() == points
    assert ring.is_convex() is False
    assert ring.area() > 0
    assert ring.perimeter() > 0
