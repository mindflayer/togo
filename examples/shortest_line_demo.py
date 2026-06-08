#!/usr/bin/env python3
"""Example script demonstrating shortest_line usage in ToGo."""

from togo import LineString, Point, Polygon, Ring, from_wkt, shortest_line


def main() -> None:
    print("=" * 60)
    print("ToGo Shortest Line Demo")
    print("=" * 60)

    # Point to point
    p1 = Point(0, 0)
    p2 = Point(3, 4)
    line = p1.shortest_line(p2)
    print("\n1. Point to point")
    print(f"   line: {line.to_wkt()}")
    print(f"   length: {line.length:.3f}")

    # Point to line
    point = Point(0, 0)
    line_geom = LineString([(10, 0), (10, 10)])
    line = point.shortest_line(line_geom)
    print("\n2. Point to line")
    print(f"   line: {line.to_wkt()}")
    print(f"   length: {line.length:.3f}")

    # Point to polygon
    point = Point(0, 0)
    poly = Polygon(Ring([(10, 0), (15, 0), (15, 5), (10, 5), (10, 0)]))
    line = point.shortest_line(poly)
    print("\n3. Point to polygon")
    print(f"   line: {line.to_wkt()}")
    print(f"   length: {line.length:.3f}")

    # Polygon to polygon
    poly1 = Polygon([(0, 0), (5, 0), (5, 5), (0, 5), (0, 0)])
    poly2 = Polygon([(10, 0), (15, 0), (15, 5), (10, 5), (10, 0)])
    line = shortest_line(poly1, poly2)
    print("\n4. Polygon to polygon")
    print(f"   line: {line.to_wkt()}")
    print(f"   length: {line.length:.3f}")

    # WKT input via module-level helper
    g1 = from_wkt("POINT(0 0)")
    g2 = from_wkt("LINESTRING(5 5, 10 10)")
    line = shortest_line(g1, g2)
    print("\n5. Module-level helper with WKT inputs")
    print(f"   line: {line.to_wkt()}")
    print(f"   length: {line.length:.3f}")

    print("\n" + "=" * 60)
    print("Shortest line demo completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
