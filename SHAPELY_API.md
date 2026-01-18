# Shapely-Compatible API in ToGo

ToGo now provides a Shapely-compatible API, making it easy to migrate from Shapely or use ToGo as a drop-in replacement for many common geometric operations.

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
- `Polygon` - Create polygons (alias for `Poly`)
- `MultiPoint()` - Create multi-point geometries
- `MultiLineString()` - Create multi-linestring geometries
- `MultiPolygon()` - Create multi-polygon geometries
- `GeometryCollection()` - Create geometry collections

### Point

```python
from togo import Point

# Create a point
p = Point(1.5, 2.5)

# Shapely-compatible properties
p.geom_type      # 'Point'
p.x              # 1.5
p.y              # 2.5
p.coords         # [(1.5, 2.5)]
p.bounds         # (1.5, 2.5, 1.5, 2.5)
p.is_empty       # False
p.is_valid       # True
p.wkt            # 'POINT(1.5 2.5)'
p.wkb            # bytes object
p.__geo_interface__  # {'type': 'Point', 'coordinates': [1.5, 2.5]}
```

### LineString

```python
from togo import LineString

# Create a linestring
line = LineString([(0, 0), (1, 1), (2, 2), (3, 3)])

# Shapely-compatible properties
line.geom_type   # 'LineString'
line.coords      # [(0, 0), (1, 1), (2, 2), (3, 3)]
line.bounds      # (0, 0, 3, 3)
line.is_empty    # False
line.is_valid    # True
line.length      # 4.242... (property)
line.wkt         # 'LINESTRING(0 0,1 1,2 2,3 3)'
line.wkb         # bytes object
line.__geo_interface__  # GeoJSON-like dict
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
poly.exterior  # Ring object
poly.interiors   # List of Ring objects (holes)
poly.wkt         # 'POLYGON((0 0,4 0,4 4,0 4,0 0))'
poly.wkb         # bytes object
poly.__geo_interface__  # GeoJSON-like dict
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
point.coords      # [(x, y)]

# LineString
line.coords       # List of (x, y) tuples
line.length       # Float: length of line (property)

# Polygon
poly.area         # Float: area of polygon
poly.exterior   # Ring: exterior ring
poly.interiors    # List[Ring]: list of holes
poly.centroid     # Point: center of mass
```

## Spatial Predicates

All predicates work with Shapely-compatible API:

```python
from togo import Point, Polygon, Ring, from_wkt

# Create geometries
poly1 = Polygon([(0, 0), (2, 0), (2, 2), (0, 2), (0, 0)])
poly2 = Polygon([(1, 1), (3, 1), (3, 3), (1, 3), (1, 1)])
point = Point(0.5, 0.5)

# Convert to Geometry for predicates
geom1 = poly1.as_geometry()
geom2 = poly2.as_geometry()
pt_geom = point.as_geometry()

# Test predicates
geom1.intersects(geom2)  # True
geom1.contains(pt_geom)  # True
geom1.equals(geom2)      # False
geom1.disjoint(geom2)    # False
geom1.touches(geom2)     # False
geom1.within(geom2)      # False
geom1.covers(pt_geom)    # True
geom1.coveredby(geom2)   # False
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

### Convex Hull

All geometry types support the `convex_hull()` method for computing the smallest convex geometry that encloses all points:

```python
from togo import Point, LineString, Polygon, MultiPoint, convex_hull

# Convex hull of a polygon - direct method call
poly = Polygon([(0, 0), (2, 0), (2, 2), (1, 1), (0, 2), (0, 0)])
hull = poly.convex_hull()
print(hull.geom_type)  # 'Polygon'

# Convex hull of scattered points
points = MultiPoint([(0, 0), (1, 1), (0, 2), (2, 2), (3, 1), (1, 0)])
hull = points.convex_hull()
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
hull = geom.convex_hull()
print(hull.area)  # 9.0
```

The `convex_hull()` method:
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
4. **Module functions**: `from_wkt()`, `from_geojson()`, `to_wkt()`

5. **Predicates**: `contains()`, `intersects()`, `touches()`, `crosses()`, `within()`, `equals()`
6. **Operations**: `union()`, `intersection()`, `difference()`, `buffer()`, `simplify()`
### Differences

1. **Geometry conversion**: ToGo uses `.as_geometry()` for predicates:
   ```python
   # ToGo
   poly_geom = poly.as_geometry()
   poly_geom.contains(point.as_geometry())

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
from togo import Point, LineString, Polygon
from togo import from_wkt, to_wkt

# Create various geometries
point = Point(1.0, 2.0)
line = LineString([(0, 0), (1, 1), (2, 2)])
poly = Polygon([(0, 0), (5, 0), (5, 5), (0, 5), (0, 0)])

# Check properties
print(f"Point: {point.geom_type}, coords: {point.coords}")
print(f"Line: length = {line.length:.2f}, bounds = {line.bounds}")
print(f"Polygon: area = {poly.area}, bounds = {poly.bounds}")

# Parse from WKT
wkt = "POLYGON ((0 0, 10 0, 10 10, 0 10, 0 0), (2 2, 8 2, 8 8, 2 8, 2 2))"
parsed = from_wkt(wkt)
print(f"Parsed: {parsed.geom_type}")

# Test spatial relationships
pt_geom = point.as_geometry()
poly_geom = poly.as_geometry()

if poly_geom.contains(pt_geom):
    print("Polygon contains the point!")

# Export to different formats
print(f"WKT: {point.wkt}")
print(f"GeoJSON: {point.__geo_interface__}")
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

| Shapely API | ToGo API | Status |
|-------------|----------|--------|
| `Point(x, y)` | `Point(x, y)` | ✅ Supported |
| `LineString(coords)` | `LineString(coords)` | ✅ Supported |
| `Polygon(shell, holes)` | `Polygon(shell, holes=[...])` | ✅ Supported |
| `geom.geom_type` | `geom.geom_type` | ✅ Supported |
| `geom.bounds` | `geom.bounds` | ✅ Supported |
| `geom.area` | `geom.area` | ✅ Supported |
| `geom.length` | `geom.length` | ✅ Supported |
| `geom.centroid` | `geom.centroid` | ✅ Supported (via GEOS) |
| `geom.convex_hull` | `geom.convex_hull` | ✅ Supported (via GEOS) |
| `geom.is_empty` | `geom.is_empty` | ✅ Supported |
| `geom.coords` | `geom.coords` | ✅ Supported |
| `geom.wkt` | `geom.wkt` | ✅ Supported |
| `geom.wkb` | `geom.wkb` | ✅ Supported |
| `geom.__geo_interface__` | `geom.__geo_interface__` | ✅ Supported |
| `from_wkt()` | `from_wkt()` | ✅ Supported |
| `from_geojson()` | `from_geojson()` | ✅ Supported |
| `to_wkt()` | `to_wkt()` | ✅ Supported |
| `contains()` | `contains()` | ✅ Supported |
| `intersects()` | `intersects()` | ✅ Supported |
| `touches()` | `touches()` | ✅ Supported |
| `within()` | `within()` | ✅ Supported |
| `geom.buffer()` | `geom.buffer()` | ✅ Supported (via GEOS) |
| `geom.simplify()` | `geom.simplify()` | ✅ Supported (via GEOS) |
| `unary_union()` | `unary_union()` | ✅ Supported (via GEOS) |
| `transform()` | `transform()` | ✅ Supported |
| `nearest_points()` | `nearest_points()` | ✅ Supported (via GEOS) |
| `shortest_line()` | `shortest_line()` | ✅ Supported (via GEOS, v2 API) |
| `convex_hull()` | `convex_hull()` | ✅ Supported (via GEOS) |
| `intersection()` | - | ❌ Not yet (use GEOS via tgx) |

## Conclusion

ToGo now provides a Shapely-compatible API that makes it easy to use for developers familiar with Shapely, while leveraging the high performance of the underlying TG C library. The API is designed to be intuitive and follows Shapely conventions wherever possible.
