#!/opt/homebrew/bin/python3
from __future__ import annotations
import numpy as np

from typing import List, final
from typing import Set
from typing import Tuple


class Point:
  """Point is a container for hashable (x, y) coords."""

  def __init__(self, x, y):
    self.x = x
    self.y = y

  def __repr__(self):
    return "<Point {:4d}, {:4d}>".format(self.x, self.y)

  def __eq__(self, other: Point) -> bool:
    return self.x == other.x and self.y == other.y

  def __hash__(self):
    return hash((self.x, self.y))


# Typedef
PointPair = Tuple[Tuple[Point, int], Tuple[Point, int]]


def generate_points(n: int, disperse: int = 2) -> List[Point]:
  """generate_points produces a random sample of n integer coordinates."""
  vals = np.random.randint(0, n * disperse, (n, 2))
  points: Set[Point] = set()
  for _ in vals:
    points.add(Point(_[0], _[1]))
  return [_ for _ in points]


def distance(p1: Point, p2: Point) -> float:
  """distance is a euclidean distance between two Point types."""
  return ((p1.x - p2.x)**2 + (p1.y - p2.y)**2)**(1 / 2)


def brute_force(pts: List[Point], left: int, right: int) -> Tuple[float, List[PointPair]]:
  """brute_force performs pairwise comparisons over a list between two indices.

  This method is O(n^2), but can be considered O(1) time when run over a constant input size.
  """
  minimum = 9999999999
  closest: Set[PointPair] = set()
  for i in range(left, right - 1):
    for j in range(i + 1, right):
      d = distance(pts[i], pts[j])
      this_pair: PointPair = (
        (pts[i], i),
        (pts[j], j)
      )
      if d < minimum:
        minimum = d
        closest.clear()
        closest.add(this_pair)
      elif d == minimum:
        closest.add(this_pair)
  return minimum, list(closest)


def div_conq_closest_pair(
  x_srt_points: List[Point],
  y_srt_points: List[Tuple[Point, int]],
  left: int,
  right: int,
  depth: int = 0) -> Tuple[float, List[PointPair]]:
  if right - left < 4:
    # if left and right are near, run constant time brute force
    # O(1)
    return brute_force(x_srt_points, left, right)

  # find the midpoint index over the x axis.
  mid = (left + right) // 2
  x_midpoint = x_srt_points[mid].x

  closest: Set[PointPair] = set()

  # linearly divide our y_sorted list into the left side and right side
  # O(n)
  y_srt_left = []
  y_srt_right = []
  for _ in y_srt_points:
    if _[0].x < x_midpoint:
      y_srt_left.append(_)
    elif _[0].x > x_midpoint:
      y_srt_right.append(_)
    else:
      y_srt_left.append(_)
      y_srt_right.append(_)

  # recurse left and right, passing the reduced y_sort list 
  min_left, left_pts = div_conq_closest_pair(
    x_srt_points, y_srt_left, left, mid, depth + 1)

  min_right, right_pts = div_conq_closest_pair(
    x_srt_points, y_srt_right, mid, right, depth + 1)

  # merge the results depending on which side had the smaller delta
  # O(1)
  delta = 99999999999
  if min_left < min_right:
    closest = set(left_pts)
    delta = min_left
  elif min_right < min_left:
    closest = set(right_pts)
    delta = min_right
  else:
    delta = min_right
    closest = set(left_pts).union(set(right_pts))

  # Filter y_sorted by the center strip
  # O(n)  
  strip_sorted = []
  for _ in y_srt_points:
    if _[0].x >= x_midpoint - delta or _[0].x <= x_midpoint + delta:
      strip_sorted.append(_)

  # Search the middle strip in order, checking a constant 8 next points
  # from each point.
  # O(n) * O(1) = O(n)
  strip_minimum = 9999999
  strip_closest = set()
  for i in range(len(strip_sorted)):
    for j in range(i + 1, i + 9):
      if j > len(strip_sorted) - 1:
        # at the end, skip
        continue
      p1 = strip_sorted[i][0]
      p2 = strip_sorted[j][0]

      d = distance(p1, p2)

      pos_pair1 = (p1, strip_sorted[i][1])
      pos_pair2 = (p2, strip_sorted[j][1])

      if d < strip_minimum:
        strip_minimum = d
        strip_closest.clear()
        strip_closest.add((pos_pair1, pos_pair2))
      elif d == strip_minimum:
        strip_closest.add((pos_pair1, pos_pair2))

  # check if the middle strip had a closer pair of points
  # and update if necessary
  # O(1)
  if strip_minimum < delta:
    delta = strip_minimum
    closest = strip_closest
  elif strip_minimum == delta:
    closest = closest.union(strip_closest)

  return delta, closest


def closest_pairs(points: List[Point]):
  # Sort by x coord
  # Theta(n * logn)
  x_sorted = sorted(pts, key=lambda x: x.x)

  # Add the x_sorted position index
  x_sorted_idx: List[Tuple[Point, int]] = []
  for i in range(len(x_sorted)):
    x_sorted_idx.append(
      (x_sorted[i], i)
    )

  # Sort by y coord
  # Theta(n * logn)
  y_sorted = sorted(x_sorted_idx, key=lambda x: x[0].y)
  
  # Recurrence is:
  # T(n) = 2 * T(n/2) + n 
  # T(n) = Theta(n * log n)
  # total (with sorts) = Theta(n * logn)

  return div_conq_closest_pair(x_sorted, y_sorted, 0, len(points) - 1)


if __name__ == "__main__":
  pts = generate_points(1000, 1)

  final_dist, final_pts = closest_pairs(pts)

  print("\nDivide and Conquer:")
  print(final_dist)
  for _ in final_pts:
    p1 = _[0][0]
    p2 = _[1][0]
    print(distance(p1, p2), p1, p2)

  actual_dist, actual_pts = brute_force(pts, 0, len(pts))
  print("\nBrute Force:")
  print(actual_dist)
  for _ in actual_pts:
    p1 = _[0][0]
    p2 = _[1][0]
    print(distance(p1, p2), p1, p2)