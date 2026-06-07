# Quick Reference: ToGo Shapely-Compatible API

## v0.4.1 Notes (vs v0.4.0)

- `LineString.project(..., normalized=True)` is supported.
- `Geometry.exterior`, `Geometry.interiors`, and `Geometry.boundary` have safer lifetime handling.
- Mixed-input `unary_union()` coercion is safer (coerced objects are kept alive during union).

## Installation

```bash
pip install togo
```

## Import Shapely-Compatible Classes

```python
from togo import Point, LineString, Polygon, Ring
from togo import from_wkt, from_geojson, to_wkt, to_geojson
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
poly.exterior    # Get exterior Ring
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
```

## Geometric Operations

```python
from togo import convex_hull, nearest_points, shortest_line

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
| Multi-geometries | Auto-created | Explicit constructors |

---

**Status:** Production Ready ✅
**Last Updated:** December 6, 2025
