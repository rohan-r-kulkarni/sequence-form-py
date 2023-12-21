from itertools import chain
from itertools import product
from itertools import combinations, permutations
import numpy as np
from scipy.sparse import lil_matrix
import scipy.special as spsp
import matrix_game
from extensive_form_game import extensive_form_game as efg
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

def get_order_hands(order, n=10, k=1):
    """
    Returns the hands out of all possible hands that follow this ordering
    order = np.array()
    """
    deck = np.arange(1,n+1)
    perm_list = np.array(list(permutations(deck, k))) #all possible nPk
    argsorts = perm_list.argsort(axis=1)+1
    matches = np.sum(order == argsorts, axis=1)==k
    return perm_list[matches]

def contains_same_card(hand1, hand2):
    """
    Returns True if hand1 and hand2 contain the same card
    """
    for card in hand1:
        if card in hand2:
            return True
    return False

def init_matrix(n=10, k=1):
    ## Action space:
    ## what you bet * all possible orderings of your cards
    ## (k+1) * (k!) = (k+1)!
    ## for each row, col action pair:
        ## calculate the number of hands that follow this rank ordering that you and the opponent can play
        ## calculate the number of wins + payoff against all possible ways that opponent can play
        ## average the payoff (expected value)
    
    N = int(spsp.factorial(k+1)) # number of ordered strategies

    A = np.empty((N, N))

    deck = np.arange(1,n+1)
    perm_list = list(permutations(range(1,k+1))) # every ordering to play of k cards
    x = []
    for k_prime in range(k+1): #all possible bets you can make
        for perm in perm_list:
            perm = np.array(perm)
            x.append(np.insert(perm, 0, k_prime)) #bet, ordering
    x = np.array(x)
    y = x.copy()

    for i in range(N):
        for j in range(N):
            X_bet, X_ordering = x[i, 0], x[i, 1:]
            Y_bet, Y_ordering = y[j, 0], y[j, 1:]
            
            X_all_hands = get_order_hands(X_ordering, n, k)
            Y_all_hands = get_order_hands(Y_ordering, n, k)

            payoffs = np.array([])
            probs = np.array([])

            for X_hand in X_all_hands:
                for Y_hand in Y_all_hands:
                    if contains_same_card(X_hand, Y_hand):
                        payoffs = np.append(payoffs, 0)
                        probs = np.append(probs, 0) #impossible
                        continue

                    X_wins, Y_wins = calculate_wins(X_hand, Y_hand)
                    X_diff = abs(X_bet - X_wins)
                    Y_diff = abs(Y_bet - Y_wins)
                    payoffs = np.append(payoffs, Y_diff - X_diff)
                    probs = np.append(probs, 1)

            # normalize probabilities (all hand dealings have equal probability)
            if np.sum(probs) != 0:
                probs = probs / np.sum(probs)
                ev = np.sum(payoffs*probs)
                A[i, j] = ev
            else:
                A[i,j] = 0

    # print(A)
    return matrix_game.MatrixGame('SingleShotJudgment%d' % k, A)

if __name__ == "__main__":
    print(init_matrix(n=6, k=3))
