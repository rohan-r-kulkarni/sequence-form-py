import numpy as np
from judgmenttree import Node

def UCT(node):
    # UCT formula
    return node.value[0] / node.visit_count + np.sqrt(2 * np.log(node.parent.visit_count) / node.visit_count)

def select(node):
    # Select a child node
    while node.children:
        node = max(node.children, key=UCT)
    return node

import random

def expand(node):
    # Expand a node
    if not node.is_terminal():
        node.generate_children()
        if node.children:
            return random.choice(node.children)
        else:
            raise ValueError("Expansion attempted on a node with no children.")
    else:
        raise ValueError("Expansion attempted on a terminal node.")

def simulate(node):
    # Simulate a random game from this node to a terminal node
    while not node.is_terminal():
        if node.children:
            node = np.random.choice(node.children)
        else:
            break
    if node.is_terminal():
        return node.calculate_utility()
    else:
        raise ValueError("Simulation ended on a non-terminal node.")

def MCTS(root, iterations):
    for _ in range(iterations):
        # Selection
        node = root
        while node.children:
            node = np.random.choice(node.children)

        # Expansion
        if not node.is_terminal():
            node.generate_children()

        # Simulation
        node = np.random.choice(node.children) if node.children else node
        while not node.is_terminal():
            node.generate_children()
            node = np.random.choice(node.children) if node.children else node

        # Calculate utility and Backpropagation
        if node.is_terminal():
            utility = node.calculate_utility()
            node.backpropagate(utility)
    
    # Return the best child of the root
    return max(root.children, key=lambda node: node.value[0])
