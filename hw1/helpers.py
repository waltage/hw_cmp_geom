from __future__ import annotations
import numpy as np

from typing import List
from typing import Set
from typing import Tuple

class Point:
  """Point is a container for hashable (x, y) coords."""

  def __init__(self, x: int, y: int):
    self.x: int = x
    self.y: int = y
    self.x_rank: int = -1
    self.y_rank: int = -1

  def __repr__(self):
    return "<Point {:4d}, {:4d}, x_rank={:4d} y_rank={:4d}>".format(
      self.x, self.y, self.x_rank, self.y_rank)

  def __eq__(self, other: Point) -> bool:
    return self.x == other.x and self.y == other.y

  def __hash__(self):
    return hash((self.x, self.y))


# Typedefs
PointList = List[Point]
PointPair = Tuple[Point, Point]

def generate_points(n: int, disperse: int = 2) -> PointList:
  """generate_points produces a random sample of n integer coordinates."""
  vals = np.random.randint(0, n * disperse, (n, 2))
  points: Set[Point] = set()
  for _ in vals:
    p = Point(_[0], _[1])
    points.add(p)
  return [_ for _ in points]


def distance(p1: Point, p2: Point) -> float:
  """distance is a euclidean distance between two Point types."""
  return ((p1.x - p2.x)**2 + (p1.y - p2.y)**2)**(1 / 2)