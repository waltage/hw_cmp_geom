#!/opt/homebrew/bin/python3
from helpers import PointPair
from helpers import PointList

from helpers import generate_points
from helpers import distance

import typing
import math

SingleResult = typing.Tuple[float, PointPair]


def brute_force(point_list: PointList, left: int, right: int) -> SingleResult:
  """brute_force performs pairwise comparisons over a list between two indices.

  This method is O(n^2), but can be considered O(1) time when run over a constant input size.
  """
  # print("brute:", left, right)
  minimum = math.inf
  closest_pair = None
  for i in range(left, right - 1):
    for j in range(i + 1, right):
      d = distance(point_list[i], point_list[j])
      this_pair: PointPair = (point_list[i], point_list[j])
      if d < minimum:
        minimum = d
        closest_pair = this_pair

  return minimum, closest_pair


def div_conq_closest_pair(
    x_srt_points: PointList,
    y_srt_points: PointList,
    left: int,
    right: int,
    depth: int = 0) -> SingleResult:
  """div_conq_closest_pair follows the general CLRS implementation."""
  if right - left < 4:
    return brute_force(x_srt_points, left, right)
  
  mid = (left + right) // 2
  x_midpoint = x_srt_points[mid].x

  closest: PointPair = None
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


  delta_left, delta_pair_left = div_conq_closest_pair(
    x_srt_points, y_srt_left, left, mid, depth + 1
  )

  delta_right, delta_pair_right = div_conq_closest_pair(
    x_srt_points, y_srt_right, mid, right, depth + 1
  )

  delta = math.inf
  if delta_left < delta_right:
    delta = delta_left
    closest = delta_pair_left
  else:
    delta = delta_right
    closest = delta_pair_right
  
  filtered_y = []
  for _ in y_srt_points:
    if _.x >= x_midpoint - delta and _.x <= x_midpoint + delta:
      filtered_y.append(_)
  
  for i in range(len(filtered_y)):
    for j in range(i + 1, i + 9):
      if j > len(filtered_y) - 1:
        # at the end, skip
        continue
      p1 = filtered_y[i]
      p2 = filtered_y[j]

      d = distance(p1, p2)

      if d < delta:
        delta = d
        closest = (p1, p2)

  return delta, closest
  


def closest_pairs(point_list: PointList) -> SingleResult:
  x_sorted = sorted(point_list, key=lambda x: x.x)
  for i in range(len(x_sorted)):
    x_sorted[i].x_rank = i
    # print(x_sorted[i])

  y_sorted = sorted(point_list, key=lambda x: x.y)
  for i in range(len(y_sorted)):
    # x_sorted[i].y_rank = i
    y_sorted[i].y_rank = i

  return div_conq_closest_pair(x_sorted, y_sorted, 0, len(point_list) - 1)


if __name__ == "__main__":
  pts = generate_points(10000, 3)

  dist, a_pair = closest_pairs(pts)
  print("dist:", dist)
  print("  p1:", a_pair[0])
  print("  p2:", a_pair[1])
