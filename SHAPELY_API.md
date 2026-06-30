# Shapely-Compatible API in ToGo

ToGo now provides a Shapely-compatible API, making it easy to migrate from Shapely or use ToGo as a drop-in replacement for many common geometric operations.


## Quick Start

```python
from togo import Point, LineString, LinearRing, Polygon
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
- `LinearRing` - Ring-like line type (subclass of `Line` / `LineString`) used by `Polygon.exterior`
- `Polygon` - Create polygons (subclass of `Poly`)
- `MultiPoint` - **Real Python class** inheriting from `Geometry`; `isinstance()` checks work
- `MultiLineString` - **Real Python class** inheriting from `Geometry`; `isinstance()` checks work
- `MultiPolygon` - **Real Python class** inheriting from `Geometry`; `isinstance()` checks work
- `GeometryCollection` - **Real Python class** inheriting from `Geometry`; `isinstance()` checks work
- `BaseGeometry` - Shapely-style base-type check target for concrete ToGo geometry classes (`Geometry`, `Point`, `LineString`, `Polygon`, `Multi*`, `GeometryCollection`)

```python
from togo import BaseGeometry, MultiPolygon, MultiLineString, Geometry, Point, Polygon, Poly, Ring

poly1 = Poly(Ring([(0,0), (1,0), (1,1), (0,1), (0,0)]))
mp = MultiPolygon([poly1])
print(isinstance(mp, MultiPolygon))  # True
print(isinstance(mp, Geometry))      # True
print(isinstance(mp, BaseGeometry))  # True

pt = Point(1, 2)
poly = Polygon([(0, 0), (1, 0), (1, 1), (0, 0)])
print(isinstance(pt, BaseGeometry))    # True
print(isinstance(poly, BaseGeometry))  # True

mls = MultiLineString([[(0,0), (1,1)]])
print(isinstance(mls, MultiLineString))  # True
```

### Point

```python
from togo import Point

# Create a point
p = Point(1.5, 2.5)

# Shapely-compatible properties
print(p.geom_type)         # 'Point'
print(p.x)                 # 1.5
print(p.y)                 # 2.5
print(p.coords)            # [(1.5, 2.5)]  — indexable sequence
print(p.coords[0])         # (1.5, 2.5)
print(len(p.coords))       # 1
print(p.bounds)            # (1.5, 2.5, 1.5, 2.5)
print(p.is_empty)          # False
print(p.is_valid)          # True
print(p.wkt)               # 'POINT(1.5 2.5)'
print(p.wkb)               # bytes object
print(p.__geo_interface__) # {'type': 'Point', 'coordinates': [1.5, 2.5]}

# Equality
print(Point(1.5, 2.5) == Point(1.5, 2.5))   # True
print(Point(1.5, 2.5) == Point(0.0, 0.0))    # False
```

### LineString

```python
from togo import LineString

# Create a linestring
line = LineString([(0, 0), (1, 1), (2, 2), (3, 3)])

# Shapely-compatible properties
print(line.geom_type)          # 'LineString'
print(line.coords)             # [(0, 0), (1, 1), (2, 2), (3, 3)]  — indexable sequence
print(line.coords[0])          # (0, 0)
print(line.coords[-1])         # (3, 3)
print(len(line.coords))        # 4
print(line.bounds)             # (0, 0, 3, 3)
print(line.is_empty)           # False
print(line.is_valid)           # True
print(line.length)             # 4.242... (property)
print(line.wkt)                # 'LINESTRING(0 0,1 1,2 2,3 3)'
print(line.wkb)                # bytes object
print(line.__geo_interface__)  # GeoJSON-like dict

# project(point) — distance along line to nearest projected point (Shapely-compatible)
from togo import Point
line = LineString([(0, 0), (10, 0)])
print(line.project(Point(5, 3).as_geometry()))   # 5.0 — projects perpendicularly
print(line.project(Point(0, 0).as_geometry()))   # 0.0 — start of line
print(line.project(Point(10, 0).as_geometry()))  # 10.0 — end of line

# project(..., normalized=True) — fraction in [0.0, 1.0]
print(line.project(Point(5, 0).as_geometry(), normalized=True))   # 0.5
print(line.project(Point(10, 0).as_geometry(), normalized=True))  # 1.0

# Geometry objects that are line-like also support project()
line_geom = line.as_geometry()
print(line_geom.project(Point(5, 3)))                   # 5.0
print(line_geom.project(Point(5, 3), normalized=True))  # 0.5
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
print(poly.geom_type)         # 'Polygon'
print(poly.bounds)            # (0, 0, 4, 4)
print(poly.area)              # 16.0
print(poly.centroid)          # Point geometry (center of mass; concrete Point when non-empty)
print(poly.is_empty)          # False
print(poly.is_valid)          # True
print(poly.exterior)          # LinearRing object (also LineString-compatible)
print(poly.interiors)         # List of Ring objects (holes)
print(poly.boundary)          # LineString (no holes) or MultiLineString (with holes)
print(poly.wkt)               # 'POLYGON((0 0,4 0,4 4,0 4,0 0))'
print(poly.wkb)               # bytes object
print(poly.__geo_interface__) # GeoJSON-like dict

# intersects() — accepts wrapper objects directly (Shapely-compatible)
other = Polygon([(3, 3), (5, 3), (5, 5), (3, 5), (3, 3)])
print(poly.intersects(other))   # True (touching at corner)

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
point_geom = from_wkt("POINT (1 2)")
line_geom = from_wkt("LINESTRING (0 0, 1 1, 2 2)")
poly_geom = from_wkt("POLYGON ((0 0, 4 0, 4 4, 0 4, 0 0))")
print(point_geom.geom_type)
print(line_geom.geom_type)
print(poly_geom.geom_type)

# Parse GeoJSON
geojson_geom = from_geojson('{"type":"Point","coordinates":[1,2]}')
print(geojson_geom.geom_type)

# Parse WKB
wkb_bytes = bytes.fromhex("0101000000000000000000F03F0000000000000040")
wkb_geom = from_wkb(wkb_bytes)
print(wkb_geom.geom_type)

# Parsing helpers materialize concrete classes when determinable
pt = from_geojson('{"type":"Point","coordinates":[1,2]}')
print(type(pt).__name__)  # Point

poly = from_geojson('{"type":"Polygon","coordinates":[[[0,0],[1,0],[1,1],[0,0]]]}')
print(type(poly).__name__)  # Geometry (use shape() for concrete Polygon materialization)

# Multi geometries are materialized directly
mp = from_geojson('{"type":"MultiPolygon","coordinates":[[[[0,0],[1,0],[1,1],[0,1],[0,0]]]]}')
print(type(mp).__name__)  # MultiPolygon
```

### shape() and box()

```python
from togo import shape, box

# shape() from GeoJSON-like mapping or __geo_interface__ object
geom = shape({"type": "Point", "coordinates": [1, 2]})
print(geom.geom_type)  # 'Point'
print(type(geom).__name__)  # Point

poly = shape({"type": "Polygon", "coordinates": [[(0, 0), (1, 0), (1, 1), (0, 0)]]})
print(type(poly).__name__)  # Polygon

# box() from bounds
rect = box(0, 0, 3, 2)
print(rect.geom_type)  # 'Polygon'
print(rect.bounds)     # (0.0, 0.0, 3.0, 2.0)
```

### Serialization Functions

```python
from togo import to_wkt, to_geojson, to_wkb
from togo import Point, LineString, Polygon

# Convert to WKT
point = Point(1, 2)
line = LineString([(0, 0), (1, 1)])
poly = Polygon([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)])
print(to_wkt(point))
print(to_wkt(line))

# Convert to GeoJSON
print(to_geojson(poly))

# Convert to WKB
geom = poly.as_geometry()
print(len(to_wkb(geom)))
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

`unary_union()` also includes a robustness fallback for conversion edge-cases: if converting an
intermediate TG GeometryCollection to GEOS fails, ToGo retries by converting/unioning child
geometries iteratively.

### force_2d()

`force_2d(geometry)` returns a 2D copy of the input geometry with any Z/M coordinates dropped.
This is useful when you want to normalize mixed-dimension inputs before overlay or predicate work:

```python
from togo import force_2d, from_wkt

geom = from_wkt("POINT ZM (1 2 3 4)")
geom2d = force_2d(geom)
print(geom2d.geom_type)  # 'Point'
print(geom2d.coords)     # [(1.0, 2.0)]
```

The `force_2d()` helper:
- preserves the underlying geometry type and topology
- drops Z/M ordinates from all coordinates
- works recursively for multi-geometries and geometry collections
- is module-level and Shapely-like in style

Overlay operations (`intersection`, `union`, `difference`, `unary_union`) now accept 3D
inputs and normalize to 2D internally (Z/M is ignored for topology).

## Geometry Properties

All geometry types support these Shapely-compatible properties:

### Common Properties

```python
# For any geometry
from togo import Geometry

geom = Geometry("POINT(1 2)", fmt="wkt")
print(geom.geom_type)          # String: 'Point', 'LineString', 'Polygon', etc.
print(geom.bounds)             # Tuple: (minx, miny, maxx, maxy)
print(geom.is_empty)           # Boolean: True if geometry is empty (property)
print(geom.is_valid)           # Boolean: True if geometry is valid (property)
print(geom.wkt)                # String: WKT representation
print(geom.wkb)                # Bytes: WKB representation
print(geom.__geo_interface__)  # Dict: GeoJSON-like interface

# Point-like Geometry results expose x/y like Shapely
centroid = Geometry("POLYGON((0 0,4 0,4 4,0 4,0 0))", fmt="wkt").centroid
print(centroid.geom_type)      # 'Point'
print(centroid.x, centroid.y)  # 2.0 2.0
```

### Type-Specific Properties

```python
from togo import Point, LineString, Polygon

# Point
point = Point(1, 2)
print(point.x)               # x coordinate
print(point.y)               # y coordinate
print(point.coords)          # [(x, y)] — indexable, len() works
print(point.coords[0])       # (x, y)

# LineString
line = LineString([(0, 0), (1, 1), (2, 2)])
print(line.coords)           # List of (x, y) tuples — indexable, len() works
print(line.coords[0])        # first coordinate
print(line.coords[-1])       # last coordinate
print(line.length)           # Float: length of line (property)
print(line.project(point))   # Float: distance along line to projected point

# Polygon
poly = Polygon([(0, 0), (2, 0), (2, 2), (0, 2), (0, 0)])
print(poly.area)             # Float: area of polygon
print(poly.exterior)         # LinearRing: exterior ring (LineString-compatible)
print(poly.interiors)        # List[Ring]: list of holes
print(poly.centroid)         # Point: center of mass
print(poly.boundary)         # LineString: exterior ring as a line
print(poly_with_hole.boundary)  # MultiLineString: exterior + interior rings

line = LineString([(1, 2), (5, 2), (8, 9)])
endpoints = line.boundary.geoms
print(type(endpoints[0]).__name__)  # Point
print(endpoints[0].x, endpoints[0].y)  # 1.0 2.0
```

For multi-geometries and geometry collections, use `.geoms` to access members as a tuple.
Collection-like geometries also support `len(geom)`, while non-collection
types (for example `Point` and `Polygon`) raise `TypeError`.

For compatibility in mixed-result overlay flows, single-part `Geometry` values
(`Point`, `LineString`, `Polygon`) also expose `.geoms` as a singleton tuple
containing the geometry itself.

```python
from togo import GeometryCollection, Point, Polygon

collection = GeometryCollection([Point(0, 0), Point(1, 1)])
print(len(collection))  # 2

try:
    len(Polygon([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)]))
except TypeError:
    print("Polygon does not define len()")
```

Geometry values are safe in boolean contexts and follow emptiness semantics:

```python
from togo import Geometry

g1 = Geometry("LINESTRING(0 0, 1 1)", fmt="wkt")
g2 = Geometry("GEOMETRYCOLLECTION EMPTY", fmt="wkt")

print(bool(g1))  # True
print(bool(g2))  # False
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
print(poly1.intersects(poly2))  # True  — Polygon.intersects() available
print(poly1.intersects(point))  # True

# Geometry-level predicates also accept wrappers directly
geom1 = from_wkt("POLYGON((0 0, 2 0, 2 2, 0 2, 0 0))")
print(geom1.intersects(poly2))  # True  — no .as_geometry() needed
print(geom1.contains(point))    # True
print(geom1.equals(poly1))      # True
print(geom1.disjoint(poly2))    # False
print(geom1.touches(poly2))     # False
print(geom1.within(poly2))      # False
print(geom1.covers(point))      # True
print(geom1.coveredby(poly2))    # False
```

The same forwarding behavior applies to operations and line-reference helpers,
so wrappers expose methods like `.difference()`, `.union()`, `.equals()`,
`.covers()`, and `.project()` without manual conversion.

## Geometric Operations

### Buffer

All geometry types support the `buffer()` method for creating expanded or shrunk versions of geometries:

```python
from togo import Point, LineString, Polygon, Ring

# Buffer a point - creates a circular polygon
point = Point(0, 0)
circle = point.buffer(10.0, quad_segs=16)
print(circle.geom_type)

# Buffer a line - creates polygon around line
line = LineString([(0, 0), (10, 10)])
zone = line.buffer(2.0, cap_style=1)  # round caps
print(zone.geom_type)

# Buffer a polygon - expand outward or shrink inward
ring = Ring([(0, 0), (10, 0), (10, 10), (0, 10), (0, 0)])
poly = Polygon(ring)

expanded = poly.buffer(2.0)   # Expand outward
shrunk = poly.buffer(-1.0)    # Shrink inward
print(expanded.area)
print(shrunk.area)

# Via Geometry object
geom = Polygon([(0, 0), (10, 0), (10, 10), (0, 10), (0, 0)]).as_geometry()
buffered = geom.buffer(
    distance=2.0,
    quad_segs=16,      # Segments per quadrant
    cap_style=1,        # 1=round, 2=flat, 3=square (for lines)
    join_style=1,       # 1=round, 2=mitre, 3=bevel
    mitre_limit=5.0     # For mitre joins
)
print(buffered.geom_type)
```

For detailed buffer documentation, see [BUFFER_API.md](BUFFER_API.md).

### Simplify

All geometry types support the `simplify()` method for reducing the complexity of geometries using the Douglas-Peucker algorithm:

```python
from togo import Point, LineString, Polygon, Ring

# Simplify a line
line = LineString([(0, 0), (0.1, 0.1), (0.2, 0.2), (1, 1), (2, 2)])
simplified_line = line.simplify(0.5, preserve_topology=True)
print(simplified_line.length)

# Simplify a polygon with topology preservation (default)
poly = Polygon([
    (0, 0), (0.1, 0), (0.2, 0), (1, 0),
    (2, 0), (2, 1), (2, 2), (1, 2), (0, 2), (0, 0)
])
simplified_poly = poly.simplify(0.5)  # preserve_topology=True by default
print(simplified_poly.geom_type)

# Simplify without topology preservation (faster, may create invalid geometries)
rough_poly = poly.simplify(1.0, preserve_topology=False)
print(rough_poly.geom_type)

# Via Geometry object
geom = LineString([(0, 0), (0.1, 0.1), (1, 1), (1.1, 1.1), (2, 2)]).as_geometry()
simplified_geom = geom.simplify(
    tolerance=0.5,          # Max distance from original coordinates
    preserve_topology=True  # Preserve topology (default)
)
print(simplified_geom.geom_type)
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
print(intersection(poly1, poly2).geom_type)

# Line crossing polygon
line = LineString([(0, 1), (3, 1)])
poly = Polygon([(1, 0), (2, 0), (2, 2), (1, 2), (1, 0)])
line_result = line.intersection(poly)
print(line_result.geom_type)  # 'LineString'
print(line_result.length)     # 1.0

# Point in polygon
point = Point(1.5, 1.5)
poly = Polygon([(0, 0), (3, 0), (3, 3), (0, 3), (0, 0)])
point_result = point.intersection(poly)
print(point_result.geom_type)  # 'Point'

# Non-intersecting geometries return empty
poly1 = Polygon([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)])
poly2 = Polygon([(5, 5), (6, 5), (6, 6), (5, 6), (5, 5)])
print(intersection(poly1, poly2).is_empty)   # True

# Via Geometry object
geom1 = Polygon([(0, 0), (2, 0), (2, 2), (0, 2), (0, 0)]).as_geometry()
geom2 = Polygon([(1, 1), (3, 1), (3, 3), (1, 3), (1, 1)]).as_geometry()
print(geom1.intersection(geom2).geom_type)
```

The `intersection()` method:
- Returns the set of points common to both geometries
- Result type depends on input geometries and spatial relationship
- Point-Point: Point (if overlapping) or empty
- Line-Line: Point, LineString, or MultiLineString
- Polygon-Polygon: Point, LineString, Polygon, or MultiPolygon
- Returns empty geometry if inputs don't intersect
- Compatible with Shapely's intersection API

### Union

All geometry types support the `union()` method for computing the geometric union of two geometries:

```python
from togo import Point, LineString, Polygon

# Union of overlapping polygons
poly1 = Polygon([(0, 0), (2, 0), (2, 2), (0, 2), (0, 0)])
poly2 = Polygon([(1, 1), (3, 1), (3, 3), (1, 3), (1, 1)])
result = poly1.union(poly2)
print(result.geom_type)  # 'Polygon' or 'MultiPolygon'

# Union with other wrapper types also works
line = LineString([(0, 1), (3, 1)])
point = Point(1.5, 1.5)
print(poly1.union(line).geom_type)
print(poly1.union(point).geom_type)
```

The `union()` method:
- Returns the geometric union of both inputs
- Is compatible with Shapely-style wrapper objects directly
- Returns empty geometry for invalid Shapely-style inputs such as `None` or unsupported objects on
  wrapper-facing helpers
- Uses explicit empty-geometry fast-paths
- Is currently guarded to 2D overlay inputs

The `union()` method follows the same high-level conventions as `intersection()`. A module-level
`union(g1, g2)` helper is also available and mirrors the Shapely-style API.

### Difference

All geometry types support the `difference()` method for computing the geometric difference of two
geometries (`A - B`):

```python
from togo import Polygon, difference

# Difference of overlapping polygons
poly1 = Polygon([(0, 0), (2, 0), (2, 2), (0, 2), (0, 0)])
poly2 = Polygon([(1, 1), (3, 1), (3, 3), (1, 3), (1, 1)])

result = poly1.difference(poly2)
print(result.geom_type)  # 'Polygon' or 'MultiPolygon'
print(result.area)       # 3.0

# Module-level helper (Shapely-compatible)
result2 = difference(poly1, poly2)
print(result2.area)      # 3.0
```

The `difference()` method:
- Returns points from the left-hand geometry that are not in the right-hand geometry
- Accepts wrapper objects directly (e.g. `Polygon`, `LineString`, `Point`)
- Returns empty geometry for invalid Shapely-style wrapper-facing inputs
- Uses GEOS overlay and follows the same 2D overlay guardrails as `intersection()` / `union()`

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
geom = MultiPoint([(0, 0), (3, 0), (3, 3), (0, 3)])
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

### Safety Notes

Recent hardening work focused on making the highest-risk paths safer to call from Shapely-style
code:

- Overlay operations:
  - `intersection()`
  - `union()`
- Predicates:
  - `contains()`
  - `within()`
  - `covers()`
  - `coveredby()`
  - `touches()`
  - `intersects()`
- Accessors:
  - `geom_type`
  - `bounds`
  - `area`
  - `centroid`
  - `convex_hull`

Behavior to rely on:

- Shapely-style invalid overlay inputs such as `None` or unsupported Python objects return empty
  geometries from wrapper-facing `intersection()` / `union()` helpers.
- Uninitialized base `Geometry()` objects now raise `ValueError` on unsafe accessor, predicate,
  and overlay paths instead of touching null pointers.
- Empty geometries use explicit fast-path handling for overlay operations.
- Binary overlay operations automatically normalize 3D inputs to 2D.

### Error Behavior vs Shapely

ToGo aims to match Shapely-style calling patterns, but it makes the failure mode explicit for the
highest-risk paths:

- wrapper-facing module helpers such as `intersection(g1, g2)`, `union(g1, g2)`, and
  `difference(g1, g2)` return empty
  geometries for invalid or unsupported inputs, mirroring the Shapely-friendly convenience style
- base `Geometry()` instances now fail fast with `ValueError` when you call unsafe accessor,
  predicate, or overlay operations on an uninitialized geometry
- overlay operations on valid geometries continue to raise managed Python exceptions instead of
  crashing the process if the underlying GEOS/TG conversion fails

In practice, this means code that already uses ToGo wrapper objects can keep the same high-level
control flow, while null/uninitialized geometry bugs are surfaced earlier and more clearly.

## Comparison with Shapely

### Similarities

1. **Class names**: `Point`, `LineString`, `Polygon`
2. **Properties**: `geom_type`, `bounds`, `area`, `coords`, `is_empty`, `is_valid`
3. **Serialization**: `wkt`, `wkb`, `__geo_interface__`
4. **Module functions**: `from_wkt()`, `from_geojson()`, `to_wkt()`, `shape()`, `box()`, `unary_union()`, `union()`, `difference()`, `force_2d()`
5. **Predicates**: `contains()`, `intersects()`, `touches()`, `within()`, `covers()`, `coveredby()`, `equals()`
6. **Operations**: `intersection()`, `union()`, `difference()`, `buffer()`, `simplify()`, `project()`
7. **Multi-geometry classes**: `MultiPoint`, `MultiLineString`, `MultiPolygon`, and `GeometryCollection` are real Python classes, `isinstance()` works
8. **Equality**: `geom1 == geom2` works consistently, geometries are hashable

### Differences

1. **Low-level access**: ToGo exposes the TG object model (`Ring`, `Poly`, `Line`) which
   Shapely does not have. Use `.as_geometry()` when you need to pass a wrapper object to
   a function that specifically requires a `Geometry` instance.

2. **GEOS dependency**: Buffer, simplify, centroid, convex_hull, intersection, union, difference, unary_union,
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
# Before (Shapely)
# from shapely.geometry import Point, LineString, Polygon
# from shapely import from_wkt, to_wkt

# After (ToGo)
from togo import Point, LineString, Polygon
from togo import from_wkt, to_wkt
```

## Complete Example

```python
from togo import Point, LineString, Polygon, MultiPolygon, unary_union, from_wkt, to_wkt

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

# Polygon.boundary — LineString (no holes) or MultiLineString (with holes)
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

For a standalone runnable version of the `shortest_line()` examples, see
`examples/shortest_line_demo.py`.

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
| `MultiPoint(points)` | `MultiPoint(points)` | ✅ Real class; `isinstance` works |
| `MultiPolygon(polys)` | `MultiPolygon(polys)` | ✅ Real class; `isinstance` works |
| `MultiLineString(lines)` | `MultiLineString(lines)` | ✅ Real class; `isinstance` works |
| `GeometryCollection(geoms)` | `GeometryCollection(geoms)` | ✅ Real class; `isinstance` works |
| `geom.geom_type` | `geom.geom_type` | ✅ |
| `geom.bounds` | `geom.bounds` | ✅ |
| `geom.area` | `geom.area` | ✅ |
| `geom.length` | `geom.length` | ✅ |
| `geom.centroid` | `geom.centroid` | ✅ via GEOS |
| `geom.convex_hull` | `geom.convex_hull` | ✅ via GEOS |
| `geom.boundary` | `poly.boundary` | ✅ on Polygon/Poly |
| `geom.geoms` | `geom.geoms` | ✅ on multi-geometries and GeometryCollection |
| `len(geom)` (collections only) | `len(geom)` | ✅ on Multi* and GeometryCollection; TypeError otherwise |
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
| `from_wkb()` | `from_wkb()` | ✅ |
| `shape(mapping_or_geo_interface)` | `shape(mapping_or_geo_interface)` | ✅ |
| `box(minx,miny,maxx,maxy)` | `box(minx,miny,maxx,maxy)` | ✅ |
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
| `geom.union(other)` | `geom.union(other)` | ✅ via GEOS; accepts wrappers |
| `geom.difference(other)` | `geom.difference(other)` | ✅ via GEOS; accepts wrappers |
| `line.project(point, normalized=False)` | `line.project(point, normalized=False)` | ✅ via GEOS |
| `geom.project(point, normalized=False)` | `geom.project(point, normalized=False)` | ✅ for LineString/MultiLineString geometries |
| `unary_union(geoms)` | `unary_union(geoms)` | ✅ Module-level; via GEOS |
| `union(g1, g2)` | `union(g1, g2)` | ✅ Module-level; via GEOS |
| `difference(g1, g2)` | `difference(g1, g2)` | ✅ Module-level; via GEOS |
| `force_2d(geom)` | `force_2d(geom)` | ✅ Module-level; drops Z/M ordinates |
| `transform(fn, geom)` | `transform(fn, geom)` | ✅ |
| `nearest_points(g1, g2)` | `nearest_points(g1, g2)` | ✅ via GEOS |
| `shortest_line(g1, g2)` | `shortest_line(g1, g2)` | ✅ via GEOS |
| `convex_hull(geom)` | `convex_hull(geom)` | ✅ via GEOS |
| `intersection(g1, g2)` | `intersection(g1, g2)` | ✅ via GEOS |

## Conclusion

ToGo provides a comprehensive Shapely-compatible API that makes it easy to migrate from Shapely or use it as a drop-in replacement for common geometric operations. Key highlights:

- **Wrapper objects are first-class citizens** — all spatial predicates and operations accept `Point`, `LineString`, `Polygon`, etc. directly without calling `.as_geometry()`.
- **`MultiPoint`, `MultiLineString`, `MultiPolygon`, and `GeometryCollection` are real Python classes** — `isinstance()` checks work as expected.
- **`shape()` and `box()`** are available as module-level Shapely-style helpers.
- **`unary_union(geoms)`**, **`union(g1, g2)`**, **`difference(g1, g2)`**, and **`force_2d(geom)`** are proper module-level functions aligned with Shapely's API.
- **New Polygon conveniences**: `from_bounds()`, improved `boundary`, `intersects()`.
- **`LineString.project()`** for measuring distance-along-line projections.
- **Geometry equality** via `==` and hashability are supported on all geometry types.

All of this sits on top of the ultra-fast TG C library, with advanced operations powered by the bundled `libgeos`.
