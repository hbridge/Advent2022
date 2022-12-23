from typing import List
import enum

class Coord:
  def __init__(self, x, y) -> None:
    self.x = x
    self.y = y

  def __str__(self):
    return f'[{self.x}, {self.y}]'

  def __eq__(self, __o: object) -> bool:
    return self.x == __o.x and self.y == __o.y

  def straight_line_to(self, other):
    if self.x == other.x:
      y_vals = sorted([self.y, other.y])
      return [Coord(self.x, y) for y in range(y_vals[0], y_vals[1] + 1, 1)]
    elif self.y == other.y:
      x_vals = sorted([self.x, other.x])
      return [Coord(x, self.y) for x in range(x_vals[0], x_vals[1] + 1, 1)]
    else:
      raise Exception(f"No straight line between {self} and {other}")


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
        row = "[ "
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


