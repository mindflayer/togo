import pytest
from togo import Line, Rect, Geometry, Point


def test_line_basic():
    points = [(0, 0), (1, 1), (2, 2)]
    line = Line(points)
    assert line.num_points == 3
    assert line.points(as_tuples=True) == points
    assert isinstance(line.length, float)
    rect = line.rect()
    assert isinstance(rect, Rect)
    assert rect.min.as_tuple() == (0, 0)
    assert rect.max.as_tuple() == (2, 2)
    assert line.is_clockwise() in (True, False)


def test_line_points_default_as_tuples_false():
    """Test Line.points() with default as_tuples=False returns Point objects"""
    points = [(0, 0), (1, 1), (2, 2)]
    line = Line(points)

    # Call points() with default parameter (as_tuples=False)
    result = line.points()

    assert isinstance(result, list)
    assert len(result) == 3

    # Each element should be a Point object
    for i, pt in enumerate(result):
        assert isinstance(pt, Point), f"Element {i} should be Point, got {type(pt)}"
        assert pt.x == points[i][0]
        assert pt.y == points[i][1]

    # Verify coordinates match
    assert result[0].x == 0 and result[0].y == 0
    assert result[1].x == 1 and result[1].y == 1
    assert result[2].x == 2 and result[2].y == 2


def test_line_points_explicit_as_tuples_false():
    """Test Line.points(as_tuples=False) explicitly returns Point objects"""
    points = [(5, 10), (15, 20), (25, 30)]
    line = Line(points)

    result = line.points(as_tuples=False)

    assert isinstance(result, list)
    assert len(result) == 3

    for i, pt in enumerate(result):
        assert isinstance(pt, Point)
        assert pt.x == points[i][0]
        assert pt.y == points[i][1]


def test_line_two_points():
    points = [(0, 0), (1, 0)]
    line = Line(points)
    assert line.num_points == 2
    assert line.points(as_tuples=True) == points
    assert line.length == pytest.approx(1.0)


def test_line_two_points_as_tuples_false():
    """Test Line with two points returns two Point objects"""
    points = [(0, 0), (1, 0)]
    line = Line(points)

    result = line.points(as_tuples=False)

    assert len(result) == 2
    assert all(isinstance(pt, Point) for pt in result)
    assert result[0].x == 0 and result[0].y == 0
    assert result[1].x == 1 and result[1].y == 0


def test_line_collinear():
    points = [(0, 0), (1, 1), (2, 2)]
    line = Line(points)
    # Length should be sqrt(2) + sqrt(2)
    expected_length = 2**0.5 + 2**0.5
    assert line.length == pytest.approx(expected_length)
    assert line.num_points == 3


def test_line_closed():
    points = [(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)]
    line = Line(points)
    assert line.num_points == 5
    assert line.points(as_tuples=True) == points
    # Perimeter of a square
    assert line.length == pytest.approx(4.0)


def test_line_closed_as_tuples_false():
    """Test closed line with as_tuples=False"""
    points = [(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)]
    line = Line(points)

    result = line.points(as_tuples=False)

    assert len(result) == 5
    assert all(isinstance(pt, Point) for pt in result)

    # Verify it closes
    assert result[0].x == result[4].x and result[0].y == result[4].y


def test_line_as_geometry():
    points = [(0, 0), (1, 1), (2, 2)]
    line = Line(points)
    g = line.as_geometry()
    assert isinstance(g, Geometry)
    assert g.type_string() == "LineString"
    rect = g.bounds
    assert rect == (0.0, 0.0, 2.0, 2.0)


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
