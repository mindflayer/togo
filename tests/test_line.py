import pytest
from togo import Line, Rect, Geometry


def test_line_basic():
    points = [(0, 0), (1, 1), (2, 2)]
    line = Line(points)
    assert line.num_points() == 3
    assert line.points() == points
    assert isinstance(line.length, float)
    rect = line.rect()
    assert isinstance(rect, Rect)
    assert rect.min.as_tuple() == (0, 0)
    assert rect.max.as_tuple() == (2, 2)
    assert line.is_clockwise() in (True, False)


def test_line_two_points():
    points = [(0, 0), (1, 0)]
    line = Line(points)
    assert line.num_points() == 2
    assert line.points() == points
    assert line.length == pytest.approx(1.0)


def test_line_collinear():
    points = [(0, 0), (1, 1), (2, 2)]
    line = Line(points)
    # Length should be sqrt(2) + sqrt(2)
    expected_length = 2**0.5 + 2**0.5
    assert line.length == pytest.approx(expected_length)


def test_line_closed():
    points = [(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)]
    line = Line(points)
    assert line.num_points() == 5
    assert line.points() == points
    # Perimeter of a square
    assert line.length == pytest.approx(4.0)


def test_line_as_geometry():
    points = [(0, 0), (1, 1), (2, 2)]
    line = Line(points)
    g = line.as_geometry()
    assert isinstance(g, Geometry)
    assert g.type_string() == "LineString"
    rect = g.rect()
    assert rect == ((0.0, 0.0), (2.0, 2.0))


def test_line_getitem():
    points = [(10, 20), (30, 40), (50, 60)]
    line = Line(points)
    pt0 = line[0]
    pt1 = line[1]
    pt2 = line[2]
    assert pt0.x == 10 and pt0.y == 20
    assert pt1.x == 30 and pt1.y == 40
    assert pt2.x == 50 and pt2.y == 60
    with pytest.raises(IndexError):
        _ = line[3]
    with pytest.raises(IndexError):
        _ = line[-1]
