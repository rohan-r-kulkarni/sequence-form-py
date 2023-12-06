import matplotlib.pyplot as plt
import numpy as np

from judgment import JudgementGameRankOnly

from agents import RandomAgent
from agents import AggressiveAgent
from agents import SlyAgent

# Creating the agents
agent1 = SlyAgent()
agent2 = AggressiveAgent()

# Initializing the game with 5 cards per hand
game = JudgementGameRankOnly(agent1, agent2, num_cards_per_hand=5)

# Running the game simulation with verbose output
game_score = game.play_game(verbose=True)
print(game_score)


# ## EXAMPLE CUMULATIVE UTILITY OUTPUT
# # running the game simulation 1000 times to calculate cumulative utility for each agent
# num_games = 1000

# # initialize the cumulative utility for each agent
# agent_1_utility = []
# agent_2_utility = []

# for i in range(num_games):
#     # define a game with agents and 5 cards per hand
#     game = JudgementGameRankOnly(agent1, agent2, num_cards_per_hand=5)
#     # play the game
#     utility_scores = game.play_game()
#     # update the cumulative utility for each agent using the utility scores
#     agent_1_utility.append(utility_scores[0])
#     agent_2_utility.append(utility_scores[1])
    
# agent_1_cumulative_utility = np.cumsum(agent_1_utility)
# agent_2_cumulative_utility = np.cumsum(agent_2_utility)    

# # plot the cumulative utility for each agent
# plt.plot(agent_1_cumulative_utility, label='Agent 1')
# plt.plot(agent_2_cumulative_utility, label='Agent 2')
# plt.legend()
# plt.xlabel('Game Number')
# plt.ylabel('Cumulative Utility')
# plt.show()

# # This output shows that the AgressiveAgent gameplay dominates SlyAgent gameplay.
