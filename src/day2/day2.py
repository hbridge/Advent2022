import pathlib
script_directory = pathlib.Path(__file__).parent.resolve()

select_value = {
  "R": 1,
  "P": 2,
  "S": 3
}

shapes_to_outcomes = {
  "R": {"R": 3, "P": 0, "S": 6},
  "P": {"R": 6, "P": 3, "S": 0},
  "S": {"R": 0, "P": 6, "S": 3}
}

shape_map = {}
for i, char in enumerate("RPS"):
  shape_map["ABC"[i]] = char
  shape_map["XYZ"[i]] = char

outcomes_to_shapes = {
  0: {"R": "S", "P": "R", "S": "P"},
  3: {"R": "R", "P": "P", "S": "S"},
  6: {"R": "P", "P": "S", "S": "R"}
}

decrypt_outcome_map = {
  "X": 0,
  "Y": 3, 
  "Z": 6
}

def score_round(opp, own):
  return select_value[own] + shapes_to_outcomes[own][opp]

def pick_move(opp, outcome):
  return outcomes_to_shapes[outcome][opp]

example_file = open(f"{script_directory}/example.txt")
input_file = open(f"{script_directory}/input.txt")

example = example_file.read();
input = input_file.read();

example_file.close();
input_file.close();

lines = input.split("\n")
total_score = 0
for line in lines:
  moves = line.split(" ")
  opp = shape_map[moves[0]]
  outcome = decrypt_outcome_map[moves[1]]
  own = pick_move(opp, outcome)
  round_score = score_round(opp, own)
  total_score += round_score
  # print(f'line {line}\n moves:{moves}, round_score:{round_score}')

print(f'Total score: {total_score}')
