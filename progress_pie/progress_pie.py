from __future__ import annotations
import math


class Point:

    def __init__(self, x: int, y: int) -> None:
        self._x = x
        self._y = y

    def __repr__(self) -> str:
        return "X: %d, Y: %d" % (self._x, self._y)


class Vector:

    def __init__(self, p1: Point, p2: Point) -> None:
        self._x = p1._x - p2._x
        self._y = p1._y - p2._y

    def __mul__(self, other: Vector) -> int:
        return self._x * other._x + self._y * other._y

    @property
    def length(self) -> int:
        return math.sqrt(self._x * self._x + self._y * self._y)


class ProgressPie:

    distant_epsilon = 10 ** (-6)
    START_VECTOR = Vector(Point(50, 50), Point(50, 100))

    def __init__(self, percentage: int) -> None:
        self._percentage = percentage

    def angle_epsilon(self, v: Vector) -> float:
        """ Due to the constraint: all points within a distance
            of 10​-6 of (X, Y) are the same color as (X, Y).
        """
        return math.asin(self.distant_epsilon / v.length)

    def contains(self, p: Point) -> bool:
        # Compute angle of given point with starting line segment
        v = Vector(Point(50, 50), p)
        if v.length > 50 + self.distant_epsilon:
            # Already outside circle
            return False
        cos = (self.START_VECTOR * v) / (self.START_VECTOR.length * v.length)
        angle = math.acos(cos)
        if p._x < 50:
            # Angle is more than pi in radian
            angle = 2 * math.pi - angle
        # Compute progress angle of pie charge
        progress_angle = self._percentage * 2 * math.pi / 100
        return angle <= progress_angle + self.angle_epsilon(v)


with open("input.txt", "r", encoding="utf-8") as input, open("output.txt", "w", encoding="utf-8") as output:
    T = int(input.readline())
    for c in range(1, T + 1):
        P, X, Y = map(int, input.readline().split())
        pie = ProgressPie(P)
        point = Point(X, Y)
        color = "black" if pie.contains(point) else "white"
        output.write("Case #%d: %s\n" % (c, color))
