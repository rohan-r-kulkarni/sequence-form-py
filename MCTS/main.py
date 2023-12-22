import numpy as np
import random
import matplotlib.pyplot as plt

from judgmenttree import Node
from mcts import MCTS, MCTS_UCT
from tqdm import tqdm

def randomPlayerVersusMCTS(deck, handSize, MCTSSimNumber, playerOne = 0):
    # Play a game of Judgment with a random player versus MCTS
    
    # Shuffle the deck and deal Player 1's hand
    random.shuffle(deck)
    player1_hand = deck[:handSize]
    deck = deck[handSize:] # Remove Player 1's hand from the deck
    
    if playerOne == 0:
        returnedHand = player1_hand
    else:
        returnedHand = deck
    
    if playerOne == 0:
        # Create the root node
        root = Node(player1_hand, deck)
        
        # MCTS plays first
        # while loop to play the game until a terminal node is reached
        curGameState = root
        
        while not curGameState.is_terminal():
            # MCTS plays
            MCTS_choice = MCTS(curGameState, MCTSSimNumber, playerOne)
            # print("MCTS choice:", MCTS_choice.bets, MCTS_choice.player1_hand, MCTS_choice.deck)
            curGameState = MCTS_choice
            
            # Random player plays
            curGameState.generate_children()
            random_choice = random.choice(curGameState.children)
            # print("Random choice:", random_choice.bets, random_choice.player1_hand, random_choice.deck)
            curGameState = random_choice
            
        # calculate utility of the terminal node that we reached
        utility = curGameState.calculate_utility()
        MCTSBet = curGameState.bets[0]
        otherPlayerBet = curGameState.bets[1]
        
        return utility, MCTSBet, returnedHand, otherPlayerBet
    
    elif playerOne == 1:
        # Create the root node
        root = Node(deck, player1_hand)
        
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
            MCTS_choice = MCTS(curGameState, MCTSSimNumber, playerOne)
            # print("MCTS choice:", MCTS_choice.bets, MCTS_choice.player1_hand, MCTS_choice.deck)
            curGameState = MCTS_choice
            
        # calculate utility of the terminal node that we reached
        utility = curGameState.calculate_utility()
        # print("Utility:", utility)
        MCTSBet = curGameState.bets[1]
        otherPlayerBet = curGameState.bets[0]
        # print("MCTS Bet:", MCTSBet)
        
        return utility, MCTSBet, returnedHand, otherPlayerBet

def randomPlayerVersusMCTS_UCT(deck, handSize, MCTSSimNumber, playerOne = 0):
    # Play a game of Judgment with a random player versus MCTS
    
    # Shuffle the deck and deal Player 1's hand
    random.shuffle(deck)
    player1_hand = deck[:handSize]
    deck = deck[handSize:] # Remove Player 1's hand from the deck
    
    if playerOne == 0:
        returnedHand = player1_hand
    else:
        returnedHand = deck
    
    if playerOne == 0:
        # Create the root node
        root = Node(player1_hand, deck)
        
        # MCTS plays first
        # while loop to play the game until a terminal node is reached
        curGameState = root
        
        while not curGameState.is_terminal():
            # MCTS plays
            MCTS_choice = MCTS_UCT(curGameState, MCTSSimNumber, playerOne)
            # print("MCTS choice:", MCTS_choice.bets, MCTS_choice.player1_hand, MCTS_choice.deck)
            curGameState = MCTS_choice
            
            # Random player plays
            curGameState.generate_children()
            random_choice = random.choice(curGameState.children)
            # print("Random choice:", random_choice.bets, random_choice.player1_hand, random_choice.deck)
            curGameState = random_choice
            
        # calculate utility of the terminal node that we reached
        utility = curGameState.calculate_utility()
        MCTSBet = curGameState.bets[0]
        otherPlayerBet = curGameState.bets[1]
        
        return utility, MCTSBet, returnedHand, otherPlayerBet
    
    elif playerOne == 1:
        # Create the root node
        root = Node(deck, player1_hand)
        
        #MCTS plays second
        # while loop to play the game until a terminal node is reached
        curGameState = root
        
        while not curGameState.is_terminal():
            # Random player plays00
            curGameState.generate_children()
            random_choice = random.choice(curGameState.children)
            # print("Random choice:", random_choice.bets, random_choice.player1_hand, random_choice.deck)
            curGameState = random_choice
            
            # MCTS plays
            MCTS_choice = MCTS_UCT(curGameState, MCTSSimNumber, playerOne)
            # print("MCTS choice:", MCTS_choice.bets, MCTS_choice.player1_hand, MCTS_choice.deck)
            curGameState = MCTS_choice
            
        # calculate utility of the terminal node that we reached
        utility = curGameState.calculate_utility()
        MCTSBet = curGameState.bets[1]
        otherPlayerBet = curGameState.bets[0]
        
        return utility, MCTSBet, returnedHand, otherPlayerBet

def main():
    # Test the MCTS Algorithms
    deck = np.arange(1, 14)
    elevens = np.full(13, 14)
    deck = np.concatenate((deck, deck, deck, elevens)) # essentially, three regular suits, and one trump suit
    handSize = 7
    iterationsPerRun = 1000
    simNumber = 1000
    test_UTC = False
    
    # Test MCTS versus random player 1000 times with MCTS playing first, and add returned utilities to a list to graph
    MCTSUtilitiesFirst = np.array([])
    MCTSBetsFirst = np.array([])
    MCTSAverageHandValueFirst = np.array([])
    SecondPlayerBets = np.array([])
    for i in tqdm(range(iterationsPerRun), desc="MCTS plays first"):
        utility, bet, hand, secondBet = randomPlayerVersusMCTS(deck, handSize, simNumber, playerOne = 0)
        MCTSUtilitiesFirst = np.append(MCTSUtilitiesFirst, utility[0])
        MCTSBetsFirst = np.append(MCTSBetsFirst, bet)
        MCTSAverageHandValueFirst = np.append(MCTSAverageHandValueFirst, np.mean(hand))
        SecondPlayerBets = np.append(SecondPlayerBets, secondBet)
        
    # Test MCTS versus random player 1000 times with MCTS playing second, and add returned utilities to a list to graph
    MCTSUtilitiesSecond = np.array([])
    MCTSBetsSecond = np.array([])
    MCTSAverageHandValueSecond = np.array([])
    FirstPlayerBets = np.array([])
    for i in tqdm(range(iterationsPerRun), desc="MCTS plays second"):
        utility, bet, hand, firstBet = randomPlayerVersusMCTS(deck, handSize, simNumber, playerOne = 1)
        MCTSUtilitiesSecond = np.append(MCTSUtilitiesSecond, utility[1])
        MCTSBetsSecond = np.append(MCTSBetsSecond, bet)
        MCTSAverageHandValueSecond = np.append(MCTSAverageHandValueSecond, np.mean(hand))
        FirstPlayerBets = np.append(FirstPlayerBets, firstBet)
        
    if test_UTC:
        # Test MCTS_UCT versus random player 1000 times with MCTS playing first, and add returned utilities to a list to graph
        MCTS_UCTUtilitiesFirst = np.array([])
        MCTS_UCTBetsFirst = np.array([])
        MCTS_UCTAverageHandValueFirst = np.array([])
        SecondPlayerBetsUTC = np.array([])
        for i in tqdm(range(iterationsPerRun), desc="MCTS_UCT plays first"):
            utility, bet, hand, secondBet = randomPlayerVersusMCTS_UCT(deck, handSize, simNumber, playerOne = 0)
            MCTS_UCTUtilitiesFirst = np.append(MCTS_UCTUtilitiesFirst, utility[0])
            MCTS_UCTBetsFirst = np.append(MCTS_UCTBetsFirst, bet)
            MCTS_UCTAverageHandValueFirst = np.append(MCTS_UCTAverageHandValueFirst, np.mean(hand))
            MCTS_UCTBetsFirst = np.append(MCTS_UCTBetsFirst, secondBet)
            
        # Test MCTS_UCT versus random player 1000 times with MCTS playing second, and add returned utilities to a list to graph
        MCTS_UCTUtilitiesSecond = np.array([])
        MCTS_UCTBetsSecond = np.array([])
        MCTS_UCTAverageHandValueSecond = np.array([])
        FirstPlayerBetsUTC = np.array([])
        for i in tqdm(range(iterationsPerRun), desc="MCTS_UCT plays second"):
            utility, bet, hand, firstBet = randomPlayerVersusMCTS_UCT(deck, handSize, simNumber, playerOne = 1)
            MCTS_UCTUtilitiesSecond = np.append(MCTS_UCTUtilitiesSecond, utility[1])
            MCTS_UCTBetsSecond = np.append(MCTS_UCTBetsSecond, bet)
            MCTS_UCTAverageHandValueSecond = np.append(MCTS_UCTAverageHandValueSecond, np.mean(hand))
            FirstPlayerBetsUTC = np.append(FirstPlayerBetsUTC, firstBet)
    
        
    # Plot the cumulative utilities
    MCTSPlaysFirstCumUtility = np.cumsum(MCTSUtilitiesFirst)
    MCTSPlaysSecondCumUtility = np.cumsum(MCTSUtilitiesSecond)
    plt.title(f"MCTS vs. Random Player (Cumulative Utility)\nDeck Size: {len(deck)}, Hand Size: {handSize}")
    plt.plot(MCTSPlaysFirstCumUtility, label = "MCTS plays first")
    plt.plot(MCTSPlaysSecondCumUtility, label = "MCTS plays second")     
    plt.legend()
    plt.savefig('MCTS/output/first_versus_second.png')
    plt.clf()    
    
    if test_UTC:
        MCTS_UCTPlaysFirstCumUtility = np.cumsum(MCTS_UCTUtilitiesFirst)
        MCTS_UCTPlaysSecondCumUtility = np.cumsum(MCTS_UCTUtilitiesSecond)
        plt.title(f"MCTS_UTC vs. Random Player (Cumulative Utility)\nDeck Size: {len(deck)}, Hand Size: {handSize}")
        plt.plot(MCTS_UCTPlaysFirstCumUtility, label = "MCTS_UCT plays first")
        plt.plot(MCTS_UCTPlaysSecondCumUtility, label = "MCTS_UCT plays second")
        plt.legend()
        plt.savefig('MCTS/output/first_versus_second_UTC.png')
        plt.clf() 
        
    
    plt.figure(figsize=(20, 10))
    
    plt.subplot(1, 2, 1)
    plt.title(f"MCTS Bet Distribution (MCTS plays first)\nDeck Size: {len(deck)}, Hand Size: {handSize}")
    plt.hist(MCTSBetsFirst, bins=np.arange(min(MCTSBetsFirst), max(MCTSBetsFirst) + 1, 1), align='mid')
    plt.xlabel("Bet")
    plt.ylabel("Frequency")
    plt.xticks(np.arange(min(MCTSBetsFirst), max(MCTSBetsFirst) + 1, 1))

    plt.subplot(1, 2, 2)
    plt.title(f"MCTS Bet Distribution (MCTS plays second)\nDeck Size: {len(deck)}, Hand Size: {handSize}")
    plt.hist(MCTSBetsSecond, bins=np.arange(min(MCTSBetsSecond), max(MCTSBetsSecond) + 1, 1), align='mid')
    plt.xlabel("Bet")
    plt.ylabel("Frequency")
    plt.xticks(np.arange(min(MCTSBetsSecond), max(MCTSBetsSecond) + 1, 1))
    
    plt.tight_layout()
    plt.savefig('MCTS/output/bets_normal.png')
    plt.clf()
    
    if test_UTC:
        plt.subplot(1, 2, 1)
        plt.title(f"MCTS_UCT Bet Distribution (MCTS_UCT plays first)\nDeck Size: {len(deck)}, Hand Size: {handSize}")
        plt.hist(MCTS_UCTBetsFirst, bins=np.arange(min(MCTS_UCTBetsFirst), max(MCTS_UCTBetsFirst) + 1, 1), align='mid')
        plt.xlabel("Bet")
        plt.ylabel("Frequency")
        plt.xticks(np.arange(min(MCTS_UCTBetsFirst), max(MCTS_UCTBetsFirst) + 1, 1))
        
        plt.subplot(1, 2, 2)
        plt.title(f"MCTS_UCT Bet Distribution (MCTS_UCT plays second)\nDeck Size: {len(deck)}, Hand Size: {handSize}")
        plt.hist(MCTS_UCTBetsSecond, bins=np.arange(min(MCTS_UCTBetsSecond), max(MCTS_UCTBetsSecond) + 1, 1), align='mid')
        plt.xlabel("Bet")
        plt.ylabel("Frequency")
        plt.xticks(np.arange(min(MCTS_UCTBetsSecond), max(MCTS_UCTBetsSecond) + 1, 1))

        plt.tight_layout()
        plt.savefig('MCTS/output/bets_UTC.png')
        plt.clf()
    
    # Scatter plot of average hand value versus bet (MCTS plays first)
    plt.subplot(1, 2, 1)
    plt.title(f"Average Hand Value vs. Bet (MCTS plays first)\nDeck Size: {len(deck)}, Hand Size: {handSize}")
    plt.scatter(MCTSAverageHandValueFirst, MCTSBetsFirst)
    plt.xlabel("Average Hand Value")
    plt.ylabel("Bet")

    # Scatter plot of average hand value versus bet (MCTS plays second)
    plt.subplot(1, 2, 2)
    plt.title(f"Average Hand Value vs. Bet (MCTS plays second)\nDeck Size: {len(deck)}, Hand Size: {handSize}")
    plt.scatter(MCTSAverageHandValueSecond, MCTSBetsSecond)
    plt.xlabel("Average Hand Value")
    plt.ylabel("Bet")

    plt.tight_layout()
    plt.savefig('MCTS/output/average_hand_value_versus_bet.png')
    plt.clf()
    
    if test_UTC:
        # Scatter plot of average hand value versus bet (MCTS_UCT plays first)
        plt.subplot(1, 2, 1)
        plt.title(f"Average Hand Value vs. Bet (MCTS_UCT plays first)\nDeck Size: {len(deck)}, Hand Size: {handSize}")
        plt.scatter(MCTS_UCTAverageHandValueFirst, MCTS_UCTBetsFirst)
        plt.xlabel("Average Hand Value")
        plt.ylabel("Bet")
    
        # Scatter plot of average hand value versus bet (MCTS_UCT plays second)
        plt.subplot(1, 2, 2)
        plt.title(f"Average Hand Value vs. Bet (MCTS_UCT plays second)\nDeck Size: {len(deck)}, Hand Size: {handSize}")
        plt.scatter(MCTS_UCTAverageHandValueSecond, MCTS_UCTBetsSecond)
        plt.xlabel("Average Hand Value")
        plt.ylabel("Bet")
    
        plt.tight_layout()
        plt.savefig('MCTS/output/average_hand_value_versus_bet_UTC.png')
        plt.clf()
        
    plt.title("First Player Bet vs. Second Player Bet (MCTS plays second)\nDeck Size: {len(deck)}, Hand Size: {handSize}")
    plt.scatter(MCTSBetsSecond, FirstPlayerBets)
    plt.xlabel("MCTS Bet")
    plt.ylabel("First Player Bet")
    plt.savefig('MCTS/output/first_player_bet_versus_second_player_bet.png')
    plt.clf()
    
main()
