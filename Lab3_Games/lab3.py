# MIT 6.034 Lab 3: Games
# Written by 6.034 staff

from game_api import *
from boards import *
from toytree import GAME1
from collections import deque

INF = float('inf')

# Please see wiki lab page for full description of functions and API.

#### Part 1: Utility Functions #################################################

def is_game_over_connectfour(board):
    """Returns True if game is over, otherwise False."""
    if len(board.get_all_chains()):
      if game_won(board) or board_full(board):
        return True
    return False

def game_won(board, current_player=None):
    return max([len(chain) for chain in board.get_all_chains(current_player)]) >= 4

def board_full(board):
    return all([board.is_column_full(column_number) for column_number in range(board.num_cols)])

def next_boards_connectfour(board):
    """Returns a list of ConnectFourBoard objects that could result from the
    next move, or an empty list if no moves can be made."""
    if is_game_over_connectfour(board):
      return []
    else:
      return [board.add_piece(col) for col in range(board.num_cols) if not board.is_column_full(col)]

def endgame_score_connectfour(board, is_current_player_maximizer):
    """Given an endgame board, returns 1000 if the maximizer has won,
    -1000 if the minimizer has won, or 0 in case of a tie."""
    if board_full(board):
      return 0
    if game_won(board, current_player=True):
      return 1000 if is_current_player_maximizer else -1000
    else:
      return 1000 if not is_current_player_maximizer else -1000

def endgame_score_connectfour_faster(board, is_current_player_maximizer):
    """Given an endgame board, returns an endgame score with abs(score) >= 1000,
    returning larger absolute scores for winning sooner."""
    maximal_chains_player2 = board.get_all_chains(False)
    won_player2 = False
    for chain in maximal_chains_player2:
      if len(chain) >= 4:
        won_player2 = True

    if won_player2 and is_current_player_maximizer:
      return -1000 - (board.num_cols * board.num_rows - board.count_pieces(False))
    elif won_player2 and not is_current_player_maximizer:
      return 1000 + (board.num_cols * board.num_rows - board.count_pieces(False))
    else:
      return 0

def heuristic_connectfour(board, is_current_player_maximizer):
    """Given a non-endgame board, returns a heuristic score with
    abs(score) < 1000, where higher numbers indicate that the board is better
    for the maximizer."""
    score = sum([len(chain)*len(chain)*10 \
                 for chain in board.get_all_chains(current_player=True)]) - \
            sum([len(chain)*len(chain)*10 \
                 for chain in board.get_all_chains(current_player=False)])
    return score if is_current_player_maximizer else -score


# Now we can create AbstractGameState objects for Connect Four, using some of
# the functions you implemented above.  You can use the following examples to
# test your dfs and minimax implementations in Part 2.

# This AbstractGameState represents a new ConnectFourBoard, before the game has started:
state_starting_connectfour = AbstractGameState(snapshot = ConnectFourBoard(),
                                 is_game_over_fn = is_game_over_connectfour,
                                 generate_next_states_fn = next_boards_connectfour,
                                 endgame_score_fn = endgame_score_connectfour_faster)

# This AbstractGameState represents the ConnectFourBoard "NEARLY_OVER" from boards.py:
state_NEARLY_OVER = AbstractGameState(snapshot = NEARLY_OVER,
                                 is_game_over_fn = is_game_over_connectfour,
                                 generate_next_states_fn = next_boards_connectfour,
                                 endgame_score_fn = endgame_score_connectfour_faster)

# This AbstractGameState represents the ConnectFourBoard "BOARD_UHOH" from boards.py:
state_UHOH = AbstractGameState(snapshot = BOARD_UHOH,
                                 is_game_over_fn = is_game_over_connectfour,
                                 generate_next_states_fn = next_boards_connectfour,
                                 endgame_score_fn = endgame_score_connectfour_faster)


#### Part 2: Searching a Game Tree #############################################

# Note: Functions in Part 2 use the AbstractGameState API, not ConnectFourBoard.

def extensions(path):
    """Returns a list of paths. Each path in the list should be a one-node
    extension of the input path, where an extension is defined as a path formed
    by adding a neighbor node (of the final node in the path) to the path.
    Returned paths should not have loops, i.e. should not visit the same node
    twice. The returned paths should be sorted in lexicographic order."""
    neighbors = path[-1].generate_next_states()
    paths = []
    for neighbor in neighbors:
        if neighbor not in path:
            new_path = path[:]
            new_path.append(neighbor)
            paths.append(new_path)

    return paths

def dfs_maximizing(state) :
    """Performs depth-first search to find path with highest endgame score.
    Returns a tuple containing:
     0. the best path (a list of AbstractGameState objects),
     1. the score of the leaf node (a number), and
     2. the number of static evaluations performed (a number)"""
    stack = [[state]]
    best_path = []
    highest_score = 0
    static_evaluations = 0
    while len(stack) > 0:
      current_path = stack.pop(0)
      connected = extensions(current_path)
      if len(connected) == 0:
        static_evaluations += 1
        score = abs(current_path[-1].get_endgame_score())
        if score > highest_score:
          highest_score = score
          best_path = current_path

      stack = connected + stack

    return (best_path, highest_score, static_evaluations)


# Uncomment the line below to try your dfs_maximizing on an
# AbstractGameState representing the games tree "GAME1" from toytree.py:

# pretty_print_dfs_type(dfs_maximizing(GAME1))


def minimax_endgame_aux(state, evaluations, max=True):
    if state.is_game_over():
      return ([state], state.get_endgame_score(is_current_player_maximizer=max), evaluations + 1)

    best_value = -INF if max else INF
    best_path = []
    for new_state in state.generate_next_states():
      new_path, new_value, evaluations = minimax_endgame_aux(new_state, evaluations, not max)

      if (max and new_value > best_value) or (not max and new_value < best_value):
        best_path = new_path
        best_value = new_value

    best_path.append(state)
    return (best_path, best_value, evaluations)


def minimax_endgame_search(state, maximize=True) :
    """Performs minimax search, searching all leaf nodes and statically
    evaluating all endgame scores.  Same return type as dfs_maximizing."""
    best_path, best_value, evaluations = minimax_endgame_aux(state, evaluations=0, max=maximize)
    best_path.reverse()
    return [best_path, best_value, evaluations]


# Uncomment the line below to try your minimax_endgame_search on an
# AbstractGameState representing the ConnectFourBoard "NEARLY_OVER" from boards.py:

# pretty_print_dfs_type(minimax_endgame_search(state_NEARLY_OVER))


def minimax_search_aux(state, evaluations, function, depth, max=True):
    if state.is_game_over():
      return ([state], state.get_endgame_score(is_current_player_maximizer=max), evaluations + 1)
    elif depth == 0:
      return ([state], function(state.get_snapshot(), max), evaluations + 1)

    best_value = -INF if max else INF
    best_path = []
    for new_state in state.generate_next_states():
      new_path, new_value, evaluations = minimax_search_aux(new_state, evaluations, function, depth - 1, not max)

      if (max and new_value > best_value) or (not max and new_value < best_value):
        best_path = new_path
        best_value = new_value

    best_path.append(state)
    return (best_path, best_value, evaluations)


def minimax_search(state, heuristic_fn=always_zero, depth_limit=INF, maximize=True):
    """Performs standard minimax search. Same return type as dfs_maximizing."""
    best_path, best_value, evaluations = minimax_search_aux(state, evaluations=0, function=heuristic_fn, depth=depth_limit, max=maximize)
    best_path.reverse()
    return [best_path, best_value, evaluations]

# Uncomment the line below to try minimax_search with "BOARD_UHOH" and
# depth_limit=1. Try increasing the value of depth_limit to see what happens:

# pretty_print_dfs_type(minimax_search(state_UHOH, heuristic_fn=heuristic_connectfour, depth_limit=1))


def minimax_search_alphabeta_aux(state, evaluations, alpha, beta, function, depth, max=True):
  if state.is_game_over():
    return ([state], state.get_endgame_score(is_current_player_maximizer=max), evaluations + 1)
  elif depth == 0:
    return ([state], function(state.get_snapshot(), max), evaluations + 1)

  best_path = []
  for new_state in state.generate_next_states():
    new_path, new_value, evaluations = minimax_search_alphabeta_aux(new_state, evaluations, alpha, beta, function, depth - 1, not max)

    if (max and new_value > alpha) or (not max and new_value < beta):
      if max:
        alpha = new_value
      else:
        beta = new_value
      best_path = new_path

    if alpha >= beta:
      return (best_path, alpha if max else beta, evaluations)

  best_path.append(state)
  return (best_path, alpha if max else beta, evaluations)


def minimax_search_alphabeta(state, alpha=-INF, beta=INF, heuristic_fn=always_zero,
                             depth_limit=INF, maximize=True) :
    """"Performs minimax with alpha-beta pruning. Same return type
    as dfs_maximizing."""
    best_path, best_value, evaluations = minimax_search_alphabeta_aux(state, evaluations=0, alpha=alpha, beta=beta, function=heuristic_fn, depth=depth_limit, max=maximize)
    best_path.reverse()
    return [best_path, best_value, evaluations]


# Uncomment the line below to try minimax_search_alphabeta with "BOARD_UHOH" and
# depth_limit=4. Compare with the number of evaluations from minimax_search for
# different values of depth_limit.

# pretty_print_dfs_type(minimax_search_alphabeta(state_UHOH, heuristic_fn=heuristic_connectfour, depth_limit=4))


def progressive_deepening(state, heuristic_fn=always_zero, depth_limit=INF,
                          maximize=True) :
    """Runs minimax with alpha-beta pruning. At each level, updates anytime_value
    with the tuple returned from minimax_search_alphabeta. Returns anytime_value."""
    anytime_value = AnytimeValue()
    for depth in range(1, depth_limit + 1):
      new_best_option = minimax_search_alphabeta(state, alpha=-INF, beta=INF, heuristic_fn=heuristic_fn, depth_limit=depth, maximize=maximize)
      anytime_value.set_value(new_best_option)

    return anytime_value

# Uncomment the line below to try progressive_deepening with "BOARD_UHOH" and
# depth_limit=4. Compare the total number of evaluations with the number of
# evaluations from minimax_search or minimax_search_alphabeta.

# progressive_deepening(state_UHOH, heuristic_fn=heuristic_connectfour, depth_limit=4).pretty_print()


# Progressive deepening is NOT optional. However, you may find that 
#  the tests for progressive deepening take a long time. If you would
#  like to temporarily bypass them, set this variable False. You will,
#  of course, need to set this back to True to pass all of the local
#  and online tests.
TEST_PROGRESSIVE_DEEPENING = True
if not TEST_PROGRESSIVE_DEEPENING:
    def not_implemented(*args): raise NotImplementedError
    progressive_deepening = not_implemented


#### Part 3: Multiple Choice ###################################################

ANSWER_1 = '4'

ANSWER_2 = '1'

ANSWER_3 = '4'

ANSWER_4 = '5'


#### SURVEY ###################################################

NAME = 'Alejandro Gamboa'
COLLABORATORS = None
HOW_MANY_HOURS_THIS_LAB_TOOK = '10'
WHAT_I_FOUND_INTERESTING = 'I found this lab particularly challenging but made think in interesting solutions'
WHAT_I_FOUND_BORING = 'Nothing'
SUGGESTIONS = None
