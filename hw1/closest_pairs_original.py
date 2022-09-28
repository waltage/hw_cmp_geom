#!/opt/homebrew/bin/python3
from helpers import PointPair
from helpers import PointList

from helpers import generate_points
from helpers import distance

import typing
import math

SingleResult = typing.Tuple[float, PointPair]


def brute_force(point_list: PointList, left: int, right: int) -> PointPair:
  """brute_force performs pairwise comparisons over a list between two indices.

  This method is O(n^2), but can be considered O(1) time when run over a constant input size.
  """
  closest_pair = PointPair(None, None)
  for i in range(left, right - 1):
    for j in range(i + 1, right):
      this_pair = PointPair(point_list[i], point_list[j])
      if this_pair.dist < closest_pair.dist:
        closest_pair = this_pair

  return closest_pair


def div_conq_closest_pair(
        x_srt_points: PointList,
        y_srt_points: PointList,
        left: int,
        right: int,
        depth: int = 0) -> PointPair:
  """div_conq_closest_pair follows the general CLRS implementation."""
  if right - left < 4:
    return brute_force(x_srt_points, left, right)

  mid = (left + right) // 2
  x_midpoint = x_srt_points[mid].x

  y_srt_left = []
  y_srt_right = []
  for pt in y_srt_points:
    if pt.x < x_midpoint:
      y_srt_left.append(pt)
    elif pt.x > x_midpoint:
      y_srt_right.append(pt)
    else:
      y_srt_left.append(pt)
      y_srt_right.append(pt)

  closest: PointPair = PointPair(None, None)

  left_pair = div_conq_closest_pair(
    x_srt_points, y_srt_left, left, mid, depth + 1
  )

  right_pair = div_conq_closest_pair(
    x_srt_points, y_srt_right, mid, right, depth + 1
  )

  if left_pair.dist < right_pair.dist:
    closest = left_pair
  else:
    closest = right_pair

  delta = closest.dist

  filtered_y = []
  for _ in y_srt_points:
    if _.x >= x_midpoint - delta and _.x <= x_midpoint + delta:
      filtered_y.append(_)

  for i in range(len(filtered_y)):
    for j in range(i + 1, i + 9):
      if j > len(filtered_y) - 1:
        # at the end, skip
        continue
      this_pair = PointPair(filtered_y[i], filtered_y[j])
      if this_pair.dist < delta:
        closest = this_pair

  return closest


def closest_pairs(point_list: PointList) -> PointPair:
  x_sorted = sorted(point_list, key=lambda x: x.x)
  for i in range(len(x_sorted)):
    x_sorted[i].x_rank = i

  y_sorted = sorted(point_list, key=lambda x: x.y)
  for i in range(len(y_sorted)):
    y_sorted[i].y_rank = i

  return div_conq_closest_pair(x_sorted, y_sorted, 0, len(point_list) - 1)


if __name__ == "__main__":
  pts = generate_points(5000, 3)

  result = closest_pairs(pts)
  print("closest:")
  print(result)

  check = brute_force(pts, 0, len(pts) - 1)
  print("\nbrute:")
  print(check)
