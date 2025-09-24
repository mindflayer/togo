from togo import Point, Segment


def test_segment_creation_and_rect():
    a = Point(0, 0)
    b = Point(1, 1)
    seg = Segment(a, b)
    rect = seg.rect()
    assert rect == ((0, 0), (1, 1))


def test_segment_intersects():
    seg1 = Segment(Point(0, 0), Point(1, 1))
    seg2 = Segment(Point(0, 1), Point(1, 0))
    seg3 = Segment(Point(2, 2), Point(3, 3))
    assert seg1.intersects(seg2)
    assert not seg1.intersects(seg3)
