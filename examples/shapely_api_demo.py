#!/usr/bin/env python3
"""
Example script demonstrating Shapely-compatible API in ToGo
"""

from togo import Point, LineString, Polygon
from togo import from_wkt, from_geojson

print("=" * 60)
print("ToGo Shapely-Compatible API Examples")
print("=" * 60)

# Example 1: Creating geometries
print("\n1. Creating Geometries:")
print("-" * 40)

point = Point(1.5, 2.5)
print(f"Point: {point}")
print(f"  geom_type: {point.geom_type}")
print(f"  coords: {point.coords}")
print(f"  bounds: {point.bounds}")

line = LineString([(0, 0), (1, 1), (2, 2), (3, 3)])
print(f"\nLineString: {line}")
print(f"  geom_type: {line.geom_type}")
print(f"  length: {line.length:.3f}")
print(f"  bounds: {line.bounds}")

exterior = [(0, 0), (5, 0), (5, 5), (0, 5), (0, 0)]
hole = [(1, 1), (4, 1), (4, 4), (1, 4), (1, 1)]
poly = Polygon(exterior, holes=[hole])
print(f"\nPolygon: {poly}")
print(f"  geom_type: {poly.geom_type}")
print(f"  area: {poly.area}")
print(f"  bounds: {poly.bounds}")
print(f"  num holes: {len(poly.interiors)}")

# Example 2: Parsing from WKT
print("\n2. Parsing from WKT:")
print("-" * 40)

wkt_point = "POINT (10 20)"
parsed_point = from_wkt(wkt_point)
print(f"Parsed: {wkt_point}")
print(f"  Type: {parsed_point.geom_type}")
print(f"  Bounds: {parsed_point.bounds}")

wkt_poly = "POLYGON ((0 0, 10 0, 10 10, 0 10, 0 0))"
parsed_poly = from_wkt(wkt_poly)
print(f"\nParsed: {wkt_poly}")
print(f"  Type: {parsed_poly.geom_type}")
print(f"  Area: {parsed_poly.area}")

# Example 3: Parsing from GeoJSON
print("\n3. Parsing from GeoJSON:")
print("-" * 40)

geojson = '{"type":"Point","coordinates":[3.5,4.5]}'
parsed_geojson = from_geojson(geojson)
print(f"Parsed: {geojson}")
print(f"  Type: {parsed_geojson.geom_type}")
print(f"  Coords: {parsed_geojson.coords}")

# Example 4: Exporting to different formats
print("\n4. Exporting Geometries:")
print("-" * 40)

print(f"Point as WKT: {point.wkt}")
print(f"Point as GeoJSON: {point.__geo_interface__()}")
print(f"Point as WKB: {len(point.wkb)} bytes")

# Example 5: Spatial Predicates
print("\n5. Spatial Predicates:")
print("-" * 40)

# Create two overlapping polygons
poly1 = Polygon([(0, 0), (3, 0), (3, 3), (0, 3), (0, 0)])
poly2 = Polygon([(2, 2), (5, 2), (5, 5), (2, 5), (2, 2)])
test_point = Point(1, 1)

# Convert to Geometry objects for predicates
geom1 = poly1.as_geometry()
geom2 = poly2.as_geometry()
pt_geom = test_point.as_geometry()

print(f"Polygon 1 bounds: {poly1.bounds}")
print(f"Polygon 2 bounds: {poly2.bounds}")
print(f"Test point: {test_point.coords}")

print("\nPredicate results:")
print(f"  poly1.intersects(poly2): {geom1.intersects(geom2)}")
print(f"  poly1.contains(point): {geom1.contains(pt_geom)}")
print(f"  poly2.contains(point): {geom2.contains(pt_geom)}")
print(f"  poly1.touches(poly2): {geom1.touches(geom2)}")
print(f"  poly1.equals(poly2): {geom1.equals(geom2)}")

# Example 6: Working with properties
print("\n6. Geometry Properties:")
print("-" * 40)

big_poly = Polygon([(0, 0), (10, 0), (10, 10), (0, 10), (0, 0)])

print("Polygon properties:")
print(f"  geom_type: {big_poly.geom_type}")
print(f"  bounds: {big_poly.bounds}")
print(f"  area: {big_poly.area}")
print(f"  is_empty: {big_poly.is_empty}")
print(f"  exterior points: {len(big_poly.exterior.coords)}")
print(f"  num holes: {len(big_poly.interiors)}")

# Example 7: Coordinate access
print("\n7. Accessing Coordinates:")
print("-" * 40)

test_line = LineString([(0, 0), (5, 5), (10, 0)])
print(f"LineString with {len(test_line.coords)} points:")
for i, coord in enumerate(test_line.coords):
    print(f"  Point {i}: {coord}")

print("\n" + "=" * 60)
print("All examples completed successfully!")
print("=" * 60)
