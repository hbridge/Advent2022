import pathlib
script_directory = pathlib.Path(__file__).parent.resolve()

example_file = open(f"{script_directory}/example.txt")
input_file = open(f"{script_directory}/input.txt")

EXAMPLE = example_file.read();
INPUT = input_file.read();

example_file.close();
input_file.close();

######## MODIFY AFTER HERE ########

def char_to_pri(char):
  val = ord(char)
  if (ord(char) < ord('a')):
    # it's a capital
    return ord(char) - ord('A') + 27
  else:
    return ord(char) - ord('a') + 1



lines = INPUT.split("\n")
total_dupe_priority = 0
total_badge_priority = 0;
group_set = {}
for i, line in enumerate(lines):
  # add each half of the letters to a set
  half = len(line) // 2
  a = set(line[0:half])
  b = set(line[half:])
  # intersect them
  dupe = (a & b).pop()
  # map to a priority and add to total
  pri = char_to_pri(dupe)
  total_dupe_priority += pri
  # print(f'a: {a} b: {b} \ndupe:{dupe} pri:{pri}')

  
  if (len(group_set) == 0):
    group_set = (a | b)
  else:
    group_set = group_set & (a | b)

  if (i + 1) % 3 == 0:
    badge = group_set.pop()
    total_badge_priority += char_to_pri(badge)
    # print(f'Group {i} badge: {badge} pri: {char_to_pri(badge)}')

print(f'Part 1 Total: {total_dupe_priority}')
print(f'Part 2 Total: {total_badge_priority}')
