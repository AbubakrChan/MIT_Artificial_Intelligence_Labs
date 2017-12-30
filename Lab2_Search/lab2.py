# MIT 6.034 Lab 2: Search
# Written by 6.034 staff

from search import Edge, UndirectedGraph, do_nothing_fn, make_generic_search
import read_graphs
from functools import reduce

all_graphs = read_graphs.get_graphs()
GRAPH_0 = all_graphs['GRAPH_0']
GRAPH_1 = all_graphs['GRAPH_1']
GRAPH_2 = all_graphs['GRAPH_2']
GRAPH_3 = all_graphs['GRAPH_3']
GRAPH_FOR_HEURISTICS = all_graphs['GRAPH_FOR_HEURISTICS']


# Please see wiki lab page for full description of functions and API.

#### PART 1: Helper Functions ##################################################

def path_length(graph, path):
    """Returns the total length (sum of edge weights) of a path defined by a
    list of nodes coercing an edge-linked traversal through a graph.
    (That is, the list of nodes defines a path through the graph.)
    A path with fewer than 2 nodes should have length of 0.
    You can assume that all edges along the path have a valid numeric weight."""
    if len(path) < 2:
        return 0

    length = 0
    for i, node in enumerate(path[:-1]):
        edge = graph.get_edge(node, path[i + 1])
        length += edge.length

    return length

def has_loops(path):
    """Returns True if this path has a loop in it, i.e. if it
    visits a node more than once. Returns False otherwise."""
    if (len(path) == len(set(path))):
        return False
    else:
        return True

def extensions(graph, path):
    """Returns a list of paths. Each path in the list should be a one-node
    extension of the input path, where an extension is defined as a path formed
    by adding a neighbor node (of the final node in the path) to the path.
    Returned paths should not have loops, i.e. should not visit the same node
    twice. The returned paths should be sorted in lexicographic order."""
    neighbors = graph.get_neighbors(path[-1])
    paths = []
    for neighbor in sorted(neighbors):
        if neighbor not in path:
            new_path = path[:]
            new_path.append(neighbor)
            paths.append(new_path)

    return paths


def sort_by_heuristic(graph, goalNode, nodes):
    """Given a list of nodes, sorts them best-to-worst based on the heuristic
    from each node to the goal node. Here, and in general for this lab, we
    consider a smaller heuristic value to be "better" because it represents a
    shorter potential path to the goal. Break ties lexicographically by 
    node name."""
    def heuristic(node):
        return graph.get_heuristic_value(node, goalNode)

    return sorted(nodes, key=lambda t: (heuristic(t), t))

# You can ignore the following line.  It allows generic_search (PART 3) to
# access the extensions and has_loops functions that you just defined in PART 1.
generic_search = make_generic_search(extensions, has_loops)  # DO NOT CHANGE


#### PART 2: Basic Search ######################################################

def basic_dfs(graph, start, goal):
    """
    Performs a depth-first search on a graph from a specified start
    node to a specified goal node, returning a path-to-goal if it
    exists, otherwise returning None.
    Uses backtracking, but does not use an extended set.
    """
    stack = [[start]]
    while len(stack) > 0 and stack[0][-1] != goal:
        current_path = stack.pop(0)
        connected = extensions(graph, current_path)
        stack = connected + stack

    if len(stack) > 0:
        return stack[0]
    else:
        return None


def basic_bfs(graph, start, goal):
    """
    Performs a breadth-first search on a graph from a specified start
    node to a specified goal node, returning a path-to-goal if it
    exists, otherwise returning None.
    """
    queue = [[start]]
    while len(queue) > 0 and queue[0][-1] != goal:
        current_path = queue.pop(0)
        connected = extensions(graph, current_path)
        queue = queue + connected

    if len(queue) > 0:
        return queue[0]
    else:
        return None


#### PART 3: Generic Search ####################################################

# Generic search requires four arguments (see wiki for more details):
# sort_new_paths_fn: a function that sorts new paths that are added to the agenda
# add_paths_to_front_of_agenda: True if new paths should be added to the front of the agenda
# sort_agenda_fn: function to sort the agenda after adding all new paths 
# use_extended_set: True if the algorithm should utilize an extended set


# Define your custom path-sorting functions here.
# Each path-sorting function should be in this form:
# def my_sorting_fn(graph, goalNode, paths):
#     # YOUR CODE HERE
#     return sorted_paths


def break_ties(paths):
    return sorted(paths)

generic_dfs = [do_nothing_fn, True, do_nothing_fn, False]

generic_bfs = [do_nothing_fn, False, do_nothing_fn, False]

def sort_hill_climbing(graph, goalNode, paths):
    paths_copy = paths[:]
    def heuristic(path):
        return graph.get_heuristic_value(path[-1], goalNode)

    return sorted(paths_copy, key=lambda path: (heuristic(path), path[-1]))

generic_hill_climbing = [sort_hill_climbing, True, do_nothing_fn, False]


def sort_best_first(graph, goalNode, agenda):
    agenda_copy = agenda[:]

    def heuristic(path):
        return graph.get_heuristic_value(path[-1], goalNode)

    agenda_copy = break_ties(agenda)
    return sorted(agenda_copy, key=heuristic)

generic_best_first = [do_nothing_fn, True, sort_best_first, False]


def sort_branch_and_bound(graph, goalNode, agenda):
    return sorted(agenda, key=lambda path: path_length(graph, path))

generic_branch_and_bound = [do_nothing_fn, False, sort_branch_and_bound, False]


def sort_branch_and_bound_with_heuristic(graph, goalNode, agenda):
    def heuristic(path):
        return graph.get_heuristic_value(path[-1], goalNode)

    return sorted(agenda, key=lambda path: path_length(graph, path) + heuristic(path))


generic_branch_and_bound_with_heuristic = [do_nothing_fn, False, sort_branch_and_bound_with_heuristic, False]

generic_branch_and_bound_with_extended_set = [do_nothing_fn, False, sort_branch_and_bound, True]

generic_a_star = [do_nothing_fn, False, sort_branch_and_bound_with_heuristic, True]


# Here is an example of how to call generic_search (uncomment to run):
# my_dfs_fn = generic_search(*generic_dfs)
# my_dfs_path = my_dfs_fn(GRAPH_2, 'S', 'G')
# print(my_dfs_path)

# Or, combining the first two steps:
# my_dfs_path = generic_search(*generic_dfs)(GRAPH_2, 'S', 'G')
# print(my_dfs_path)


### OPTIONAL: Generic Beam Search

# If you want to run local tests for generic_beam, change TEST_GENERIC_BEAM to True:
TEST_GENERIC_BEAM = True

# The sort_agenda_fn for beam search takes fourth argument, beam_width:
def my_beam_sorting_fn(graph, goalNode, paths, beam_width):
    if not paths:
        return []
    current_level = len(paths[-1])
    level_extended = True
    for path in paths:
        has_extensions = len(graph.get_neighbors(path[-1])) > 0
        if len(path) == (current_level - 1) and has_extensions:
            level_extended = False

    if not level_extended:
        return paths

    def heuristic(path):
        return graph.get_heuristic_value(path[-1], goalNode)

    return sorted(paths, key=lambda path: heuristic(path))[:beam_width]


generic_beam = [do_nothing_fn, False, my_beam_sorting_fn, False]


# Uncomment this to test your generic_beam search:
# print(generic_search(*generic_beam)(GRAPH_2, 'S', 'G', beam_width=2))


#### PART 4: Heuristics ########################################################

def dijkstras(graph, start):
    queue = [(0, start)]
    distances = {start: 0}
    parents = {start: None}
    finished_set = {}
    while len(queue) > 0:
        tup = queue.pop(0)
        current_node = tup[1]
        original_distance = tup[0]
        finished_set[current_node] = True
        for node in graph.get_neighbors(current_node):
            if node not in finished_set:
                new_distance = original_distance + graph.get_edge(current_node, node).length
                if node in distances:
                    if new_distance < distances[node]:
                        distances[node] = new_distance
                        parents[node] = current_node
                        queue.append((new_distance, node))
                else:
                    distances[node] = new_distance
                    parents[node] = current_node
                    queue.append((new_distance, node))

        queue.sort(key=lambda tup: tup[0])
    return (distances, parents)


def is_admissible(graph, goalNode):
    """Returns True if this graph's heuristic is admissible; else False.
    A heuristic is admissible if it is either always exactly correct or overly
    optimistic; it never over-estimates the cost to the goal."""
    distances, parents = dijkstras(graph, goalNode)
    for node in graph.nodes:
        if distances[node] < graph.get_heuristic_value(node, goalNode):
            return False
    return True


def is_consistent(graph, goalNode):
    """Returns True if this graph's heuristic is consistent; else False.
    A consistent heuristic satisfies the following property for all
    nodes v in the graph:
        Suppose v is a node in the graph, and N is a neighbor of v,
        then, heuristic(v) <= heuristic(N) + edge_weight(v, N)
    In other words, moving from one node to a neighboring node never unfairly
    decreases the heuristic.
    This is equivalent to the heuristic satisfying the triangle inequality."""
    for edge in graph.edges:
        node1 = edge.startNode
        node2 = edge.endNode
        h1 = graph.get_heuristic_value(node1, goalNode)
        h2 = graph.get_heuristic_value(node2, goalNode)
        if abs(h1 - h2) > edge.length:
            return False
    return True


### OPTIONAL: Picking Heuristics

# If you want to run local tests on your heuristics, change TEST_HEURISTICS to True.
#  Note that you MUST have completed generic a_star in order to do this:
TEST_HEURISTICS = True


# heuristic_1: admissible and consistent

[h1_S, h1_A, h1_B, h1_C, h1_G] = [6, 6, 7, 5, 0]

heuristic_1 = {'G': {}}
heuristic_1['G']['S'] = h1_S
heuristic_1['G']['A'] = h1_A
heuristic_1['G']['B'] = h1_B
heuristic_1['G']['C'] = h1_C
heuristic_1['G']['G'] = h1_G


# heuristic_2: admissible but NOT consistent

[h2_S, h2_A, h2_B, h2_C, h2_G] = [6, 6, 8, 5, 0]

heuristic_2 = {'G': {}}
heuristic_2['G']['S'] = h2_S
heuristic_2['G']['A'] = h2_A
heuristic_2['G']['B'] = h2_B
heuristic_2['G']['C'] = h2_C
heuristic_2['G']['G'] = h2_G


# heuristic_3: admissible but A* returns non-optimal path to G
# generic_search(*generic_a_star)(GRAPH_FOR_HEURISTICS, 'S', 'G'))

[h3_S, h3_A, h3_B, h3_C, h3_G] = [1, 5, 4, 1, 0]

heuristic_3 = {'G': {}}
heuristic_3['G']['S'] = h3_S
heuristic_3['G']['A'] = h3_A
heuristic_3['G']['B'] = h3_B
heuristic_3['G']['C'] = h3_C
heuristic_3['G']['G'] = h3_G


# heuristic_4: admissible but not consistent, yet A* finds optimal path

[h4_S, h4_A, h4_B, h4_C, h4_G] = [6, 6, 8, 5, 0]

heuristic_4 = {'G': {}}
heuristic_4['G']['S'] = h4_S
heuristic_4['G']['A'] = h4_A
heuristic_4['G']['B'] = h4_B
heuristic_4['G']['C'] = h4_C
heuristic_4['G']['G'] = h4_G


##### PART 5: Multiple Choice ##################################################

ANSWER_1 = '2'

ANSWER_2 = '4'

ANSWER_3 = '1'

ANSWER_4 = '3'


#### SURVEY ####################################################################

NAME = 'Alejandro Gamboa'
COLLABORATORS = None
HOW_MANY_HOURS_THIS_LAB_TOOK = '3'
WHAT_I_FOUND_INTERESTING = 'Everything'
WHAT_I_FOUND_BORING = None
SUGGESTIONS = None



###########################################################
### Ignore everything below this line; for testing only ###
###########################################################

# The following lines are used in the online tester. DO NOT CHANGE!

generic_dfs_sort_new_paths_fn = generic_dfs[0]
generic_bfs_sort_new_paths_fn = generic_bfs[0]
generic_hill_climbing_sort_new_paths_fn = generic_hill_climbing[0]
generic_best_first_sort_new_paths_fn = generic_best_first[0]
generic_branch_and_bound_sort_new_paths_fn = generic_branch_and_bound[0]
generic_branch_and_bound_with_heuristic_sort_new_paths_fn = generic_branch_and_bound_with_heuristic[0]
generic_branch_and_bound_with_extended_set_sort_new_paths_fn = generic_branch_and_bound_with_extended_set[0]
generic_a_star_sort_new_paths_fn = generic_a_star[0]

generic_dfs_sort_agenda_fn = generic_dfs[2]
generic_bfs_sort_agenda_fn = generic_bfs[2]
generic_hill_climbing_sort_agenda_fn = generic_hill_climbing[2]
generic_best_first_sort_agenda_fn = generic_best_first[2]
generic_branch_and_bound_sort_agenda_fn = generic_branch_and_bound[2]
generic_branch_and_bound_with_heuristic_sort_agenda_fn = generic_branch_and_bound_with_heuristic[2]
generic_branch_and_bound_with_extended_set_sort_agenda_fn = generic_branch_and_bound_with_extended_set[2]
generic_a_star_sort_agenda_fn = generic_a_star[2]

# Creates the beam search using generic beam args, for optional beam tests
beam = generic_search(*generic_beam) if TEST_GENERIC_BEAM else None

# Creates the A* algorithm for use in testing the optional heuristics
if TEST_HEURISTICS:
    a_star = generic_search(*generic_a_star)
