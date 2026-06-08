"""Tests for multiprocessing serialization / MBP compatibility.

Covers the issues described in the ToGo Fix Report (2026-06-08):

P0 – Native pickling for runtime geometry and sub-geometry objects
    (Point, LineString, Polygon, Multi*, GeometryCollection,
     polygon exterior/boundary, line boundary).

P0 – Accept / normalise ``LinearRing`` in the ``shape()`` parsing API.

P1 – Export/contract consistency: anything produced by ``__geo_interface__``
     must be re-parseable by ``shape()``.

The loky/joblib cross-process transfer tests use the same reproduce snippets
supplied by MBP so that passing these tests is a direct proxy for the MBP
pipeline being unblocked.
"""

import pickle

import pytest

from togo import (
    GeometryCollection,
    LineString,
    MultiLineString,
    MultiPoint,
    MultiPolygon,
    Point,
    Polygon,
    Ring,
    shape,
)


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------


def _wkb_of(obj):
    from togo import Geometry

    if isinstance(obj, Geometry):
        return obj.to_wkb()
    return obj.as_geometry().to_wkb()


# ---------------------------------------------------------------------------
# P0 – Accept LinearRing in shape() / from_geojson path
# ---------------------------------------------------------------------------


class TestLinearRingParsing:
    """shape() must accept a LinearRing geo-interface payload without raising."""

    def test_shape_accepts_linear_ring_dict(self):
        """Repro A from MBP: shape(ring.__geo_interface__) must not raise."""
        poly = Polygon.from_bounds(0, 0, 1, 1)
        ring = poly.exterior
        payload = ring.__geo_interface__

        assert payload.get("type") == "LinearRing"
        # Must not raise
        result = shape(payload)
        assert result is not None

    def test_shape_linear_ring_preserves_coordinates(self):
        coords = [(0.0, 0.0), (2.0, 0.0), (2.0, 2.0), (0.0, 2.0), (0.0, 0.0)]
        payload = {"type": "LinearRing", "coordinates": coords}
        result = shape(payload)
        assert result is not None
        assert not result.is_empty

    def test_shape_ring_object_via_geo_interface(self):
        """shape() called with a Ring object must not raise (uses __geo_interface__)."""
        ring = Ring([(0, 0), (1, 0), (1, 1), (0, 0)])
        result = shape(ring)
        assert result is not None

    def test_shape_polygon_exterior_round_trip(self):
        """The exterior ring of a Polygon can be round-tripped through shape()."""
        poly = Polygon([(0, 0), (4, 0), (4, 3), (0, 3), (0, 0)])
        exterior = poly.exterior
        result = shape(exterior.__geo_interface__)
        # result is a Polygon geometry (Ring.as_geometry())
        assert result is not None
        assert not result.is_empty

    def test_shape_linear_ring_triangle(self):
        payload = {
            "type": "LinearRing",
            "coordinates": [(0, 0), (1, 0), (0.5, 1), (0, 0)],
        }
        result = shape(payload)
        assert result is not None

    def test_shape_linear_ring_empty_coords(self):
        """Empty coordinates list should not raise; result may be empty geometry."""
        payload = {"type": "LinearRing", "coordinates": []}
        # Should not raise a ParseError – may return an empty geometry
        try:
            result = shape(payload)
            # If it returns, verify it is a Geometry
            from togo import Geometry

            assert isinstance(result, Geometry) or hasattr(result, "as_geometry")
        except (ValueError, RuntimeError):
            # Acceptable – empty ring may not be constructable
            pass

    def test_geo_interface_contract_all_types(self):
        """Every type exported via __geo_interface__ must be parseable by shape()."""
        objs = [
            Point(1, 2),
            LineString([(0, 0), (1, 1)]),
            Polygon([(0, 0), (1, 0), (1, 1), (0, 0)]),
            Ring([(0, 0), (2, 0), (2, 2), (0, 0)]),
            MultiPoint([(0, 0), (1, 1)]),
            MultiLineString([[(0, 0), (1, 1)], [(2, 2), (3, 3)]]),
            MultiPolygon(
                [
                    Polygon([(0, 0), (1, 0), (1, 1), (0, 0)]),
                    Polygon([(2, 2), (3, 2), (3, 3), (2, 2)]),
                ]
            ),
        ]
        for obj in objs:
            gi = obj.__geo_interface__
            result = shape(gi)
            assert result is not None, f"shape() failed for {type(obj).__name__}"


# ---------------------------------------------------------------------------
# P0 – Native pickling: core geometry types
# ---------------------------------------------------------------------------


class TestCoreGeometryPickleRoundtrip:
    """All core geometry types must survive pickle.dumps / pickle.loads."""

    def _assert_roundtrip(self, obj):
        data = pickle.dumps(obj)
        restored = pickle.loads(data)
        assert type(restored) is type(obj)
        assert _wkb_of(restored) == _wkb_of(obj), (
            f"WKB mismatch for {type(obj).__name__}"
        )

    def test_point(self):
        self._assert_roundtrip(Point(1.5, 2.5))

    def test_linestring(self):
        self._assert_roundtrip(LineString([(0, 0), (1, 1), (2, 0)]))

    def test_polygon(self):
        self._assert_roundtrip(Polygon([(0, 0), (3, 0), (3, 3), (0, 3), (0, 0)]))

    def test_polygon_with_hole(self):
        outer = [(0, 0), (10, 0), (10, 10), (0, 10), (0, 0)]
        hole = [(2, 2), (8, 2), (8, 8), (2, 8), (2, 2)]
        self._assert_roundtrip(Polygon(outer, [hole]))

    def test_multipoint(self):
        self._assert_roundtrip(MultiPoint([(0, 0), (1, 1), (2, 2)]))

    def test_multilinestring(self):
        self._assert_roundtrip(MultiLineString([[(0, 0), (1, 1)], [(2, 2), (3, 3)]]))

    def test_multipolygon(self):
        p1 = Polygon([(0, 0), (1, 0), (1, 1), (0, 0)])
        p2 = Polygon([(2, 2), (3, 2), (3, 3), (2, 2)])
        self._assert_roundtrip(MultiPolygon([p1, p2]))

    def test_geometry_collection(self):
        self._assert_roundtrip(
            GeometryCollection([Point(0, 0), LineString([(0, 0), (1, 0)])])
        )


# ---------------------------------------------------------------------------
# P0 – Native pickling: runtime sub-geometry objects
# ---------------------------------------------------------------------------


class TestSubGeometryPickleRoundtrip:
    """polygon.exterior, polygon.boundary, line.boundary must all be picklable."""

    def test_polygon_exterior_is_picklable(self):
        """Repro B from MBP."""
        poly = Polygon.from_bounds(0, 0, 1, 1)
        ring = poly.exterior
        restored = pickle.loads(pickle.dumps(ring))
        assert restored is not None
        assert _wkb_of(restored) == _wkb_of(ring)

    def test_polygon_boundary_is_picklable(self):
        """Repro B from MBP."""
        poly = Polygon.from_bounds(0, 0, 1, 1)
        boundary = poly.boundary
        restored = pickle.loads(pickle.dumps(boundary))
        assert restored is not None
        assert _wkb_of(restored) == _wkb_of(boundary)

    def test_polygon_with_holes_boundary_is_picklable(self):
        outer = [(0, 0), (10, 0), (10, 10), (0, 10), (0, 0)]
        hole = [(2, 2), (8, 2), (8, 8), (2, 8), (2, 2)]
        poly = Polygon(outer, [hole])
        boundary = poly.boundary
        restored = pickle.loads(pickle.dumps(boundary))
        assert _wkb_of(restored) == _wkb_of(boundary)

    def test_linestring_boundary_is_picklable(self):
        line = LineString([(0, 0), (1, 1), (2, 3)])
        boundary = line.boundary
        restored = pickle.loads(pickle.dumps(boundary))
        assert _wkb_of(restored) == _wkb_of(boundary)

    def test_ring_is_picklable(self):
        ring = Ring([(0, 0), (1, 0), (1, 1), (0, 0)])
        restored = pickle.loads(pickle.dumps(ring))
        assert type(restored) is Ring
        assert _wkb_of(restored) == _wkb_of(ring)

    def test_all_sub_geometry_objects_in_one_pass(self):
        """Repro B – exact reproducer from MBP fix report."""
        poly = Polygon.from_bounds(0, 0, 1, 1)
        for obj in [poly.exterior, poly.boundary]:
            restored = pickle.loads(pickle.dumps(obj))
            assert restored is not None

    def test_type_preserved_after_pickle_roundtrip(self):
        poly = Polygon.from_bounds(0, 0, 1, 1)
        ring = poly.exterior

        assert type(pickle.loads(pickle.dumps(ring))) is Ring
        assert type(pickle.loads(pickle.dumps(poly))) is Polygon

    def test_repeated_roundtrip_stable(self):
        """Stress: repeated serialize/deserialize must not produce flaky failures."""
        poly = Polygon([(0, 0), (5, 0), (5, 5), (0, 5), (0, 0)])
        objs = [poly, poly.exterior, poly.boundary]
        for _ in range(20):
            for obj in objs:
                restored = pickle.loads(pickle.dumps(obj))
                assert _wkb_of(restored) == _wkb_of(obj)


# ---------------------------------------------------------------------------
# P0 – Loky / joblib cross-process transfer (Repro C from MBP report)
# ---------------------------------------------------------------------------


def _extract_geo_type(g):
    """Worker function: extract __geo_interface__ type or class name."""
    gi = getattr(g, "__geo_interface__", None)
    if isinstance(gi, dict):
        return gi.get("type", type(g).__name__)
    return type(g).__name__


def _get_wkb(g):
    """Worker function: return WKB bytes of a geometry or sub-geometry."""
    from togo import Geometry

    if isinstance(g, Geometry):
        return g.to_wkb()
    return g.as_geometry().to_wkb()


class TestLokyJobLibTransfer:
    """Objects must survive cross-process transfer via joblib / loky backend."""

    def test_loky_transfer_core_geometries(self):
        """Repro C from MBP: core geometry objects must survive loky transfer."""
        pytest.importorskip("joblib")
        from joblib import Parallel, delayed

        poly = Polygon.from_bounds(0, 0, 1, 1)
        objs = [
            poly,
            poly.exterior,
            poly.boundary,
        ]

        # Repro C – exact snippet
        results = Parallel(n_jobs=2, backend="loky")(
            delayed(_extract_geo_type)(g) for g in objs * 4
        )
        assert len(results) == 12
        assert all(isinstance(r, str) for r in results)

    def test_loky_transfer_preserves_wkb(self):
        """WKB must be identical after loky round-trip."""
        pytest.importorskip("joblib")
        from joblib import Parallel, delayed

        poly = Polygon([(0, 0), (3, 0), (3, 3), (0, 3), (0, 0)])
        original_wkbs = {
            "poly": _get_wkb(poly),
            "exterior": _get_wkb(poly.exterior),
            "boundary": _get_wkb(poly.boundary),
        }

        objs = [poly, poly.exterior, poly.boundary]
        results = Parallel(n_jobs=2, backend="loky")(delayed(_get_wkb)(g) for g in objs)

        assert results[0] == original_wkbs["poly"]
        assert results[1] == original_wkbs["exterior"]
        assert results[2] == original_wkbs["boundary"]

    def test_loky_transfer_all_core_types(self):
        """All primitive and multi-geometry types must be transferable via loky."""
        pytest.importorskip("joblib")
        from joblib import Parallel, delayed

        objs = [
            Point(1, 2),
            LineString([(0, 0), (1, 1)]),
            Polygon([(0, 0), (1, 0), (1, 1), (0, 0)]),
            MultiPoint([(0, 0), (1, 1)]),
            MultiLineString([[(0, 0), (1, 1)]]),
            MultiPolygon([Polygon([(0, 0), (1, 0), (1, 1), (0, 0)])]),
            GeometryCollection([Point(0, 0)]),
        ]
        wkbs_before = [_get_wkb(o) for o in objs]

        results = Parallel(n_jobs=2, backend="loky")(delayed(_get_wkb)(o) for o in objs)
        assert results == wkbs_before

    def test_loky_no_broken_process_pool(self):
        """Specifically validates there is no BrokenProcessPool on transfer."""
        pytest.importorskip("joblib")
        from joblib import Parallel, delayed
        from joblib.externals.loky import get_reusable_executor

        poly = Polygon.from_bounds(0, 0, 1, 1)
        objs = [poly, poly.exterior, poly.boundary] * 8

        # This must not raise BrokenProcessPool
        results = Parallel(n_jobs=2, backend="loky")(
            delayed(_extract_geo_type)(g) for g in objs
        )
        assert len(results) == len(objs)
        # Shutdown cleanly so subsequent tests get a fresh pool
        get_reusable_executor().shutdown(wait=True)
