# MIT Artificial Intelligence Labs

This is my Python implementation of all the labs of the subject 6.034 Artificial Intelligence at MIT during Fall Semester 2017.

To test the code just go the directory of the lab (using cd) and write: python3 tester.py

Note: Please let me know any suggestion or comment you could have about the code.

## Lab 0 - Getting Started
Warm up Functions
- def is_even(x):
      "If x is even, returns True; otherwise returns False"
- def decrement(x):
      "Given a number x, returns x - 1 unless that would be less than zero, in which case returns 0."
- def cube(x):
      "Given a number x, returns its cube (x^3)"      

Iteration Functions:
- def is_prime(x):
      "Given a number x, returns True if it is prime; otherwise returns False"
- def primes_up_to(x):
      "Given a number x, returns an in-order list of all primes up to and including x"

Recursion Functions:
- def fibonacci(n):
      "Given a positive int n, uses recursion to return the nth Fibonacci number."
- def expression_depth(expr):
      """Given an expression expressed as Python lists, uses recursion to return
      the depth of the expression, where depth is defined by the maximum number of
      nested operations."""
      Example: x^2 + y^2 as Python List in prefix notation is ['+', ['expt', 'x', 2], ['expt', 'y', 2]]

Built-in data types (strings, sets, lists, tuples and dictionaries):
- def remove_from_string(string, letters):
      """Given a string and a list of individual letters, returns a new string
      which is the same as the old one except all occurrences of those letters
      have been removed from it."""
- def compute_string_properties(string):
      """Given a string of lowercase letters, returns a tuple containing the
      following three elements:
          0. The length of the string
          1. A list of all the characters in the string (including duplicates, if
             any), sorted in REVERSE alphabetical order
          2. The number of distinct characters in the string (hint: use a set)
      """
- def tally_letters(string):
      """Given a string of lowercase letters, returns a dictionary mapping each
      letter to the number of times it occurs in the string."""     
 
Functions that return functions
- def create_multiplier_function(m):
      "Given a multiplier m, returns a function that multiplies its input by m."
- def create_length_comparer_function(check_equal):
      """Returns a function that takes as input two lists. If check_equal == True,
      this function will check if the lists are of equal lengths. If
      check_equal == False, this function will check if the lists are of different
      lengths."""      
 
Objects and APIs
- def sum_of_coordinates(point):
      """Given a 2D point (represented as a Point object), returns the sum
      of its X- and Y-coordinates."""
- def get_neighbors(point):
     """Given a 2D point (represented as a Point object), returns a list of the
     four points that neighbor it in the four coordinate directions. Uses the
     "copy" method to avoid modifying the original point."""       

Using the "key" argument
- def sort_points_by_Y(list_of_points):
      """Given a list of 2D points (represented as Point objects), uses "sorted"
      with the "key" argument to create and return a list of the SAME (not copied)
      points sorted in decreasing order based on their Y coordinates, without
      modifying the original list."""
- def furthest_right_point(list_of_points):
      """Given a list of 2D points (represented as Point objects), uses "max" with
      the "key" argument to return the point that is furthest to the right (that
      is, the point with the largest X coordinate)."""      

Note: These functions are implemented in the file lab0.py in the folder Lab0_GettingStarted   

# Lab 1 - Rule-Based Systems

Part 1: Multiple Choice
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
ANSWER_4 = '0'

Question 5: Consider the following set of assertions about Garfield.
assertions = ( 'Garfield is a hypothetical cat',
               'Garfield likes lasagna' )
Which rules would match in the first round of forward chaining? Answer with a string of numbers in ANSWER_5. If no rules match, answer '0'.
ANSWER_5 = '3'

ANSWER_6 = '1'

ANSWER_7 = '0'















