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

Built-in data types (strings, sets, lists and tuples):
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
      
 Note: These functions are implemented in lab0.py     
