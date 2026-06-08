<img src="https://github.com/mindflayer/togo/blob/main/togo.png?raw=true" width="256px" alt="ToGo logo">

Python bindings for [TG](https://github.com/tidwall/tg)
(Geometry library for C - Fast point-in-polygon)

ToGo is a high-performance Python library for computational geometry, providing a Cython wrapper around the above-mentioned C library.

Note on pronunciation: "ToGo" is pronounced like the country Togo ("TOH-go"), not like "to go".

The main goal is to offer a Pythonic, object-oriented, fast and memory-efficient library for geometric operations, including spatial predicates, format conversions, and spatial indexing. ToGo's API is flexible and allows you to reason in either TG concepts (if you're familiar with the TG library) or Shapely conventions (the de facto standard for geospatial work in Python)—whichever fits your workflow best.

See [SHAPELY_API.md](SHAPELY_API.md) for more details on Shapely compatibility.
See [CHANGELOG.md](CHANGELOG.md) for version-by-version release notes.


## Installation

```bash
pip install togo
```

## Features

- Fast and efficient geometric operations
- Support for standard geometry types: Point, Line, Ring, Polygon, and their multi-variants
- Flexible API supporting both TG and Shapely conventions
- Geometric predicates: contains, intersects, covers, touches, etc. — accept any wrapper type directly (no manual `.as_geometry()` conversion needed)
- Format conversion between WKT, GeoJSON, WKB, and HEX
- Spatial indexing for accelerated queries
- Memory-efficient C implementation with Python-friendly interface
- Advanced operations via libgeos integration (buffer, unary union, simplify, centroid, convex_hull, etc.)
- Distance and proximity operations (nearest_points, shortest_line, project)
- `MultiPolygon` and `MultiLineString` are real Python classes — `isinstance()` checks work correctly
- Geometry equality via `==` operator consistent with Shapely semantics

## Basic Usage

ToGo's API supports multiple styles of interaction. You can use Shapely-like conventions for familiarity, TG-like conventions if you're already familiar with that library, or mix both as needed.

### Creating Geometries

```python
from togo import Point, LineString, Polygon, Ring, Poly, Geometry

# Shapely-like syntax
point = Point(1.0, 2.0)
line = LineString([(0, 0), (1, 1), (2, 2)])
poly = Polygon([(0, 0), (4, 0), (4, 4), (0, 4), (0, 0)])

# TG-like syntax with Ring and Poly
ring = Ring([(0,0), (10,0), (10,10), (0,10), (0,0)])
polygon = Poly(ring)

# Direct Geometry creation from formats
geom = Geometry("POINT(1 2)", fmt='wkt')
geom2 = Geometry('{"type":"Point","coordinates":[1,2]}', fmt='geojson')
```

### Working with Geometries

```python
from togo import Point, Polygon

# Access properties (works with both API styles)
point = Point(1.0, 2.0)
print(point.geom_type)     # 'Point'
print(point.bounds)        # (1.0, 2.0, 1.0, 2.0)
print(point.coords[0])     # (1.0, 2.0)  — indexable coordinate sequence

poly = Polygon([(0, 0), (4, 0), (4, 4), (0, 4), (0, 0)])
print(poly.area)           # 16.0
print(poly.length)         # 16.0

# Convert between formats
print(point.to_wkt())      # 'POINT (1 2)'
print(point.to_geojson())  # '{"type":"Point","coordinates":[1.0,2.0]}'

# Spatial predicates — wrapper objects are accepted directly, no .as_geometry() needed
if poly.contains(point):
    print("Polygon contains point!")

if poly.intersects(Polygon([(3, 3), (5, 3), (5, 5), (3, 5), (3, 3)])):
    print("Polygons intersect!")

# Polygon.boundary — exterior ring as a LineString
boundary = poly.boundary
print(boundary.length)     # perimeter of polygon

# Polygon.from_bounds — create a rectangle from a bounding box
bbox = Polygon.from_bounds(0, 0, 10, 5)
print(bbox.area)           # 50.0

# Centroid (Shapely-compatible)
centroid = poly.centroid  # Returns a Point geometry
print(centroid.to_wkt())  # e.g., 'POINT (2 2)'

# Convex hull (Shapely-compatible)
from togo import convex_hull
concave_poly = Polygon([(0, 0), (2, 0), (2, 2), (1, 1), (0, 2), (0, 0)])
hull = convex_hull(concave_poly)
print(hull.to_wkt())  # 'POLYGON((0 0,2 0,2 2,0 2,0 0))'

# Binary union (Shapely-compatible)
other = Polygon([(3, 3), (5, 3), (5, 5), (3, 5), (3, 3)])
merged = poly.union(other)
print(merged.geom_type)
```

You can also call the module-level helper with `from togo import union` and then
`union(poly, other)`.


## Core Classes

### Geometry

The base class that wraps tg_geom structures and provides core operations:

- Create geometries directly from WKT, GeoJSON, HEX, and other supported serialized formats.
- Use common predicates such as `intersects()`, `contains()`, and `within()` directly on
  `Geometry` instances.
- Convert geometries back to WKT/GeoJSON/WKB using `to_wkt()`, `to_geojson()`, and `to_wkb()`.
- Index collection-like geometries such as `GeometryCollection`, `MultiLineString`, and
  `MultiPolygon` using `geom[idx]`.
- High-risk accessor, predicate, and overlay paths now fail with managed exceptions when used on
  uninitialized base `Geometry()` objects.

### Point

```python
from togo import Point

# Create a point
p = Point(1.0, 2.0)

# Access coordinates
print(f"X: {p.x}, Y: {p.y}")

# Get as a tuple
print(p.as_tuple())

# Convert to a Geometry object
geom = p.as_geometry()
print(geom.type_string())
```

### Segment

```python
from togo import Segment, Point

# Create a segment from two points (or tuples)
seg = Segment(Point(0, 0), Point(1, 1))
# Or using tuples
tuple_seg = Segment((0, 0), (1, 1))

# Access endpoints
print(seg.a)  # Point(0, 0)
print(seg.b)  # Point(1, 1)

# Get the bounding rectangle
rect = seg.rect()
print(rect)  # ((0.0, 0.0), (1.0, 1.0))

# Check intersection with another segment
other = Segment((1, 1), (2, 2))
print(seg.intersects(other))  # True or False
```

### Line

```python
from togo import Line

# Create a line from a list of tuples
line = Line([(0,0), (1,1), (2,0)])

# Get number of points
print(f"Number of points: {line.num_points}")

# Get all points as a list of tuples
print(f"Points: {line.points()}")

# Get the length of the line
print(f"Length: {line.length}")

# Get the bounding box
print(f"Bounding box: {line.rect()}")

# Get a point by index
print(f"First point: {line[0].as_tuple()}")
```

### Ring

```python
from togo import Ring

# Create a ring (must be closed)
ring = Ring([(0,0), (10,0), (10,10), (0,10), (0,0)])

# Get area and perimeter
print(f"Area: {ring.area}")
print(f"Perimeter: {ring.length}")

# Check if it's convex or clockwise
print(f"Is convex: {ring.is_convex()}")
print(f"Is clockwise: {ring.is_clockwise()}")

# Get bounding box
min_pt, max_pt = ring.rect().min, ring.rect().max
print(f"Bounding box: {min_pt.as_tuple()}, {max_pt.as_tuple()}")
```

### Poly

```python
from togo import Poly, Ring, Point

# Create a polygon with one exterior ring and one interior hole
exterior = Ring([(0,0), (10,0), (10,10), (0,10), (0,0)])
hole1 = Ring([(1,1), (2,1), (2,2), (1,2), (1,1)])
poly = Poly(exterior, holes=[hole1])

# Get the exterior ring
ext_ring = poly.exterior
print(f"Exterior has {ext_ring.num_points} points")

# Get number of holes
print(f"Number of holes: {poly.num_holes()}")

# Get a hole by index
h = poly.hole(0)
print(f"Hole area: {h.area()}")

# A polygon is a geometry, so you can use geometry methods
geom = poly.as_geometry()
print(f"Contains point (5,5): {geom.contains(Point(5,5).as_geometry())}")
# Point is inside the hole, so it is not contained by the polygon
print(f"Contains point (1.5,1.5): {geom.contains(Point(1.5,1.5).as_geometry())}")
```

### MultiGeometries

`MultiPolygon` and `MultiLineString` are real Python classes, so `isinstance()` checks work correctly:

```python
from togo import MultiPoint, MultiLineString, MultiPolygon, Poly, Ring, Geometry

# MultiPolygon — real class, supports isinstance
poly1 = Poly(Ring([(0,0), (1,0), (1,1), (0,1), (0,0)]))
poly2 = Poly(Ring([(2,2), (3,2), (3,3), (2,3), (2,2)]))
multi_poly = MultiPolygon([poly1, poly2])
print(isinstance(multi_poly, MultiPolygon))  # True
print(isinstance(multi_poly, Geometry))      # True

# MultiLineString — real class, supports isinstance
multi_line = MultiLineString([[(0,0), (1,1)], [(2,2), (3,3)]])
print(isinstance(multi_line, MultiLineString))  # True

# MultiPoint — factory (returns Geometry)
multi_point = MultiPoint([(0,0), (1,1), (2,2)])

# Low-level factory methods still available on Geometry
multi_poly2 = Geometry.from_multipolygon([poly1, poly2])
```

### LineString.project()

`project()` returns the distance along a line to the nearest projected point — equivalent to Shapely's `project()`. Use `normalized=True` to get a fraction of total line length:

```python
from togo import LineString, Point

line = LineString([(0, 0), (10, 0)])

# Distance to the start: 0.0
print(line.project(Point(0, 0).as_geometry()))   # 0.0

# Distance to the midpoint: 5.0
print(line.project(Point(5, 0).as_geometry()))   # 5.0

# Point above the midpoint still projects to 5.0
print(line.project(Point(5, 3).as_geometry()))   # 5.0

# Normalized distance in [0.0, 1.0]
print(line.project(Point(5, 0).as_geometry(), normalized=True))   # 0.5
print(line.project(Point(10, 0).as_geometry(), normalized=True))  # 1.0
```

## Polygon Indexing

Togo supports different polygon indexing strategies for optimized spatial operations:

```python
from togo import TGIndex, set_polygon_indexing_mode

# Set the indexing mode
set_polygon_indexing_mode(TGIndex.NATURAL)  # or NONE, YSTRIPES
```

## Integration with tgx and libgeos

Togo integrates with the [tgx](https://github.com/tidwall/tgx) extension and [libgeos](https://libgeos.org/) to provide advanced geometry operations, such as topological unions and conversions between TG and GEOS geometry formats. This allows you to leverage the speed of TG for basic operations and the flexibility of GEOS for more complex tasks.

### Example: Unary Union (GEOS integration)

`unary_union` is a module-level function (Shapely-compatible) that merges multiple geometries into one using GEOS topological union. It accepts any wrapper type directly — no `.as_geometry()` conversion required:

```python
from togo import Polygon, unary_union

# Create several polygons using the Shapely-compatible constructor
poly1 = Polygon([(0,0), (2,0), (2,2), (0,2), (0,0)])
poly2 = Polygon([(1,1), (3,1), (3,3), (1,3), (1,1)])

# Module-level unary_union — accepts Polygon wrapper objects directly
union = unary_union([poly1, poly2])

# The result is a single geometry representing the union
print(union.geom_type)   # 'Polygon'
print(union.to_wkt())

# Works with mixed types (Poly, Polygon, Geometry, etc.)
from togo import Poly, Ring, Geometry
poly3 = Poly(Ring([(5,0), (7,0), (7,2), (5,2), (5,0)]))
union2 = unary_union([poly1, poly3])
print(union2.geom_type)  # 'MultiPolygon' (non-overlapping)
```

This operation uses `tgx` to convert `TG` geometries to `GEOS`, applies the union in `libgeos`, and converts the result back to `TG` format for further use in `ToGo`.

### Example: Buffer Operations (GEOS integration)

The `buffer()` method creates geometrical buffers (expanded or shrunk versions of geometries) using GEOS:

```python
from togo import Point, LineString, Polygon, Ring, Geometry

# Buffer a point to create a circular zone
point = Point(0, 0)
circular_zone = point.buffer(10.0, quad_segs=16)
print(f"Point buffer: {circular_zone.geom_type}")  # Polygon

# Buffer a line to create a corridor around it
line = LineString([(0, 0), (10, 10)])
corridor = line.buffer(2.0, cap_style=1)  # round ends
print(f"Line buffer: {corridor.geom_type}")  # Polygon

# Buffer a polygon to expand or shrink it
exterior = Ring([(0, 0), (10, 0), (10, 10), (0, 10), (0, 0)])
poly = Polygon(exterior)

expanded = poly.buffer(2.0)    # Expand outward by 2 units
shrunk = poly.buffer(-1.0)     # Shrink inward by 1 unit

# Via Geometry object with advanced parameters
geom = Geometry("POLYGON((0 0, 20 0, 20 20, 0 20, 0 0))")
buffered = geom.buffer(
    distance=3.0,
    quad_segs=16,           # Segments per quadrant (higher = smoother)
    cap_style=1,            # 1=round, 2=flat, 3=square
    join_style=1,           # 1=round, 2=mitre, 3=bevel
    mitre_limit=5.0         # Mitre ratio limit
)
```

Like `unary_union`, buffer operations automatically handle TG ↔ GEOS conversions. For comprehensive buffer documentation, see [BUFFER_API.md](BUFFER_API.md).

### Example: Distance and Proximity Operations (GEOS integration)

The `nearest_points()` and `shortest_line()` functions find the closest points between geometries:

```python
from togo import Point, LineString, Polygon, Ring, nearest_points, shortest_line, from_wkt

# Find nearest points between geometries (module-level function)
point = Point(0, 0)
line = LineString([(10, 0), (10, 10)])
pt1, pt2 = nearest_points(point, line)
print(f"Nearest on point: ({pt1.x}, {pt1.y})")  # (0.0, 0.0)
print(f"Nearest on line: ({pt2.x}, {pt2.y})")   # (10.0, 0.0)

# Get the connecting line (Shapely v2 API - module-level function)
shortest = shortest_line(point, line)
print(f"Distance: {shortest.length}")  # 10.0
print(f"Connecting line: {shortest.coords}")  # [(0.0, 0.0), (10.0, 0.0)]

# Method style also works
shortest = point.shortest_line(line)
pt1, pt2 = point.nearest_points(line)

# Measure gap between polygons
poly1 = Polygon(Ring([(0, 0), (5, 0), (5, 5), (0, 5), (0, 0)]))
poly2 = Polygon(Ring([(10, 0), (15, 0), (15, 5), (10, 5), (10, 0)]))
gap_line = shortest_line(poly1, poly2)
print(f"Gap between polygons: {gap_line.length}")  # 5.0

# Practical use case: Check if features are within distance
def within_distance(geom1, geom2, max_dist):
    return shortest_line(geom1, geom2).length <= max_dist

building1 = Polygon(Ring([(0, 0), (10, 0), (10, 10), (0, 10), (0, 0)]))
building2 = Polygon(Ring([(20, 0), (30, 0), (30, 10), (20, 10), (20, 0)]))

if within_distance(building1, building2, 15):
    print("Buildings meet separation requirement")

# Works with WKT geometries
g1 = from_wkt("POINT(0 0)")
g2 = from_wkt("LINESTRING(5 5, 10 10)")
connecting = shortest_line(g1, g2)
print(f"Distance: {connecting.length:.2f}")
```

For more examples, see the shortest-line tests and `examples/shortest_line_demo.py`.

## Performance Considerations

- Togo is optimized for speed and memory efficiency
- For large datasets, proper indexing can significantly improve performance
- Creating geometries with the appropriate format avoids unnecessary conversions
- Buffer operations support quad_segs parameter to balance quality vs. performance

Soon there will be a full API documentation, for now please refer to the test suite for more usage examples.
