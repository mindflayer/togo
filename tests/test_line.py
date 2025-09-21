import pytest
from togo import Line, Rect


def test_line_basic():
    points = [(0, 0), (1, 1), (2, 2)]
    line = Line(points)
    assert line.num_points() == 3
    assert line.points() == points
    assert isinstance(line.length(), float)
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
    assert line.length() == pytest.approx(1.0)


def test_line_collinear():
    points = [(0, 0), (1, 1), (2, 2)]
    line = Line(points)
    # Length should be sqrt(2) + sqrt(2)
    expected_length = 2**0.5 + 2**0.5
    assert line.length() == pytest.approx(expected_length)


def test_line_closed():
    points = [(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)]
    line = Line(points)
    assert line.num_points() == 5
    assert line.points() == points
    # Perimeter of a square
    assert line.length() == pytest.approx(4.0)
