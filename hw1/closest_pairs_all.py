#!/opt/homebrew/bin/python3
from helpers import PointPair
from helpers import PointList
from helpers import PointPairList

from helpers import generate_points
from helpers import distance

import typing
import math

SingleResult = typing.Tuple[float, PointPair]


def brute_force(point_list: PointList, left_idx: int, right_idx: int) -> PointPairList:
  """brute_force performs pairwise comparisons over a list between two indices.

  This method is O(n^2), but can be considered O(1) time when run over a constant input size.
  """
  closest_pairs = [
    PointPair(None, None),
  ]
  for i in range(left_idx, right_idx):
    for j in range(i + 1, right_idx + 1):
      this_pair = PointPair(point_list[i], point_list[j])
      if this_pair.dist < closest_pairs[0].dist:
        closest_pairs = [this_pair,]
      elif this_pair.dist == closest_pairs[0].dist:
        closest_pairs.append(this_pair)
  # print (" ".join(["{:8.4f}".format(_.dist) for _ in closest_pairs]))
  return closest_pairs


def div_conq_closest_pair_all(
        x_srt_points: PointList,
        y_srt_points: PointList,
        left: int,
        right: int,
        depth: int = 0) -> PointPairList:
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

  left_pairs = div_conq_closest_pair_all(
    x_srt_points, y_srt_left, left, mid, depth + 1
  )

  right_pairs = div_conq_closest_pair_all(
    x_srt_points, y_srt_right, mid, right, depth + 1
  )

  if left_pairs[0].dist < right_pairs[0].dist:
    closest_pairs = left_pairs
  elif right_pairs[0].dist < left_pairs[0].dist:
    closest_pairs = right_pairs
  else:
    closest_pairs = left_pairs + right_pairs

  delta = closest_pairs[0].dist

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
        closest_pairs = [this_pair,]
        delta = this_pair.dist
      elif this_pair.dist == delta:
        closest_pairs.append(this_pair)

  return list(set(closest_pairs))


def closest_pairs(point_list: PointList) -> PointPair:
  x_sorted = sorted(point_list, key=lambda x: x.x)
  for i in range(len(x_sorted)):
    x_sorted[i].x_rank = i

  y_sorted = sorted(point_list, key=lambda x: x.y)
  for i in range(len(y_sorted)):
    y_sorted[i].y_rank = i

  return div_conq_closest_pair_all(x_sorted, y_sorted, 0, len(point_list) - 1)


if __name__ == "__main__":
  pts = generate_points(500, 0.5)

  result = closest_pairs(pts)
  print("closest:")
  for _ in result:
    print("  ", _)

  check = brute_force(pts, 0, len(pts) - 1)
  print("\nbrute:")
  for _ in check:
    print("  ", _)
