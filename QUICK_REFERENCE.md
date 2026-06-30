# Quick Reference: ToGo Shapely-Compatible API

## Installation

```bash
pip install togo
```

## Import Shapely-Compatible Classes

```python
from togo import Point, LineString, LinearRing, Polygon, Ring
from togo import from_wkt, from_geojson, to_wkt, to_geojson, shape, box
from togo import BaseGeometry
```

## Create Geometries

### Point
```python
p = Point(1.0, 2.0)
p.x, p.y           # Access coordinates
p.coords           # [(1.0, 2.0)]
p.bounds           # (1.0, 2.0, 1.0, 2.0)
p.geom_type        # 'Point'
```

### LineString
```python
line = LineString([(0, 0), (1, 1), (2, 2)])
line.coords        # List of coordinates
line.bounds        # (minx, miny, maxx, maxy)
line.length        # Length of line
line.geom_type     # 'LineString'
```

### Polygon
```python
exterior = [(0, 0), (4, 0), (4, 4), (0, 4), (0, 0)]
hole = [(1, 1), (3, 1), (3, 3), (1, 3), (1, 1)]

# Without holes
poly = Polygon(exterior)

# With holes
poly = Polygon(exterior, holes=[hole])

# Properties
poly.area          # Polygon area
poly.bounds        # Bounding box
poly.exterior      # Get exterior LinearRing (also LineString-compatible)
poly.interiors     # List of holes
poly.geom_type     # 'Polygon'
```

## Parse from Different Formats

```python
# From WKT
geom = from_wkt("POINT (1 2)")
geom = from_wkt("LINESTRING (0 0, 1 1, 2 2)")
geom = from_wkt("POLYGON ((0 0, 4 0, 4 4, 0 4, 0 0))")

# From GeoJSON
geom = from_geojson('{"type":"Point","coordinates":[1,2]}')

# From WKB
geom = from_wkb(wkb_bytes)

# Multi geometries are materialized as concrete classes when determinable
mp = from_geojson('{"type":"MultiPolygon","coordinates":[[[[0,0],[1,0],[1,1],[0,1],[0,0]]]]}')
type(mp).__name__  # 'MultiPolygon'
```

## Convert to Different Formats

```python
# To WKT
wkt = point.wkt
wkt = line.wkt
wkt = poly.wkt
wkt = to_wkt(geom)

# To GeoJSON
geojson_str = to_geojson(point)
geojson_str = to_geojson(line)
geojson_str = to_geojson(poly)

# To WKB
wkb = point.wkb
wkb = to_wkb(geom)

# To GeoJSON dict
geo_dict = point.__geo_interface__
```

## Spatial Predicates

```python
# Create test geometries
poly = Polygon([(0, 0), (10, 0), (10, 10), (0, 10), (0, 0)])
point = Point(5, 5)

# Predicates (wrapper objects accepted directly)
poly.contains(point)                 # Point in polygon?
poly.intersects(poly)                # Overlap?
poly.equals(poly)                    # Same geometry?
poly.disjoint(poly)                  # No overlap?
point.within(poly)                   # Inside?
poly.covers(point)                   # Covers?
point.coveredby(poly)                # Covered by?
poly.touches(poly)                   # Touch?

# Geometry-level predicates also accept wrappers directly
poly_geom = poly.as_geometry()
poly_geom.contains(point)
```

## LineString Projection

```python
line = LineString([(0, 0), (10, 0)])
p = Point(5, 3)

line.project(p)                       # 5.0 (distance along line)
line.project(p, normalized=True)      # 0.5 (fraction of line length)

# Geometry values that are line-like also support project()
line_geom = line.as_geometry()
line_geom.project(p)                  # 5.0
line_geom.project(p, normalized=True) # 0.5
```

## Multi-Geometries

```python
from togo import MultiPoint, MultiLineString, MultiPolygon, GeometryCollection

# MultiPoint
points = [Point(0, 0), Point(1, 1), Point(2, 2)]
multi = MultiPoint(points)

# MultiLineString
lines = [LineString([(0, 0), (1, 1)]), LineString([(2, 2), (3, 3)])]
multi = MultiLineString(lines)

# MultiPolygon
polys = [Polygon([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)]),
         Polygon([(2, 2), (3, 2), (3, 3), (2, 3), (2, 2)])]
multi = MultiPolygon(polys)

# GeometryCollection
geoms = [Point(0, 0), LineString([(1, 1), (2, 2)])]
collection = GeometryCollection(geoms)

# Access children as a tuple
parts = collection.geoms
len(parts)

# Collection geometries implement len() directly
len(collection)   # 2
len(multi)        # size of the corresponding Multi*

# Single-part Geometry values also expose singleton .geoms for mixed-result flows
single = LineString([(0, 0), (2, 0)]).intersection(
    Polygon([(1, -1), (3, -1), (3, 1), (1, 1), (1, -1)])
)
len(single.geoms)  # 1
```

## Geometry Truthiness

```python
from togo import Geometry

bool(Geometry("LINESTRING(0 0, 1 1)", fmt="wkt"))       # True
bool(Geometry("GEOMETRYCOLLECTION EMPTY", fmt="wkt"))   # False
```

## shape() and box()

```python
geom = shape({"type": "Point", "coordinates": [1, 2]})
type(geom).__name__  # 'Point'

poly = shape({"type": "Polygon", "coordinates": [[(0, 0), (1, 0), (1, 1), (0, 0)]]})
type(poly).__name__  # 'Polygon'

rect = box(0, 0, 10, 5)
```

## Common Properties

All geometries support:

```python
geom.geom_type     # String: 'Point', 'LineString', 'Polygon', etc.
geom.bounds        # Tuple: (minx, miny, maxx, maxy)
geom.is_empty      # Boolean: True if geometry is empty
geom.is_valid      # Boolean: True if geometry is valid
geom.wkt           # String: WKT representation
geom.wkb           # Bytes: WKB representation
geom.__geo_interface__  # Dict: GeoJSON-like

# Point Geometry results expose x/y (e.g., centroid outputs)
center = Polygon([(0, 0), (4, 0), (4, 4), (0, 4), (0, 0)]).centroid
center.x, center.y

# Line boundary endpoints are exposed as Point-like values
endpoints = LineString([(1, 2), (5, 2), (8, 9)]).boundary.geoms
endpoints[0].x, endpoints[0].y
```

## Geometric Operations

```python
from togo import convex_hull, difference, nearest_points, shortest_line

# Centroid - center of mass
poly = Polygon([(0, 0), (4, 0), (4, 4), (0, 4), (0, 0)])
center = poly.centroid
print(center.to_wkt())  # 'POINT(2 2)'

# Convex Hull - smallest convex geometry enclosing all points
from togo import MultiPoint
points = MultiPoint([(0, 0), (1, 1), (0, 2), (2, 2), (3, 1), (1, 0)])
hull = points.convex_hull  # Property access
# Or: hull = convex_hull(points)  # Module-level function

# Buffer - expand/shrink geometry
line = LineString([(0, 0), (10, 10)])
buffered = line.buffer(2.0)

# Set operations
a = Polygon([(0, 0), (2, 0), (2, 2), (0, 2), (0, 0)])
b = Polygon([(1, 1), (3, 1), (3, 3), (1, 3), (1, 1)])
overlap = a.intersection(b)
merged = a.union(b)
cutout = a.difference(b)

# Module-level equivalent
cutout2 = difference(a, b)

# 3D inputs are accepted for topology operations and normalized to 2D
zpoly = from_wkt("POLYGON Z ((0 0 5,2 0 5,2 2 5,0 2 5,0 0 5))")
zpoly2 = from_wkt("POLYGON Z ((1 1 9,3 1 9,3 3 9,1 3 9,1 1 9))")
zmerge = zpoly.union(zpoly2)
zmerge.has_z  # False

# Simplify - reduce complexity
complex_line = LineString([(0, 0), (0.1, 0.1), (1, 1), (2, 2)])
simple = complex_line.simplify(0.5)

# Nearest points between geometries
p1 = Point(0, 0)
p2 = Point(10, 10)
pt1, pt2 = nearest_points(p1, p2)

# Shortest line connecting geometries
line = shortest_line(p1, p2)
```

## Migration from Shapely

### Before (Shapely)
```python
from shapely.geometry import Point, LineString, Polygon
from shapely import from_wkt, to_wkt

point = Point(1, 2)
wkt = point.wkt
```

### After (ToGo)
```python
from togo import Point, LineString, Polygon
from togo import from_wkt, to_wkt

point = Point(1, 2)
wkt = point.wkt
```

## Error Handling

```python
from togo import from_wkt, from_geojson

# Invalid WKT raises ValueError
try:
    geom = from_wkt("INVALID")
except ValueError as e:
    print(f"Invalid WKT: {e}")

# Invalid GeoJSON raises ValueError
try:
    geom = from_geojson('{"invalid": "json"}')
except ValueError as e:
    print(f"Invalid GeoJSON: {e}")
```

## Performance Tips

1. **Reuse geometries** - Parse once, use multiple times
2. **Use predicates** - Fast spatial operations
3. **Bounds checking** - Quick preliminary filtering
4. **Index for large datasets** - Use TGIndex for polygon indexing

## Backward Compatibility

Old ToGo API still works:
```python
from togo import Geometry, Line, Ring, Poly

# Old API still works
geom = Geometry(wkt, fmt="wkt")
line = Line([(0, 0), (1, 1)])
poly = Poly(Ring([...]))
```

## Getting Help

- **Documentation:** See `SHAPELY_API.md`
- **Examples:** See `examples/shapely_api_demo.py`
- **Tests:** See `tests/test_shapely_api.py`
- **Implementation:** See `IMPLEMENTATION_SUMMARY.md`

## Key Differences from Shapely

| Feature | Shapely | ToGo |
|---------|---------|------|
| Predicates | Work on shapes directly | Work on wrapper objects directly |
| Multi-geometries | Class-based | Class-based (`isinstance` works) |

---

**Status:** Production Ready ✅
**Last Updated:** June 8, 2026
