# MIT Artificial Intelligence Labs

This is my Python implementation of all the labs of the subject 6.034 Artificial Intelligence at MIT during Fall Semester 2017.

To test the code just go the directory of the lab (using cd) and write: python3 tester.py

Note: Please let me know any suggestion or comment you could have about the code.

## Lab 0 - Getting Started
Warm up Functions
      
      def is_even(x):
          "If x is even, returns True; otherwise returns False"
          
      def decrement(x):
          "Given a number x, returns x - 1 unless that would be less than zero, in which case returns 0."
      
      def cube(x):
          "Given a number x, returns its cube (x^3)"      

Iteration Functions:
      
      def is_prime(x):
          "Given a number x, returns True if it is prime; otherwise returns False"

      def primes_up_to(x):
          "Given a number x, returns an in-order list of all primes up to and including x"

Recursion Functions:

      def fibonacci(n):
          "Given a positive int n, uses recursion to return the nth Fibonacci number."

      def expression_depth(expr):
          """Given an expression expressed as Python lists, uses recursion to return
          the depth of the expression, where depth is defined by the maximum number of
          nested operations."""
          Example: x^2 + y^2 as Python List in prefix notation is ['+', ['expt', 'x', 2], ['expt', 'y', 2]]

Built-in data types (strings, sets, lists, tuples and dictionaries):

      def remove_from_string(string, letters):
          """Given a string and a list of individual letters, returns a new string
          which is the same as the old one except all occurrences of those letters
          have been removed from it."""
      
      def compute_string_properties(string):
          """Given a string of lowercase letters, returns a tuple containing the
          following three elements:
             0. The length of the string
             1. A list of all the characters in the string (including duplicates, if
                any), sorted in REVERSE alphabetical order
             2. The number of distinct characters in the string (hint: use a set)
          """

      def tally_letters(string):
          """Given a string of lowercase letters, returns a dictionary mapping each
          letter to the number of times it occurs in the string."""     
 
Functions that return functions

      def create_multiplier_function(m):
          "Given a multiplier m, returns a function that multiplies its input by m."
      
      def create_length_comparer_function(check_equal):
          """Returns a function that takes as input two lists. If check_equal == True,
          this function will check if the lists are of equal lengths. If
          check_equal == False, this function will check if the lists are of different
          lengths."""      
 
Objects and APIs

      def sum_of_coordinates(point):
          """Given a 2D point (represented as a Point object), returns the sum
          of its X- and Y-coordinates."""
          
      def get_neighbors(point):
          """Given a 2D point (represented as a Point object), returns a list of the
          four points that neighbor it in the four coordinate directions. Uses the
          "copy" method to avoid modifying the original point."""       

Using the "key" argument
      
      def sort_points_by_Y(list_of_points):
          """Given a list of 2D points (represented as Point objects), uses "sorted"
          with the "key" argument to create and return a list of the SAME (not copied)
          points sorted in decreasing order based on their Y coordinates, without
          modifying the original list."""

      def furthest_right_point(list_of_points):
          """Given a list of 2D points (represented as Point objects), uses "max" with
          the "key" argument to return the point that is furthest to the right (that
          is, the point with the largest X coordinate)."""      

Note: These functions are implemented in the file lab0.py in the folder Lab0_GettingStarted   


## Lab 1 - Rule-Based Systems

### Part 1: Multiple Choice
- Question 1: In forward chaining, after all the variables in a rule have been bound, which part of the rule may appear as a new assertion in the data?

      1. the antecedent
      2. the consequent
      3. both
      4. neither 

     **ANSWER_1 = '2'**

- Question 2: In backward chaining, after all the variables in a rule have been bound, which part of the rule may appear as a new assertion in the data?

      1. the antecedent
      2. the consequent
      3. both
      4. neither 
     **ANSWER_2 = '4'**

 Consider the following rules about hypothetical cats.
 
      rule1 = IF( AND( '(?x) is a hypothetical cat',<br />
                       '(?x) is alive',<br />
                       NOT('(?x) is alive')),<br /> 
                  THEN( '(?x) is a paradox' ) ) 

      rule2 = IF( AND( '(?x) is a hypothetical cat',
                       '(?x) is alive',
                       '(?x) is dead'),
                  THEN( "(?x) is Schrodinger's cat" ) )

      rule3 = IF( AND( '(?x) is a hypothetical cat',
                       NOT('(?x) is alive'),
                       NOT('(?x) is dead')),
                  THEN( '(?x) is amortal' ) )

- Question 3: Consider the following set of assertions about Kitty.

      assertions = ( 'Kitty is a hypothetical cat',
                     'Kitty is alive',
                     'Kitty is dead' )
                     
  Which rules would match in the first round of forward chaining? Answer with a string of numbers in ANSWER_3. (For example, if
  the assertions match rule1 and rule2, answer '12'.) If no rules match, answer '0'. 
   
   **ANSWER_3 = '2'**

- Question 4: Consider the following set of assertions about Nyan.

      assertions = ( 'Nyan is a hypothetical cat',
                     'Nyan is alive',
                     'Nyan is not alive' )

  Which rules would match in the first round of forward chaining? Answer with a string of numbers in ANSWER_4. If no rules match, answer '0'.

  **ANSWER_4 = '0'**

- Question 5: Consider the following set of assertions about Garfield.

      assertions = ( 'Garfield is a hypothetical cat',
                     'Garfield likes lasagna' )

  Which rules would match in the first round of forward chaining? Answer with a string of numbers in ANSWER_5. If no rules match, answer '0'.

  **ANSWER_5 = '3'**

  In a completely different scenario, suppose we have the following two rules:

      rule1 = IF( AND( '(?x) has feathers',
                       '(?x) has a beak' ),
             THEN( '(?x) is a bird' ))
      rule2 = IF( AND( '(?y) is a bird',
                       '(?y) cannot fly',
                       '(?y) can swim' ),
                  THEN( '(?y) is a penguin' ) )

  and the following list of initial data:

      ( 'Pendergast is a penguin',
      'Pendergast has feathers',
      'Pendergast has a beak',
      'Pendergast cannot fly',
      'Pendergast can swim' )

- Question 6: After starting the system, which rule fires first? In ANSWER_6, answer '1' or '2', or '0' if neither rule fires.
  
  **ANSWER_6 = '1'**

- Question 7: Which rule fires second? In ANSWER_7, answer '1' or '2', or '0' if neither rule fires. 

  **ANSWER_7 = '0'**

### Part 2: Poker Hands

You're given this data about poker hands:

      poker_data = [ 'two-pair beats pair',
                     'three-of-a-kind beats two-pair',
                     'straight beats three-of-a-kind',
                     'flush beats straight',
                     'full-house beats flush',
                     'straight-flush beats full-house' ]

Write a one-rule system that finds all other combinations of which poker hands beat which, transitively, given some of the rankings already. For example, it should be able to deduce that a three-of-a-kind beats a pair, because a three-of-a-kind beats two-pair and a two-pair beats a pair. The rankings (data) are all provided in the form '(?x) beats (?y)'. 

**ANSWER**

      transitive_rule = IF( AND( '(?x) beats (?y)',
                                 '(?y) beats (?z)'),
                            THEN( '(?x) beats (?z)' ))

### Part 3: Family relations 

You will be given data that includes two kinds of statements:

    'person (?x)': x is a person
    'parent (?x) (?y)': x is a parent of y 

Every person in the data set will be explicitly defined as a person.

Your task is to deduce, wherever you can, the following relations:

    'sibling (?x) (?y)': x is the sibling of y (x and y are different people, but share at least one parent)
    
    'child (?x) (?y)': x is the child of y
    
    'cousin (?x) (?y)': x and y are cousins (a parent of x and a parent of y are siblings, but x and y are not siblings)
    
    'grandparent (?x) (?y)': x is the grandparent of y
    
    'grandchild (?x) (?y)': x is the grandchild of y 

**ANSWER**

    friend_rule = IF( AND("person (?x)", "person (?y)"), THEN ("friend (?x) (?y)", "friend (?y) (?x)") )

    self = IF ( 'parent (?y) (?x)', THEN ('self (?x) (?x)') )

    sibling = IF ( AND('parent (?a) (?x)', 'parent (?a) (?y)', NOT('self (?x) (?y)')), THEN('sibling (?x) (?y)', 'sibling (?y) (?x)') )

    child = IF ( 'parent (?y) (?x)', THEN ('child (?x) (?y)') )

    cousin = IF ( AND('parent (?a) (?x)', 'parent (?b) (?y)', 'sibling (?a) (?b)'), THEN('cousin (?x) (?y)') )

    grandparent = IF ( AND('parent (?a) (?y)', 'parent (?x) (?a)'), THEN('grandparent (?x) (?y)') )

    grandchild = IF ( 'grandparent (?x) (?y)', THEN('grandchild (?y) (?x)') )

### Part 4: Backward Chaining

      def backchain_to_goal_tree(rules, hypothesis):
          """
          Takes a hypothesis (string) and a list of rules (list
          of IF objects), returning an AND/OR tree representing the
          backchain of possible statements we may need to test
          to determine if this hypothesis is reachable or not.

          This method should return an AND/OR tree, that is, an
          AND or OR object, whose constituents are the subgoals that
          need to be tested. The leaves of this tree should be strings
          (possibly with unbound variables), *not* AND or OR objects.
          Make sure to use simplify(...) to flatten trees where appropriate.
          """


## Lab 2 - Search

### Part 1: Utility Functions 

      def path_length(graph, path):
          """Returns the total length (sum of edge weights) of a path defined by a
          list of nodes coercing an edge-linked traversal through a graph.
          (That is, the list of nodes defines a path through the graph.)
          A path with fewer than 2 nodes should have length of 0.
          You can assume that all edges along the path have a valid numeric weight."""

      def has_loops(path):
          """Returns True if this path has a loop in it, i.e. if it
          visits a node more than once. Returns False otherwise."""

      def extensions(graph, path):
          """Returns a list of paths. Each path in the list should be a one-node
          extension of the input path, where an extension is defined as a path formed
          by adding a neighbor node (of the final node in the path) to the path.
          Returned paths should not have loops, i.e. should not visit the same node
          twice. The returned paths should be sorted in lexicographic order."""

      def sort_by_heuristic(graph, goalNode, nodes):
          """Given a list of nodes, sorts them best-to-worst based on the heuristic
          from each node to the goal node. Here, and in general for this lab, we
          consider a smaller heuristic value to be "better" because it represents a
          shorter potential path to the goal. Break ties lexicographically by 
          node name."""

### Part 2: Basic Search 

      def basic_dfs(graph, start, goal):
          """
          Performs a depth-first search on a graph from a specified start
          node to a specified goal node, returning a path-to-goal if it
          exists, otherwise returning None.
          Uses backtracking, but does not use an extended set.
          """

      def basic_bfs(graph, start, goal):
          """
          Performs a breadth-first search on a graph from a specified start
          node to a specified goal node, returning a path-to-goal if it
          exists, otherwise returning None.
          """
 
### Part 3: Generic Search 
 
Generic search requires four arguments:
- sort_new_paths_fn: a function that sorts new paths that are added to the agenda
- add_paths_to_front_of_agenda: True if new paths should be added to the front of the agenda
- sort_agenda_fn: function to sort the agenda after adding all new paths 
- use_extended_set: True if the algorithm should utilize an extended set

Please implement the following search algorithms by designing the correct arguments to pass to the generic search algorithm. Your answer to each should be an ordered list of the appropriate four arguments to generic_search. No argument should be None. 

generic_dfs = [None, None, None, None]
generic_bfs = [None, None, None, None]
generic_hill_climbing = [None, None, None, None]
generic_best_first = [None, None, None, None]
generic_branch_and_bound = [None, None, None, None]
generic_branch_and_bound_with_heuristic = [None, None, None, None]
generic_branch_and_bound_with_extended_set = [None, None, None, None]
generic_a_star = [None, None, None, None]
generic_beam = [None, None, None, None]

### Part 4: Heuristics

      def is_admissible(graph, goalNode):
          """Returns True if this graph's heuristic is admissible; else False.
          A heuristic is admissible if it is either always exactly correct or overly
          optimistic; it never over-estimates the cost to the goal."""

      def is_consistent(graph, goalNode):
          """Returns True if this graph's heuristic is consistent; else False.
          A consistent heuristic satisfies the following property for all
          nodes v in the graph:
          Suppose v is a node in the graph, and N is a neighbor of v,
          then, heuristic(v) <= heuristic(N) + edge_weight(v, N)
          In other words, moving from one node to a neighboring node never unfairly
          decreases the heuristic.
          This is equivalent to the heuristic satisfying the triangle inequality."""

### Part 5: Multiple Choice

- Question 1: You are in a new house and want to know where all the bedrooms are. You want to find the bedrooms as quickly as possible. Which algorithm should you use?

      1. Breadth First Search
      2. British Museum
      3. A*
      4. Branch and Bound with Extended Set
  
  **ANSWER_1 = '2'**

- Question 2: You are playing a game in which you are in a maze, and you are trying to exit. All the rooms are different colors, so you know which ones you've been in before, but there is no way of telling where you are in the maze with respect to the exit (until you reach the exit). You win the game if you exit the maze as quickly as possible. Which algorithm should you use?

      1. Breadth First Search
      2. British Museum
      3. A*
      4. Branch and Bound with Extended Set
  
  **ANSWER_2 = '4'**

- Question 3: Your friend Hammer is an amateur map-maker, and you have asked for directions for a route from your hometown of Oakvale to Bowerstone Marketplace. Your goal is to visit as few towns as possible along the way. Hammer is very bad at estimating distances and remembering where she's already been, so she wants to use the simplest algorithm possible to find what path you should take. Which algorithm should Hammer use?

      1. Breadth First Search
      2. British Museum
      3. A*
      4. Branch and Bound with Extended Set
  
  **ANSWER_3 = '1'**

- Question 4: Hammer goes to map-maker school and becomes better at distances and memory. Now you ask her for directions for the shortest distance from Bowerstone Marketplace to Silverpine. Which algorithm should Hammer use?

      1. Breadth First Search
      2. British Museum
      3. A*
      4. Branch and Bound with Extended Set
  
  **ANSWER_4 = '3'**      
