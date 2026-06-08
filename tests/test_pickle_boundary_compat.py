import pickle
from concurrent.futures import ProcessPoolExecutor
import multiprocessing as mp

from togo import Geometry, LineString, Point, Polygon


def _wkb_of(obj):
    if isinstance(obj, Geometry):
        return obj.to_wkb()
    return obj.as_geometry().to_wkb()


def _roundtrip_area(geom):
    restored = pickle.loads(pickle.dumps(geom))
    return restored.area


def test_linestring_boundary_returns_endpoint_multipoint():
    line = LineString([(0, 0), (1, 1), (2, 3)])

    boundary = line.boundary

    assert isinstance(boundary, Geometry)
    assert boundary.geom_type == "MultiPoint"
    coords = [tuple(pt) for pt in boundary.__geo_interface__["coordinates"]]
    assert coords == [(0.0, 0.0), (2.0, 3.0)]


def test_closed_linestring_boundary_is_empty():
    line = LineString([(0, 0), (1, 1), (0, 0)])

    boundary = line.boundary

    assert boundary.geom_type == "MultiPoint"
    assert boundary.is_empty


def test_ring_exposes_geo_interface_and_pickles():
    poly = Polygon([(0, 0), (3, 0), (3, 2), (0, 0)])
    ring = poly.exterior

    geo = ring.__geo_interface__
    restored = pickle.loads(pickle.dumps(ring))

    assert geo["type"] == "LinearRing"
    assert len(geo["coordinates"]) == ring.num_points
    assert _wkb_of(restored) == _wkb_of(ring)


def test_pickle_roundtrip_core_geometry_types():
    poly = Polygon([(0, 0), (1, 0), (1, 1), (0, 0)])
    objs = [
        Point(0.1, 0.2),
        LineString([(0, 0), (1, 1)]),
        poly,
        poly.exterior,
        poly.boundary,
        poly.as_geometry(),
    ]

    for obj in objs:
        restored = pickle.loads(pickle.dumps(obj))
        assert type(restored) is type(obj)
        assert _wkb_of(restored) == _wkb_of(obj)


def test_geometry_roundtrips_through_spawned_process_pool():
    poly = Polygon([(0, 0), (1, 0), (1, 1), (0, 0)])
    ctx = mp.get_context("spawn")

    with ProcessPoolExecutor(max_workers=2, mp_context=ctx) as pool:
        results = list(pool.map(_roundtrip_area, [poly, poly, poly, poly]))

    assert results == [0.5, 0.5, 0.5, 0.5]
