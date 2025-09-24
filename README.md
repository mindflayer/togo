# ToGo
Python bindings for [TG](https://github.com/tidwall/tg)
(Geometry library for C - Fast point-in-polygon)

ToGo is a high-performance Python library for computational geometry, providing a Cython wrapper around the above-mentioned C library.

The main goal is to offer a Pythonic, object-oriented, fast and memory-efficient library for geometric operations, including spatial predicates, format conversions, and spatial indexing.

While ToGo's API interfaces are still a work in progress, the underling C library is stable and well-tested.

## Installation

```bash
pip install togo
```

## Features

- Fast and efficient geometric operations
- Support for standard geometry types: Point, Line, Ring, Polygon, and their multi-variants
- Geometric predicates: contains, intersects, covers, touches, etc.
- Format conversion between WKT, GeoJSON, WKB, and HEX
- Spatial indexing for accelerated queries
- Memory-efficient C implementation with Python-friendly interface

## Basic Usage

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

### Point, Line, Ring, Poly

Building blocks for constructing geometries:

```python
# Create a point
p = Point(1.0, 2.0)

# Create a line
line = Line([(0,0), (1,1), (2,2)])

# Create a ring (closed line)
ring = Ring([(0,0), (10,0), (10,10), (0,10), (0,0)])

# Create a polygon with holes
exterior = Ring([(0,0), (10,0), (10,10), (0,10), (0,0)])
hole = Ring([(2,2), (8,2), (8,8), (2,8), (2,2)])
poly = Poly(exterior, [hole])
```

### MultiGeometries

Creating collections of geometries:

```python
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

### Segment

Represents a line segment between two points:

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

## Polygon Indexing

Togo supports different polygon indexing strategies for optimized spatial operations:

```python
from togo import TGIndex, set_polygon_indexing_mode

# Set the indexing mode
set_polygon_indexing_mode(TGIndex.NATURAL)  # or NONE, YSTRIPES
```

## Performance Considerations

- Togo is optimized for speed and memory efficiency
- For large datasets, proper indexing can significantly improve performance
- Creating geometries with the appropriate format avoids unnecessary conversions

Soon there will be a full API documentation, for now please refer to the test suite for more usage examples.
