Description
-----------

This is the solution for Assignment 1 in CS820 - Artificial Intelligence.
The solution proposes an implementation of the STRIPS algorithm for solving the 8-puzzle problem.
There are 5 files in this solution:
  - strips.py: contains the main implementation of algorithms and utilities
  - run.py: utility for running a STRIP example
  - README: overview and instructions
  - initial_states.txt: input file for solving multiple 8-puzzle initial states
  - solution.txt: output file for solutions of input from initial_states.txt



How it Works
-------------
There are 3 run mode for this program
1) Interactive mode by argument
    - User input one initial state when calling the run.py program using the "-i" argument
2) Interactive mode standalone
    - User input one initial state using interactive menu when run.py without any argument
3) File mode
    - User input multiple initial states by calling run.py with a file name in "-f" argument
Notice that all state input is *comma separated* and with numbers filling the board from *top* to *down* and from *left* to *right* and *number zero* representing the clear block.
For example, an initial state 1,2,3,0,6,4,8,7,5 represents the following board configuration:


|---|---|---|
| 1 | 2 | 3 |
|   | 6 | 4 |
| 8 | 7 | 5 |

where the X is the clear block.



Getting Started
---------------

1) Interactive mode by argument:
$ python run.py -i 1,2,3,0,6,4,8,7,5
#
2) Interactive mode standalone
$ python run.py
#
3) File mode
$ python run.py -f initial_states.txt



Arguments
---------

There are 4 possible arguments when calling the run.py utility:
  - i, --initial-state: input one initial state with comma separated values and 0 representing clear block.
  -v, --verbose: hide all internal messages during STRIPS run. For example: elapsed running time. (Default=Show).
  -t, --time: set maximum time, in seconds, STRIPS can spend trying to solve an initial state. (Default=5s).
  -f, --file: file name with multiple initial states comma separated, one per line.

More information about arguments can be found by calling:
  $ python run.py --help



AUTHOR
---------
Jhonatan S. Oliveira
oliveira@uregina.ca
Department of Computer Science
University of Regina
Canada