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

class Directory: 
  def __init__(self, parent):
    self.parent = parent
    self.files_to_sizes = {}
    self.subdirectories = {}

  def size(self):
    return sum(self.files_to_sizes.values()) \
      + sum([subdir.size() for subdir in self.subdirectories.values()])

  def subdir(self, dirname):
    if dirname not in self.subdirectories:
      self.subdirectories[dirname] = Directory(self)
    return self.subdirectories[dirname]

def dirs_matching_fun(dir, fun, result_list):
  if fun(dir):
    result_list.append(dir)
  
  for subdir in dir.subdirectories.values():
    dirs_matching_fun(subdir, fun, result_list)


command_regex = re.compile("\$ ([a-z]+) ?(.*)?$");

for part in part_answers.keys():
  for input_type, input in inputs.items():
    print(f'**** Beginning Part {part} Input {input_type} ****')
    # create and populate a root directory
    root = Directory(None)
    current_directory = None

    # parse each line of input
    for i, line in enumerate(input.split("\n")):
      re_result = command_regex.match(line)
      if re_result != None:
        match re_result.group(1):
          case "cd":
            match re_result.group(2):
              case "/":
                current_directory = root
              case "..":
                current_directory = current_directory.parent
              case _: # going into a directory
                current_directory = current_directory.subdir(re_result.group(2))
          case "ls":
            pass
      else: # this is a directory listing line
        words = line.split(" ")
        if words[0] != "dir":
          [size, filename] = words
          current_directory.files_to_sizes[filename] = int(size)

    # part 1: get directories <= 100,000
    if part == 1:
      filtered_dirs = []
      lt_100k = lambda dir:dir.size() < 100_000
      dirs_matching_fun(root, lt_100k, filtered_dirs)
      part_answers[part][input_type] = sum([dir.size() for dir in filtered_dirs])

    # part 2: need 30_000_000 of 70_000_000 size disk
    if part == 2:
      amount_free = 70_000_000 - root.size()
      amount_needed = 30_000_000 - amount_free
      gt_amount_needed = lambda dir:dir.size() >= amount_needed
      filtered_dirs = []
      dirs_matching_fun(root, gt_amount_needed, filtered_dirs)
      part_answers[part][input_type] = min([dir.size() for dir in filtered_dirs])
    
for part in part_answers.keys():
  print(f'Part {part} Answers:')
  print(f'  Example: {part_answers[part]["example"]}')
  print(f'  Input: {part_answers[part]["input"]}')


