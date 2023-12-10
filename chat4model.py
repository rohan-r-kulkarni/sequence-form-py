from extensive_form_game import extensive_form_game as efg
from scipy.sparse import lil_matrix

def init_efg(num_players=2, max_rounds=2, integer=False, prox_infoset_weights=False, prox_scalar=-1, deck_size=10):
    assert num_players >= 2
    num_cards_per_round = [r for r in range(1, max_rounds + 1)] + [r for r in range(max_rounds - 1, 0, -1)]

    parent = ([], [])
    begin = ([], [])
    end = ([], [])
    payoff = []
    reach = []
    next_s = [1, 1]

    # Function to calculate the probability of a certain card being played
    def _p_card_play(chosen_card, hand_size):
        if integer:
            return 1 / hand_size
        else:
            return 1.0 / hand_size

    # Function to build terminal nodes based on bids and tricks won
    def _build_terminal(bid, tricks_won, previous_seq):
        for i in range(num_players):
            for j in range(num_players):
                score = -1 if abs(bid-tricks_won)<=1 else 1
                payoff.append((previous_seq[0][i], previous_seq[1][j], _p_card_play(j, len(num_cards_per_round)) * score))

    # Recursive function to build the game tree
    def _build(round_number, trick_number, player, bid, tricks_won, previous_seq):
        hand_size = num_cards_per_round[round_number]
        num_actions = hand_size  # Number of possible cards to play

        info_set = len(begin[player])
        for i in range(num_players):
            parent[player].append(previous_seq[player][i])
            begin[player].append(next_s[player])
            next_s[player] += num_actions
            end[player].append(next_s[player])
            for j in range(num_players):
                reach.append((player, info_set + i, previous_seq[1 - player][j], _p_card_play(j, hand_size)))

        def _pn(idx):
            t = [begin[player][info_set + i] + idx for i in range(num_players)]
            return (t, previous_seq[1]) if player == 0 else (previous_seq[0], t)

        if trick_number == hand_size:
            _build_terminal(bid, tricks_won, previous_seq)
        else:
            # Recursive call for the next card play
            for action in range(num_actions):
                _build(round_number, trick_number + 1, 1 - player, bid, tricks_won, _pn(action))
                _build(round_number, trick_number + 1, 1 - player, bid, tricks_won+1, _pn(action))

    previous_seq = ([0] * num_players, [0] * num_players)
    for round_number in range(len(num_cards_per_round)):
        for bid in range(num_cards_per_round[round_number] + 1):
            _build(round_number, 0, 0, bid, 0, previous_seq)

    payoff_matrix = lil_matrix((next_s[0], next_s[1]), dtype=int if integer else float)
    for i, j, payoff_value in payoff:
        payoff_matrix[i, j] += payoff_value

    reach_matrix = (lil_matrix((len(begin[0]), next_s[1])), lil_matrix((len(begin[1]), next_s[0])))
    for player, infoset, opponent_seq, prob in reach:
        reach_matrix[player][infoset, opponent_seq] += prob


    print(reach_matrix)


    return efg.ExtensiveFormGame(
            'BOZOJ-%d' % max_rounds,
            payoff_matrix,
            begin,
            end,
            parent,
            prox_infoset_weights=prox_infoset_weights,
            prox_scalar=prox_scalar,
            reach=reach_matrix)