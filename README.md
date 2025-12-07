# ToGo
Python bindings for [TG](https://github.com/tidwall/tg)
(Geometry library for C - Fast point-in-polygon)

ToGo is a high-performance Python library for computational geometry, providing a Cython wrapper around the above-mentioned C library.

The main goal is to offer a Pythonic, object-oriented, fast and memory-efficient library for geometric operations, including spatial predicates, format conversions, and spatial indexing.

**New:** ToGo now provides a **Shapely-compatible API**! See [SHAPELY_API.md](SHAPELY_API.md) for details.

## Installation

```bash
pip install togo
```

## Features

- Fast and efficient geometric operations
- Support for standard geometry types: Point, Line, Ring, Polygon, and their multi-variants
- **Shapely-compatible API** with familiar class names and properties
- Geometric predicates: contains, intersects, covers, touches, etc.
- Format conversion between WKT, GeoJSON, WKB, and HEX
- Spatial indexing for accelerated queries
- Memory-efficient C implementation with Python-friendly interface

## Basic Usage

### Shapely-Compatible API

```python
from togo import Point, LineString, Polygon, Ring
from togo import from_wkt, from_geojson

# Create geometries using familiar Shapely-like syntax
point = Point(1.0, 2.0)
line = LineString([(0, 0), (1, 1), (2, 2)])
poly = Polygon(Ring([(0, 0), (4, 0), (4, 4), (0, 4), (0, 0)]))

# Access Shapely-compatible properties
print(point.geom_type)  # 'Point'
print(point.bounds)     # (1.0, 2.0, 1.0, 2.0)
print(line.length)      # 2.828...
print(poly.area)        # 16.0

# Parse from WKT/GeoJSON
geom = from_wkt("POINT (1 2)")
geom2 = from_geojson('{"type":"Point","coordinates":[3,4]}')

# Spatial predicates
poly_geom = poly.as_geometry()
point_geom = point.as_geometry()
if poly_geom.contains(point_geom):
    print("Polygon contains point!")
```

### Original ToGo API

```python
from togo import Geometry, Point, Ring, Poly

# Create a geometry from GeoJSON
geom = Geometry('{"type":"Point","coordinates":[1.0,2.0]}')

# Create a point
point = Point(1.0, 2.0)

# Create a polygon
ring = Ring([(0,0), (10,0), (10,10), (0,10), (0,0)])
polygon = Poly(ring)

# Convert to various formats
wkt = polygon.as_geometry().to_wkt()
geojson = polygon.as_geometry().to_geojson()

# Perform spatial predicates
point_geom = point.as_geometry()
contains = polygon.as_geometry().contains(point_geom)
```

## Core Classes

### Geometry

The base class that wraps tg_geom structures and provides core operations:

```python
# Create from various formats
g1 = Geometry('POINT(1 2)', fmt='wkt')
g2 = Geometry('{"type":"Point","coordinates":[1,2]}', fmt='geojson')

# Geometric predicates
g1.intersects(g2)
g1.contains(g2)
g1.within(g2)

# Format conversion
g1.to_wkt()
g1.to_geojson()

# Access sub-geometries by index (e.g., for GeometryCollection, MultiPoint, etc.)
gc = Geometry('GEOMETRYCOLLECTION(POINT(1 2),POINT(3 4))', fmt='wkt')
first = gc[0]  # Bound to TG function call tg_geom_geometry_at(idx)
second = gc[1]
print(first.type_string())  # 'Point'
```

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
print(f"Number of points: {line.num_points()}")

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
print(f"Area: {ring.area()}")
print(f"Perimeter: {ring.perimeter()}")

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
ext_ring = poly.exterior()
print(f"Exterior has {ext_ring.num_points()} points")

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

Creating collections of geometries:

```python
from togo import Geometry, Point, Line, Poly, Ring

# Create a MultiPoint
multi_point = Geometry.from_multipoint([(0,0), (1,1), Point(2,2)])

# Create a MultiLineString
multi_line = Geometry.from_multilinestring([
    [(0,0), (1,1)],
    Line([(2,2), (3,3)])
])

# Create a MultiPolygon
poly1 = Poly(Ring([(0,0), (1,0), (1,1), (0,1), (0,0)]))
poly2 = Poly(Ring([(2,2), (3,2), (3,3), (2,3), (2,2)]))
multi_poly = Geometry.from_multipolygon([poly1, poly2])
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

The `unary_union` method demonstrates this integration. It combines multiple geometries into a single geometry using GEOS's topological union, with all conversions handled automatically:

```python
from togo import Geometry, Point, Poly, Ring

# Create several polygons
poly1 = Poly(Ring([(0,0), (2,0), (2,2), (0,2), (0,0)]))
poly2 = Poly(Ring([(1,1), (3,1), (3,3), (1,3), (1,1)]))

# Perform unary union (requires tgx and libgeos)
union = Geometry.unary_union([poly1, poly2])

# The result is a single geometry representing the union of the input polygons
print(union.to_wkt())
```

This operation uses `tgx` to convert `TG` geometries to `GEOS`, applies the union in `libgeos`, and converts the result back to `TG` format for further use in `ToGo`.

### Example: Buffer Operations (GEOS integration)

The `buffer()` method creates geometrical buffers (expanded or shrunk versions of geometries) using GEOS:

```python
from togo import Point, LineString, Polygon, Ring, Geometry

# Buffer a point to create a circular zone
point = Point(0, 0)
circular_zone = point.buffer(10.0, resolution=16)
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
    resolution=16,           # Segments per quadrant (higher = smoother)
    cap_style=1,            # 1=round, 2=flat, 3=square
    join_style=1,           # 1=round, 2=mitre, 3=bevel
    mitre_limit=5.0         # Mitre ratio limit
)
```

Like `unary_union`, buffer operations automatically handle TG ↔ GEOS conversions. For comprehensive buffer documentation, see [BUFFER_API.md](BUFFER_API.md).

## Performance Considerations

- Togo is optimized for speed and memory efficiency
- For large datasets, proper indexing can significantly improve performance
- Creating geometries with the appropriate format avoids unnecessary conversions
- Buffer operations support resolution parameter to balance quality vs. performance

Soon there will be a full API documentation, for now please refer to the test suite for more usage examples.
