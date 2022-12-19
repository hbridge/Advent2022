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
class Monkey:
  def __init__(self) -> None:
    self.items = [] # numbers
    self.inspections = 0
    self.operation = None # e.g. old + 6
    self.test_modulus = None 
    self.true_monkey_index = None
    self.false_monkey_index = None

  def inspect_item(self, old):
    self.inspections += 1
    return eval(self.operation)

  def test_and_throw(self, item, monkeys):
    if item % self.test_modulus == 0:
      monkeys[self.true_monkey_index].items.append(item)
    else:
      monkeys[self.false_monkey_index].items.append(item)

  def take_turn(self, monkeys, anxiety_reduce = lambda x: x // 3):
    while len(self.items) > 0:
      item = self.items.pop(0)
      new_item = self.inspect_item(item)
      new_item = anxiety_reduce(new_item) # reduce anxiety
      self.test_and_throw(new_item, monkeys)

def monkeyFromChunk(chunk):
  monkey = Monkey()
  lines = chunk.split("\n")
  monkey.items = [int(s) for s in re.findall(r'\d+', lines[1])]
  monkey.operation = lines[2].split("= ")[1]
  monkey.test_modulus = int(re.search(r'\d+', lines[3]).group(0))
  monkey.true_monkey_index = int(re.search(r'\d+', lines[4]).group(0))
  monkey.false_monkey_index = int(re.search(r'\d+', lines[5]).group(0))

  return monkey


for part in part_answers.keys():
  for input_type, input in inputs.items():
    print(f'**** Beginning Part {part} Input {input_type} ****')
    ###### START SOLVING HERE ######
    monkeys = []
    chunks = input.split("\n\n")
    for chunk in chunks:
      monkeys.append(monkeyFromChunk(chunk))

    if part == 1:
      for i in range(20):
        for monkey in monkeys:
          monkey.take_turn(monkeys)
    if part == 2:
      moduli_product = math.prod([monkey.test_modulus for monkey in monkeys])
      for i in range(10_000):
        for monkey in monkeys:
          monkey.take_turn(monkeys, lambda i: i % moduli_product)

    inspections = sorted([monkey.inspections for monkey in monkeys])
    monkey_business = inspections[-2] * inspections[-1]
    part_answers[part][input_type] = monkey_business


###### PRINT OUT ANSWERS ######

for part in part_answers.keys():
  print(f'Part {part} Answers:')
  for input_type in part_answers[part].keys():
    print(f'  {input_type}: {part_answers[part][input_type]}')


