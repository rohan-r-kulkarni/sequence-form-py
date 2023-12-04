import numpy as np
from scipy.sparse import lil_matrix
from extensive_form_game import extensive_form_game as efg

def init_efg(num_rounds=5, num_players=2, prox_infoset_weights=False, prox_scalar=-1):
    
    assert num_rounds >= 1

    num_cards = 52  # Standard deck
    num_bids = num_rounds + 1  # Including the final bid

    parent = [[], []]
    begin = [[], []]
    end = [[], []]
    payoff = []
    reach = []
    next_s = [1] * num_players

    def _p_chance(rnd, bid, card, player):
        if rnd == 0:
            return 1.0 / num_cards  # Initial chance node: dealing cards
        else:
            return 1.0 / (num_cards - card)  # Subsequent chance nodes

    def _build_terminal(rnd, bid, card, player, previous_seq):
        # Payoff function for the terminal node
        def _value(player, bid, card):
            # zero-sum payoff version of the game
            # Calculate the difference between the bid and the actual tricks taken
            player_diff = bid - card
            other_players = [p for p in range(num_players) if p != player]
    
            # Calculate the difference for the other player
            other_player_diff = sum(bid - card for p in other_players)
    
            # Calculate the payoff based on the zero-sum structure
            if player_diff < other_player_diff:
                # Player is closer to their bid
                return player_diff - other_player_diff
            elif player_diff > other_player_diff:
                # Other player is closer to their bid
                return other_player_diff - player_diff
            else:
                # Both players are equally distant from their bids (tie)
                return 0

        for p in range(num_players):
            payoff.append((previous_seq[p], _value(p, bid, card)))

    def _build_bid(rnd, bid, card, player, previous_seq):
        info_set = len(begin[player])
        parent[player].append(previous_seq[player])
        begin[player].append(next_s[player])
        next_s[player] += 2  # Two possible actions: bid or pass
        end[player].append(next_s[player])

        for b in range(num_bids):
            reach.append((player, info_set, _as_list(previous_seq[player]), _p_chance(rnd, b, card, player)))

            if b == bid:
                _build_play(rnd, b, card, player, _pn(b))

    def _build_play(rnd, bid, card, player, previous_seq):
        info_set = len(begin[player])
        parent[player].append(previous_seq[player])
        begin[player].append(next_s[player])
        next_s[player] += num_cards - card
        end[player].append(next_s[player])

        for c in range(card, num_cards):
            reach.append((player, info_set, _as_list(previous_seq[player]), _p_chance(rnd, bid, c, player)))

            _build_terminal(rnd, bid, c, player, _pn(c))

    def _pn(idx):
        return tuple(begin[p][-1] + idx if begin[p] else idx for p in range(num_players))

    def _as_list(value):
        # Convert a single value to a list
        return [value] if not isinstance(value, list) else value

    for r in range(num_rounds):
        for p in range(num_players):
            _build_bid(r, 0, 0, p, _pn(0))

    # Construct matrices
    payoff_matrix = lil_matrix((next_s[0],) * num_players)
    reach_matrix = (lil_matrix(len(begin[0]), next_s[1]), lil_matrix(len(begin[1]), next_s[0]))

    for i, v in payoff:
        payoff_matrix[i] += v

    for player, infoset, opponent_seq, prob in reach:
        #print(reach_matrix[player].shape, infoset, opponent_seq)
        #print(reach_matrix[player][infoset, opponent_seq])
        reach_matrix[player][0,0] = prob

    return efg.ExtensiveFormGame(
        'Judgment%d' % num_rounds,
        payoff_matrix,
        begin,
        end,
        parent,
        prox_infoset_weights=prox_infoset_weights,
        prox_scalar=prox_scalar,
        reach=reach_matrix
    )