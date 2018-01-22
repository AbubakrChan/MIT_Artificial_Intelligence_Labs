# MIT 6.034 Lab 6: Neural Nets
# Written by 6.034 Staff

from nn_problems import *
from math import e
INF = float('inf')


#### Part 1: Wiring a Neural Net ###############################################

nn_half = [1]

nn_angle = [2, 1]

nn_cross = [2, 2, 1]

nn_stripe = [3, 1]

nn_hexagon = [6, 1]

nn_grid = [4, 2, 1]


#### Part 2: Coding Warmup #####################################################

# Threshold functions
def stairstep(x, threshold=0):
    "Computes stairstep(x) using the given threshold (T)"
    return 1 if x >= threshold else 0

def sigmoid(x, steepness=1, midpoint=0):
    "Computes sigmoid(x) using the given steepness (S) and midpoint (M)"
    return 1 / (1 + e**(-steepness*(x-midpoint)))

def ReLU(x):
    "Computes the threshold of an input using a rectified linear unit."
    return max(0, x)

# Accuracy function
def accuracy(desired_output, actual_output):
    "Computes accuracy. If output is binary, accuracy ranges from -0.5 to 0."
    return -1/2 * (desired_output - actual_output) ** 2


#### Part 3: Forward Propagation ###############################################

def node_value(node, input_values, neuron_outputs):  # PROVIDED BY THE STAFF
    """
    Given 
     * a node (as an input or as a neuron),
     * a dictionary mapping input names to their values, and
     * a dictionary mapping neuron names to their outputs
    returns the output value of the node.
    This function does NOT do any computation; it simply looks up
    values in the provided dictionaries.
    """
    if isinstance(node, str):
        # A string node (either an input or a neuron)
        if node in input_values:
            return input_values[node]
        if node in neuron_outputs:
            return neuron_outputs[node]
        raise KeyError("Node '{}' not found in either the input values or neuron outputs dictionary.".format(node))
    
    if isinstance(node, (int, float)):
        # A constant input, such as -1
        return node
    
    raise TypeError("Node argument is {}; should be either a string or a number.".format(node))

def forward_prop(net, input_values, threshold_fn=stairstep):
    """Given a neural net and dictionary of input values, performs forward
    propagation with the given threshold function to compute binary output.
    This function should not modify the input net.  Returns a tuple containing:
    (1) the final output of the neural net
    (2) a dictionary mapping neurons to their immediate outputs"""
    neuron_outputs = {}
    for neuron in net.topological_sort():
        input_wires = net.get_wires(endNode=neuron)
        output = 0

        for wire in input_wires:
            startNode_value = node_value(wire.startNode, input_values, neuron_outputs)
            output += startNode_value * wire.get_weight()

        output = threshold_fn(output)
        neuron_outputs[neuron] = output

    return output, neuron_outputs


#### Part 4: Backward Propagation ##############################################

def gradient_ascent_step(func, inputs, step_size):
    """Given an unknown function of three variables and a list of three values
    representing the current inputs into the function, increments each variable
    by +/- step_size or 0, with the goal of maximizing the function output.
    After trying all possible variable assignments, returns a tuple containing:
    (1) the maximum function output found, and
    (2) the list of inputs that yielded the highest function output."""
    max_output = -INF
    best_inputs = []
    dx = [1, -1, 0]
    for i in range(3):
        for j in range(3):
            for k in range(3):
                arg1 = inputs[0] + (dx[i] * step_size)
                arg2 = inputs[1] + (dx[j] * step_size)
                arg3 = inputs[2] + (dx[k] * step_size)
                output = func(arg1, arg2, arg3)
                if output > max_output:
                    max_output = output
                    best_inputs = [arg1, arg2, arg3]

    return (max_output, best_inputs)

def get_back_prop_dependencies(net, wire):
    """Given a wire in a neural network, returns a set of inputs, neurons, and
    Wires whose outputs/values are required to update this wire's weight."""
    dependencies = [wire]
    nodeA = wire.startNode
    nodeB = wire.endNode
    dependencies.extend([nodeA, nodeB])
    for w in net.get_wires(startNode=nodeB):
        dependencies.extend(get_back_prop_dependencies(net, w))

    return set(dependencies)


def calculate_deltas(net, desired_output, neuron_outputs):
    """Given a neural net and a dictionary of neuron outputs from forward-
    propagation, computes the update coefficient (delta_B) for each
    neuron in the net. Uses the sigmoid function to compute neuron output.
    Returns a dictionary mapping neuron names to update coefficient (the
    delta_B values). """
    output_neuron = net.get_output_neuron()
    output = neuron_outputs[output_neuron]
    neurons = net.topological_sort()
    neurons.reverse()
    deltas = {}
    deltas[output_neuron] = output * (1 - output) * (desired_output - output)

    for neuron in neurons[1:]:
        deltas[neuron] = calculate_one_delta(net, neuron, neuron_outputs, deltas)

    return deltas


def calculate_one_delta(net, neuron, prev_outputs, prev_deltas):
    new_delta = 0
    for outgoing_wire in net.get_wires(startNode=neuron):
        weight = outgoing_wire.get_weight()
        endNode = outgoing_wire.endNode
        prev_delta = prev_deltas[endNode]
        new_delta += weight * prev_delta

    new_delta = prev_outputs[neuron] * (1 - prev_outputs[neuron]) * new_delta

    return new_delta


def update_weights(net, input_values, desired_output, neuron_outputs, r=1):
    """Performs a single step of back-propagation.  Computes delta_B values and
    weight updates for entire neural net, then updates all weights.  Uses the
    sigmoid function to compute neuron output.  Returns the modified neural net,
    with the updated weights."""
    deltas = calculate_deltas(net, desired_output, neuron_outputs)

    for wire in net.get_wires():
        nodeA = wire.startNode
        nodeB = wire.endNode
        if nodeB != 'OUT':
            if type(nodeA) == int:
                outA = nodeA
            elif nodeA in input_values:
                outA = input_values[nodeA]
            elif nodeA in neuron_outputs:
                outA = neuron_outputs[nodeA]
            new_weight = wire.get_weight() + r * outA * deltas[nodeB]
            wire.set_weight(new_weight)

    return net


def back_prop(net, input_values, desired_output, r=1, minimum_accuracy=-0.001):
    """Updates weights until accuracy surpasses minimum_accuracy.  Uses the
    sigmoid function to compute neuron output.  Returns a tuple containing:
    (1) the modified neural net, with trained weights
    (2) the number of iterations (that is, the number of weight updates)"""
    output, neuron_outputs = forward_prop(net, input_values, threshold_fn=sigmoid)
    current_accuracy = accuracy(desired_output, output)
    iterations = 0

    while current_accuracy < minimum_accuracy:
        net = update_weights(net, input_values, desired_output, neuron_outputs, r)
        output, neuron_outputs = forward_prop(net, input_values, threshold_fn=sigmoid)
        current_accuracy = accuracy(desired_output, output)
        iterations += 1

    return net, iterations


#### Part 5: Training a Neural Net #############################################

ANSWER_1 = 20
ANSWER_2 = 20
ANSWER_3 = 6
ANSWER_4 = 70
ANSWER_5 = 18

ANSWER_6 = 1
ANSWER_7 = 'checkerboard'
ANSWER_8 = set(['small', 'medium', 'large'])
ANSWER_9 = 'B'

ANSWER_10 = 'D'
ANSWER_11 = set('AC')
ANSWER_12 = set('AE')


#### SURVEY ####################################################################

NAME = 'Alejandro Gamboa'
COLLABORATORS = None
HOW_MANY_HOURS_THIS_LAB_TOOK = 4
WHAT_I_FOUND_INTERESTING = 'The calculate_deltas was the most interesting and challenging function'
WHAT_I_FOUND_BORING = None
SUGGESTIONS = None
