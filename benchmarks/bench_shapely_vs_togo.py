"""
Benchmark comparing togo vs Shapely geometry libraries.

This benchmark uses the new Shapely-compatible API for togo, allowing a true
apples-to-apples comparison between the two libraries.

ToGo now offers:
- Shapely-compatible class names (Point, LineString, Polygon)
- Shapely-compatible properties (geom_type, bounds, area, length, coords, etc.)
- Shapely-compatible module functions (from_wkt, from_geojson, to_wkt, etc.)

Run with: python benchmarks/bench_shapely_vs_togo.py
"""

import os
import sys
import json
import time

# Ensure repo root and tests are importable
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
TESTS_DIR = os.path.join(ROOT, "tests")
if TESTS_DIR not in sys.path:
    sys.path.insert(0, TESTS_DIR)

# Import togo classes - using new Shapely-compatible API
try:
    from togo import (
        LineString,
        Polygon,
        Ring,
        from_wkt,
        from_geojson,
        to_geojson,
        Geometry,
        transform,
        shortest_line,
    )
except Exception as e:
    print("ERROR: Failed to import togo:", e)
    sys.exit(1)

# Import Shapely with compatibility across 1.x/2.x
try:
    import shapely
    from shapely.ops import unary_union, transform as shp_transform

    try:
        # Shapely 2.x preferred API
        from shapely import from_wkt as shp_from_wkt, to_wkt as shp_to_wkt
        from shapely import (
            from_geojson as shp_from_geojson,
            to_geojson as shp_to_geojson,
        )
        from shapely import shortest_line as shp_shortest_line
        from shapely.geometry import (
            Point as ShpPoint,
            LineString as ShpLineString,
            Polygon as ShpPolygon,
        )

        HAVE_SHAPELY2 = True
    except Exception:
        # Fallback to Shapely 1.x style
        from shapely import wkt as shp_wkt
        from shapely.geometry import shape as shp_shape
        from shapely.geometry import (
            Point as ShpPoint,
            LineString as ShpLineString,
            Polygon as ShpPolygon,
            mapping as shp_mapping,
        )

        HAVE_SHAPELY2 = False

        def shp_from_wkt(wkt: str):
            return shp_wkt.loads(wkt)

        def shp_to_wkt(geom) -> str:
            return geom.wkt

        def shp_from_geojson(geojson: str):
            return shp_shape(json.loads(geojson))

        def shp_to_geojson(geom) -> str:
            return json.dumps(shp_mapping(geom))

        # Shapely 1.x doesn't have shortest_line
        shp_shortest_line = None
except Exception as e:
    print(
        "ERROR: Shapely is required for this benchmark. Install it with 'pip install shapely'."
    )
    print("Details:", e)
    sys.exit(2)

# Try to import test geometry strings, with fallbacks
TOGO_JSON = None
BENIN_JSON = None
GBA_WKT = None
try:
    import geometries as tg

    TOGO_JSON = tg.TOGO.strip()
    BENIN_JSON = tg.BENIN.strip()
    GBA_WKT = tg.GRAN_BUENOS_AIRES_AREA.strip()
except Exception:
    # Minimal fallbacks
    TOGO_JSON = '{"type":"Polygon","coordinates":[[[0,0],[2,0],[2,2],[0,2],[0,0]]]]}'
    BENIN_JSON = '{"type":"Polygon","coordinates":[[[0,0],[4,0],[4,4],[0,4],[0,0]]]]}'
    GBA_WKT = "POLYGON ((0 0, 3 0, 3 2, 0 2, 0 0))"


def time_op(fn, iters=1000, warmup=200):
    # Warmup
    for _ in range(warmup):
        fn()
    t0 = time.perf_counter()
    for _ in range(iters):
        fn()
    t1 = time.perf_counter()
    return t1 - t0


def bench_case(name, togo_fn, shapely_fn, iters=1000):
    # Run both and compute ops/sec
    t_togo = time_op(togo_fn, iters=iters)
    t_shp = time_op(shapely_fn, iters=iters)
    ops_togo = iters / t_togo if t_togo > 0 else float("inf")
    ops_shp = iters / t_shp if t_shp > 0 else float("inf")
    print(f"- {name}:")
    print(f"  togo:    {ops_togo:12.1f} ops/s   ({t_togo * 1000:.2f} ms for {iters})")
    print(f"  shapely: {ops_shp:12.1f} ops/s   ({t_shp * 1000:.2f} ms for {iters})")


def main():
    print("Benchmark: togo vs Shapely")
    print(f"Python: {sys.version.split()[0]}")
    print(
        f"Shapely: {getattr(shapely, '__version__', 'unknown')} (2.x={HAVE_SHAPELY2})"
    )

    # Pre-parse big polygons for predicate tests
    g_togo_a = from_geojson(TOGO_JSON)
    g_togo_b = from_geojson(BENIN_JSON)

    g_shp_a = shp_from_geojson(TOGO_JSON)
    g_shp_b = shp_from_geojson(BENIN_JSON)
    # Ensure 2D in Shapely if polygon has Z
    if hasattr(g_shp_b, "has_z") and g_shp_b.has_z:  # type: ignore[attr-defined]
        # Drop Z by constructing a 2D Polygon
        g_shp_b = ShpPolygon(
            [(x, y) for x, y, *_ in g_shp_b.exterior.coords],
            [[(x, y) for x, y, *_ in r.coords] for r in g_shp_b.interiors],
        )

    # Small primitives
    wkt_point = "POINT (1 2)"
    geojson_point = '{"type":"Point","coordinates":[1,2]}'
    wkt_line = "LINESTRING (0 0, 1 1, 2 2, 3 3, 4 4)"
    ring_pts = [(0, 0), (10, 0), (10, 10), (0, 10), (0, 0)]

    # Parsing WKT
    bench_case(
        "parse WKT point",
        lambda: from_wkt(wkt_point),
        lambda: shp_from_wkt(wkt_point),
        iters=2000,
    )
    bench_case(
        "parse WKT linestring",
        lambda: from_wkt(wkt_line),
        lambda: shp_from_wkt(wkt_line),
        iters=1000,
    )
    bench_case(
        "parse GeoJSON polygon (country-scale)",
        lambda: from_geojson(TOGO_JSON),
        lambda: shp_from_geojson(TOGO_JSON),
        iters=200,
    )

    # Serialization
    bench_case(
        "to WKT (point)",
        lambda: from_wkt(wkt_point).wkt,
        lambda: shp_to_wkt(shp_from_wkt(wkt_point)),
        iters=2000,
    )
    bench_case(
        "to GeoJSON (point)",
        lambda: to_geojson(from_geojson(geojson_point)),
        lambda: shp_to_geojson(shp_from_geojson(geojson_point)),
        iters=2000,
    )

    # Bounds/rect
    bench_case(
        "bounds/rect (big polygon)",
        lambda: g_togo_a.bounds,
        lambda: g_shp_a.bounds,
        iters=2000,
    )

    # Predicates
    bench_case(
        "intersects (big polygons)",
        lambda: g_togo_a.intersects(g_togo_b),
        lambda: g_shp_a.intersects(g_shp_b),
        iters=400,
    )
    bench_case(
        "contains (polygon contains point)",
        lambda: g_togo_a.contains(from_wkt("POINT (1 8)")),
        lambda: g_shp_a.contains(ShpPoint(1, 8)),
        iters=1000,
    )
    bench_case(
        "covers (polygon covers point)",
        lambda: g_togo_a.covers(from_wkt("POINT (1 8)")),
        lambda: g_shp_a.covers(ShpPoint(1, 8)),
        iters=1000,
    )

    # Line length
    line_points = [(i, (i * i) % 10) for i in range(0, 200)]
    togo_line = LineString(line_points)
    shp_line = ShpLineString(line_points)
    bench_case(
        "line length (200 vertices)",
        lambda: togo_line.length,
        lambda: shp_line.length,
        iters=2000,
    )

    # Ring area/perimeter via exterior
    ring = Ring(ring_pts)
    poly = Polygon(ring)
    shp_poly = ShpPolygon(ring_pts)
    bench_case(
        "polygon area (square)",
        lambda: poly.area,
        lambda: shp_poly.area,
        iters=5000,
    )
    bench_case(
        "polygon perimeter (square)",
        lambda: poly.exterior.length,
        lambda: shp_poly.exterior.length,
        iters=5000,
    )

    # Geometry equals
    bench_case(
        "equals (point)",
        lambda: from_wkt(wkt_point).equals(from_geojson(geojson_point)),
        lambda: shp_from_wkt(wkt_point).equals(shp_from_geojson(geojson_point)),
        iters=3000,
    )

    # Unary union (polygon merge)
    bench_case(
        "unary_union (merge two polygons)",
        lambda: Geometry.unary_union(
            [from_geojson(TOGO_JSON), from_geojson(BENIN_JSON)]
        ),
        lambda: unary_union(
            [shp_from_geojson(TOGO_JSON), shp_from_geojson(BENIN_JSON)]
        ),
        iters=2000,
    )

    # Buffer operations
    buffer_point = from_wkt("POINT (0 0)")
    shp_buffer_point = shp_from_wkt("POINT (0 0)")

    buffer_line = from_wkt("LINESTRING (0 0, 10 10, 20 0)")
    shp_buffer_line = shp_from_wkt("LINESTRING (0 0, 10 10, 20 0)")

    buffer_poly = from_geojson(TOGO_JSON)
    shp_buffer_poly = shp_from_geojson(TOGO_JSON)

    bench_case(
        "buffer point (distance=1.0, quad_segs=8)",
        lambda: buffer_point.buffer(1.0, quad_segs=8),
        lambda: shp_buffer_point.buffer(1.0, quad_segs=8),
        iters=500,
    )

    bench_case(
        "buffer linestring (distance=2.0, quad_segs=8)",
        lambda: buffer_line.buffer(2.0, quad_segs=8),
        lambda: shp_buffer_line.buffer(2.0, quad_segs=8),
        iters=500,
    )

    bench_case(
        "buffer polygon (distance=1.0, quad_segs=8)",
        lambda: buffer_poly.buffer(1.0, quad_segs=8),
        lambda: shp_buffer_poly.buffer(1.0, quad_segs=8),
        iters=200,
    )

    bench_case(
        "buffer polygon (distance=1.0, quad_segs=16, custom join)",
        lambda: buffer_poly.buffer(1.0, quad_segs=16, join_style=2),
        lambda: shp_buffer_poly.buffer(1.0, quad_segs=16, join_style=2),
        iters=200,
    )

    # Simplify operations
    simplify_line = from_wkt(
        "LINESTRING (0 0, 0.1 0.1, 0.2 0.2, 0.3 0.3, 1 1, 1.1 1.1, 1.2 1.2, 2 2, 2.1 2.1, 2.2 2.2, 3 3)"
    )
    shp_simplify_line = shp_from_wkt(
        "LINESTRING (0 0, 0.1 0.1, 0.2 0.2, 0.3 0.3, 1 1, 1.1 1.1, 1.2 1.2, 2 2, 2.1 2.1, 2.2 2.2, 3 3)"
    )

    simplify_poly = from_geojson(TOGO_JSON)
    shp_simplify_poly = shp_from_geojson(TOGO_JSON)

    bench_case(
        "simplify linestring (tolerance=0.5, preserve_topology=True)",
        lambda: simplify_line.simplify(0.5, preserve_topology=True),
        lambda: shp_simplify_line.simplify(0.5, preserve_topology=True),
        iters=1000,
    )

    bench_case(
        "simplify linestring (tolerance=0.5, preserve_topology=False)",
        lambda: simplify_line.simplify(0.5, preserve_topology=False),
        lambda: shp_simplify_line.simplify(0.5, preserve_topology=False),
        iters=1000,
    )

    bench_case(
        "simplify polygon (tolerance=0.05, preserve_topology=True)",
        lambda: simplify_poly.simplify(0.05, preserve_topology=True),
        lambda: shp_simplify_poly.simplify(0.05, preserve_topology=True),
        iters=500,
    )

    bench_case(
        "simplify polygon (tolerance=0.05, preserve_topology=False)",
        lambda: simplify_poly.simplify(0.05, preserve_topology=False),
        lambda: shp_simplify_poly.simplify(0.05, preserve_topology=False),
        iters=500,
    )

    bench_case(
        "simplify polygon (tolerance=0.1, preserve_topology=True)",
        lambda: simplify_poly.simplify(0.1, preserve_topology=True),
        lambda: shp_simplify_poly.simplify(0.1, preserve_topology=True),
        iters=500,
    )

    bench_case(
        "simplify polygon (tolerance=0.1, preserve_topology=False)",
        lambda: simplify_poly.simplify(0.1, preserve_topology=False),
        lambda: shp_simplify_poly.simplify(0.1, preserve_topology=False),
        iters=500,
    )

    # Nearest points operations
    from shapely.ops import nearest_points as shp_nearest_points

    # Point to point
    np_point1 = from_wkt("POINT (0 0)")
    shp_np_point1 = shp_from_wkt("POINT (0 0)")
    np_point2 = from_wkt("POINT (10 10)")
    shp_np_point2 = shp_from_wkt("POINT (10 10)")

    bench_case(
        "nearest_points (point to point)",
        lambda: np_point1.nearest_points(np_point2),
        lambda: shp_nearest_points(shp_np_point1, shp_np_point2),
        iters=1000,
    )

    # Point to linestring
    np_point = from_wkt("POINT (0 0)")
    shp_np_point = shp_from_wkt("POINT (0 0)")
    np_line = from_wkt("LINESTRING (1 1, 5 5, 10 1)")
    shp_np_line = shp_from_wkt("LINESTRING (1 1, 5 5, 10 1)")

    bench_case(
        "nearest_points (point to linestring)",
        lambda: np_point.nearest_points(np_line),
        lambda: shp_nearest_points(shp_np_point, shp_np_line),
        iters=500,
    )

    # Point to polygon
    np_point_poly = from_wkt("POINT (0 0)")
    shp_np_point_poly = shp_from_wkt("POINT (0 0)")
    np_poly = from_wkt("POLYGON ((1 1, 5 1, 5 5, 1 5, 1 1))")
    shp_np_poly = shp_from_wkt("POLYGON ((1 1, 5 1, 5 5, 1 5, 1 1))")

    bench_case(
        "nearest_points (point to polygon)",
        lambda: np_point_poly.nearest_points(np_poly),
        lambda: shp_nearest_points(shp_np_point_poly, shp_np_poly),
        iters=500,
    )

    # Polygon to polygon
    np_poly1 = from_wkt("POLYGON ((0 0, 2 0, 2 2, 0 2, 0 0))")
    shp_np_poly1 = shp_from_wkt("POLYGON ((0 0, 2 0, 2 2, 0 2, 0 0))")
    np_poly2 = from_wkt("POLYGON ((5 5, 8 5, 8 8, 5 8, 5 5))")
    shp_np_poly2 = shp_from_wkt("POLYGON ((5 5, 8 5, 8 8, 5 8, 5 5))")

    bench_case(
        "nearest_points (polygon to polygon)",
        lambda: np_poly1.nearest_points(np_poly2),
        lambda: shp_nearest_points(shp_np_poly1, shp_np_poly2),
        iters=500,
    )

    # shortest_line operations (Shapely v2 API)
    print("\n=== Shortest Line (Shapely v2 API) ===")

    # Point to linestring
    sl_point = from_wkt("POINT (0 0)")
    shp_sl_point = shp_from_wkt("POINT (0 0)")
    sl_line = from_wkt("LINESTRING (1 1, 5 5, 10 1)")
    shp_sl_line = shp_from_wkt("LINESTRING (1 1, 5 5, 10 1)")

    bench_case(
        "shortest_line (point to linestring)",
        lambda: shortest_line(sl_point, sl_line),
        lambda: shp_shortest_line(shp_sl_point, shp_sl_line)
        if shp_shortest_line
        else None,
        iters=500,
    )

    # Point to polygon
    sl_point_poly = from_wkt("POINT (0 0)")
    shp_sl_point_poly = shp_from_wkt("POINT (0 0)")
    sl_poly = from_wkt("POLYGON ((1 1, 5 1, 5 5, 1 5, 1 1))")
    shp_sl_poly = shp_from_wkt("POLYGON ((1 1, 5 1, 5 5, 1 5, 1 1))")

    bench_case(
        "shortest_line (point to polygon)",
        lambda: shortest_line(sl_point_poly, sl_poly),
        lambda: shp_shortest_line(shp_sl_point_poly, shp_sl_poly)
        if shp_shortest_line
        else None,
        iters=500,
    )

    # Polygon to polygon
    sl_poly1 = from_wkt("POLYGON ((0 0, 2 0, 2 2, 0 2, 0 0))")
    shp_sl_poly1 = shp_from_wkt("POLYGON ((0 0, 2 0, 2 2, 0 2, 0 0))")
    sl_poly2 = from_wkt("POLYGON ((5 5, 8 5, 8 8, 5 8, 5 5))")
    shp_sl_poly2 = shp_from_wkt("POLYGON ((5 5, 8 5, 8 8, 5 8, 5 5))")

    bench_case(
        "shortest_line (polygon to polygon)",
        lambda: shortest_line(sl_poly1, sl_poly2),
        lambda: shp_shortest_line(shp_sl_poly1, shp_sl_poly2)
        if shp_shortest_line
        else None,
        iters=500,
    )

    # Transform operations
    import math

    # Simple translation function
    def translate(x, y):
        return x + 1.5, y + 2.5

    # Scaling function
    def scale(x, y):
        return x * 2.0, y * 3.0

    # Rotation function
    def rotate_45(x, y):
        angle = math.pi / 4
        cos_a, sin_a = math.cos(angle), math.sin(angle)
        return (x * cos_a - y * sin_a), (x * sin_a + y * cos_a)

    transform_point = from_wkt("POINT (0 0)")
    shp_transform_point = shp_from_wkt("POINT (0 0)")

    transform_line = from_wkt(
        "LINESTRING (0 0, 1 1, 2 2, 3 3, 4 4, 5 5, 6 6, 7 7, 8 8, 9 9)"
    )
    shp_transform_line = shp_from_wkt(
        "LINESTRING (0 0, 1 1, 2 2, 3 3, 4 4, 5 5, 6 6, 7 7, 8 8, 9 9)"
    )

    transform_poly = from_geojson(TOGO_JSON)
    shp_transform_poly = shp_from_geojson(TOGO_JSON)

    bench_case(
        "transform point (translate)",
        lambda: transform(translate, transform_point),
        lambda: shp_transform(translate, shp_transform_point),
        iters=1000,
    )

    bench_case(
        "transform linestring (scale)",
        lambda: transform(scale, transform_line),
        lambda: shp_transform(scale, shp_transform_line),
        iters=500,
    )

    bench_case(
        "transform polygon (rotate 45°)",
        lambda: transform(rotate_45, transform_poly),
        lambda: shp_transform(rotate_45, shp_transform_poly),
        iters=200,
    )

    print("\nNote: Results are rough microbenchmarks. Real-world performance can vary.")


if __name__ == "__main__":
    main()
