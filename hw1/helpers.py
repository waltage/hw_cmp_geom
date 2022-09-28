from __future__ import annotations

import math
import numpy as np

from typing import List
from typing import Set


def distance(p1: Point, p2: Point) -> float:
  """distance is a euclidean distance between two Point types."""
  return ((p1.x - p2.x)**2 + (p1.y - p2.y)**2)**(1 / 2)


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


class PointPair:
  """PointPair is a hashable container for two points (with invariant)."""

  def __init__(self, p1: Point, p2: Point):
    if not p1 or not p2:
      self.dist = math.inf
      self.p1 = p1
      self.p2 = p2
      return

    self.dist = distance(p1, p2)
    if p1.x < p2.x:
      self.p1 = p1
      self.p2 = p2
    elif p1.x > p2.x:
      self.p1 = p2
      self.p2 = p1
    else:
      if p1.y < p2.y:
        self.p1 = p1
        self.p2 = p2
      else:
        self.p1 = p2
        self.p2 = p1

  def __repr__(self):
    return "Pair< d={:5.3f} ({:4},{:4}) ({:4},{:4})>".format(
      self.dist,
      self.p1.x,
      self.p1.y,
      self.p2.x,
      self.p2.y
    )

  def __hash__(self):
    return hash((self.p1, self.p2))

  def __eq__(self, other: PointPair):
    return self.p1 == other.p1 and self.p2 == other.p2


# Typedefs
PointList = List[Point]
PointPairList = List[PointPair]


def generate_points(n: int, disperse: int = 2) -> PointList:
  """generate_points produces a random sample of n integer coordinates."""
  vals = np.random.randint(0, n * disperse, (n, 2))
  points: Set[Point] = set()
  for _ in vals:
    p = Point(_[0], _[1])
    points.add(p)
  return [_ for _ in points]


def remove_duplicate_distance(point_list: PointList):
  def check(pl):
    result = set()
    for i in range(len(pl) - 1):
      for j in range(i + 1, len(pl)):
        d = distance(pl[i], pl[j])
        if d in result:
          pl.pop(j)
          return True
        else:
          result.add(d)
    return False

  had_removed = True
  while had_removed:
    had_removed = check(point_list)


def generate_points_unique_distances(n: int, disperse: int = 2) -> PointList:
  pts = generate_points(n, disperse)
  remove_duplicate_distance(pts)
  return pts
