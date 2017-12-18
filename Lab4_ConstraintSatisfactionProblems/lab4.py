# MIT 6.034 Lab 4: Constraint Satisfaction Problems
# Written by 6.034 staff

from constraint_api import *
from test_problems import get_pokemon_problem


#### Part 1: Warmup ############################################################

def has_empty_domains(csp) :
    """Returns True if the problem has one or more empty domains, otherwise False"""
    for variable in csp.variables:
        if not csp.get_domain(variable):
            return True
    return False

def check_all_constraints(csp) :
    """Return False if the problem's assigned values violate some constraint,
    otherwise True"""
    for cst in csp.constraints:
        var1 = cst.var1
        var2 = cst.var2
        if var1 in csp.assignments and var2 in csp.assignments:
            value1 = csp.get_assignment(var1)
            value2 = csp.get_assignment(var2)
            if not cst.check(value1, value2):
                return False
    return True

#### Part 2: Depth-First Constraint Solver #####################################

def solve_constraint_dfs(problem) :
    """
    Solves the problem using depth-first search.  Returns a tuple containing:
    1. the solution (a dictionary mapping variables to assigned values)
    2. the number of extensions made (the number of problems popped off the agenda).
    If no solution was found, return None as the first element of the tuple.
    """
    agenda = [problem]
    num_extensions = 0
    while agenda:
        currentProb = agenda.pop(0)
        num_extensions += 1
        if not has_empty_domains(currentProb):
            if check_all_constraints(currentProb):
                if not currentProb.unassigned_vars:
                    return (currentProb.assignments, num_extensions)
                first_noassign = currentProb.pop_next_unassigned_var()
                potential_solutions = []
                for value in currentProb.get_domain(first_noassign):
                    csp_copy = currentProb.copy()
                    csp_copy.set_assignment(first_noassign, value)
                    potential_solutions.append(csp_copy)
                potential_solutions.extend(agenda)
                agenda = potential_solutions
    return (None, num_extensions)


# QUESTION 1: How many extensions does it take to solve the Pokemon problem
#    with DFS?

# Hint: Use get_pokemon_problem() to get a new copy of the Pokemon problem
#    each time you want to solve it with a different search method.

ANSWER_1 = solve_constraint_dfs(get_pokemon_problem())[1]


#### Part 3: Forward Checking ##################################################

def eliminate_from_neighbors(csp, var) :
    """
    Eliminates incompatible values from var's neighbors' domains, modifying
    the original csp.  Returns an alphabetically sorted list of the neighboring
    variables whose domains were reduced, with each variable appearing at most
    once.  If no domains were reduced, returns empty list.
    If a domain is reduced to size 0, quits immediately and returns None.
    """
    modified = []
    for neighbor in csp.get_neighbors(var):
        constraints = csp.constraints_between(var, neighbor)
        to_eliminate = []

        for neighbor_val in csp.get_domain(neighbor):
            inconsistent_with_value = True
            for var_val in csp.get_domain(var):
                if all([constraint.check(var_val, neighbor_val) for constraint in constraints]):
                    inconsistent_with_value = False

            if inconsistent_with_value:
                to_eliminate.append(neighbor_val)

        if to_eliminate:
            for value in to_eliminate:
                csp.eliminate(neighbor, value)
            if csp.get_domain(neighbor) == []:
                return None
            modified.append(neighbor)

    modified.sort()
    return modified

# Because names give us power over things (you're free to use this alias)
forward_check = eliminate_from_neighbors

def solve_constraint_forward_checking(problem) :
    """
    Solves the problem using depth-first search with forward checking.
    Same return type as solve_constraint_dfs.
    """
    agenda = [problem]
    num_extensions = 0
    while agenda:
        currentProb = agenda.pop(0)
        num_extensions += 1
        if not has_empty_domains(currentProb):
            if check_all_constraints(currentProb):
                if not currentProb.unassigned_vars:
                    return (currentProb.assignments, num_extensions)
                first_noassign = currentProb.pop_next_unassigned_var()
                potential_solutions = []
                for value in currentProb.get_domain(first_noassign):
                    csp_copy = currentProb.copy()
                    csp_copy.set_assignment(first_noassign, value)
                    eliminate_from_neighbors(csp_copy, first_noassign)
                    potential_solutions.append(csp_copy)
                potential_solutions.extend(agenda)
                agenda = potential_solutions
    return (None, num_extensions)


# QUESTION 2: How many extensions does it take to solve the Pokemon problem
#    with DFS and forward checking?

ANSWER_2 = solve_constraint_forward_checking(get_pokemon_problem())[1]


#### Part 4: Domain Reduction ##################################################

def domain_reduction(csp, queue=None) :
    """
    Uses constraints to reduce domains, propagating the domain reduction
    to all neighbors whose domains are reduced during the process.
    If queue is None, initializes propagation queue by adding all variables in
    their default order.
    Returns a list of all variables that were dequeued, in the order they
    were removed from the queue.  Variables may appear in the list multiple times.
    If a domain is reduced to size 0, quits immediately and returns None.
    This function modifies the original csp.
    """
    dequeued = []
    if queue == None:
        queue = csp.get_all_variables()
    while queue:
        var = queue.pop(0)
        dequeued.append(var)

        for neighbor in csp.get_neighbors(var):
            constraints = csp.constraints_between(var, neighbor)
            to_eliminate = []

            for neighbor_value in csp.get_domain(neighbor):
                insconsistency_with_value = True
                for var_value in csp.get_domain(var):
                    if all([constraint.check(var_value, neighbor_value) for constraint in constraints]):
                        insconsistency_with_value = False

                if insconsistency_with_value:
                    to_eliminate.append(neighbor_value)

            if to_eliminate:
                for value in to_eliminate:
                    csp.eliminate(neighbor, value)

                if csp.get_domain(neighbor) == []:
                    return None

                if neighbor is not queue:
                    queue.append(neighbor)

    return dequeued



# QUESTION 3: How many extensions does it take to solve the Pokemon problem
#    with DFS (no forward checking) if you do domain reduction before solving it?

csp = get_pokemon_problem()
domain_reduction(csp)
ANSWER_3 = solve_constraint_dfs(csp)[1]


def solve_constraint_propagate_reduced_domains(problem):
    """
    Solves the problem using depth-first search with forward checking and
    propagation through all reduced domains.  Same return type as
    solve_constraint_dfs.
    """
    agenda = [problem]
    num_extensions = 0
    while agenda:
        currentProb = agenda.pop(0)
        num_extensions += 1
        if not has_empty_domains(currentProb):
            if check_all_constraints(currentProb):
                if not currentProb.unassigned_vars:
                    return (currentProb.assignments, num_extensions)
                first_noassign = currentProb.pop_next_unassigned_var()
                potential_solutions = []
                for value in currentProb.get_domain(first_noassign):
                    csp_copy = currentProb.copy()
                    csp_copy.set_assignment(first_noassign, value)
                    domain_reduction(csp_copy, [first_noassign])
                    potential_solutions.append(csp_copy)
                potential_solutions.extend(agenda)
                agenda = potential_solutions
    return (None, num_extensions)


# QUESTION 4: How many extensions does it take to solve the Pokemon problem
#    with forward checking and propagation through reduced domains?

ANSWER_4 = solve_constraint_propagate_reduced_domains(get_pokemon_problem())[1]


#### Part 5A: Generic Domain Reduction #########################################

def propagate(enqueue_condition_fn, csp, queue=None) :
    """
    Uses constraints to reduce domains, modifying the original csp.
    Uses enqueue_condition_fn to determine whether to enqueue a variable whose
    domain has been reduced. Same return type as domain_reduction.
    """
    dequeued = []
    if queue == None:
        queue = csp.get_all_variables()
    while queue:
        var = queue.pop(0)
        dequeued.append(var)

        for neighbor in csp.get_neighbors(var):
            constraints = csp.constraints_between(var, neighbor)
            to_eliminate = []

            for neighbor_value in csp.get_domain(neighbor):
                insconsistency_with_value = True
                for var_value in csp.get_domain(var):
                    if all([constraint.check(var_value, neighbor_value) for constraint in constraints]):
                        insconsistency_with_value = False

                if insconsistency_with_value:
                    to_eliminate.append(neighbor_value)

            if to_eliminate:
                for value in to_eliminate:
                    csp.eliminate(neighbor, value)

                if csp.get_domain(neighbor) == []:
                    return None

                if enqueue_condition_fn(csp, neighbor):
                    if neighbor is not queue:
                        queue.append(neighbor)

    return dequeued

def condition_domain_reduction(csp, var) :
    """Returns True if var should be enqueued under the all-reduced-domains
    condition, otherwise False"""
    return True

def condition_singleton(csp, var) :
    """Returns True if var should be enqueued under the singleton-domains
    condition, otherwise False"""
    return len(csp.get_domain(var)) == 1

def condition_forward_checking(csp, var) :
    """Returns True if var should be enqueued under the forward-checking
    condition, otherwise False"""
    return False


#### Part 5B: Generic Constraint Solver ########################################

def solve_constraint_generic(problem, enqueue_condition=None) :
    """
    Solves the problem, calling propagate with the specified enqueue
    condition (a function). If enqueue_condition is None, uses DFS only.
    Same return type as solve_constraint_dfs.
    """
    agenda = [problem]
    num_extensions = 0
    while agenda:
        currentProb = agenda.pop(0)
        num_extensions += 1
        if not has_empty_domains(currentProb):
            if check_all_constraints(currentProb):
                if not currentProb.unassigned_vars:
                    return (currentProb.assignments, num_extensions)
                first_noassign = currentProb.pop_next_unassigned_var()
                potential_solutions = []
                for value in currentProb.get_domain(first_noassign):
                    csp_copy = currentProb.copy()
                    csp_copy.set_assignment(first_noassign, value)
                    if enqueue_condition:
                        propagate(enqueue_condition, csp_copy, queue=[first_noassign])
                    potential_solutions.append(csp_copy)
                potential_solutions.extend(agenda)
                agenda = potential_solutions
    return (None, num_extensions)

# QUESTION 5: How many extensions does it take to solve the Pokemon problem
#    with forward checking and propagation through singleton domains? (Don't
#    use domain reduction before solving it.)

ANSWER_5 = solve_constraint_generic(get_pokemon_problem(), condition_singleton)[1]


#### Part 6: Defining Custom Constraints #######################################

def constraint_adjacent(m, n) :
    """Returns True if m and n are adjacent, otherwise False.
    Assume m and n are ints."""
    return abs(m - n) == 1

def constraint_not_adjacent(m, n) :
    """Returns True if m and n are NOT adjacent, otherwise False.
    Assume m and n are ints."""
    return abs(m - n) != 1

def all_different(variables) :
    """Returns a list of constraints, with one difference constraint between
    each pair of variables."""
    constraints_list = []
    for i, first_var in enumerate(variables):
        for second_var in variables[i+1:]:
            if first_var != second_var:
                new_constraint = Constraint(first_var, second_var, constraint_different)
                constraints_list.append(new_constraint)
    return constraints_list



#### SURVEY ####################################################################

NAME = 'Alejandro Gamboa'
COLLABORATORS = None
HOW_MANY_HOURS_THIS_LAB_TOOK = 4
WHAT_I_FOUND_INTERESTING = 'All the propagation algorithms'
WHAT_I_FOUND_BORING = None
SUGGESTIONS = None
