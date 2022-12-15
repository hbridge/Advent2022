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

move_regex = re.compile("move (\\d+) from (\\d+) to (\\d+)")


def print_stacks(stacks):
  print('Stacks: ')
  tallest = max([len(stack) for stack in stacks])
  for i in range(tallest - 1, -1, -1):
    line = ""
    for stack in stacks:
      if i > len(stack) - 1:
        line += "    "
      else:
        line += f'[{stack[i]}] '
    print(line)
for part in [1, 2]:
  print(f'**** Beginning Part {part}')
  for input_type, input in inputs.items():
    [drawing_section, moves_section] = input.split("\n\n")

    # create and read in the the stacks
    drawing_lines = drawing_section.split("\n")
    num_stacks = int(re.search('(\d+) +\Z', drawing_lines[-1]).groups()[0])
    stacks = [[] for i in range(num_stacks)]
    for line in drawing_lines[:-1]:
      for i in range(num_stacks):
        char = line[i * 4 + 1]
        if char != " ":
          stacks[i].insert(0, char)

    # go through the moves
    move_lines = moves_section.split("\n")
    for line in move_lines:
      print_stacks(stacks)
      print(line)
      [count, src, dst] = [int(s) for s in move_regex.match(line).groups()]
      src -= 1 # src and dst are 1 indexed in the input
      dst -= 1

      if part == 1:
        for i in range(count):
          stacks[dst].append(stacks[src].pop())
      else:
        stacks[dst] += stacks[src][-count:]
        del stacks[src][-count:]

    # get the top of each stack
    if part == 1:
      part_answers[part][input_type] = [stack.pop() for stack in stacks]
    else:
      part_answers[part][input_type] = [stack.pop() for stack in stacks]

for part in [1, 2]:
  print(f'Part {part} Answers:')
  print(f'  Example: {part_answers[part]["example"]}')
  print(f'  Input: {part_answers[part]["input"]}')


