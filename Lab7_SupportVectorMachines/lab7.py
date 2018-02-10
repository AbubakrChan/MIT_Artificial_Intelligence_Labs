# MIT 6.034 Lab 7: Support Vector Machines
# Written by 6.034 staff

from svm_data import *
import math
from functools import reduce


#### Part 1: Vector Math #######################################################

def dot_product(u, v):
    """Computes the dot product of two vectors u and v, each represented 
    as a tuple or list of coordinates. Assume the two vectors are the
    same length."""
    dot_product = 0
    for u_coord, v_coord in zip(u,v):
        dot_product += u_coord * v_coord

    return dot_product

def norm(v):
    """Computes the norm (length) of a vector v, represented 
    as a tuple or list of coords."""
    return math.sqrt(dot_product(v, v))


#### Part 2: Using the SVM Boundary Equations ##################################

def positiveness(svm, point):
    """Computes the expression (w dot x + b) for the given Point x."""
    return dot_product(svm.w, point.coords) + svm.b

def classify(svm, point):
    """Uses the given SVM to classify a Point. Assume that the point's true
    classification is unknown.
    Returns +1 or -1, or 0 if point is on boundary."""
    classification = positiveness(svm, point)
    if classification == 0:
        return 0
    else:
        return 1 if classification > 0 else -1

def margin_width(svm):
    """Calculate margin width based on the current boundary."""
    return 2 / norm(svm.w)

def check_gutter_constraint(svm):
    """Returns the set of training points that violate one or both conditions:
        * gutter constraint (positiveness == classification, for support vectors)
        * training points must not be between the gutters
    Assumes that the SVM has support vectors assigned."""
    illegal_points = []
    for point in svm.support_vectors:
        if positiveness(svm, point) != point.classification:
            illegal_points.append(point)

    for point in svm.training_points:
        if abs(positiveness(svm, point)) < 1:
            illegal_points.append(point)

    return set(illegal_points)



#### Part 3: Supportiveness ####################################################

def check_alpha_signs(svm):
    """Returns the set of training points that violate either condition:
        * all non-support-vector training points have alpha = 0
        * all support vectors have alpha > 0
    Assumes that the SVM has support vectors assigned, and that all training
    points have alpha values assigned."""
    illegal_points = []
    for point in svm.training_points:
        is_support_vector = True if point in svm.support_vectors else False
        if not is_support_vector and point.alpha != 0:
            illegal_points.append(point)
        if is_support_vector and point.alpha <= 0:
            illegal_points.append(point)

    return set(illegal_points)

def compute_vector_sum_equation5(svm):
    vector_sum_equation5 = [0] * len(svm.training_points[0].coords)
    for point in svm.training_points:
        vector_sum_equation5 = vector_add(vector_sum_equation5,
                                          scalar_mult(point.alpha * point.classification, point.coords))
    return vector_sum_equation5

def check_alpha_equations(svm):
    """Returns True if both Lagrange-multiplier equations are satisfied,
    otherwise False. Assumes that the SVM has support vectors assigned, and
    that all training points have alpha values assigned."""
    sum_equation4 = 0

    for point in svm.training_points:
        sum_equation4 += point.alpha * point.classification

    if sum_equation4 != 0:
        return False

    if svm.w != compute_vector_sum_equation5(svm):
        return False

    return True


#### Part 4: Evaluating Accuracy ###############################################

def misclassified_training_points(svm):
    """Returns the set of training points that are classified incorrectly
    using the current decision boundary."""
    misclassified_points = []
    for point in svm.training_points:
        if classify(svm, point) != point.classification:
            misclassified_points.append(point)

    return set(misclassified_points)


#### Part 5: Training an SVM ###################################################

def update_svm_from_alphas(svm):
    """Given an SVM with training data and alpha values, use alpha values to
    update the SVM's support vectors, w, and b. Return the updated SVM."""

    # Any training point with alpha > 0 is a support vector.
    support_vectors = []
    for point in svm.training_points:
        if point.alpha > 0:
            support_vectors.append(point)

    svm.support_vectors = support_vectors

    # w can be calculated using Equation 5
    svm.w = compute_vector_sum_equation5(svm)

    # b can be calculated as the average of two values: the minimum value of b
    # produced by a negative support vector, and the maximum value of b produced
    # by a positive support vector. Each b can be computed using Equation 3
    negmin = None
    posmax = None
    for point in svm.support_vectors:
        b = -dot_product(svm.w, point.coords)

        if point.classification == -1:
            if negmin is None or negmin > b:
                negmin = b

        elif point.classification == 1:
            if posmax is None or posmax < b:
                posmax = b

    svm.b = (negmin + posmax) / 2

    return svm

#### Part 6: Multiple Choice ###################################################

ANSWER_1 = 11
ANSWER_2 = 6
ANSWER_3 = 3
ANSWER_4 = 2

ANSWER_5 = ['A', 'D']
ANSWER_6 = ['A', 'B', 'D']
ANSWER_7 = ['A', 'B', 'D']
ANSWER_8 = []
ANSWER_9 = ['A', 'B', 'D']
ANSWER_10 = ['A', 'B', 'D']

ANSWER_11 = False
ANSWER_12 = True
ANSWER_13 = False
ANSWER_14 = False
ANSWER_15 = False
ANSWER_16 = True

ANSWER_17 = [1, 3, 6, 8]
ANSWER_18 = [1, 2, 4, 5, 6, 7, 8]
ANSWER_19 = [1, 2, 4, 5, 6, 7, 8]

ANSWER_20 = 6


#### SURVEY ####################################################################

NAME = 'Alejandro Gamboa'
COLLABORATORS = None
HOW_MANY_HOURS_THIS_LAB_TOOK = 4
WHAT_I_FOUND_INTERESTING = 'Every single function'
WHAT_I_FOUND_BORING = None
SUGGESTIONS = None
