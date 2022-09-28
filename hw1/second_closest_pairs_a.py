#!/opt/homebrew/bin/python3
from __future__ import annotations

from helpers import Point
from helpers import PointPair
from helpers import PointList
from helpers import PointPairList

from helpers import generate_points_unique_distances
from helpers import distance

import typing
import math


def update_if_closer(test_pair: PointPair, closest: PointPairList) -> PointPairList:
  for _ in closest:
    if test_pair.dist < _.dist:
      closest.append(test_pair)
      closest = list(set(closest))
      closest.sort(key=lambda x: x.dist)
      return closest[:2]
  return closest[:2]


def brute_force_two(point_list: PointList, left_idx: int, right_idx: int) -> PointPairList:
  closest_pairs = [
    PointPair(None, None),
    PointPair(None, None),
  ]

  for i in range(left_idx, right_idx):
    for j in range(i + 1, right_idx + 1):
      p1 = point_list[i]
      p2 = point_list[j]
      this_pair = PointPair(p1, p2)
      closest_pairs = update_if_closer(this_pair, closest_pairs)

  return closest_pairs


def div_conq_two_closest(
        x_srt_points: PointList,
        y_srt_points: PointList,
        left: int,
        right: int,
        depth: int = 0) -> PointPairList:
  if right - left < 4:
    return brute_force_two(x_srt_points, left, right)

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

  left1, left2 = div_conq_two_closest(
    x_srt_points, y_srt_left, left, mid, depth + 1
  )

  right1, right2 = div_conq_two_closest(
    x_srt_points, y_srt_right, mid, right, depth + 1
  )

  closest = [
    left1, left2, right1, right2
  ]

  for_merge = list(set(closest))
  for_merge.sort(key=lambda x: x.dist)
  merged = for_merge[:2]

  if len(merged) == 2:
    delta = merged[1].dist
  elif len(merged) == 1:
    delta = merged[0].dist
  else:
    delta = math.inf

  filtered_y = []
  for _ in y_srt_points:
    if _.x >= x_midpoint - delta and _.x <= x_midpoint + delta:
      filtered_y.append(_)

  for i in range(len(filtered_y)):
    for j in range(i + 1, i + 9):
      if j > len(filtered_y) - 1:
        break
      p1 = filtered_y[i]
      p2 = filtered_y[j]
      this_pair = PointPair(p1, p2)
      merged = update_if_closer(this_pair, merged)

  return merged


def closest_two_pairs(point_list: PointList) -> PointPairList:
  x_sorted = sorted(point_list, key=lambda x: x.x)
  for i in range(len(x_sorted)):
    x_sorted[i].x_rank = i

  y_sorted = sorted(point_list, key=lambda x: x.y)
  for i in range(len(y_sorted)):
    y_sorted[i].y_rank = i

  return div_conq_two_closest(x_sorted, y_sorted, 0, len(point_list) - 1)


if __name__ == "__main__":
  pts = generate_points_unique_distances(200, 5)
  print("ready")

  print("\nClosest:")
  results = closest_two_pairs(pts)
  print(results[0])
  print(results[1])

  print("\nBrute:")
  results = brute_force_two(pts, 0, len(pts) - 1)
  print(results[0])
  print(results[1])
