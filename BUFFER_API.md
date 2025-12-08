# Buffer Method - Shapely-Compatible API

The `buffer()` method has been added to all geometry types in Togo for Shapely compatibility. This method uses GEOS (Geometry Engine - Open Source) to compute geometrical buffers.

## Overview

The buffer operation creates a new geometry that is the input geometry expanded or shrunk by a specified distance. This is useful for:
- Creating safety zones around geometries
- Simplifying complex geometries
- Detecting nearby features
- Expanding/shrinking areas

## Available on All Geometry Types

- `Geometry.buffer()`
- `Point.buffer()`
- `LineString.buffer()` (Line class)
- `Polygon.buffer()` (Poly class)
- `Ring.buffer()`

## Method Signature

```python
def buffer(self, distance: float, quad_segs: int = 16,
           cap_style: int = 1, join_style: int = 1,
           mitre_limit: float = 5.0) -> Geometry
```

## Parameters

### `distance: float` (required)
The buffer distance in the geometry's coordinate units.
- **Positive values**: Expand geometry outward
- **Negative values**: Shrink geometry inward (for Polygons only; may produce empty result if too large)
- **Zero**: Returns the original geometry unchanged

### `quad_segs: int` (optional, default: 16)
Number of segments per quadrant of a circle. Higher values create smoother buffers but take more computation.
- Typical values: 4, 8, 16, 32
- Higher values = smoother curves
- Lower values = faster computation

### `cap_style: int` (optional, default: 1)
End cap style for buffer endings. Only affects LineString buffers.
- `1` (round): Rounded ends (default)
- `2` (flat): Flat/square ends
- `3` (square): Square ends

### `join_style: int` (optional, default: 1)
Join style for buffer corners. Affects how corners are rendered.
- `1` (round): Rounded joins (default)
- `2` (mitre): Angled joins
- `3` (bevel): Beveled joins

### `mitre_limit: float` (optional, default: 5.0)
Mitre ratio limit for mitre joins. Only used when `join_style=2`.
- Controls how sharp a corner must be before it's beveled
- Values < 1.0 effectively disable mitre joins

## Return Value

Returns a new `Geometry` object representing the buffered shape. The result is always a Polygon (or an empty geometry if the buffer operation produces nothing).

## Examples

### Buffer a Point

```python
from togo import Point, Geometry

# Create a circular buffer around a point
p = Point(0, 0)
circular_buffer = p.buffer(10.0, quad_segs=16)
# Result: Polygon (circle with radius 10)

# Via Geometry interface
geom = Geometry("POINT(5 5)")
buffered = geom.buffer(2.5)
# Result: Polygon (circle with radius 2.5)
```

### Buffer a LineString

```python
from togo import LineString, Geometry

# Create a buffer zone around a line
line = LineString([(0, 0), (10, 0), (15, 5)])
buffer_zone = line.buffer(5.0, cap_style=1)  # Round ends
# Result: Polygon with rounded ends

# Different end cap styles
square_ends = line.buffer(5.0, cap_style=3)  # Square ends
flat_ends = line.buffer(5.0, cap_style=2)    # Flat ends

# Via Geometry
geom = Geometry("LINESTRING(0 0, 10 10)")
buffered = geom.buffer(1.0, quad_segs=8)
```

### Buffer a Polygon

```python
from togo import Polygon

# Expand a polygon
exterior = [(0, 0), (10, 0), (10, 10), (0, 10), (0, 0)]
poly = Polygon(exterior)

# Expand outward by 2 units
expanded = poly.buffer(2.0)

# Shrink inward by 1 unit
shrunk = poly.buffer(-1.0)

# Polygon with holes
hole = [(2, 2), (4, 2), (4, 4), (2, 4), (2, 2)]
poly_with_hole = Polygon(exterior, holes=[hole])
buffered = poly_with_hole.buffer(1.0)
```

### Buffer with Custom Parameters

```python
from togo import Geometry

geom = Geometry("POLYGON((0 0, 20 0, 20 20, 0 20, 0 0))")

# Smooth buffer with high quad_segs
smooth = geom.buffer(2.0, quad_segs=32)

# Fast buffer with low quad_segs
fast = geom.buffer(2.0, quad_segs=4)

# Custom join style with mitre limit
mitre_join = geom.buffer(2.0, join_style=2, mitre_limit=3.0)

# Bevel joins
bevel_join = geom.buffer(2.0, join_style=3)
```

## Special Cases

### Zero Distance

```python
geom = Geometry("POINT(0 0)")
same_geom = geom.buffer(0.0)
# Returns the same geometry object without modification
```

### Negative Distance (Shrinking)

```python
# Only meaningful for Polygons
poly = Polygon(Ring([(0, 0), (10, 0), (10, 10), (0, 10), (0, 0)]))
shrunk = poly.buffer(-1.0)
# Result: Smaller polygon 1 unit inward

# If shrink distance is too large, may produce empty geometry
very_shrunk = poly.buffer(-6.0)  # May be empty
```

### Empty Results

Some buffer operations may produce empty geometries:
- Buffering a line with negative distance
- Shrinking a polygon too much
- Buffering degenerate geometries

## Performance Considerations

- **Resolution**: Higher quad_segs produces smoother buffers but takes longer
  - For visualization: quad_segs 8-16 usually sufficient
  - For precision work: use quad_segs 16-32
  - For quick approximations: use quad_segs 4-8

- **Join/Cap Styles**: Different styles have different performance characteristics
  - Round joins/caps are generally fastest
  - Mitre joins can be slower

- **Geometry Complexity**: Buffer time increases with geometry complexity
  - Complex polygons with many vertices take longer
  - Consider simplifying complex geometries first if performance is critical

## Comparison with Shapely

Togo's `buffer()` method works the same as Shapely's:

```python
# Shapely
from shapely.geometry import Point as ShapelyPoint
p = ShapelyPoint(0, 0)
buffered = p.buffer(10.0, quad_segs=16)

# Togo
from togo import Point
p = Point(0, 0)
buffered = p.buffer(10.0, quad_segs=16)

# Results are identical!
```

## Implementation Details

- Buffer operations use GEOS (Geometry Engine - Open Source)
- GEOS is initialized and cleaned up automatically
- Thread-safe: Each buffer call initializes its own GEOS context
- Memory efficient: Temporary geometries are properly freed

## See Also

- [SHAPELY_API.md](SHAPELY_API.md) - Complete Shapely-compatible API documentation
- [README.md](README.md) - General library documentation
