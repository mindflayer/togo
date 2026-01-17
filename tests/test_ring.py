import pytest
from togo import Ring, Rect, Geometry, Poly, Point


def test_ring_triangle():
    points = [(0, 0), (1, 0), (0, 1), (0, 0)]
    ring = Ring(points)
    assert ring.num_points == 4
    assert ring.points(as_tuples=True) == points
    assert ring.area == 0.5
    assert ring.length > 0
    rect = ring.rect()
    assert isinstance(rect, Rect)
    assert rect.min.as_tuple() == (0, 0)
    assert rect.max.as_tuple() == (1, 1)
    assert ring.is_convex in (True, False)
    assert ring.is_clockwise in (True, False)


def test_ring_points_default_as_tuples_false():
    """Test Ring.points() with default as_tuples=False returns Point objects"""
    points = [(0, 0), (1, 0), (0, 1), (0, 0)]
    ring = Ring(points)

    # Call points() with default parameter (as_tuples=False)
    result = ring.points()

    assert isinstance(result, list)
    assert len(result) == 4

    # Each element should be a Point object
    for i, pt in enumerate(result):
        assert isinstance(pt, Point), f"Element {i} should be Point, got {type(pt)}"
        assert pt.x == points[i][0]
        assert pt.y == points[i][1]

    # Verify coordinates match
    assert result[0].x == 0 and result[0].y == 0
    assert result[1].x == 1 and result[1].y == 0
    assert result[2].x == 0 and result[2].y == 1
    assert result[3].x == 0 and result[3].y == 0


def test_ring_points_explicit_as_tuples_false():
    """Test Ring.points(as_tuples=False) explicitly returns Point objects"""
    points = [(0, 0), (1, 0), (0, 1), (0, 0)]
    ring = Ring(points)

    result = ring.points(as_tuples=False)

    assert isinstance(result, list)
    assert len(result) == 4

    for i, pt in enumerate(result):
        assert isinstance(pt, Point)
        assert pt.x == points[i][0]
        assert pt.y == points[i][1]


def test_ring_square():
    points = [(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)]
    ring = Ring(points)
    assert ring.num_points == 5
    assert ring.points(as_tuples=True) == points
    assert ring.area == pytest.approx(1.0)
    assert ring.length == pytest.approx(4.0)
    rect = ring.rect()
    assert rect.min.as_tuple() == (0, 0)
    assert rect.max.as_tuple() == (1, 1)
    assert ring.is_convex is True


def test_ring_square_as_tuples_false():
    """Test square ring returns Point objects with as_tuples=False"""
    points = [(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)]
    ring = Ring(points)

    result = ring.points(as_tuples=False)

    assert len(result) == 5
    assert all(isinstance(pt, Point) for pt in result)

    # Verify it closes
    assert result[0].x == result[4].x and result[0].y == result[4].y

    # Verify specific coordinates
    assert result[1].x == 1 and result[1].y == 0
    assert result[2].x == 1 and result[2].y == 1


def test_ring_degenerate():
    points = [(0, 0), (0, 0), (0, 0)]
    ring = Ring(points)
    assert ring.num_points == 3
    assert ring.area == 0
    assert ring.length == 0
    rect = ring.rect()
    assert rect.min.as_tuple() == (0, 0)
    assert rect.max.as_tuple() == (0, 0)


def test_ring_degenerate_as_tuples_false():
    """Test degenerate ring returns Point objects"""
    points = [(0, 0), (0, 0), (0, 0)]
    ring = Ring(points)

    result = ring.points(as_tuples=False)

    assert len(result) == 3
    assert all(isinstance(pt, Point) for pt in result)
    assert all(pt.x == 0 and pt.y == 0 for pt in result)


def test_ring_nonconvex():
    points = [(0, 0), (2, 0), (1, 1), (2, 2), (0, 2), (0, 0)]
    ring = Ring(points)
    assert ring.num_points == 6
    assert ring.points(as_tuples=True) == points
    assert ring.is_convex is False
    assert ring.area > 0
    assert ring.length > 0


def test_ring_nonconvex_as_tuples_false():
    """Test nonconvex ring returns Point objects"""
    points = [(0, 0), (2, 0), (1, 1), (2, 2), (0, 2), (0, 0)]
    ring = Ring(points)

    result = ring.points(as_tuples=False)

    assert len(result) == 6
    assert all(isinstance(pt, Point) for pt in result)

    # Verify specific points
    assert result[0].x == 0 and result[0].y == 0
    assert result[1].x == 2 and result[1].y == 0
    assert result[2].x == 1 and result[2].y == 1


def test_ring_as_geometry():
    points = [(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)]
    ring = Ring(points)
    p = ring.as_poly()
    assert isinstance(p, Poly)
    assert p.num_holes() == 0
    assert p.exterior.points(as_tuples=True) == points
    assert p.num_holes() == 0
    g = p.as_geometry()
    assert isinstance(g, Geometry)
    assert g.type_string() == "Polygon"
    assert g.bounds == (0.0, 0.0, 1.0, 1.0)
