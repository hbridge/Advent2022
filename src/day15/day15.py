import pathlib
import re
import math
from functools import cmp_to_key
import sys

script_directory = pathlib.Path(__file__).parent.resolve()
sys.path.append(script_directory.parent.as_posix() + "/util")
from util import Grid2d, Coord, Direction, extract_ints, Line1d

example_file = open(f"{script_directory}/example.txt")
input_file = open(f"{script_directory}/input.txt")

EXAMPLE = example_file.read();
INPUT = input_file.read();

example_file.close();
input_file.close();

inputs = {
  "example": EXAMPLE,
  "input": INPUT
}

part_answers = {
  1: {},
  2: {}
}

def run():
  for part in part_answers.keys():
    for input_type, input in inputs.items():
      print(f'**** Beginning Part {part} Input {input_type} ****')
      ######## MODIFY AFTER HERE ########
      solution = solve1(input, input_type) if part == 1 else solve2(input, input_type)
      part_answers[part][input_type] = solution

  for part in part_answers.keys():
    print(f'Part {part} Answers:')
    for input_type in part_answers[part].keys():
      print(f'  {input_type}: {part_answers[part][input_type]}')



######## MODIFY AFTER HERE ########
def sensor_coverage_for_row(sensor, closest_beacon, row):
  row_dist = abs(sensor.y - row)
  sensor_rad = sensor.taxi_dist(closest_beacon)
  sens_min_row = sensor_rad - row_dist # 
  if sens_min_row < 0:
    return None
  return Line1d(sensor.x - sens_min_row, sensor.x + sens_min_row)

def row_range_for_sensor(sensor, closest_beacon):
  sensor_rad = sensor.taxi_dist(closest_beacon)
  return range(sensor.y - sensor_rad, sensor.y + sensor_rad + 1)

def solve2(input, input_type):
  print(f"Solving 2: {input_type}")
  coverage_by_row = {}

  for line in input.split("\n"):
    nums = extract_ints(line)
    sensor_loc = Coord(nums[0], nums[1])
    closest_beacon = Coord(nums[2], nums[3])

    for row in row_range_for_sensor(sensor_loc, closest_beacon):
      if row % 1_000_000 == 0:
        print(f'Processing row {row} for sensor {sensor_loc}')
      max_row = 20 if input_type == "example" else 4_000_000
      if row < 0 or row > max_row:
        continue
      coverage = sensor_coverage_for_row(sensor_loc, closest_beacon, row)
      if row in coverage_by_row:
        coverage_by_row[row].add(coverage)
      else:
        coverage_by_row[row] = {coverage}

  result = []
  compressed = {}
  for row in coverage_by_row.keys():
    compress_coverage = Line1d.compress(coverage_by_row[row], by_point_coverage=True)
    compressed[row] = compress_coverage
    if len(compress_coverage) > 1:
      return 4_000_000 * (compress_coverage[0].end + 1) + row

def solve1(input, input_type):
  print("Solving 1")
  beacons_by_row = {10: set(), 2000000: set()}
  coverage_by_row = {10: set(), 2000000: set()}

  for line in input.split("\n"):
    nums = extract_ints(line)
    sensor_loc = Coord(nums[0], nums[1])
    closest_beacon = Coord(nums[2], nums[3])
    if closest_beacon.y in beacons_by_row.keys():
      beacons_by_row[closest_beacon.y].add(closest_beacon)
    
    for row in coverage_by_row.keys():
      coverage = sensor_coverage_for_row(sensor_loc, closest_beacon, row)
      if coverage is not None:
        coverage_by_row[row].add(coverage)

  counts = {10: 0, 2000000: 0}
  for row in counts.keys():
    compress_coverage = Line1d.compress(coverage_by_row[row])
    counts[row] = (
      sum([l.points() for l in compress_coverage])
      - len(beacons_by_row[row])
    )
    
  return counts

run()

