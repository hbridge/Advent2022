import pathlib
import re
import math
from functools import cmp_to_key

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

LIST = type([0])
INT = type(0)

def is_pair_ordered(p1, p2):
  t1 = type(p1)
  t2 = type(p2)

  if t1 == t2 and t1 == INT:
    if p1 == p2:
      return None
    else:
      return p1 < p2

  if t1 == t2 and t1 == LIST:
    for i, val in enumerate(p1):
      if i == len(p2):
        # right ran out of items first
        return False
      else:
        ordered = is_pair_ordered(p1[i], p2[i])
        if ordered != None:
          return ordered
    return True if len(p1) < len(p2) else None # went through all with no decision

  # one is an int, one is a list
  new_p1 = p1 if t1 == LIST else [p1]
  new_p2 = p2 if t2 == LIST else [p2]

  return is_pair_ordered(new_p1, new_p2)


def packet_compare(p1, p2):
  result = is_pair_ordered(p1, p2)
  if result == None:
    return 0
  if result == True: # ascending 
    return -1

  return 1
  

for part in part_answers.keys():
  for input_type, input in inputs.items():
    print(f'**** Beginning Part {part} Input {input_type} ****')
    ###### START SOLVING HERE ######
    right_order_index_sum = 0

    packet_pairs = input.split("\n\n")
    packets = [[[2]], [[6]]]
    for pair_index, packet_pair in enumerate(packet_pairs):
      [p1, p2] = [eval(packet_str) for packet_str in packet_pair.split("\n")]
      if is_pair_ordered(p1, p2):
        right_order_index_sum += pair_index + 1
      packets.append(p1)
      packets.append(p2)

    # part 1 
    if part == 1:
      part_answers[part][input_type] = right_order_index_sum

    # part 2
    if part == 2:
      sorted_packets = sorted(packets, key=cmp_to_key(packet_compare))
      part_answers[part][input_type] = \
        (sorted_packets.index([[2]]) + 1) * (sorted_packets.index([[6]]) + 1)

###### PRINT OUT ANSWERS ######

for part in part_answers.keys():
  print(f'Part {part} Answers:')
  for input_type in part_answers[part].keys():
    print(f'  {input_type}: {part_answers[part][input_type]}')


