# Shapely-Compatible API in ToGo

ToGo now provides a Shapely-compatible API, making it easy to migrate from Shapely or use ToGo as a drop-in replacement for many common geometric operations.

## v0.4.1 Update (vs v0.4.0)

v0.4.1 includes targeted compatibility and safety improvements:

- Added support for `LineString.project(other, normalized=True)`.
- Hardened `Geometry.exterior` and `Geometry.interiors` lifetime behavior.
- Hardened `Geometry.boundary` extraction paths for polygon and multipolygon outputs.
- Fixed mixed-input `unary_union()` lifetime handling for coerced geometry objects.

## Quick Start

```python
from togo import Point, LineString, Polygon
from togo import from_wkt, from_geojson, to_wkt

# Create geometries using Shapely-like constructors
point = Point(1.0, 2.0)
line = LineString([(0, 0), (1, 1), (2, 2)])
poly = Polygon([(0, 0), (4, 0), (4, 4), (0, 4), (0, 0)])

# Access Shapely-compatible properties
print(point.geom_type)  # 'Point'
print(point.bounds)     # (1.0, 2.0, 1.0, 2.0)
print(line.length)      # 2.828...
print(poly.area)        # 16.0
print(poly.centroid)    # Point geometry (centroid)

# Use module-level functions
geom = from_wkt("POINT (1 2)")
print(to_wkt(geom))
```

## Shapely-Compatible Classes

### Class Aliases

ToGo provides the following Shapely-compatible class names:

- `Point` - Create points
- `LineString` - Create linestrings (alias for `Line`)
- `Polygon` - Create polygons (subclass of `Poly`)
- `MultiPoint()` - Create multi-point geometries (returns `Geometry`)
- `MultiLineString` - **Real Python class** inheriting from `Geometry`; `isinstance()` checks work
- `MultiPolygon` - **Real Python class** inheriting from `Geometry`; `isinstance()` checks work
- `GeometryCollection()` - Create geometry collections (returns `Geometry`)

```python
from togo import MultiPolygon, MultiLineString, Geometry, Poly, Ring

poly1 = Poly(Ring([(0,0), (1,0), (1,1), (0,1), (0,0)]))
mp = MultiPolygon([poly1])
print(isinstance(mp, MultiPolygon))  # True
print(isinstance(mp, Geometry))      # True

mls = MultiLineString([[(0,0), (1,1)]])
print(isinstance(mls, MultiLineString))  # True
```

### Point

```python
from togo import Point

# Create a point
p = Point(1.5, 2.5)

# Shapely-compatible properties
p.geom_type      # 'Point'
p.x              # 1.5
p.y              # 2.5
p.coords         # [(1.5, 2.5)]  — indexable sequence
p.coords[0]      # (1.5, 2.5)
len(p.coords)    # 1
p.bounds         # (1.5, 2.5, 1.5, 2.5)
p.is_empty       # False
p.is_valid       # True
p.wkt            # 'POINT(1.5 2.5)'
p.wkb            # bytes object
p.__geo_interface__  # {'type': 'Point', 'coordinates': [1.5, 2.5]}

# Equality
Point(1.5, 2.5) == Point(1.5, 2.5)   # True
Point(1.5, 2.5) == Point(0.0, 0.0)   # False
```

### LineString

```python
from togo import LineString

# Create a linestring
line = LineString([(0, 0), (1, 1), (2, 2), (3, 3)])

# Shapely-compatible properties
line.geom_type   # 'LineString'
line.coords      # [(0, 0), (1, 1), (2, 2), (3, 3)]  — indexable sequence
line.coords[0]   # (0, 0)
line.coords[-1]  # (3, 3)
len(line.coords) # 4
line.bounds      # (0, 0, 3, 3)
line.is_empty    # False
line.is_valid    # True
line.length      # 4.242... (property)
line.wkt         # 'LINESTRING(0 0,1 1,2 2,3 3)'
line.wkb         # bytes object
line.__geo_interface__  # GeoJSON-like dict

# project(point) — distance along line to nearest projected point (Shapely-compatible)
from togo import Point
line = LineString([(0, 0), (10, 0)])
line.project(Point(5, 3).as_geometry())   # 5.0 — projects perpendicularly
line.project(Point(0, 0).as_geometry())   # 0.0 — start of line
line.project(Point(10, 0).as_geometry())  # 10.0 — end of line

# project(..., normalized=True) — fraction in [0.0, 1.0]
line.project(Point(5, 0).as_geometry(), normalized=True)   # 0.5
line.project(Point(10, 0).as_geometry(), normalized=True)  # 1.0
```

### Polygon

```python
from togo import Polygon

# Create a polygon
exterior = [(0, 0), (4, 0), (4, 4), (0, 4), (0, 0)]
poly = Polygon(exterior)

# With holes
hole = [(1, 1), (3, 1), (3, 3), (1, 3), (1, 1)]
poly_with_hole = Polygon(exterior, holes=[hole])

# Shapely-compatible properties
poly.geom_type   # 'Polygon'
poly.bounds      # (0, 0, 4, 4)
poly.area        # 16.0
poly.centroid    # Point geometry (center of mass)
poly.is_empty    # False
poly.is_valid    # True
poly.exterior    # Ring object (exterior ring)
poly.interiors   # List of Ring objects (holes)
poly.boundary    # LineString — the exterior ring as a line
poly.wkt         # 'POLYGON((0 0,4 0,4 4,0 4,0 0))'
poly.wkb         # bytes object
poly.__geo_interface__  # GeoJSON-like dict

# intersects() — accepts wrapper objects directly (Shapely-compatible)
other = Polygon([(3, 3), (5, 3), (5, 5), (3, 5), (3, 3)])
poly.intersects(other)   # True (touching at corner)

# from_bounds() — create a rectangle from a bounding box (Shapely-compatible)
bbox = Polygon.from_bounds(0, 0, 10, 5)
print(bbox.area)    # 50.0
print(bbox.bounds)  # (0.0, 0.0, 10.0, 5.0)
```

## Module-Level Functions

### Parsing Functions

```python
from togo import from_wkt, from_geojson, from_wkb

# Parse WKT
geom = from_wkt("POINT (1 2)")
geom = from_wkt("LINESTRING (0 0, 1 1, 2 2)")
geom = from_wkt("POLYGON ((0 0, 4 0, 4 4, 0 4, 0 0))")

# Parse GeoJSON
geom = from_geojson('{"type":"Point","coordinates":[1,2]}')

# Parse WKB
wkb_bytes = b'...'  # WKB bytes
geom = from_wkb(wkb_bytes)
```

### Serialization Functions

```python
from togo import to_wkt, to_geojson, to_wkb

# Convert to WKT
wkt_str = to_wkt(point)
wkt_str = to_wkt(line)

# Convert to GeoJSON
geojson_str = to_geojson(poly)

# Convert to WKB
wkb_bytes = to_wkb(geom)
```

### unary_union()

`unary_union(geoms)` merges a sequence of geometries into a single geometry using GEOS (Shapely-compatible). Accepts any wrapper type directly — no `.as_geometry()` needed:

```python
from togo import Polygon, unary_union

# Merge overlapping polygons
poly1 = Polygon([(0, 0), (2, 0), (2, 2), (0, 2), (0, 0)])
poly2 = Polygon([(1, 1), (3, 1), (3, 3), (1, 3), (1, 1)])
union = unary_union([poly1, poly2])
print(union.geom_type)  # 'Polygon'
print(union.area)       # 7.0 (merged area)

# Non-overlapping → MultiPolygon
poly3 = Polygon([(10, 10), (11, 10), (11, 11), (10, 11), (10, 10)])
union2 = unary_union([poly1, poly3])
print(union2.geom_type)  # 'MultiPolygon'
```

## Geometry Properties

All geometry types support these Shapely-compatible properties:

### Common Properties

```python
# For any geometry
geom.geom_type    # String: 'Point', 'LineString', 'Polygon', etc.
geom.bounds       # Tuple: (minx, miny, maxx, maxy)
geom.is_empty     # Boolean: True if geometry is empty (property)
geom.is_valid     # Boolean: True if geometry is valid (property)
geom.wkt          # String: WKT representation
geom.wkb          # Bytes: WKB representation
geom.__geo_interface__  # Dict: GeoJSON-like interface
```

### Type-Specific Properties

```python
# Point
point.x           # x coordinate
point.y           # y coordinate
point.coords      # [(x, y)] — indexable, len() works
point.coords[0]   # (x, y)

# LineString
line.coords       # List of (x, y) tuples — indexable, len() works
line.coords[0]    # first coordinate
line.coords[-1]   # last coordinate
line.length       # Float: length of line (property)
line.project(pt)  # Float: distance along line to projected point

# Polygon
poly.area         # Float: area of polygon
poly.exterior     # Ring: exterior ring
poly.interiors    # List[Ring]: list of holes
poly.centroid     # Point: center of mass
poly.boundary     # LineString: exterior ring as a line
```

## Spatial Predicates

All predicates accept wrapper objects (`Point`, `LineString`, `Polygon`, etc.) **directly** — no manual `.as_geometry()` conversion is needed:

```python
from togo import Point, Polygon, from_wkt

# Create geometries
poly1 = Polygon([(0, 0), (2, 0), (2, 2), (0, 2), (0, 0)])
poly2 = Polygon([(1, 1), (3, 1), (3, 3), (1, 3), (1, 1)])
point = Point(0.5, 0.5)

# Predicates work directly on wrapper objects
poly1.intersects(poly2)  # True  — Polygon.intersects() available
poly1.intersects(point)  # True

# Geometry-level predicates also accept wrappers directly
geom1 = from_wkt("POLYGON((0 0, 2 0, 2 2, 0 2, 0 0))")
geom1.intersects(poly2)  # True  — no .as_geometry() needed
geom1.contains(point)    # True
geom1.equals(poly1)      # True
geom1.disjoint(poly2)    # False
geom1.touches(poly2)     # False
geom1.within(poly2)      # False
geom1.covers(point)      # True
geom1.coveredby(poly2)   # False
```

## Geometric Operations

### Buffer

All geometry types support the `buffer()` method for creating expanded or shrunk versions of geometries:

```python
from togo import Point, LineString, Polygon, Ring

# Buffer a point - creates a circular polygon
point = Point(0, 0)
circle = point.buffer(10.0, quad_segs=16)

# Buffer a line - creates polygon around line
line = LineString([(0, 0), (10, 10)])
zone = line.buffer(2.0, cap_style=1)  # round caps

# Buffer a polygon - expand outward or shrink inward
ring = Ring([(0, 0), (10, 0), (10, 10), (0, 10), (0, 0)])
poly = Polygon(ring)

expanded = poly.buffer(2.0)   # Expand outward
shrunk = poly.buffer(-1.0)    # Shrink inward

# Via Geometry object
geom = from_wkt("POLYGON((0 0, 10 0, 10 10, 0 10, 0 0))")
buffered = geom.buffer(
    distance=2.0,
    quad_segs=16,      # Segments per quadrant
    cap_style=1,        # 1=round, 2=flat, 3=square (for lines)
    join_style=1,       # 1=round, 2=mitre, 3=bevel
    mitre_limit=5.0     # For mitre joins
)
```

For detailed buffer documentation, see [BUFFER_API.md](BUFFER_API.md).

### Simplify

All geometry types support the `simplify()` method for reducing the complexity of geometries using the Douglas-Peucker algorithm:

```python
from togo import Point, LineString, Polygon, Ring

# Simplify a line
line = LineString([(0, 0), (0.1, 0.1), (0.2, 0.2), (1, 1), (2, 2)])
simplified = line.simplify(0.5, preserve_topology=True)

# Simplify a polygon with topology preservation (default)
poly = Polygon([
    (0, 0), (0.1, 0), (0.2, 0), (1, 0),
    (2, 0), (2, 1), (2, 2), (1, 2), (0, 2), (0, 0)
])
simplified = poly.simplify(0.5)  # preserve_topology=True by default

# Simplify without topology preservation (faster, may create invalid geometries)
simplified = poly.simplify(1.0, preserve_topology=False)

# Via Geometry object
geom = from_wkt("LINESTRING(0 0, 0.1 0.1, 1 1, 1.1 1.1, 2 2)")
simplified = geom.simplify(
    tolerance=0.5,          # Max distance from original coordinates
    preserve_topology=True  # Preserve topology (default)
)
```

The `simplify()` method:
- Reduces the number of vertices/points in a geometry
- Uses the Douglas-Peucker algorithm
- `preserve_topology=True` (default): Uses topology-preserving simplification to avoid self-intersections and invalid geometries
- `preserve_topology=False`: Uses standard Douglas-Peucker for faster simplification but may produce invalid geometries
- `tolerance`: Maximum distance from original coordinates. Larger tolerance = more simplification

### Intersection

All geometry types support the `intersection()` method for computing the geometric intersection of two geometries:

```python
from togo import Point, LineString, Polygon, intersection

# Intersection of overlapping polygons
poly1 = Polygon([(0, 0), (2, 0), (2, 2), (0, 2), (0, 0)])
poly2 = Polygon([(1, 1), (3, 1), (3, 3), (1, 3), (1, 1)])
result = poly1.intersection(poly2)
print(result.geom_type)  # 'Polygon'
print(result.area)       # 1.0 (1x1 square)

# Module-level function (Shapely-compatible)
result = intersection(poly1, poly2)

# Line crossing polygon
line = LineString([(0, 1), (3, 1)])
poly = Polygon([(1, 0), (2, 0), (2, 2), (1, 2), (1, 0)])
result = line.intersection(poly)
print(result.geom_type)  # 'LineString'
print(result.length)     # 1.0

# Point in polygon
point = Point(1.5, 1.5)
poly = Polygon([(0, 0), (3, 0), (3, 3), (0, 3), (0, 0)])
result = point.intersection(poly)
print(result.geom_type)  # 'Point'

# Non-intersecting geometries return empty
poly1 = Polygon([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)])
poly2 = Polygon([(5, 5), (6, 5), (6, 6), (5, 6), (5, 5)])
result = intersection(poly1, poly2)
print(result.is_empty)   # True

# Via Geometry object
geom1 = from_wkt("POLYGON((0 0, 2 0, 2 2, 0 2, 0 0))")
geom2 = from_wkt("POLYGON((1 1, 3 1, 3 3, 1 3, 1 1))")
result = geom1.intersection(geom2)
```

The `intersection()` method:
- Returns the set of points common to both geometries
- Result type depends on input geometries and spatial relationship
- Point-Point: Point (if overlapping) or empty
- Line-Line: Point, LineString, or MultiLineString
- Polygon-Polygon: Point, LineString, Polygon, or MultiPolygon
- Returns empty geometry if inputs don't intersect
- Compatible with Shapely's intersection API

### Convex Hull

All geometry types support the `convex_hull()` method for computing the smallest convex geometry that encloses all points:

```python
from togo import Point, LineString, Polygon, MultiPoint, convex_hull

# Convex hull of a polygon - property access
poly = Polygon([(0, 0), (2, 0), (2, 2), (1, 1), (0, 2), (0, 0)])
hull = poly.convex_hull
print(hull.geom_type)  # 'Polygon'

# Convex hull of scattered points
points = MultiPoint([(0, 0), (1, 1), (0, 2), (2, 2), (3, 1), (1, 0)])
hull = points.convex_hull
print(hull.geom_type)  # 'Polygon'

# Module-level function (Shapely-compatible)
line = LineString([(0, 0), (1, 2), (2, 0)])
hull = convex_hull(line)
print(hull.geom_type)  # 'Polygon'

# Convex hull of a point returns a point
point = Point(5, 5)
hull = convex_hull(point)
print(hull.geom_type)  # 'Point'

# Via Geometry object
geom = from_wkt("MULTIPOINT((0 0), (3 0), (3 3), (0 3))")
hull = geom.convex_hull
print(hull.area)  # 9.0
```

The `convex_hull` property:
- Returns the smallest convex geometry containing all points
- Equivalent to stretching a rubber band around the geometry
- For points: returns a Point
- For collinear points: returns a LineString
- For 3+ non-collinear points: returns a Polygon
- Useful for bounding analysis and spatial clustering

## Comparison with Shapely

### Similarities

1. **Class names**: `Point`, `LineString`, `Polygon`
2. **Properties**: `geom_type`, `bounds`, `area`, `coords`, `is_empty`, `is_valid`
3. **Serialization**: `wkt`, `wkb`, `__geo_interface__`
4. **Module functions**: `from_wkt()`, `from_geojson()`, `to_wkt()`, `unary_union()`
5. **Predicates**: `contains()`, `intersects()`, `touches()`, `within()`, `equals()`
6. **Operations**: `intersection()`, `buffer()`, `simplify()`, `project()`
7. **Multi-geometry classes**: `MultiPolygon`, `MultiLineString` are real Python classes, `isinstance()` works
8. **Equality**: `geom1 == geom2` works consistently, geometries are hashable

### Differences

1. **Low-level access**: ToGo exposes the TG object model (`Ring`, `Poly`, `Line`) which
   Shapely does not have. Use `.as_geometry()` when you need to pass a wrapper object to
   a function that specifically requires a `Geometry` instance.

2. **GEOS dependency**: Buffer, simplify, centroid, convex_hull, intersection, unary_union,
   nearest_points, shortest_line, and project all require the bundled `libgeos`.

## Performance

ToGo is built on the ultra-fast TG C library and offers excellent performance for:

- Parsing WKT/GeoJSON/WKB
- Spatial predicates (contains, intersects, etc.)
- Bounds/rect calculations
- Area and length computations

See `benchmarks/bench_shapely_vs_togo.py` for performance comparisons.

## Migration from Shapely

For many use cases, you can simply replace:

```python
# Before
from shapely.geometry import Point, LineString, Polygon
from shapely import from_wkt, to_wkt

# After
from togo import Point, LineString, Polygon
from togo import from_wkt, to_wkt
```

## Complete Example

```python
from togo import Point, LineString, Polygon, MultiPolygon, unary_union
from togo import from_wkt, to_wkt

# Create various geometries
point = Point(1.0, 2.0)
line = LineString([(0, 0), (1, 1), (2, 2)])
poly = Polygon([(0, 0), (5, 0), (5, 5), (0, 5), (0, 0)])

# Check properties
print(f"Point: {point.geom_type}, coords[0]: {point.coords[0]}")
print(f"Line: length = {line.length:.2f}, bounds = {line.bounds}")
print(f"Polygon: area = {poly.area}, bounds = {poly.bounds}")

# project() — distance along line to projected point
road = LineString([(0, 0), (100, 0)])
stop = Point(40, 10)
print(f"Stop is at {road.project(stop.as_geometry()):.1f}m along the road")  # 40.0m

# Polygon.from_bounds() — create a bounding box rectangle
bbox = Polygon.from_bounds(0, 0, 10, 5)
print(f"BBox area: {bbox.area}")   # 50.0

# Polygon.boundary — exterior ring as a LineString
print(f"Perimeter via boundary: {poly.boundary.length:.2f}")  # same as poly.length

# Spatial predicates — no .as_geometry() needed
other_poly = Polygon([(3, 3), (7, 3), (7, 7), (3, 7), (3, 3)])
print(f"Intersects: {poly.intersects(other_poly)}")  # True
print(f"Contains point: {from_wkt('POLYGON((0 0,5 0,5 5,0 5,0 0))').contains(point)}")  # True

# unary_union — module-level Shapely-compatible function
poly1 = Polygon([(0, 0), (2, 0), (2, 2), (0, 2), (0, 0)])
poly2 = Polygon([(1, 1), (3, 1), (3, 3), (1, 3), (1, 1)])
union = unary_union([poly1, poly2])
print(f"Union type: {union.geom_type}, area: {union.area:.1f}")  # Polygon, 7.0

# MultiPolygon — real class, isinstance works
mp = MultiPolygon([poly1, Polygon([(10, 10), (11, 10), (11, 11), (10, 11), (10, 10)])])
print(f"isinstance check: {isinstance(mp, MultiPolygon)}")  # True

# Equality
p1, p2 = Point(1, 2), Point(1, 2)
print(f"p1 == p2: {p1 == p2}")  # True
```

## Nearest Points and Shortest Line (Shapely v2 API)

### nearest_points()

The `nearest_points()` method returns a tuple of the two nearest points between two geometries. This is compatible with Shapely's `nearest_points` function.

```python
from togo import Point, LineString, Polygon, Ring

# Point to LineString
point = Point(0, 0)
line = LineString([(10, 0), (10, 10)])
pt1, pt2 = point.nearest_points(line)
print(f"Nearest on point: ({pt1.x}, {pt1.y})")  # (0.0, 0.0)
print(f"Nearest on line: ({pt2.x}, {pt2.y})")   # (10.0, 0.0)

# Point to Polygon
point = Point(0, 0)
exterior = Ring([(10, 0), (15, 0), (15, 5), (10, 5), (10, 0)])
poly = Polygon(exterior)
pt1, pt2 = point.nearest_points(poly)
print(f"Distance: {((pt2.x - pt1.x)**2 + (pt2.y - pt1.y)**2)**0.5:.2f}")  # 10.0

# Polygon to Polygon
exterior1 = Ring([(0, 0), (5, 0), (5, 5), (0, 5), (0, 0)])
poly1 = Polygon(exterior1)
exterior2 = Ring([(10, 0), (15, 0), (15, 5), (10, 5), (10, 0)])
poly2 = Polygon(exterior2)
pt1, pt2 = poly1.nearest_points(poly2)
print(f"Distance between polygons: {((pt2.x - pt1.x)**2 + (pt2.y - pt1.y)**2)**0.5:.2f}")  # 5.0
```

### shortest_line() (Shapely v2 API)

The `shortest_line()` method returns a LineString connecting the two nearest points between two geometries. This is compatible with Shapely v2's `shortest_line` method and is essentially a convenience wrapper around `nearest_points()`.

```python
from togo import Point, LineString, Polygon, Ring

# Point to LineString - returns the connecting line
point = Point(0, 0)
line = LineString([(10, 0), (10, 10)])
shortest = point.shortest_line(line)
print(f"Shortest line length: {shortest.length:.2f}")  # 10.0
print(f"Connects: {shortest.coords}")  # [(0.0, 0.0), (10.0, 0.0)]

# Point to Polygon
point = Point(0, 0)
exterior = Ring([(10, 0), (15, 0), (15, 5), (10, 5), (10, 0)])
poly = Polygon(exterior)
shortest = point.shortest_line(poly)
print(f"Shortest distance: {shortest.length:.2f}")  # 10.0

# Polygon to Polygon
exterior1 = Ring([(0, 0), (5, 0), (5, 5), (0, 5), (0, 0)])
poly1 = Polygon(exterior1)
exterior2 = Ring([(10, 0), (15, 0), (15, 5), (10, 5), (10, 0)])
poly2 = Polygon(exterior2)
shortest = poly1.shortest_line(poly2)
print(f"Gap between polygons: {shortest.length:.2f}")  # 5.0
coords = shortest.coords
print(f"Connects ({coords[0][0]:.1f}, {coords[0][1]:.1f}) to ({coords[1][0]:.1f}, {coords[1][1]:.1f})")

# Works with intersecting geometries too (length = 0)
line1 = LineString([(0, 0), (10, 10)])
line2 = LineString([(0, 10), (10, 0)])
shortest = line1.shortest_line(line2)
print(f"Intersecting lines distance: {shortest.length:.10f}")  # ~0.0
```

## Coordinate Transformation

The `transform` function applies a coordinate transformation function to all coordinates in a geometry. This is similar to `shapely.ops.transform` and is useful for coordinate system transformations, scaling, rotations, and other operations.

```python
from togo import transform, Point, LineString, Polygon

# Simple translation
def translate(x, y):
    return x + 10, y + 20

point = Point(0, 0)
translated = transform(translate, point)
print(translated.coords)  # [(10.0, 20.0)]

# Scaling
def scale(x, y):
    return x * 2, y * 3

line = LineString([(0, 0), (1, 1), (2, 2)])
scaled = transform(scale, line)
print(scaled.coords)  # [(0.0, 0.0), (2.0, 3.0), (4.0, 6.0)]

# More complex transformations (e.g., rotation)
import math
def rotate_45(x, y):
    angle = math.pi / 4
    cos_a, sin_a = math.cos(angle), math.sin(angle)
    return (x * cos_a - y * sin_a), (x * sin_a + y * cos_a)

poly = Polygon([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)])
rotated = transform(rotate_45, poly)
```

The `transform` function works with:
- Simple geometries: `Point`, `LineString`, `Polygon`
- Multi-geometries: `MultiPoint`, `MultiLineString`, `MultiPolygon`
- Geometry collections with mixed types

## API Reference Summary

| Shapely API | ToGo API | Notes |
|-------------|----------|-------|
| `Point(x, y)` | `Point(x, y)` | ✅ |
| `LineString(coords)` | `LineString(coords)` | ✅ |
| `Polygon(shell, holes)` | `Polygon(shell, holes=[...])` | ✅ |
| `Polygon.from_bounds(x1,y1,x2,y2)` | `Polygon.from_bounds(x1,y1,x2,y2)` | ✅ |
| `MultiPolygon(polys)` | `MultiPolygon(polys)` | ✅ Real class; `isinstance` works |
| `MultiLineString(lines)` | `MultiLineString(lines)` | ✅ Real class; `isinstance` works |
| `geom.geom_type` | `geom.geom_type` | ✅ |
| `geom.bounds` | `geom.bounds` | ✅ |
| `geom.area` | `geom.area` | ✅ |
| `geom.length` | `geom.length` | ✅ |
| `geom.centroid` | `geom.centroid` | ✅ via GEOS |
| `geom.convex_hull` | `geom.convex_hull` | ✅ via GEOS |
| `geom.boundary` | `poly.boundary` | ✅ on Polygon/Poly |
| `geom.is_empty` | `geom.is_empty` | ✅ |
| `geom.is_valid` | `geom.is_valid` | ✅ via GEOS |
| `geom.coords` | `geom.coords` | ✅ Indexable; `coords[i]` and `len()` work |
| `geom.exterior` | `poly.exterior` | ✅ on Polygon/Poly |
| `geom.interiors` | `poly.interiors` | ✅ on Polygon/Poly |
| `geom.wkt` | `geom.wkt` | ✅ |
| `geom.wkb` | `geom.wkb` | ✅ |
| `geom.__geo_interface__` | `geom.__geo_interface__` | ✅ |
| `geom1 == geom2` | `geom1 == geom2` | ✅ |
| `from_wkt()` | `from_wkt()` | ✅ |
| `from_geojson()` | `from_geojson()` | ✅ |
| `to_wkt()` | `to_wkt()` | ✅ |
| `geom.contains(other)` | `geom.contains(other)` | ✅ Accepts wrapper objects directly |
| `geom.intersects(other)` | `geom.intersects(other)` | ✅ Accepts wrapper objects directly |
| `poly.intersects(other)` | `poly.intersects(other)` | ✅ on Polygon/Poly |
| `geom.touches(other)` | `geom.touches(other)` | ✅ Accepts wrapper objects directly |
| `geom.within(other)` | `geom.within(other)` | ✅ Accepts wrapper objects directly |
| `geom.equals(other)` | `geom.equals(other)` | ✅ Accepts wrapper objects directly |
| `geom.buffer()` | `geom.buffer()` | ✅ via GEOS |
| `geom.simplify()` | `geom.simplify()` | ✅ via GEOS |
| `geom.intersection(other)` | `geom.intersection(other)` | ✅ via GEOS; accepts wrappers |
| `line.project(point, normalized=False)` | `line.project(point, normalized=False)` | ✅ via GEOS |
| `unary_union(geoms)` | `unary_union(geoms)` | ✅ Module-level; via GEOS |
| `transform(fn, geom)` | `transform(fn, geom)` | ✅ |
| `nearest_points(g1, g2)` | `nearest_points(g1, g2)` | ✅ via GEOS |
| `shortest_line(g1, g2)` | `shortest_line(g1, g2)` | ✅ via GEOS |
| `convex_hull(geom)` | `convex_hull(geom)` | ✅ via GEOS |
| `intersection(g1, g2)` | `intersection(g1, g2)` | ✅ via GEOS |

## Conclusion

ToGo provides a comprehensive Shapely-compatible API that makes it easy to migrate from Shapely or use it as a drop-in replacement for common geometric operations. Key highlights:

- **Wrapper objects are first-class citizens** — all spatial predicates and operations accept `Point`, `LineString`, `Polygon`, etc. directly without calling `.as_geometry()`.
- **`MultiPolygon` and `MultiLineString` are real Python classes** — `isinstance()` checks work as expected.
- **`unary_union(geoms)`** is a proper module-level function aligned with Shapely's API.
- **New Polygon conveniences**: `from_bounds()`, `boundary`, `intersects()`.
- **`LineString.project()`** for measuring distance-along-line projections.
- **Geometry equality** via `==` and hashability are supported on all geometry types.

All of this sits on top of the ultra-fast TG C library, with advanced operations powered by the bundled `libgeos`.
