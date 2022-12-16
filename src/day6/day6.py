import pathlib
import re

script_directory = pathlib.Path(__file__).parent.resolve()

example_file = open(f"{script_directory}/example.txt")
input_file = open(f"{script_directory}/input.txt")

EXAMPLE = example_file.read();
INPUT = input_file.read();

example_file.close();
input_file.close();

######## MODIFY AFTER HERE ########

inputs = {
  "example": EXAMPLE,
  "input": INPUT
}

part_answers = {
  1: {},
  2: {}
}

PACKET_START_LEN = 4
MESSAGE_START_LEN = 14

for part in part_answers.keys():
  print(f'**** Beginning Part {part}')
  for input_type, input in inputs.items():
    if part == 1:
      for i in range(len(input) - PACKET_START_LEN - 1):
        chars = input[i:i+PACKET_START_LEN]
        if len(set(chars)) == 4:
          part_answers[part][input_type] = i + PACKET_START_LEN
          break
    
    if part == 2:
      for i in range(len(input) - MESSAGE_START_LEN - 1):
        chars = input[i:i+MESSAGE_START_LEN]
        if len(set(chars)) == MESSAGE_START_LEN:
          part_answers[part][input_type] = i + MESSAGE_START_LEN
          break

for part in part_answers.keys():
  print(f'Part {part} Answers:')
  print(f'  Example: {part_answers[part]["example"]}')
  print(f'  Input: {part_answers[part]["input"]}')


