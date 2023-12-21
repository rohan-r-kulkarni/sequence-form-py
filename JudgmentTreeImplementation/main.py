import numpy as np
import random
import matplotlib.pyplot as plt

from judgmenttree import Node
from mcts import MCTS
from tqdm import tqdm

def randomPlayerVersusMCTS(deck, handSize, MCTSSimNumber,playerOne = 0):
    # Play a game of Judgment with a random player versus MCTS
    
    # Shuffle the deck and deal Player 1's hand
    random.shuffle(deck)
    player1_hand = deck[:handSize]
    deck = deck[handSize:] # Remove Player 1's hand from the deck
    
    # Create the root node
    root = Node(player1_hand, deck)
    
    if playerOne == 0:
        # MCTS plays first
        # while loop to play the game until a terminal node is reached
        curGameState = root
        
        while not curGameState.is_terminal():
            # MCTS plays
            MCTS_choice = MCTS(curGameState, MCTSSimNumber)
            # print("MCTS choice:", MCTS_choice.bets, MCTS_choice.player1_hand, MCTS_choice.deck)
            curGameState = MCTS_choice
            
            # Random player plays
            curGameState.generate_children()
            random_choice = random.choice(curGameState.children)
            # print("Random choice:", random_choice.bets, random_choice.player1_hand, random_choice.deck)
            curGameState = random_choice
            
        # calculate utility of the terminal node that we reached
        utility = curGameState.calculate_utility()
        
        return utility
    
    elif playerOne == 1:
        #MCTS plays second
        # while loop to play the game until a terminal node is reached
        curGameState = root
        
        while not curGameState.is_terminal():
            # Random player plays
            curGameState.generate_children()
            random_choice = random.choice(curGameState.children)
            # print("Random choice:", random_choice.bets, random_choice.player1_hand, random_choice.deck)
            curGameState = random_choice
            
            # MCTS plays
            MCTS_choice = MCTS(curGameState, MCTSSimNumber)
            # print("MCTS choice:", MCTS_choice.bets, MCTS_choice.player1_hand, MCTS_choice.deck)
            curGameState = MCTS_choice
            
        # calculate utility of the terminal node that we reached
        utility = curGameState.calculate_utility()
        
        return utility

def main():
    # Test the MCTS Algorithms
    deck = np.arange(1, 6)
    deck = np.append(deck, deck)
    handSize = 3
    iterationsPerRun = 100
    simNumber = 1000
    
    # Test MCTS versus random player 1000 times with MCTS playing first, and add returned utilities to a list to graph
    utilitiesPlayerOneMCTSFirst = np.array([])
    utilitiesPlayerTwoMCTSFirst = np.array([])
    for i in tqdm(range(iterationsPerRun), desc="MCTS plays first"):
        utility = randomPlayerVersusMCTS(deck, handSize, simNumber, playerOne = 0)
        utilitiesPlayerOneMCTSFirst = np.append(utilitiesPlayerOneMCTSFirst, utility[0])
        utilitiesPlayerTwoMCTSFirst = np.append(utilitiesPlayerTwoMCTSFirst, utility[1])
        
    # Test MCTS versus random player 1000 times with MCTS playing second, and add returned utilities to a list to graph
    utilitiesPlayerOneMCTSSecond = np.array([])
    utilitiesPlayerTwoMCTSSecond = np.array([])
    for i in tqdm(range(iterationsPerRun), desc="MCTS plays second"):
        utility = randomPlayerVersusMCTS(deck, handSize, simNumber, playerOne = 1)
        utilitiesPlayerOneMCTSSecond = np.append(utilitiesPlayerOneMCTSSecond, utility[0])
        utilitiesPlayerTwoMCTSSecond = np.append(utilitiesPlayerTwoMCTSSecond, utility[1])
        
    # Plot the cumulative utilities
    MCTSPlaysFirstCumUtility = np.cumsum(utilitiesPlayerOneMCTSFirst)
    MCTSPlaysSecondCumUtility = np.cumsum(utilitiesPlayerOneMCTSSecond)
    plt.title(f"MCTS vs. Random Player\nDeck Size: {len(deck)}, Hand Size: {handSize}")
    plt.plot(MCTSPlaysFirstCumUtility, label = "MCTS plays first")
    plt.plot(MCTSPlaysSecondCumUtility, label = "MCTS plays second")
    plt.legend()
    plt.show()
    
main()
