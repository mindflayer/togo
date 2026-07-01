# Changelog

## Unreleased

### New Features

- **`Ring.intersects(other)`** — New Shapely-compatible predicate method on the low-level `Ring`
  class. Checks whether the ring intersects another geometry without requiring manual
  `.as_geometry()` conversion. Accepts any ToGo wrapper type directly.
- **`Ring.boundary`** — New Shapely-compatible property on the low-level `Ring` class. Returns the
  ring's boundary as a `Line` (no holes) or `MultiLineString` (with holes), consistent with
  `Polygon.boundary` semantics.

### Performance Improvements

- Build: added default `-O2` compile flag for non-ASAN builds in `setup.py`.
- `_coerce_xy`: added tuple/list fast path to avoid slower attribute/index fallbacks.
- `Ring.__init__`, `Line.__init__`, `LinearRing.__init__`: skip redundant `list()` copy when input
  is already a list.
- `Ring.__init__`: reuse already-coerced endpoint values instead of re-coercing the closing point
  in the fill loop.
- `Geometry.__geo_interface__`: parse GeoJSON once and cache the result; return `deepcopy` to
  preserve mutation-isolation semantics.
- `Geometry.from_multipoint`: tuple/list coordinate extraction is treated as a fast path.
- `Geometry.from_multilinestring`, `from_multipolygon`, `from_geometrycollection`, `unary_union`:
  list fast-path guards to avoid redundant `list()` materialization.
- `MultiPolygon.__init__`: short-circuits when all inputs are already `Poly` instances.
- Added `_ring_points_as_tuples_from_ptr` C-level helper; `Poly.__reduce__` and
  `Poly.__geo_interface__` now extract coordinates directly from C pointers, reducing wrapper
  creation and clone overhead.
- `shape()` helper: removed per-call `import json` in favour of the module-level `_json` alias.

### Tests

- Added `test_point_geo_interface_repeated_access_is_stable` to verify that repeated
  `__geo_interface__` calls are stable and that caller mutation of one returned dict does not affect
  subsequent calls.
