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
def print_2d(arr, val_format = "%s"):
    m = len(arr)
    n = len(arr[0])

    for j in range(0, n):
      row = "[ "
      for i in range(0, m):
        try:
          row += val_format % arr[i][j]
        except:
          row += "%s" % arr[i][j]

      row += " ]"
      print(row)  

def neighbors_for(c, m, n):
  result = []
  if c.x > 0: # left
    result.append(Coord(c.x - 1, c.y))
  if c.y > 0: # above
    result.append(Coord(c.x, c.y - 1))
  if c.x < m - 1: #right
    result.append(Coord(c.x + 1, c.y))
  if c.y < n - 1: # below
    result.append(Coord(c.x, c.y + 1))
  
  return result

def get_height_num(x, y, heights):
  val = heights[x][y]
  # start and end are actually different heights
  if val == "S":
    val = "a"
  elif val == "E":
    val = "z"

  return ord(val) - 96

class Coord:
  def __init__(self, x, y) -> None:
    self.x = x
    self.y = y

for part in part_answers.keys():
  for input_type, input in inputs.items():
    print(f'**** Beginning Part {part} Input {input_type} ****')
    ###### START SOLVING HERE ######
    lines = input.split("\n")
    M = len(lines[0])
    N = len(lines)
    # make a blank 2d array for both
    heights = [[None for y in range(N)] for x in range(M)]

    # parse each line of input, looking for start and End
    start = None
    end = None
    for row, line in enumerate(lines):
      for col, c in enumerate(line):
        heights[col][row] = c
        if c == "S":
          start = Coord(col, row)
        elif c == "E":
          end = Coord(col, row)

    # part 1 
    # calculate the min cost of reaching each location from S
    if part == 1:
      costs = [[None for y in range(N)] for x in range(M)]
      costs[start.x][start.y] = 0
      queue = [start]
      while len(queue) > 0:
        cur = queue.pop()
        cur_cost = costs[cur.x][cur.y]
        neighbors = neighbors_for(cur, M, N)
        for n in neighbors:
          cur_height = get_height_num(cur.x, cur.y, heights)
          n_height = get_height_num(n.x, n.y, heights)
          if n_height - cur_height > 1: # too tall to pass move on
            continue

          n_cost = costs[n.x][n.y]
          if n_cost == None or n_cost > cur_cost + 1:
            costs[n.x][n.y] = cur_cost + 1
            queue.append(n)
        
      print_2d(costs, "%3d")
      # part 1 shortest path = cost at end point
      part_answers[part][input_type] = costs[end.x][end.y]

    # part 2, make end the start and walk downhill to everywhere
    # then look through costs at all a's
    if part == 2:
      costs = [[None for y in range(N)] for x in range(M)]
      costs[end.x][end.y] = 0
      queue = [end]
      while len(queue) > 0:
        cur = queue.pop()
        cur_cost = costs[cur.x][cur.y]
        neighbors = neighbors_for(cur, M, N)
        for n in neighbors:
          cur_height = get_height_num(cur.x, cur.y, heights)
          n_height = get_height_num(n.x, n.y, heights)
          if cur_height - n_height > 1: # reversed as we're going downhill
            continue

          n_cost = costs[n.x][n.y]
          if n_cost == None or n_cost > cur_cost + 1:
            costs[n.x][n.y] = cur_cost + 1
            queue.append(n)

      # loop through the heights, find all a's and find the lowest a cost
      lowest_a = None
      for y in range(N):
        for x in range(M):
          if heights[x][y] == "a":
            if lowest_a == None:
              lowest_a = costs[x][y]
            elif costs[x][y] != None and costs[x][y] < lowest_a:
              lowest_a = costs[x][y]

      print_2d(costs, "%4d")
      part_answers[part][input_type] = lowest_a    


###### PRINT OUT ANSWERS ######

for part in part_answers.keys():
  print(f'Part {part} Answers:')
  for input_type in part_answers[part].keys():
    print(f'  {input_type}: {part_answers[part][input_type]}')


