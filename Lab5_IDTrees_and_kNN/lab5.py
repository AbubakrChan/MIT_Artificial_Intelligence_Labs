# MIT 6.034 Lab 5: k-Nearest Neighbors and Identification Trees
# Written by 6.034 Staff

from api import *
from data import *
import math
log2 = lambda x: math.log(x, 2)
INF = float('inf')


################################################################################
############################# IDENTIFICATION TREES #############################
################################################################################


#### Part 1A: Classifying points ###############################################

def id_tree_classify_point(point, id_tree):
    """Uses the input ID tree (an IdentificationTreeNode) to classify the point.
    Returns the point's classification."""
    if id_tree.is_leaf():
        return id_tree.get_node_classification()

    child_node = id_tree.apply_classifier(point)
    return id_tree_classify_point(point, child_node)


#### Part 1B: Splitting data with a classifier #################################

def split_on_classifier(data, classifier):
    """Given a set of data (as a list of points) and a Classifier object, uses
    the classifier to partition the data.  Returns a dict mapping each feature
    values to a list of points that have that value."""
    dict = {}
    for datum in data:
        value = classifier.classify(datum)
        if value not in dict:
            dict[value] = [datum]
        else:
            dict[value].append(datum)

    return dict


#### Part 1C: Calculating disorder #############################################

def branch_disorder(data, target_classifier):
    """Given a list of points representing a single branch and a Classifier
    for determining the true classification of each point, computes and returns
    the disorder of the branch."""
    dict = split_on_classifier(data, target_classifier)
    disorder = 0
    for classification_value in dict.keys():
        ratio = len(dict[classification_value]) / len(data)
        disorder += -ratio * log2(ratio)

    return disorder

def average_test_disorder(data, test_classifier, target_classifier):
    """Given a list of points, a feature-test Classifier, and a Classifier
    for determining the true classification of each point, computes and returns
    the disorder of the feature-test stump."""
    dict = split_on_classifier(data, test_classifier)
    average_disorder = 0
    for classification_value in dict.keys():
        branch_dis = branch_disorder(dict[classification_value], target_classifier)
        branch_weight = len(dict[classification_value]) / len(data)
        average_disorder += branch_weight * branch_dis

    return average_disorder


## To use your functions to solve part A2 of the "Identification of Trees"
## problem from 2014 Q2, uncomment the lines below and run lab5.py:

# for classifier in tree_classifiers:
#     print(classifier.name, average_test_disorder(tree_data, classifier, feature_test("tree_type")))


#### Part 1D: Constructing an ID tree ##########################################

def find_best_classifier(data, possible_classifiers, target_classifier):
    """Given a list of points, a list of possible Classifiers to use as tests,
    and a Classifier for determining the true classification of each point,
    finds and returns the classifier with the lowest disorder.  Breaks ties by
    preferring classifiers that appear earlier in the list.  If the best
    classifier has only one branch, raises NoGoodClassifiersError."""
    lowest_disorder = INF
    best_classifier = possible_classifiers[0]
    for classifier in possible_classifiers:
        avg_disorder = average_test_disorder(data, classifier, target_classifier)

        if avg_disorder < lowest_disorder:
            lowest_disorder = avg_disorder
            best_classifier = classifier

    if lowest_disorder == 1:
        raise NoGoodClassifiersError

    return best_classifier


## To find the best classifier from 2014 Q2, Part A, uncomment:
# print(find_best_classifier(tree_data, tree_classifiers, feature_test("tree_type")))

def construct_greedy_id_tree(data, possible_classifiers, target_classifier, id_tree_node=None):
    """Given a list of points, a list of possible Classifiers to use as tests,
    a Classifier for determining the true classification of each point, and
    optionally a partially completed ID tree, returns a completed ID tree by
    adding classifiers and classifications until either perfect classification
    has been achieved, or there are no good classifiers left."""
    if not id_tree_node:
        id_tree_node = IdentificationTreeNode(target_classifier)

    if(len(split_on_classifier(data, target_classifier).keys()) == 1):
        id_tree_node.set_node_classification(target_classifier.classify(data[0]))
    else:
        try:
            best_classifier = find_best_classifier(data, possible_classifiers, target_classifier)
            features = split_on_classifier(data, best_classifier)
            id_tree_node.set_classifier_and_expand(best_classifier, features)
            branch_dic = id_tree_node.get_branches()
            for feature in branch_dic:
                construct_greedy_id_tree(features[feature], possible_classifiers, target_classifier, branch_dic[feature])
        except NoGoodClassifiersError:
            return id_tree_node

    return id_tree_node

## To construct an ID tree for 2014 Q2, Part A:
# print(construct_greedy_id_tree(tree_data, tree_classifiers, feature_test("tree_type")))

## To use your ID tree to identify a mystery tree (2014 Q2, Part A4):
# tree_tree = construct_greedy_id_tree(tree_data, tree_classifiers, feature_test("tree_type"))
# print(id_tree_classify_point(tree_test_point, tree_tree))

## To construct an ID tree for 2012 Q2 (Angels) or 2013 Q3 (numeric ID trees):
# print(construct_greedy_id_tree(angel_data, angel_classifiers, feature_test("Classification")))
# print(construct_greedy_id_tree(numeric_data, numeric_classifiers, feature_test("class")))


#### Part 1E: Multiple choice ##################################################

ANSWER_1 = 'bark_texture'
ANSWER_2 = 'leaf_shape'
ANSWER_3 = 'orange_foliage'

# ANSWER 4 DEMONSTRATION
# print('binary_tree_1')
# for point in binary_data:
#    print(point['name'] + ' ' + str(id_tree_classify_point(point, get_binary_tree_1())))

# print('binary_tree_2')
# for point in binary_data:
#    print(point['name'] + ' ' + str(id_tree_classify_point(point, get_binary_tree_2())))

# print('binary_tree_3')
# for point in binary_data:
#    print(point['name'] + ' ' + str(id_tree_classify_point(point, get_binary_tree_3())))

# ANSWER 5 DEMONSTRATION
# binary_id_tree = construct_greedy_id_tree(binary_data, binary_classifiers, feature_test('Classification'))
# print(binary_id_tree)

# ANSWER 6 DEMONSTRATION
# test_binary = {"name":"point8", "Classification":1, "A":1, "B":0, "C":0}
# print(get_binary_tree_1().print_with_data([test_binary]))
# print(get_binary_tree_2().print_with_data([test_binary]))
# print(get_binary_tree_3().print_with_data([test_binary]))

ANSWER_4 = [2,3]
ANSWER_5 = [3]
ANSWER_6 = [2]
ANSWER_7 = 2

ANSWER_8 = 'No'
ANSWER_9 = 'No'


#### OPTIONAL: Construct an ID tree with medical data ##########################

## Set this to True if you'd like to do this part of the lab
DO_OPTIONAL_SECTION = True

if DO_OPTIONAL_SECTION:
    from parse import *
    medical_id_tree = construct_greedy_id_tree(heart_training_data, heart_classifiers, heart_target_classifier_discrete)
    # print(medical_id_tree.print_with_data(heart_training_data))

    test_patient1 = {\
        'Age': 23, #int
        'Sex': 'M', #M or F
        'Chest pain type': 'asymptomatic', #typical angina, atypical angina, non-anginal pain, or asymptomatic
        'Resting blood pressure': 100, #int
        'Cholesterol level': 90, #int
        'Is fasting blood sugar < 120 mg/dl': 'Yes', #Yes or No
        'Resting EKG type': 'normal', #normal, wave abnormality, or ventricular hypertrophy
        'Maximum heart rate': 160, #int
        'Does exercise cause chest pain?': 'No', #Yes or No
        'ST depression induced by exercise': 0, #int
        'Slope type': 'flat', #up, flat, or down
        '# of vessels colored': 0, #float or '?'
        'Thal type': 'normal', #normal, fixed defect, reversible defect, or unknown
    }

    test_patient2 = { \
        'Age': 23,  # int
        'Sex': 'M',  # M or F
        'Chest pain type': 'atypical angina',  # typical angina, atypical angina, non-anginal pain, or asymptomatic
        'Resting blood pressure': 150,  # int
        'Cholesterol level': 150,  # int
        'Is fasting blood sugar < 120 mg/dl': 'Yes',  # Yes or No
        'Resting EKG type': 'ventricular hypertrophy',  # normal, wave abnormality, or ventricular hypertrophy
        'Maximum heart rate': 200,  # int
        'Does exercise cause chest pain?': 'Yes',  # Yes or No
        'ST depression induced by exercise': 0,  # int
        'Slope type': 'flat',  # up, flat, or down
        '# of vessels colored': 0,  # float or '?'
        'Thal type': 'fixed defect',  # normal, fixed defect, reversible defect, or unknown
    }

    # print(medical_id_tree.print_with_data([test_patient1]))
    # print(medical_id_tree.print_with_data([test_patient2]))

# ANSWERS TO QUESTIONS FROM LAB 5 WIKI PAGE:

# Q: Does this seem like the simplest possible tree?  If not, why not?
# A: No, it is probably overfitting and giving too much weight to outliers in
#    the data.  For example, many leaf nodes correspond to only 1-2 patients.

# Q: What could we change to make the tree simpler?
# A: One possible change is to modify the stopping condition.  Rather than
#    continuing to add classifiers until the data is perfectly separated, we
#    could stop when a node reaches some homogeneity threshold, such as 90%,
#    then assign the node the classification of the majority of the points.
#    This method would reduce overfitting, although in the extreme case, it
#    could result in underfitting (e.g. if you use a threshold of 51%, or 90%
#    but with a very small dataset).

# Q: What do you notice when you print the training data at the leaf nodes?
# A: One interesting observation is that there are many nodes that have only a
#    few training points, while there are a few nodes that have a large number
#    of training points.  The nodes with many training points are probably
#    reliable classifications, but those with few training points may be
#    misleading results due to overfitting.

# Q: Try using the other target classifier (binary or discrete).  Is the tree
#    simpler or more complicated?  Why?
# A: The binary-classification tree is simpler because it doesn't need to
#    separate the data as much.  The discrete-classification tree is more
#    complicated because nodes that contain only diseased patients don't count
#    as homogeneous if those patients have different levels of heart disease.

# Q: Try creating and classifying a few patients.  Are the results consistent
#    with your expectations?
# A: Expectations may vary, of course, but we've found that, in general,
#    patients who seem healthy (normal values for all features, as in the sample
#    test_patient) get classified as 'healthy', and patients who seem unhealthy
#    get classified as 'diseased'.  However, there are some exceptions...

# Q: What happens if a female patient has 'Thal type': 'unknown'?
# A: She gets classified as healthy (or 0) because the first test in the ID tree
#    is 'Thal type', and the first (and only) test for 'unknown' is 'Sex', with
#    'F' indicating healthy/0.

# Q: What happens if a male patient has 'Thal type': 'unknown'?
# A: He gets classified as diseased (or 2) because the first test in the ID tree
#    is 'Thal type', and the first (and only) test for 'unknown' is 'Sex', with
#    'M' indicating diseased/2.

# Q: What causes the surprising result with 'Thal type': 'unknown'?
# A: There are only two patients in the data set with 'Thal type': 'unknown'.
#    It just happens that one is female and healthy, while the other is male and
#    diseased.  This is an excellent example of overfitting.

# Q: What could we change to improve the classification accuracy of patients
#    with unknown Thal type?
# A: There are many possible changes, including (1) gather more data on patients
#    with unknown Thal type, or (2) ignore the 'Thal type' test altogether and
#    construct a tree using the remaining tests.

# Q: In the discrete classification tree, what happens if a patient has:
#        'Thal type': 'normal',
#        'Chest pain type': 'asymptomatic',
#        '# of vessels colored': '?'
#    ...and why does it happen?
# A: The first test in the ID tree is 'Thal type', the first test for 'normal'
#    is 'Chest pain type', and the first test for 'asymptomatic' is '# of
#    vessels colored > 0.5 (or ?)', but that node (# vessels) has only two
#    branches, 'Yes' and 'No', so the patient with '?' cannot be classified.
#    This problem arises because all of the patients in the training data with
#    'Thal type': 'normal' and 'Chest pain type': 'asymptomatic' also had a
#    known number of vessels colored (not '?').

# Q: Why might the issue with '# of vessels colored': '?' cause a problem for
#    classifying real patients?  What can we do to fix this issue?
# A: Many patients, especially healthy ones, may not have undergone the
#    procedure for determining how many major vessels are colored by flourosopy,
#    and it would be nice to be able to classify them without that information.
#    As with the 'Thal type' problem, solutions include (1) gathering more
#    information on patients with an unknown number of vessels colored, or (2)
#    ignoring the test altogether.  A third option is to assign these patients
#    the classification corresponding to the majority of patients who have 'Thal
#    type': 'normal' and 'Chest pain type': 'asymptomatic' (in this case,
#    healthy/0).


################################################################################
############################# k-NEAREST NEIGHBORS ##############################
################################################################################

#### Part 2A: Drawing Boundaries ###############################################

BOUNDARY_ANS_1 = 3
BOUNDARY_ANS_2 = 4

BOUNDARY_ANS_3 = 1
BOUNDARY_ANS_4 = 2

BOUNDARY_ANS_5 = 2
BOUNDARY_ANS_6 = 4
BOUNDARY_ANS_7 = 1
BOUNDARY_ANS_8 = 4
BOUNDARY_ANS_9 = 4

BOUNDARY_ANS_10 = 4
BOUNDARY_ANS_11 = 2
BOUNDARY_ANS_12 = 1
BOUNDARY_ANS_13 = 4
BOUNDARY_ANS_14 = 4


#### Part 2B: Distance metrics #################################################

def dot_product(u, v):
    """Computes dot product of two vectors u and v, each represented as a tuple
    or list of coordinates.  Assume the two vectors are the same length."""
    dot_product = 0
    for u_coord, v_coord in zip(u,v):
        dot_product += u_coord * v_coord

    return dot_product

def norm(v):
    "Computes length of a vector v, represented as a tuple or list of coords."
    return math.sqrt(dot_product(v, v))

def euclidean_distance(point1, point2):
    "Given two Points, computes and returns the Euclidean distance between them."
    euclidean_distance = 0
    for u_coord, v_coord in zip(point1, point2):
        euclidean_distance += (u_coord - v_coord) ** 2

    euclidean_distance = math.sqrt(euclidean_distance)

    return euclidean_distance

def manhattan_distance(point1, point2):
    "Given two Points, computes and returns the Manhattan distance between them."
    manhattan_distance = 0
    for u_coord, v_coord in zip(point1, point2):
        manhattan_distance += abs(u_coord - v_coord)

    return manhattan_distance

def hamming_distance(point1, point2):
    "Given two Points, computes and returns the Hamming distance between them."
    hamming_distance = 0
    for u_coord, v_coord in zip(point1, point2):
        if u_coord != v_coord:
            hamming_distance += 1

    return hamming_distance

def cosine_distance(point1, point2):
    """Given two Points, computes and returns the cosine distance between them,
    where cosine distance is defined as 1-cos(angle_between(point1, point2))."""
    return 1 - dot_product(point1, point2) / (norm(point1) * norm(point2))


#### Part 2C: Classifying points ###############################################

def get_k_closest_points(point, data, k, distance_metric):
    """Given a test point, a list of points (the data), an int 0 < k <= len(data),
    and a distance metric (a function), returns a list containing the k points
    from the data that are closest to the test point, according to the distance
    metric.  Breaks ties lexicographically by coordinates."""
    k_closest_points = []
    for datum in data:
        k_closest_points.append((datum, distance_metric(point, datum)))

    k_closest_points = sorted(k_closest_points, key=lambda item: (item[1], item[0].coords))[:k]

    return [datum for datum, distance in k_closest_points]

def knn_classify_point(point, data, k, distance_metric):
    """Given a test point, a list of points (the data), an int 0 < k <= len(data),
    and a distance metric (a function), returns the classification of the test
    point based on its k nearest neighbors, as determined by the distance metric.
    Assumes there are no ties."""
    classifications = [point.classification for point in get_k_closest_points(point, data, k, distance_metric)]
    return max(classifications, key=classifications.count)


## To run your classify function on the k-nearest neighbors problem from 2014 Q2
## part B2, uncomment the line below and try different values of k:
# print(knn_classify_point(knn_tree_test_point, knn_tree_data, 1, euclidean_distance))


#### Part 2C: Choosing k #######################################################

def cross_validate(data, k, distance_metric):
    """Given a list of points (the data), an int 0 < k <= len(data), and a
    distance metric (a function), performs leave-one-out cross-validation.
    Return the fraction of points classified correctly, as a float."""
    num_correct = 0
    for i, point in enumerate(data):
        training_data = data[:i] + data[i+1:]
        knn_classification = knn_classify_point(point, training_data, k, distance_metric)
        if knn_classification == point.classification:
            num_correct += 1

    return num_correct / len(data)

def find_best_k_and_metric(data):
    """Given a list of points (the data), uses leave-one-out cross-validation to
    determine the best value of k and distance_metric, choosing from among the
    four distance metrics defined above.  Returns a tuple (k, distance_metric),
    where k is an int and distance_metric is a function."""
    possible_k = range(1, 10)
    possible_distance_metric = [euclidean_distance, manhattan_distance, hamming_distance, cosine_distance]
    best_accuracy = 0
    for k in possible_k:
        for distance_metric in possible_distance_metric:
            accuracy = cross_validate(data, k, distance_metric)
            if accuracy > best_accuracy:
                best_accuracy = accuracy
                best_k = k
                best_distance_metric = distance_metric

    return (best_k, best_distance_metric)


## To find the best k and distance metric for 2014 Q2, part B, uncomment:
# print(find_best_k_and_metric(knn_tree_data))


#### Part 2E: More multiple choice #############################################

kNN_ANSWER_1 = 'Overfitting'
kNN_ANSWER_2 = 'Underfitting'
kNN_ANSWER_3 = 4

kNN_ANSWER_4 = 4
kNN_ANSWER_5 = 1
kNN_ANSWER_6 = 3
kNN_ANSWER_7 = 3


#### SURVEY ####################################################################

NAME = 'Alejandro Gamboa'
COLLABORATORS = None
HOW_MANY_HOURS_THIS_LAB_TOOK = '6'
WHAT_I_FOUND_INTERESTING = 'Constructing ID Trees'
WHAT_I_FOUND_BORING = None
SUGGESTIONS = None
