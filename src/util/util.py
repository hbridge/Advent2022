import enum
import re
from typing import List



class Coord:
  def __init__(self, x, y) -> None:
    self.x = x
    self.y = y

  def __str__(self):
    return f'[{self.x}, {self.y}]'

  def __repr__(self) -> str:
    return f"Coord{str(self)}"

  def __eq__(self, __o: object) -> bool:
    return self.x == __o.x and self.y == __o.y

  def __hash__(self) -> int:
    return hash(f'{self.x},{self.y}')

  def taxi_dist(self, other):
    return abs(self.x - other.x) + abs(self.y - other.y)

  def coords_in_radius(self, rad):
    result = set() 
    for y in range(0, rad + 1, 1): # for each abs row distance 
      for x in range(-(rad - y), (rad - y) + 1, 1):
        # add decreasing numbers of coords
        result.add(Coord(self.x + x, self.y - y))
        # in both the negative above and positive below
        result.add(Coord(self.x + x, self.y + y))

    return result

  def straight_line_to(self, other):
    if self.x == other.x:
      y_vals = sorted([self.y, other.y])
      return [Coord(self.x, y) for y in range(y_vals[0], y_vals[1] + 1, 1)]
    elif self.y == other.y:
      x_vals = sorted([self.x, other.x])
      return [Coord(x, self.y) for x in range(x_vals[0], x_vals[1] + 1, 1)]
    else:
      raise Exception(f"No straight line between {self} and {other}")

class Line1d:
  def __init__(self, start, end):
    self.start = start
    self.end = end

  def length(self):
    return self.end - self.start

  def points(self):
    return self.length() + 1

  def overlap(self, other):
    if self.start < other.start:
      return min(0, self.end - other.start)
    
    return min(0, other.end - self.start)

  def combined(self, other):
    return Line1d(min(self.start, other.start), max(self.end, other.end))

  # if by point coverage, <1, 3> will compress with <4, 5>
  # since 1, 5 are all covered
  def compress(lines, by_point_coverage=False):
    if len(lines) < 1:
      return []
    lines = sorted(lines, key=lambda l: l.start)
    result = [lines[0]]
    r = 1
    while r < len(lines):
      end = result[-1].end + 1 if by_point_coverage else result[-1].end
      if lines[r].start <= end:
        #overlap, merge
        result[-1] = result[-1].combined(lines[r])
      else:
        #no overlap, new segment
        result.append(lines[r])

      r += 1
    return result



  def __eq__(self, __o: object) -> bool:
    return self.start == __o.start and self.end == __o.end

  def __hash__(self) -> int:
    return hash(f'{self.start},{self.end}')

  def __str__(self):
    return f'<{self.start},{self.end}>'

  def __repr__(self) -> str:
    return f"Line{str(self)}"
  

class Direction(enum.Enum):
  TopLeft = [-1, -1]
  Top = [0, -1]
  TopRight = [1, -1]
  Left = [-1, 0]
  Right = [1, 0]
  BottomLeft = [-1, 1]
  Bottom = [0, 1]
  BottomRight = [1, 1]

class Grid2d:
  def __init__(self, width, height, initial_val = None) -> None:
    self.width = width
    self.height = height
    self.data = [[initial_val for y in range(height)] for x in range(width)]
        
  def __str__(self, val_format="%s") -> str:
    m = len(self.data)
    n = len(self.data[0])

    result = ""
    for j in range(0, n):
        row = f'{j:4}[ '
        for i in range(0, m):
            try:
              row += val_format % self.data[i][j]
            except:
              row += "%s" % self.data[i][j]

        row += " ]"
        result += row + '\n'
    return result

  def __getitem__(self, item):
    return self.data[item]

  def get(self, x, y):
    return self.data[x][y]

  def set(self, x, y, val):
    self.data[x][y] = val

  def get_c(self, c: Coord):
    return self.data[c.x][c.y]

  def set_c(self, c: Coord, val):
    self.data[c.x][c.y] = val

  def coord_in_bounds(self, c: Coord):
    return c.x >= 0 and c.x < self.width \
      and c.y >= 0 and c.y < self.height

  def neighbors_for(self, c: Coord) -> List[Coord]:
    result = []
    if c.x > 0: # left
        result.append(Coord(c.x - 1, c.y))
    if c.y > 0: # above
        result.append(Coord(c.x, c.y - 1))
    if c.x < self.width - 1: #right
        result.append(Coord(c.x + 1, c.y))
    if c.y < self.height - 1: # below
        result.append(Coord(c.x, c.y + 1))

  def neighbor_at(self, c: Coord, dir: Direction):
    neighbor = Coord(c.x + dir.value[0], c.y + dir.value[1])
    return neighbor if self.coord_in_bounds(neighbor) else None

int_regex = re.compile(r'-?\d+')
def extract_ints(s: str):
  return [int(i) for i in int_regex.findall(s)]
