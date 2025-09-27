from togo import Geometry, Rect, Point

from tests.geometries import TOGO, BENIN, GRAN_BUENOS_AIRES_AREA


def test_togo():
    togo = Geometry(TOGO)
    assert togo.memsize() == 6080
    assert not togo.is_empty()
    assert not togo.has_z()
    assert togo.dims() == 2
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
    assert benin.memsize() == 6688
    assert not benin.is_empty()
    assert not benin.has_z()
    assert benin.dims() == 2
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
    assert b_aires.memsize() == 456
    assert not b_aires.is_empty()
    assert b_aires.has_z()
    assert b_aires.dims() == 3
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


def test_togo_union_benin():
    g = Geometry.unary_union(
        [Geometry(TOGO, fmt="geojson"), Geometry(BENIN, fmt="geojson")]
    )
    # The union should not be empty and should be a valid geometry
    assert not g.is_empty()
    assert g.type_string() == "Polygon"
    wkt = g.to_wkt()
    new_g = Geometry(wkt, fmt="wkt")
    assert new_g.equals(g)
    assert new_g.rect() == g.rect()
    assert new_g.within(g) and g.within(new_g)
    assert g.contains(new_g) and new_g.contains(g)
    assert g.intersects(new_g) and new_g.intersects(g)
    assert not g.disjoint(new_g) and not new_g.disjoint(g)
    assert not g.touches(new_g) and not new_g.touches(g)
    assert g.num_points() == new_g.num_points()
    assert g.dims() == new_g.dims()
    assert g.has_z() == new_g.has_z()
    assert g.has_m() == new_g.has_m()
    assert g.is_feature() == new_g.is_feature()
    assert g.is_featurecollection() == new_g.is_featurecollection()
    assert g.to_geojson() == new_g.to_geojson()
    assert g.to_hex() == new_g.to_hex()
    assert g.to_wkb() == new_g.to_wkb()
    assert g.to_geobin() == new_g.to_geobin()
    assert g.memsize() == new_g.memsize()
    assert g.coveredby(new_g) and new_g.coveredby(g)
    assert g.covers(new_g) and new_g.covers(g)
