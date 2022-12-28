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

MAX_MINUTES = 30

class StateNode:
  def __init__(self, position, closed_valves = [], open_valves = [], cost = 0, value = 0) -> None:
    self.position = position
    self.closed_valves = closed_valves.copy() if closed_valves is not None else []
    self.open_valves = open_valves.copy() if open_valves is not None else []
    self.cost = cost
    self.value = value  

  def key(self) -> str:
    return f'{self.closed_valves}{self.open_valves}{self.cost}'

  def __repr__(self) -> str:
    return f"Node{str(self)}"

  def __str__(self) -> str:
    return f"""c:{self.cost} v:{self.value}
               closed: {self.closed_valves}
               open: {self.open_valves}"""
  
  def __hash__(self) -> int:
    return hash(self.__str__())

class Valve:
  def __init__(self, code, flow_rate, connected_valve_codes) -> None:
    self.code = code
    self.flow_rate = flow_rate
    self.connected_valve_codes = connected_valve_codes
    self.connected_valves = []

  def __eq__(self, __o: object) -> bool:
    return self.code == __o.code

  def __hash__(self) -> int:
    return hash(self.code)

  def __repr__(self) -> str:
    return f'Valve({self.code})'

class Move:
  def __init__(self, from_code, to_code, time_remaining_before, move_costs) -> None:
    self.from_code = from_code
    self.to_code = to_code
    self.time_remaining_after = time_remaining_before - move_costs[from_code][to_code] - 1

  def __str__(self) -> str:
    return f"{self.from_code}>{self.to_code}"

  def __repr__(self) -> str:
    return f'Move({self.__str__()})'
  
def min_move_cost(from_valve, to_valve, visited):
  if from_valve == to_valve:
    return 0
  
  min_additional_visits = 1000
  for valve in from_valve.connected_valves:
    if valve in visited:
      continue
    visited.add(valve)
    min_additional_visits = min(min_additional_visits, 1 + min_move_cost(valve, to_valve, visited))
    visited.remove(valve)
  
  return min_additional_visits


def parse_input(input):
  valves = {}
  valve_states = {}

  for line in input.split("\n"):
    letter_pairs = re.findall(r'[A-Z]{2}', line)
    flow_rate = extract_ints(line)[0]
    valves[letter_pairs[0]] = Valve(letter_pairs[0], flow_rate, letter_pairs[1:])
    
    if flow_rate > 0: # if a valve has a flow rate of 0, don't add it's state
      valve_states[letter_pairs[0]] = False

  for valve in valves.values():
    valve.connected_valves = [valves[code] for code in valve.connected_valve_codes]

  move_costs = {}
  for from_code in list(valve_states.keys()) + ['AA']:
    move_costs[from_code] = {}
    for to_code in valve_states.keys():
      move_costs[from_code][to_code] = min_move_cost(valves[from_code], valves[to_code], {valves[from_code]})

  return [valves, valve_states, move_costs]

def valid_moves(positions, time_remaining, move_costs, valve_states):
  valid_moves = []
  # only move to a place if a valve is open
  # valves with flow_rate 0 not in the dict
  closed_valves = {v: s for (v, s) in valve_states.items() if s == False }
  for a_code in closed_valves:
    if len(positions) == 1:
      # part 1, only you move
      move = Move(positions[0], a_code, time_remaining[0], move_costs)
      if move.time_remaining_after > 0:
        valid_moves.append([move])
    else:
      # part 2, you and elephant move
      for b_code in closed_valves:
        if a_code != b_code: # you and elephant don't move to same place
          a_move = Move(positions[0], a_code, time_remaining[0], move_costs)
          b_move = Move(positions[1], b_code, time_remaining[1], move_costs)
          if a_move.time_remaining_after > 0 or \
            b_move.time_remaining_after > 0: # have to consider one running out first
            valid_moves.append([a_move, b_move])
  return valid_moves
  
state_cache = {}

def calc_value(positions, time_remaining, move_costs, valves, valve_states, inc_value, path):
  # print(f'p:{path} tr:{time_remaining} v:{value}')
  if len(positions) > 1 and positions[1] < positions[0]:
    # states are mirror images, sort to cut down paths
    positions.reverse() 
    time_remaining.reverse()
    
  state = f'{positions}|{time_remaining}|{valve_states}'
      
  global state_cache
  if state in state_cache:
    # print(f'cache hit')
    return state_cache[state]

  moves = valid_moves(positions, time_remaining, move_costs, valve_states)
  max_value = 0;
  for move_set in moves:
    new_valve_states = valve_states.copy()
    new_time_remaining = [0] * len(time_remaining)
    for i, move in enumerate(move_set):
      new_valve_states[move.to_code] = True
      new_time_remaining[i] = move.time_remaining_after

    move_value = calc_value(
      [move.to_code for move in move_set],
      new_time_remaining,
      move_costs,
      valves,
      new_valve_states,
      sum([max(0, move.time_remaining_after) * valves[move.to_code].flow_rate for move in move_set]),
      path + f'>{move_set}'
    )
    if move_value > max_value:    
      max_value = move_value

  max_state_val = inc_value + max_value
  state_cache[state] = max_state_val
  # print(f'max value for path {path}: ({max_state_val}) ')
  return max_state_val

def solve1(input, input_type):
  global state_cache 
  state_cache = {}
  print(f"Solving 1: {input_type}")
  valves, valve_states, move_costs = parse_input(input)
  answer = calc_value(['AA'], [30], move_costs, valves, valve_states, 0, "AA")
  print(f"Part 1 {input_type} answer: {answer}")
  return answer

def solve2(input, input_type):
  global state_cache
  state_cache = {}
  print("Solving 2")
  valves, valve_states, move_costs = parse_input(input)
  answer = calc_value(['AA', 'AA'], [26, 26], move_costs, valves, valve_states, 0, "[AA,AA]")
  print(f"Part 2 {input_type} answer: {answer}")
  return answer
run()

