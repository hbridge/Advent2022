import pathlib
import re
import math

script_directory = pathlib.Path(__file__).parent.resolve()

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

######## MODIFY AFTER HERE ########

class Point:
  def __init__(self, x, y):
    self.x = x
    self.y = y

  def __eq__(self, __o: object) -> bool:
    return self.x == __o.x and self.y == __o.y

  def __str__(self):
    return f'[{self.x},{self.y}]'

  def __hash__(self) -> int:
    return hash(f'{self.x},{self.y}')


def print_rope(rope, s, width, height):
    for j in range(height-1, -1, -1):
      row = ""
      for i in range(0, width):
        for idp, point in enumerate(rope):
          found = False
          if point.x == i and point.y == j:
            row += f'{"H" if idp == 0 else idp}'
            found = True
            break
        if not found:
          if s.x == i and s.y == j:
            row += "s"
          else:
            row += "."
      print(row)  

def print_visits(points, s, width, height):
  for j in range(height-1, -1, -1):
      row = ""
      for i in range(0, width):
        if s.x == i and s.y == j:
            row += "s"
            continue
        for point in points:
          found = False
          if point.x == i and point.y == j:
            row += f'#'
            found = True
            break
        if not found:
          row += "."
      print(row)  

def move_head(h, dir):
  match dir:
    case "R":
      h.x += 1
    case "U":
      h.y += 1
    case "L":
      h.x -= 1
    case "D":
      h.y -= 1

def move_tail(h, t):
  x_off = h.x - t.x
  y_off = h.y - t.y

  if abs(x_off) + abs(y_off) < 2: #overlap, adjacent
    return

  if abs(x_off) == 1 and abs(y_off) == 1: #diagonal
    return

  if abs(x_off) == 1:
    t.x = h.x
  if abs(x_off) == 2:
    t.x = t.x + (h.x - t.x) // 2
    
  if abs(y_off) == 1:
    t.y = h.y
  elif abs(y_off) == 2:
    t.y = t.y + (h.y - t.y) // 2
      
  
for part in part_answers.keys():
  for input_type, input in inputs.items():
    print(f'**** Beginning Part {part} Input {input_type} ****')
    ###### START SOLVING HERE ######    
    # positions the tail visited, rope of 2
    if part == 1:
      h = Point(0, 0)
      t = Point(0, 0)
      t_locs = {Point(0,0)}
      for line in input.split("\n"): 
        [dir, steps] = line.split(" ")
        for step in range(int(steps)):
          move_head(h, dir)
          move_tail(h, t)
          t_locs.add(Point(t.x, t.y))
    
      part_answers[part][input_type] = len(t_locs)

    # part 2: positions tail visited, rope of 10
    if part == 2:
      s = Point(11, 5)
      rope = [Point(s.x, s.y) for i in range(10)]
      t_locs = {Point(s.x, s.y)}
      for line in input.split("\n"):        
        [dir, steps] = line.split(" ")
        for step in range(int(steps)):
          move_head(rope[0], dir)
          for i in range(len(rope) - 1):
            move_tail(rope[i], rope[i + 1])
          t_locs.add(Point(rope[-1].x, rope[-1].y))
      print_visits(t_locs, s, 27, 21)
      part_answers[part][input_type] = len(t_locs)
    
for part in part_answers.keys():
  print(f'Part {part} Answers:')
  for input_type in part_answers[part].keys():
    print(f'  {input_type}: {part_answers[part][input_type]}')


