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
  "example": EXAMPLE.split("\n"),
  "input": INPUT.split("\n")
}

part1_answers = {}
part2_answers = {}

regex = re.compile("(\\d+)-(\\d+),(\\d+)-(\\d+)")

for input_type, lines in inputs.items():
  answer1 = 0
  answer2 = 0
  for i, line in enumerate(lines):
    a_start, a_end, b_start, b_end = [int(s) for s in regex.match(line).groups()]
    if (a_start <= b_start and a_end >= b_end) \
      or (b_start <= a_start and b_end >= a_end):
      answer1 += 1

    if (a_start <= b_start and a_end >= b_start) \
      or (b_start <= a_start and b_end >= a_start):
      answer2 += 1

  part1_answers[input_type] = answer1
  part2_answers[input_type] = answer2

print(f'Part 1 Answers:')
print(f'  Example: {part1_answers["example"]}')
print(f'  Input: {part1_answers["input"]}')
print(f'Part 2 Answers:')
print(f'  Example: {part2_answers["example"]}')
print(f'  Input: {part2_answers["input"]}')
