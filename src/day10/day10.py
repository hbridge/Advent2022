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
# 2: {}
}

######## MODIFY AFTER HERE ########
CRT_WIDTH = 40
CRT_HEIGHT = 6

class Circuit:
  def __init__(self):
    self.register = 1
    self.clock = 1
    self.total_signal = 0
    self.pixel = 0
    self.crt_output = ""

  def tick(self):
    if (self.clock + 20) % 40 == 0:
      self.total_signal += self.signal_strength()
      # print(f'clock = {self.clock} signal = {self.signal_strength()} total_signal = {self.total_signal}')
    self.draw_pixel()
    self.clock += 1

  def signal_strength(self):
    return self.clock * self.register

  def add(self, val):
    self.register += val

  def draw_pixel(self):
    if self.register - 1 <= self.pixel and self.pixel <= self.register + 1:
      self.crt_output += "#"
    else:
      self.crt_output += "."

    self.pixel += 1
    if self.pixel % 40 == 0:
      self.pixel = 0
      self.crt_output += "\n"
      print(self.crt_output)

for part in part_answers.keys():
  for input_type, input in inputs.items():
    print(f'**** Beginning Part {part} Input {input_type} ****')
    ###### START SOLVING HERE ######    
    circuit = Circuit()

    for instruction in input.split("\n"):
      instruction_parts = instruction.split(" ")
      match instruction_parts[0]:
        case "noop":
          circuit.tick()
        case "addx":
          circuit.tick()
          circuit.tick()
          circuit.add(int(instruction_parts[1]))
    
    # part 1: sum of X at the 20th, 60th, 100th... 
    if part == 1:
      part_answers[part][input_type] = circuit.total_signal
      
    #




###### PRINT OUT ANSWERS ######

for part in part_answers.keys():
  print(f'Part {part} Answers:')
  for input_type in part_answers[part].keys():
    print(f'  {input_type}: {part_answers[part][input_type]}')


