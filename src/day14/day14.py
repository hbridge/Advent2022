import pathlib
import re
import math
from functools import cmp_to_key
import sys

script_directory = pathlib.Path(__file__).parent.resolve()
sys.path.append(script_directory.parent.as_posix() + "/util")
from util import Grid2d, Coord, Direction

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
      solution = solve1(input) if part == 1 else solve2(input)
      part_answers[part][input_type] = solution

  for part in part_answers.keys():
    print(f'Part {part} Answers:')
    for input_type in part_answers[part].keys():
      print(f'  {input_type}: {part_answers[part][input_type]}')



######## MODIFY AFTER HERE ########
move_dirs = [Direction.Bottom, Direction.BottomLeft, Direction.BottomRight]
def next_coord(sand_coord, grid):
  for dir in move_dirs:
    n = grid.neighbor_at(sand_coord, dir)
    if n is None: # we fell off the board, return something off the board
      return Coord(grid.width + 1, grid.height + 1)
    val = grid[n.x][n.y]
    if val is ".":
      return n
  return sand_coord # if all locations below are filled, stay put

def solve(input, floor = False):
  lines = input.split("\n")
  # figure out the size of the grid
  max_x = 0
  max_y = 0
  for line in lines:
    coords = [Coord(int(x), int(y)) for [x,y] in [s.split(",") for s in line.split(" -> ")]]
    max_x = max(max_x, max([c.x for c in coords]))
    max_y = max(max_y, max([c.y for c in coords]))

  if floor:
    max_x += 200
    max_y += 2

  grid = Grid2d(max_x + 1, max_y + 1, ".")
  for line in lines:
    coords = [Coord(int(x), int(y)) for [x,y] in [s.split(",") for s in line.split(" -> ")]]
    for i in range(0, len(coords) - 1, 1):
      line_coords = coords[i].straight_line_to(coords[i+1])
      for c in line_coords:
        grid[c.x][c.y] = "#"

  if floor:
    for x in range(0, grid.width):
      grid[x][grid.height - 1] = "#"

  count = 0
  while(True):
    cur = Coord(500, 0)
    next = next_coord(cur, grid)
    while(cur != next):
      cur = next
      next = next_coord(cur, grid)

    if cur.y > grid.height: 
      break # sand fell off edge

    grid[cur.x][cur.y] = "o"
    count += 1

    if cur.x == 500 and cur.y == 0: 
      break #cave is full
  
  print(grid)
  return count


def solve1(input):
  print("Solving 1")
  return solve(input)

def solve2(input):
  print("Solving 2")
  return solve(input, True)

run()

