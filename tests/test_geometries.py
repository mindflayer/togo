from togo import Geometry, Rect, Point

from tests.geometries import TOGO


def test_togo():
    togo = Geometry(TOGO)
    assert not togo.is_empty()
    assert togo.type_string() == "Polygon"
    bbox = togo.rect()
    assert bbox == ((-0.149762, 6.100546), (1.799327, 11.13854))
    min_, max_ = Point(*bbox[0]), Point(*bbox[1])
    rect = Rect(min_, max_)
    assert rect.min.as_tuple() == bbox[0]
    assert rect.max.as_tuple() == bbox[1]
    togo_center = rect.center()
    assert togo_center.as_tuple() == (0.8247825, 8.619543)
    togo_center_geo = Geometry(f"POINT({togo_center.x} {togo_center.y})", fmt="wkt")
    assert togo.intersects(togo_center_geo)
