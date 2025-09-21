from togo import Geometry, Rect, Point

from tests.geometries import TOGO, BENIN, GRAN_BUENOS_AIRES_AREA


def test_togo():
    togo = Geometry(TOGO)
    assert not togo.is_empty()
    assert not togo.has_z()
    assert togo.type_string() == "Polygon"
    bbox = togo.rect()
    assert bbox == ((-0.149762, 6.100546), (1.799327, 11.13854))
    min_, max_ = Point(*bbox[0]), Point(*bbox[1])
    rect = Rect(min_, max_)
    assert rect.min.as_tuple() == bbox[0]
    assert rect.max.as_tuple() == bbox[1]
    togo_center = rect.center()
    assert togo_center.as_tuple() == (0.8247825, 8.619543)
    assert togo.intersects(togo_center.as_geometry())


def test_benin():
    benin = Geometry(BENIN, fmt="geojson")
    assert not benin.is_empty()
    assert not benin.has_z()
    assert benin.type_string() == "Polygon"
    bbox = benin.rect()
    assert bbox == ((0.776667, 6.218721), (3.855, 12.396658))
    min_, max_ = Point(*bbox[0]), Point(*bbox[1])
    rect = Rect(min_, max_)
    assert rect.min.as_tuple() == bbox[0]
    assert rect.max.as_tuple() == bbox[1]
    benin_center = rect.center()
    assert benin_center.as_tuple() == (2.3158335, 9.3076895)
    assert benin.intersects(benin_center.as_geometry())


def test_buenos_aires():
    b_aires = Geometry(GRAN_BUENOS_AIRES_AREA, fmt="wkt")
    assert not b_aires.is_empty()
    assert b_aires.has_z()
    assert b_aires.type_string() == "Polygon"
    bbox = b_aires.rect()
    assert bbox == (
        (-59.01433270595447, -35.07421568123671),
        (-57.75103350378777, -34.33189712265184),
    )
    min_, max_ = Point(*bbox[0]), Point(*bbox[1])
    rect = Rect(min_, max_)
    assert rect.min.as_tuple() == bbox[0]
    assert rect.max.as_tuple() == bbox[1]
    b_aires_center = rect.center()
    assert b_aires_center.as_tuple() == (-58.38268310487112, -34.70305640194427)
    assert b_aires.intersects(b_aires_center.as_geometry())
