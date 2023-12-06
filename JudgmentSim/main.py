from judgment import JudgementGameRankOnly

from agents import RandomAgent
from agents import AggressiveAgent
from agents import SlyAgent

# Creating the agents
agent1 = RandomAgent()
agent2 = AggressiveAgent()

# Initializing the game with 5 cards per hand
game = JudgementGameRankOnly(agent1, agent2, num_cards_per_hand=5)

# Running the game simulation with verbose output
game_score = game.play_game(verbose=True)
print(game_score)