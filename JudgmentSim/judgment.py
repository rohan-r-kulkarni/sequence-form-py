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
        random.shuffle(self.deck)
        for player in range(self.num_players):
            self.hands[player] = [card.rank for card in self.deck[:self.num_cards_per_hand]]
            self.deck = self.deck[self.num_cards_per_hand:]

    def play_game(self, verbose=False):
        # Dealing Phase
        self.deal_cards()
        if verbose:
            print("--- Dealing Phase ---")
            for player in range(self.num_players):
                print(f"Player {player + 1} dealt hand: {self.hands[player]}")

        # Bidding Phase
        if verbose:
            print("\n--- Bidding Phase ---")
        for player in range(self.num_players):
            self.predictions[player] = self.agents[player].bid(self.hands[player])
            if verbose:
                print(f"Player {player + 1} bids {self.predictions[player]}")

        # Playing Phase
        if verbose:
            print("\n--- Playing Phase ---")
        for round_number in range(self.num_cards_per_hand):
            if verbose:
                print(f"--Round {round_number + 1}--")
            for player in range(self.num_players):
                card = self.agents[player].play_card(self.hands[player], round_number)
                if verbose:
                    print(f"Player {player + 1} plays {card}")
                self.play_card(player, card)
            winner = self.determine_trick_winner()
            if verbose:
                print(f"Player {winner + 1} wins")
                for player in range(self.num_players):
                    print(f"Player {player + 1} rounds won: {self.tricks_won[player]}")
                print()

        # Score the round
        return self.score_round()

    def play_card(self, player, card):
        if card in self.hands[player]:
            self.hands[player].remove(card)
            self.current_trick.append((player, card))
        else:
            raise ValueError(f"Player {player} does not have card {card}")

    def determine_trick_winner(self):
        rank_values = {str(n): n for n in range(2, 11)}
        rank_values.update({'J': 11, 'Q': 12, 'K': 13, 'A': 14})

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
            return {0: j - i, 1: i - j}

# We'll reuse the RandomAgent class for simplicity.
# Let's create a JudgementGameRankOnly instance with 5 cards per hand and simulate a game.

# Creating the agents
agent1 = RandomAgent()
agent2 = RandomAgent()

# Initializing the game with 5 cards per hand
game = JudgementGameRankOnly(agent1, agent2, num_cards_per_hand=5)

# Running the game simulation with verbose output
game_score = game.play_game()
game_score
