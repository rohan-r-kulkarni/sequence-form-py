from itertools import chain
from itertools import product
from itertools import combinations, permutations
import numpy as np
from scipy.sparse import lil_matrix
import scipy.special as spsp
# import matrix_game
# from extensive_form_game import extensive_form_game as efg
"""
create Judgment matrix game
single-shot, open hand
"""

def calculate_wins(x_play, y_play):
    """
    Calculates open hand number of wins for each player in single shot
    given hands dealt
    Tuples are always sorted
    """
    x_wins = 0
    y_wins = 0
    for p in range(len(x_play)-1, -1, -1):
        if x_play[p] > y_play[p]:
            x_wins += 1
        elif y_play[p] > x_play[p]:
            y_wins += 1
    return x_wins, y_wins

def init_matrix(n=10, k=1, ordered=True):
    if ordered == False:
        N = int(spsp.comb(n, k)*(k+1))

        A = np.empty((N, N))

        deck = np.arange(1,n+1)
        comb_list = list(combinations(deck, k)) # possible dealt hand (card1, card2)
        x = []
        for k_prime in range(k+1):
            for comb in comb_list:
                x.append((k_prime, comb))
        y = x.copy()

        print(x)

        for i in range(N):
            for j in range(N):
                x_strat = x[i]
                y_strat = y[j]
                
                x_wins, y_wins = calculate_wins(x_strat[1], y_strat[1])
                x_diff = abs(x_strat[0] - x_wins)
                y_diff = abs(y_strat[0] - y_wins)
                
                if x_diff == y_diff: #payoff matrix for player 1
                    A[i, j] = 0
                else:
                    # if x_diff > y_diff, player 1 does worse (negative payoff)
                    # if x_diff < y_diff, player 1 does better (positive payoff)
                    A[i, j] = y_diff - x_diff
    else:
        N = int(spsp.comb(n, k)*(k+1)*spsp.factorial(k))

        A = np.empty((N, N))

        deck = np.arange(1,n+1)
        perm_list = list(permutations(deck, k)) # possible dealt hand (card1, card2)
        x = []
        for k_prime in range(k+1):
            for perm in perm_list:
                perm = list(perm)
                x.append((k_prime, perm))
        y = x.copy()

        print(x)

        for i in range(N):
            for j in range(N):
                x_strat = x[i]
                y_strat = y[j]
                
                x_wins, y_wins = calculate_wins(x_strat[1], y_strat[1])
                x_diff = abs(x_strat[0] - x_wins)
                y_diff = abs(y_strat[0] - y_wins)
                
                if x_diff == y_diff: #payoff matrix for player 1
                    A[i, j] = 0
                else:
                    # if x_diff > y_diff, player 1 does worse (negative payoff)
                    # if x_diff < y_diff, player 1 does better (positive payoff)
                    A[i, j] = y_diff - x_diff
    print(A)
    # return matrix_game.MatrixGame('SingleShotJudgment%d' % k, A)

if __name__ == "__main__":
    print(init_matrix(k=3, ordered=True))
