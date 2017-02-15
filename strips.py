# strips.py
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
# We propose a solution for the 8-puzzle problem using the STRIPS algorithm.
# In [1], the 8-puzzle problem is defined as a sliding puzzle that consists of a frame of numbered square tiles in random order with one tile missing. The object of the puzzle is to place the tiles in order by making sliding moves that use the empty space.
# In artificial intelligence, STRIPS (Stanford Research Institute Problem Solver) is an automated planner developed by Richard Fikes and Nils Nilsson in 1971 at SRI International [2].
# [1] https://en.wikipedia.org/wiki/15_puzzle
# [2] https://en.wikipedia.org/wiki/STRIPS

# PROBLEM DEFINITIONS
# -------------------
# State: set of first order predicate calculus formulas (well formed formulas - WFF)
# Operators: action formed by 1) preconditions 2) additions 3) removals
#
# IMPLEMENTATION STRUCTURES
# -------------------------
# - State of positions
#   On(x,i,j): tile x is on cell i,j
#   Clear(0,i,j): cell i,j is clear (empty)
#   Adj(i,j,k,l): cell i,j is adjacent to cell k,l
# - Operators
#   move(x,i,j,k,l): moves tile x from i,i to k,l
#     preconditions: On(x,i,j), Clear(k,l), Adj(i,j,k,l)
#     add: On(x,k,l), Clear(i,j)
#     remove: On(x,i,j), Clear(k,l) 



# Necessary libraries
from random import choice
from time import time



class State:
  """
  This class represents a game state and all possible manipulations in it.
  A game state is described by a set of positions in it, that is all numbers "on" a block and one "clear".
  """
  def __init__(self, set_positions = set([])):
    """
    Description
    -----------
    Constructor for State class. A object can be declared with a set of positions.
    Each position is a tuple containing the position name ("on" or "clear"), the block number in the position (where 0 - zero - is reserved for the clear position), the line position, and the column position.
    
    Example
    -------
    >>> positions = set([("on",1,1,1), ("on",2,1,2), ("on",3,1,3),("on",8,2,1), ("clear",0,2,2), ("on",4,2,3),("on",7,3,1), ("on",6,3,2), ("on",5,3,3)])
    >>> initial_state = State(positions)
    """
    self.positions = set_positions


  def get_clear(self):
    """
    Description
    -----------
    Return the position of the clear block.
    
    Example
    -------
    >>> positions = set([("on",1,1,1), ("on",2,1,2), ("on",3,1,3),("on",8,2,1), ("clear",0,2,2), ("on",4,2,3),("on",7,3,1), ("on",6,3,2), ("on",5,3,3)])
    >>> initial_state = State(positions)
    >>> initial_state.get_clear()
    (2,2)
    """
    for s in self.positions:
      if s[0] == "clear":
        return (s[2], s[3])

  def get_number(self, i, j):
    """
    Description
    -----------
    Return the number block in given position.
    Note that number 0 (zero) is from a "clear" position.

    Example
    -------
    >>> positions = set([("on",1,1,1), ("on",2,1,2), ("on",3,1,3),("on",8,2,1), ("clear",0,2,2), ("on",4,2,3),("on",7,3,1), ("on",6,3,2), ("on",5,3,3)])
    >>> initial_state = State(positions)
    >>> initial_state.get_number(3,2)
    6
    """
    for s in self.positions:
      if (s[2] == i) and (s[3] == j):
        return s[1]

  def get_possible_moves(self):
    """
    Description
    -----------
    Return all possible moves that can be done given the clear block position.
    The moves operator are computed by filling the clear position with valid surrounded number blocks.

    Example
    -------
    >>> positions = set([("on",1,1,1), ("on",2,1,2), ("on",3,1,3),("on",8,2,1), ("clear",0,2,2), ("on",4,2,3),("on",7,3,1), ("on",6,3,2), ("on",5,3,3)])
    >>> initial_state = State(positions)
    >>> initial_state.get_possible_moves(2,2)
    {('move', 8, 2, 2, 2, 1), ('move', 6, 2, 2, 3, 2), ('move', 2, 2, 2, 1, 2), ('move', 4, 2, 2, 2, 3)}
    """
    ci, cj = self.get_clear()
    possible_moves = set()
    # Test for moving up operation
    if (ci - 1) > 0:
      n = self.get_number(ci - 1, cj)
      possible_moves.add( ("move", n, ci, cj, ci - 1, cj) )
    # Test for moving down operation
    if (ci + 1) < 4:
      n = self.get_number(ci + 1, cj)
      possible_moves.add( ("move", n, ci, cj, ci + 1, cj) )
    # Test for moving left to right operation
    if (cj - 1) > 0:
      n = self.get_number(ci, cj - 1)
      possible_moves.add( ("move", n, ci, cj, ci, cj - 1) )
    # Test for moving right to left operation
    if (cj + 1) < 4:
      n = self.get_number(ci, cj + 1)
      possible_moves.add( ("move", n, ci, cj, ci, cj + 1) )
    return possible_moves

  def copy(self):
    """
    Description
    -----------
    Standard function for copying the position set.
    """
    return State(self.positions.copy())
  
  def remove(self, el):
    """
    Description
    -----------
    Standard function for removing an element from the position set.
    """
    self.positions.remove(el)

  def add(self, el):
    """
    Description
    -----------
    Standard function for adding an element the position set.
    """
    self.positions.add(el)



class Strips:
  """
  This describes a problem using the STRIPS algorithm language.
  """
  def __init__(self, initial_state, max_elaps_time=5):
    """
    Description
    -----------
    Defines a STRIP instance for solving the 8-puzzle problem.
    The initial state is necessary. The goal state is always the same.
    The operators are always the same (given the rules of the 8-puzzle game).

    Example
    -------
    >>> positions = set([("on",1,1,1), ("on",2,1,2), ("on",3,1,3),("on",8,2,1), ("clear",0,2,2), ("on",4,2,3),("on",7,3,1), ("on",6,3,2), ("on",5,3,3)])
    >>> initial_state = State(positions)
    >>> s = Strips(initial_state)
    """
    self.initial_state = initial_state
    self.max_elaps_time = max_elaps_time
    # Computing all possible operators
    possible_operators = []
    for x in range(1,9):
      for i in range(1,4):
        for j in range(1,4):
          if (i - 1) > 0:
            possible_operators.append( ("move", x, i, j, i - 1, j) )
          if (i + 1) < 4:
            possible_operators.append( ("move", x, i, j, i + 1, j) )
          if (j - 1) > 0:
            possible_operators.append( ("move", x, i, j, i, j - 1) )
          if (j + 1) < 4:
            possible_operators.append( ("move", x, i, j, i, j + 1) )

    operators = {}
    for move in possible_operators:
      operators[("move", move[1], move[2], move[3], move[4], move[5])] = {
              "preconditions": set([("on",move[1],move[2],move[3]), ("clear",0,move[4], move[5])]),
              "add": set([("on",move[1],move[4],move[5]), ("clear",0,move[2], move[3])]),
              "remove": set([("on",move[1],move[2],move[3]), ("clear",0,move[4], move[5])])
            }
    self.operators = operators
    self.goal_state = State(set([("on",1,1,1), ("on",2,1,2), ("on",3,1,3),("on",8,2,1), ("clear",0,2,2), ("on",4,2,3),("on",7,3,1), ("on",6,3,2), ("on",5,3,3)]))
    # The current state can be modified during execution
    self.current_state = self.goal_state.copy()

  def update_current_state(self, move):
    """
    Description
    -----------
    Return the previous game state given a move.
    The returned state is considered the current one now.
    Remember that STRIPS go backwards, so the new state is suppose to be the one where the move was applied to reach the current state.

    Example
    -------
    >>> positions = set([("on",1,1,1), ("on",2,1,2), ("on",3,1,3),("on",8,2,1), ("clear",0,2,2), ("on",4,2,3),("on",7,3,1), ("on",6,3,2), ("on",5,3,3)])
    >>> initial_state = State(positions)
    >>> s = Strips(initial_state)
    >>> s.update_current_state(("move",8,2,1,2,2)).positions
    {('on', 3, 1, 3), ('on', 2, 1, 2), ('on', 4, 2, 3), ('on', 6, 3, 2), ('clear', 0, 2, 2), ('on', 7, 3, 1), ('on', 5, 3, 3), ('on', 8, 2, 1), ('on', 1, 1, 1)}
    """
    updated_current_state = self.current_state.copy()
    for s in self.current_state.positions:
      if ( (s[2] == move[2]) and (s[3] == move[3]) ) or ( (s[2] == move[4]) and (s[3] == move[5])):
        updated_current_state.remove(s)
    for pc in self.operators[move]["preconditions"]:
      updated_current_state.add(pc)
    return updated_current_state

  def pick_move(self, possible_moves):
    """
    Description
    -----------
    Computer the bes move given a set of possible moves.
    This "best" move is chosen based on the closer the move will make the previous sate to be to the initial state.
    In case of a tie, the best move is randomly chosen.

    Example
    -------
    >>> positions = set([("on",1,1,1), ("on",2,1,2), ("on",3,1,3),("on",8,2,1), ("clear",0,2,2), ("on",4,2,3),("on",7,3,1), ("on",6,3,2), ("on",5,3,3)])
    >>> initial_state = State(positions)
    >>> s = Strips(initial_state)
    >>> s.pick_move(set([('move', 8, 2, 2, 2, 1), ('move', 6, 2, 2, 3, 2), ('move', 2, 2, 2, 1, 2), ('move', 4, 2, 2, 2, 3)]))
    ('move', 4, 2, 2, 2, 3)
    """
    winner = set()
    winner_points = -1
    for move in possible_moves:
      pc = self.operators[move]["preconditions"]
      move_pts = len(pc.intersection(self.initial_state.positions))
      if move_pts > winner_points:
        winner = set()
        winner.add(move)
        winner_points = move_pts
      elif move_pts == winner_points:
        winner.add(move)
    return choice(list(winner))

  def run(self, verbose=True):
    """
    Description
    -----------
    Performs the STRIP algorithm from the goal state to the initial one.
    If a solution was found, True is the first return value and the second is the list of operations applied.
    If no solution was found, that is the maximum elapsed time is reached, False and an empty list of operations is returned.

    Example
    -------
    >>> positions = set([("on",1,1,1), ("on",2,1,2), ("on",3,1,3),("on",8,2,1), ("clear",0,2,2), ("on",4,2,3),("on",7,3,1), ("on",6,3,2), ("on",5,3,3)])
    >>> initial_state = State(positions)
    >>> s = Strips(initial_state)
    >>> s.run()
    (True, [('move', 8, 3, 1, 2, 1), ('move', 7, 3, 2, 3, 1), ('move', 6, 2, 2, 3, 2)])
    """
    tic = time()
    has_solution = True
    performed_operations = []
    while len(self.current_state.positions.intersection(self.initial_state.positions)) < 9:
      possible_moves = self.current_state.get_possible_moves()
      chosen_move = self.pick_move(possible_moves)
      performed_operations.append(chosen_move)
      self.current_state = self.update_current_state(chosen_move)
      tac = time()
      time_diff = tac - tic
      if time_diff > self.max_elaps_time:
        has_solution = False
        break
      if verbose:
        print(">>> Elapsed time: {:.4f} (s)".format(time_diff))
    if has_solution:
        performed_operations.reverse()
    return (has_solution, performed_operations)

