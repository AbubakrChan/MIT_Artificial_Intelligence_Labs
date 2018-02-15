# MIT 6.034 Lab 8: Bayesian Inference
# Written by 6.034 staff

from nets import *


#### Part 1: Warm-up; Ancestors, Descendents, and Non-descendents ##############

def get_ancestors(net, var):
    "Return a set containing the ancestors of var"
    ancestors = set()
    for parent in net.get_parents(var):
        ancestors.add(parent)
        ancestors = ancestors.union(get_ancestors(net, parent))

    return ancestors

def get_descendants(net, var):
    "Returns a set containing the descendants of var"
    descendants = set()
    for children in net.get_children(var):
        descendants.add(children)
        descendants = descendants.union(get_descendants(net, children))

    return descendants

def get_nondescendants(net, var):
    "Returns a set containing the non-descendants of var"
    nondescendants = set()
    descendants = get_descendants(net, var)
    for node in net.topological_sort():
        if node not in descendants:
            nondescendants.add(node)

    nondescendants.remove(var)
    return nondescendants

#### Part 2: Computing Probability #############################################

def simplify_givens(net, var, givens):
    """
    If givens include every parent of var and no descendants, returns a
    simplified list of givens, keeping only parents.  Does not modify original
    givens.  Otherwise, if not all parents are given, or if a descendant is
    given, returns original givens.
    """
    if not net.get_parents(var).issubset(givens.keys()) or not get_descendants(net, var).isdisjoint(givens.keys()):
        return givens

    new_givens = dict(givens)
    for variable in givens.keys():
        if variable not in net.get_parents(var):
            del new_givens[variable]

    return new_givens

def probability_lookup(net, hypothesis, givens=None):
    "Looks up a probability in the Bayes net, or raises LookupError"
    if givens is not None:
        givens = simplify_givens(net, list(hypothesis)[0], givens)
    try:
        return net.get_probability(hypothesis, givens)
    except ValueError:
        raise LookupError

def probability_joint(net, hypothesis):
    "Uses the chain rule to compute a joint probability"
    toposorted = net.topological_sort()
    toposorted = toposorted[::-1]
    givens = dict(hypothesis)
    p = 1

    for variable in toposorted:
        del givens[variable]
        p *= probability_lookup(net, {variable: hypothesis[variable]}, givens)

    return p
    
def probability_marginal(net, hypothesis):
    "Computes a marginal probability as a sum of joint probabilities"
    combinations = net.combinations(net.variables, hypothesis)
    p = 0

    for combination in combinations:
        p += probability_joint(net, combination)

    return p

def probability_conditional(net, hypothesis, givens=None):
    "Computes a conditional probability as a ratio of marginal probabilities"
    if givens == None:
        return probability_marginal(net, hypothesis)

    if givens == hypothesis:
        return 1

    for variable in hypothesis:
        if variable in givens and hypothesis[variable] != givens[variable]:
            return 0

    d3 = dict(hypothesis, **givens)
    return float(probability_marginal(net, d3)) / float(probability_marginal(net, givens))
    
def probability(net, hypothesis, givens=None):
    "Calls previous functions to compute any probability"
    return probability_conditional(net, hypothesis, givens)


#### Part 3: Counting Parameters ###############################################

def number_of_parameters(net):
    """
    Computes the minimum number of parameters required for the Bayes net.
    """
    num_params = 0
    for variable in net.topological_sort():
        num_params += product([len(net.get_domain(i))
                               for i in net.get_parents(variable)]) * (len(net.get_domain(variable)) - 1)

    return num_params


#### Part 4: Independence ######################################################

def is_independent(net, var1, var2, givens=None):
    """
    Return True if var1, var2 are conditionally independent given givens,
    otherwise False. Uses numerical independence.
    """
    for combination1 in net.get_domain(var1):
        for combination2 in net.get_domain(var2):
            if givens == None:
                # Check if var1 and var2 are marginally independent
                prob1 = probability(net, {var1: combination1}, {var2: combination2})
                prob2 = probability(net, {var1: combination1})
            else:
                # Check if var1 and var2 are conditionally independent
                d3 = dict({var2: combination2}, **givens)
                prob1 = probability(net, {var1: combination1}, d3)
                prob2 = probability(net, {var1: combination1}, givens)

            if not approx_equal(prob1, prob2):
                return False

    return True
    
def is_structurally_independent(net, var1, var2, givens=None):
    """
    Return True if var1, var2 are conditionally independent given givens,
    based on the structure of the Bayes net, otherwise False.
    Uses structural independence only (not numerical independence).
    """
    # Draw the ancestral graph
    graph_variables = set()
    graph_variables.add(var1)
    graph_variables.add(var2)
    graph_variables.update(get_ancestors(net, var1))
    graph_variables.update(get_ancestors(net, var2))

    if givens != None:
        for variable in givens:
            if net.find_path(var1, variable) != None:
                graph_variables.update(net.find_path(var1, variable))
            if net.find_path(var2, variable) != None:
                graph_variables.update(net.find_path(var2, variable))

    newnet = net.subnet(graph_variables)

    # “Moralize” the ancestral graph by “marrying” the parents.
    copy = newnet.copy()
    visited = set()

    for variable in copy.topological_sort()[::-1]:
        parents = list(copy.get_parents(variable))
        if len(parents) > 1:
            for i in range(len(parents) - 1):
                for j in range(i + 1, len(parents)):
                    if parents[i] not in visited and parents[j] not in visited:
                        newnet.link(parents[i], parents[j])
                        visited.add(parents[i])
                        visited.add(parents[j])

    # "Disorient" the graph by replacing the directed edges with undirected edges
    newnet.make_bidirectional()

    # Delete the givens and their edges
    if givens != None:
        for variable in givens:
            if variable in newnet.get_variables():
                newnet.remove_variable(variable)

    if newnet.find_path(var1, var2) == None:
        return True

    return False



#### SURVEY ####################################################################

NAME = 'Alejandro Gamboa'
COLLABORATORS = None
HOW_MANY_HOURS_THIS_LAB_TOOK = 5
WHAT_I_FOUND_INTERESTING = 'Everything. Programming Bayes Nets is really cool.'
WHAT_I_FOUND_BORING = None
SUGGESTIONS = None
