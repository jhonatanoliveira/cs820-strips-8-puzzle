# run.py
#
# AUTHOR
# ---------
# Jhonatan S. Oliveira
# oliveira@uregina.ca
# Department of Computer Science
# University of Regina
# Canada
#
# DESCRIPTION
# -----------
# Utility file to run the 8-puzzle problem using STRIPS
#
# HOW TO USE
# ----------
# There are 3 run mode for this program
# 1) Interactive mode by argument
#     - User input one initial state when calling the run.py program using the "-i" argument
# 2) Interactive mode standalone
#     - User input one initial state using interactive menu when run.py without any argument
# 3) File mode
#     - User input multiple initial states by calling run.py with a file name in "-f" argument
# Notice that all state input is *comma separated* and with numbers filling the board from *top* to *down* and from *left* to *right* and *number zero* representing the clear block.
# For example, an initial state 1,2,3,0,6,4,8,7,5 represents the following board configuration:
# 1 2 3
# X 6 4
# 8 7 5
# where the X is the clear block.
#
# EXAMPLE
# -------
# 1) Interactive mode by argument:
# $ python run.py -i 1,2,3,0,6,4,8,7,5
#
# 2) Interactive mode standalone
# $ python run.py
#
# 3) File mode
# $ python run.py -f initial_states.txt


import argparse
from strips import Strips
from strips import State
from time import time



def show_moves(solution):
  print()
  print(">>> Solution found:")
  for m in solution:
    print("---> Move " + str(m[1]) + " from " + str((m[2],m[3])) + " to " + str((m[4],m[5])) + ".")
  print()


def run_file_mode(file_name, output_file_name="solutions.txt", verbose=True, max_time=5):
  print()
  print(">>> STRIPS running in File Mode with following settings")
  print(">>> Verbose = " + str(verbose) + ", Max Solver Time = " + str(max_time) + " (s).")
  print(">>> File Name = " + file_name + ".")
  print()
  output_file = open(output_file_name, "w")
  with open(file_name) as input_file:
    tic = time()
    while True:
      initial_state_str = input_file.readline()
      if len(initial_state_str) == 0:
        break
      if (time() - tic) > 60:
        print(">>> Unfortunately, STRIPS couldn't find a solution within 1 minute.")
        print(">>> We are ending this program now.")
      positions = convert_from_str_to_positions(initial_state_str)
      initial_state = State(positions)
      s = Strips(initial_state, max_elaps_time=max_time)
      # Loop user while solution can be found or user give up
      while True:
        could_solve, solution = s.run(verbose=verbose)
        if could_solve:
          output_file.write(str(solution)+"\n")
          break
  print(">>> STRIPS done.")



def convert_from_str_to_positions(str_state):
  # Read input and convert to initial state
  list_curr_state = [int(n.strip()) for n in str_state.split(",")]
  i = 1
  j = 1
  positions = set()
  num_counter = 0
  for i in range(1,4):
    for j in range(1,4):
      number = list_curr_state[num_counter]
      if number != 0:
        positions.add( ("on", number, i, j) )
      else:
        positions.add( ("clear", 0, i, j) )
      num_counter += 1
  return positions


def run_interactive_mode(str_curr_state, verbose=True, max_time=5):
  print()
  print(">>> STRIPS running in Interactive Mode with following settings")
  print(">>> Verbose = " + str(verbose) + ", Max Solver Time = " + str(max_time) + " (s).")
  print(">>> Initial State = " + str_curr_state + ".")
  print()
  positions = convert_from_str_to_positions(str_curr_state)
  # Perform STRIPs in initial state
  initial_state = State(positions)
  s = Strips(initial_state, max_elaps_time=max_time)
  # Loop user while solution can be found or user give up
  try_again = True
  while try_again:
    could_solve, solution = s.run(verbose=verbose)
    if could_solve:
      show_moves(solution)
      try_again = False
    else:
      answer = input(">>> Do you want to try again? (y/n): ")
      if answer == "n" or answer == "N":
        try_again = False
  print(">>> STRIPS done.")


# ----
# MAIN
# ----
if __name__ == "__main__":

  # Argument parser
  parser = argparse.ArgumentParser()
  parser.add_argument("-i","--initial-state", help="Initial state comma separated with clear block being 0")
  parser.add_argument("-v","--verbose", help="View all internal messages", action="store_false")
  parser.add_argument("-t","--time", help="Set max time in sec for finding solution")
  parser.add_argument("-f","--file", help="Solve multiple initial states using a file. One state per line, comma separated.")
  args = parser.parse_args()

  # Max time finding solution
  max_time = 5
  if args.time:
    max_time = args.time

  # Decide run mode based in user's arguments
  if args.initial_state:
    run_interactive_mode(args.initial_state, verbose=args.verbose, max_time = max_time)
  elif args.file:
    run_file_mode(args.file, verbose=args.verbose, max_time = max_time)
  else:
    str_curr_state = input(">>> Initial state comma separated: ")
    run_interactive_mode(str_curr_state, verbose=args.verbose, max_time = max_time)
