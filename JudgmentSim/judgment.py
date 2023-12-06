import numpy as np
import random

from agents import RandomAgent

class Card:
    def __init__(self, rank):
        self.rank = rank

    def __repr__(self):
        return f"{self.rank}"

class JudgementGameRankOnly:
    def __init__(self, agent1, agent2, num_cards_per_hand):
        self.num_players = 2
        self.agents = [agent1, agent2]
        self.deck = self.create_deck()
        self.hands = {player: [] for player in range(self.num_players)}
        self.predictions = {player: 0 for player in range(self.num_players)}
        self.tricks_won = {player: 0 for player in range(self.num_players)}
        self.num_cards_per_hand = num_cards_per_hand
        self.current_trick = []

    def create_deck(self):
        ranks = [str(n) for n in range(2, 11)] + ['J', 'Q', 'K', 'A']
        return [Card(rank) for rank in ranks] * 4

    def deal_cards(self):
        random.shuffle(self.deck) # shuffle deck in place
        for player in range(self.num_players):
            self.hands[player] = [card.rank for card in self.deck[:self.num_cards_per_hand]] # deal cards - order doesn't really matter
            self.deck = self.deck[self.num_cards_per_hand:] # remove dealt cards from deck

    def play_game(self, verbose=False):
        # Dealing Phase
        self.deal_cards() # deal cards
        if verbose: # all verbose if statements are simply for printing out the game state for debugging and small scale testing
            print("--- Dealing Phase ---")
            for player in range(self.num_players):
                print(f"Player {player + 1} dealt hand: {self.hands[player]}")

        # Bidding Phase
        if verbose:
            print("\n--- Bidding Phase ---")
        for player in range(self.num_players):
            self.predictions[player] = self.agents[player].bid(self.hands[player]) # call on agent's method for bidding - this is where we can implement algorithmic learning for bidding
            if verbose:
                print(f"Player {player + 1} bids {self.predictions[player]}")

        # Playing Phase
        if verbose:
            print("\n--- Playing Phase ---")
        for round_number in range(self.num_cards_per_hand):
            if verbose:
                print(f"--Round {round_number + 1}--")
            for player in range(self.num_players):
                card = self.agents[player].play_card(self.hands[player], round_number) # call on an agent's method for selecting a card - this is where we can implement algorithmic learning for playing cards
                if verbose:
                    print(f"Player {player + 1} plays {card}")
                self.play_card(player, card) # we then play the card and remove it from the player's hand as implemented
            winner = self.determine_trick_winner() # determine the winner of the "trick" - the trick is the set of cards played by each player in a round
            if verbose:
                print(f"Player {winner + 1} wins")
                for player in range(self.num_players):
                    print(f"Player {player + 1} rounds won: {self.tricks_won[player]}")
                print()

        # Score the round
        return self.score_round() # return the score of the round - comparing the predictions to the actual number of tricks won

    def play_card(self, player, card):
        if card in self.hands[player]:
            self.hands[player].remove(card)
            self.current_trick.append((player, card))
        else:
            raise ValueError(f"Player {player} does not have card {card}") # raises error if agent model spits out a card that is not in the player's hand

    def determine_trick_winner(self):
        rank_values = {str(n): n for n in range(2, 11)}
        rank_values.update({'J': 11, 'Q': 12, 'K': 13, 'A': 14}) # need to update the rank values for the face cards

        if self.current_trick:
            winner, winning_card = max(self.current_trick, key=lambda x: rank_values[x[1]])
            self.tricks_won[winner] += 1
            self.current_trick = []
            return winner

    def score_round(self):
        differences = {player: abs(self.tricks_won[player] - self.predictions[player]) for player in range(self.num_players)}
        i, j = differences[0], differences[1]
        if i == j:
            return {0: 0, 1: 0}
        else:
            return {0: j - i, 1: i - j} # this returns the zero-sum score of the round according to our reference shift

