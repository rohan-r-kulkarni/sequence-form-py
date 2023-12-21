import numpy as np

class Node:
    def __init__(self, player1_hand, deck, parent = None, bets=None, tricks_won=None, current_trick=None):
        self.player1_hand = player1_hand
        self.deck = deck  # Remaining cards in the deck, excluding Player 1's hand
        self.parent = parent
        self.hand_size = len(player1_hand)  # The size of Player 1's hand
        self.deck_size = len(deck) + self.hand_size  # Total number of cards in the game
        self.bets = bets if bets is not None else [None, None]
        self.tricks_won = tricks_won if tricks_won is not None else [0, 0]
        self.current_trick = current_trick if current_trick is not None else []
        self.children = []  # Child nodes
        self.utility = []
        self.value = [0, 0]
        self.visit_count = 0

    def is_terminal(self):
        # Check if the node is a terminal node (all cards have been played)
        return len(self.player1_hand) == 0 and not self.current_trick

    def calculate_utility(self):
        # Calculate utility at terminal nodes
        if not self.is_terminal():
            raise ValueError("Utility can only be calculated for terminal nodes.")
        
        # Subtracting the number of tricks won from the bets for each player
        i_p1 = np.abs(self.bets[0] - self.tricks_won[0])
        j_p2 = np.abs(self.bets[1] - self.tricks_won[1]
        )
        utility_p1 = j_p2 - i_p1
        utility_p2 = i_p1 - j_p2
        return [utility_p1, utility_p2]

    def is_trick_over(self):
        # A trick is over if there are two cards in the current trick
        return len(self.current_trick) == 2

    def evaluate_trick_winner(self):
        # Assuming the higher card wins the trick
        if not self.is_trick_over():
            raise ValueError("Can't evaluate winner until the trick is over.")
        
        # The first card in the trick is played by Player 1
        if self.current_trick[0] > self.current_trick[1]:
            self.tricks_won[0] += 1
        elif self.current_trick[0] < self.current_trick[1]:
            self.tricks_won[1] += 1
        else:
            # If the cards are equal, the trick is a draw
            pass
        
        # Once the trick is evaluated, clear the current trick for the next one
        self.current_trick = []

    def update(self, utility):
        # Update the node's value and visit count
        self.value[0] += utility[0]
        self.value[1] += utility[1]
        self.visit_count += 1
        
    def backpropagate(self, utility):
        # Propagate the utility back up to the root node
        self.update(utility)
        if self.parent:
            self.parent.backpropagate(utility)
    
    def generate_children(self):
        if self.bets[0] is None:  # First betting round
            for bet in range(self.hand_size + 1):  # Possible bets: 0 to hand_size
                child = Node(self.player1_hand, self.deck, parent = self, bets=[bet, None], 
                             tricks_won=self.tricks_won.copy(), current_trick=self.current_trick.copy())
                self.children.append(child)
        
        elif self.bets[1] is None:  # Second betting round
            for bet in range(self.hand_size + 1):  # Player 2's possible bets
                child = Node(self.player1_hand, self.deck, parent = self,  bets=[self.bets[0], bet], 
                             tricks_won=self.tricks_won.copy(), current_trick=self.current_trick.copy())
                self.children.append(child)
        
        else:  # Playing rounds
            if not self.current_trick:  # Player 1's turn to play a card
                for card in self.player1_hand:
                    new_hand = self.player1_hand.copy()
                    new_hand = np.delete(new_hand, np.where(new_hand == card))
                    child = Node(new_hand, self.deck, parent = self,  bets=self.bets.copy(), 
                                 tricks_won=self.tricks_won.copy(), current_trick=[card])
                    self.children.append(child)
            elif len(self.current_trick) == 1:  # Player 2's turn to play a card
                # Assuming Player 2 can play any card from the deck since their hand is unknown
                for card in self.deck:
                    new_deck = self.deck.copy()
                    new_deck = np.delete(new_deck, np.where(new_deck == card))
                    child = Node(self.player1_hand, new_deck, parent = self,  bets=self.bets.copy(), 
                                tricks_won=self.tricks_won.copy(), current_trick=self.current_trick + [card])
                    self.children.append(child)
                    # After Player 2 plays, we need to evaluate the trick winner and update accordingly
                    child.evaluate_trick_winner()
                    # Clear the current trick
                    child.current_trick = []

def build_tree(node):
    if not node.is_terminal():
        node.generate_children()
        for child in node.children:
            build_tree(child)
    else:
        node.utility = node.calculate_utility()
        # backpropagate(node, node.utility)
    return node
    

# Function to output the game tree
def print_tree(node, indent="", last='updown'):
    nb_children = len(node.children)
    name = f"P1 Hand: {node.player1_hand}, Deck: {node.deck}, Bets: {node.bets}, Tricks Won: {node.tricks_won}, Current Trick: {node.current_trick}, Utility: {node.utility}"
    
    # Correcting the start_shape assignment
    start_shape = ''
    if last == 'updown':
        start_shape = "├──"
    elif last == 'up':
        start_shape = "└──"
    elif last == 'down':
        start_shape = "┌──"
        
    if nb_children > 0:
        connection = "┬"
    else:
        connection = "─"
        
    print(indent + f"{start_shape}{connection} {name}")
    indent += "   " if last == 'up' else "│   "
    
    for i, child in enumerate(node.children):
        _last = 'up' if i == nb_children - 1 else 'updown'
        print_tree(child, indent, _last)


