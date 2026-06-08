import pytest


def test_union_polygon_polygon_returns_geometry():
    from togo import Polygon

    left = Polygon([(0, 0), (2, 0), (2, 2), (0, 2), (0, 0)])
    right = Polygon([(1, 1), (3, 1), (3, 3), (1, 3), (1, 1)])

    result = left.union(right)

    assert result.geom_type in {"Polygon", "MultiPolygon"}
    assert result.area == pytest.approx(7.0)


def test_union_invalid_inputs_return_empty_geometry():
    from togo import Point, union

    p = Point(1, 2)

    assert p.union(None).is_empty
    assert p.union("invalid").is_empty
    assert union(p, None).is_empty
    assert union(p, "invalid").is_empty


def test_union_with_empty_geometry_returns_other_shape():
    from togo import Geometry, Polygon

    empty = Geometry('{"type":"GeometryCollection","geometries":[]}')
    poly = Polygon([(0, 0), (2, 0), (2, 2), (0, 2), (0, 0)])

    left = poly.union(empty)
    right = empty.union(poly)

    assert left.geom_type == "Polygon"
    assert right.geom_type == "Polygon"
    assert left.area == pytest.approx(poly.area)
    assert right.area == pytest.approx(poly.area)


def test_empty_geometry_accessors_return_managed_values():
    from togo import Geometry

    empty = Geometry('{"type":"GeometryCollection","geometries":[]}')

    assert empty.geom_type == "GeometryCollection"
    assert empty.bounds == (0.0, 0.0, 0.0, 0.0)
    assert empty.area == 0.0

    centroid = empty.centroid
    assert centroid.geom_type == "Point"
    assert centroid.is_empty
    assert centroid.to_wkt() == "POINT EMPTY"

    hull = empty.convex_hull
    assert hull.geom_type == "GeometryCollection"
    assert hull.is_empty
    assert hull.to_wkt() == "GEOMETRYCOLLECTION EMPTY"


def test_uninitialized_geometry_accessors_raise_managed_exceptions():
    from togo import Geometry, Point

    g = Geometry()

    with pytest.raises(ValueError, match="not initialized"):
        _ = g.geom_type
    with pytest.raises(ValueError, match="not initialized"):
        _ = g.bounds
    with pytest.raises(ValueError, match="not initialized"):
        _ = g.area
    with pytest.raises(ValueError, match="not initialized"):
        _ = g.centroid
    with pytest.raises(ValueError, match="not initialized"):
        _ = g.convex_hull

    with pytest.raises(ValueError, match="not initialized"):
        g.intersects(Point(0, 0).as_geometry())


@pytest.mark.parametrize(
    "method_name",
    ["contains", "covers", "intersects", "touches", "within"],
)
def test_uninitialized_other_geometry_predicates_raise_managed_exceptions(method_name):
    from togo import Geometry, Polygon

    poly = Polygon([(0, 0), (2, 0), (2, 2), (0, 2), (0, 0)]).as_geometry()
    uninitialized = Geometry()

    with pytest.raises(ValueError, match="other geometry is not initialized"):
        getattr(poly, method_name)(uninitialized)


def test_uninitialized_other_geometry_overlay_methods_raise_managed_exceptions():
    from togo import Geometry, Polygon

    poly = Polygon([(0, 0), (2, 0), (2, 2), (0, 2), (0, 0)]).as_geometry()
    uninitialized = Geometry()

    with pytest.raises(ValueError, match="other geometry is not initialized"):
        poly.intersection(uninitialized)
    with pytest.raises(ValueError, match="other geometry is not initialized"):
        poly.union(uninitialized)


def test_polygon_line_intersection_still_returns_segment():
    from togo import LineString, Polygon

    poly = Polygon([(0, 0), (2, 0), (2, 2), (0, 2), (0, 0)])
    line = LineString([(0, 1), (3, 1)])

    result = poly.intersection(line)

    assert result.geom_type == "LineString"
    assert result.length == pytest.approx(2.0)
