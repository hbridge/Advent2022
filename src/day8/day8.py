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
def print_2d(arr):
    for i in range(0, len(arr)):
      row = "[ "
      for j in range(0, len(arr[i])):
        row += f' |{str(arr[j][i])}|'
      row += " ]"
      print(row)  

class Vista: 
  def __init__(self):
    self.top_max = -2
    self.left_max = -2
    self.bottom_max = -2
    self.right_max = -2

  def __str__(self):
    return f't{self.top_max:02} l{self.left_max:02} b{self.bottom_max:02} r{self.right_max:02}'

  def set_all(self, val):
    self.top_max = val
    self.left_max = val
    self.bottom_max = val
    self.right_max = val

  def tree_visible(self, tree_val):
    for val in [self.top_max, self.left_max, self.bottom_max, self.right_max]:
      if tree_val > val:
        return True
    return False

def view_score(start_i, start_j, trees, side_length):
  tree_val = trees[start_i][start_j]
  results = []
  # right
  for i in range(start_i+1, side_length, 1):
    if trees[i][start_j] >= tree_val or i == side_length - 1:
      results.append(i - start_i)
      break

  # down
  for j in range(start_j + 1, side_length, 1):
    if trees[start_i][j] >= tree_val or j == side_length - 1:
      results.append(j - start_j)
      break

  # left
  for i in range(start_i - 1, -1, -1):
    if trees[i][start_j] >= tree_val or i == 0:
      results.append(start_i - i)
      break

  # up
  for j in range(start_j - 1, -1, -1):
    if trees[start_i][j] >= tree_val or j == 0:
      results.append(start_j - j)
      break

  return math.prod(results)

for part in part_answers.keys():
  for input_type, input in inputs.items():
    print(f'**** Beginning Part {part} Input {input_type} ****')
    ###### START SOLVING HERE ######
    lines = input.split("\n")
    side_length = len(lines[0])
    # make a blank 2d array for both
    trees = [[None for c in range(side_length)] for d in range(side_length)]
    vistas = [[Vista() for c in range(side_length)] for d in range(side_length)]

    # parse each line of input
    for row, line in enumerate(lines):
      for col, c in enumerate(line):
        trees[col][row] = int(c)
        if col == 0 or row == 0 or row == side_length - 1 or col == side_length - 1:
          vistas[col][row].set_all(-1)

    # calculate top vistas
    for i in range(1, side_length - 1, 1):
      for j in range(1, side_length - 1, 1):
        vistas[i][j].top_max = max(vistas[i][j-1].top_max, trees[i][j-1])

    # calculate bottom vistas
    for i in range(side_length - 2, 0, -1):
      for j in range(side_length -2 , 0, -1):
        print(f'calc bottom for [{i}][{j}]')
        vistas[i][j].bottom_max = max(vistas[i][j+1].bottom_max, trees[i][j+1])

    # calculate left vistas
    for j in range(1, side_length - 1, 1):
      for i in range(1, side_length - 1, 1):
        vistas[i][j].left_max = max(vistas[i-1][j].left_max, trees[i-1][j])

    # calculate right vistas
    for j in range(side_length - 2, 0, -1):
      for i in range(side_length - 2, 0, -1):
        vistas[i][j].right_max = max(vistas[i+1][j].right_max, trees[i+1][j])

    print_2d(vistas)        
    num_visible = 0
    for i in range(side_length):
      for j in range(side_length):
        if vistas[i][j].tree_visible(trees[i][j]):
          num_visible += 1


    # num trees visible
    if part == 1:
      part_answers[part][input_type] = num_visible

    # part 2: 
    if part == 2:
      highest = 0
      for i in range(1, side_length - 1, 1):
        for j in range(1, side_length - 1, 1):
          highest = max(highest, view_score(i, j, trees, side_length))
      part_answers[part][input_type] = highest
    
for part in part_answers.keys():
  print(f'Part {part} Answers:')
  print(f'  Example: {part_answers[part]["example"]}')
  print(f'  Input: {part_answers[part]["input"]}')


