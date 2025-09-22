import sys
import json
import time

# Ensure repo root and tests are importable
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
TESTS_DIR = os.path.join(ROOT, "tests")
if TESTS_DIR not in sys.path:
    sys.path.insert(0, TESTS_DIR)

# Import togo

# import togo
# togo.set_index(togo.TGIndex.YSTRIPES)

try:
    from togo import Geometry, Line, Ring, Poly
except Exception as e:
    print("ERROR: Failed to import togo:", e)
    sys.exit(1)

# Import Shapely with compatibility across 1.x/2.x
try:
    import shapely

    try:
        # Shapely 2.x preferred API
        from shapely import from_wkt as shp_from_wkt, to_wkt as shp_to_wkt
        from shapely import (
            from_geojson as shp_from_geojson,
            to_geojson as shp_to_geojson,
        )
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
    g_togo_a = Geometry(TOGO_JSON, fmt="geojson")
    g_togo_b = Geometry(BENIN_JSON, fmt="geojson")

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
        lambda: Geometry(wkt_point, fmt="wkt"),
        lambda: shp_from_wkt(wkt_point),
        iters=2000,
    )
    bench_case(
        "parse WKT linestring",
        lambda: Geometry(wkt_line, fmt="wkt"),
        lambda: shp_from_wkt(wkt_line),
        iters=1000,
    )
    bench_case(
        "parse GeoJSON polygon (country-scale)",
        lambda: Geometry(TOGO_JSON, fmt="geojson"),
        lambda: shp_from_geojson(TOGO_JSON),
        iters=200,
    )

    # Serialization
    bench_case(
        "to WKT (point)",
        lambda: Geometry(wkt_point, fmt="wkt").to_wkt(),
        lambda: shp_to_wkt(shp_from_wkt(wkt_point)),
        iters=2000,
    )
    bench_case(
        "to GeoJSON (point)",
        lambda: Geometry(geojson_point, fmt="geojson").to_geojson(),
        lambda: shp_to_geojson(shp_from_geojson(geojson_point)),
        iters=2000,
    )

    # Bounds/rect
    bench_case(
        "bounds/rect (big polygon)",
        lambda: g_togo_a.rect(),
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
        lambda: g_togo_a.contains(Geometry("POINT (1 8)", fmt="wkt")),
        lambda: g_shp_a.contains(ShpPoint(1, 8)),
        iters=1000,
    )
    bench_case(
        "covers (polygon covers point)",
        lambda: g_togo_a.covers(Geometry("POINT (1 8)", fmt="wkt")),
        lambda: g_shp_a.covers(ShpPoint(1, 8)),
        iters=1000,
    )

    # Line length
    line_points = [(i, (i * i) % 10) for i in range(0, 200)]
    togo_line = Line(line_points)
    shp_line = ShpLineString(line_points)
    bench_case(
        "line length (200 vertices)",
        lambda: togo_line.length(),
        lambda: shp_line.length,
        iters=2000,
    )

    # Ring area/perimeter via exterior
    ring = Ring(ring_pts)
    poly = Poly(ring)
    shp_poly = ShpPolygon(ring_pts)
    bench_case(
        "polygon area (square)",
        lambda: poly.exterior().area(),
        lambda: shp_poly.area,
        iters=5000,
    )
    bench_case(
        "polygon perimeter (square)",
        lambda: poly.exterior().perimeter(),
        lambda: shp_poly.exterior.length,
        iters=5000,
    )

    # Geometry equals
    bench_case(
        "equals (point)",
        lambda: Geometry(wkt_point, fmt="wkt").equals(
            Geometry(geojson_point, fmt="geojson")
        ),
        lambda: shp_from_wkt(wkt_point).equals(shp_from_geojson(geojson_point)),
        iters=3000,
    )

    print("\nNote: Results are rough microbenchmarks. Real-world performance can vary.")


if __name__ == "__main__":
    main()
