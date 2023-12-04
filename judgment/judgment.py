from itertools import chain
from itertools import product
import numpy as np
from scipy.sparse import lil_matrix
import scipy.special as spsp
# import matrix_game
# from extensive_form_game import extensive_form_game as efg
"""
create Judgment matrix game
"""

def init_matrix(k=2):
    N = spsp.factorial(k+1)
    A = np.empty((N, N))

    #ordering

    for i in range(M):
        x = [i / 3**k % 3 for k in range(num_ranks)]
        for j in range(N):
            y = [j / 4**k % 4 for k in range(num_ranks)]

            t = 0
            for c1 in range(num_ranks):
                for c2 in range(num_ranks):
                    if c1 < c2:
                        t += FOLD[x[c1]][y[c2]] - SHOWDOWN[x[c1]][y[c2]]
                    elif c1 > c2:
                        t += FOLD[x[c1]][y[c2]] + SHOWDOWN[x[c1]][y[c2]]

            A[i, j] = -alpha * t
    return A
    # return matrix_game.MatrixGame('Kuhn%d' % num_ranks, A)

if __name__ == "__main__":
    