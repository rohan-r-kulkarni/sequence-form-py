import numpy as np
from scipy.sparse import lil_matrix
from extensive_form_game import extensive_form_game as efg
from scipy.stats import norm

def init_efg(num_rounds=3, num_ranks=10, num_copy=1, k=3, prox_infoset_weights=False, prox_scalar=-1):

    assert num_rounds >= 1
    num_cards = num_ranks * num_copy

    parent = ([], [])
    begin = ([], [])
    end = ([], [])
    payoff = []
    reach = []
    next_s = [1,1]

    def _p_chance(cards_deep):
        probs = 1.0
        for i in range(cards_deep):
            probs = probs * float(1/(num_cards-i))
        return probs

    def _build_bid(player, num_rounds, previous_seq,b=0):
        opponent = 1 - player
        num_actions = num_rounds + 1

        def _p_chance_bid(i, j):
            mean_bid = num_rounds / 2  # Center the distribution around the middle bid
            std_dev_bid = num_rounds / 3  # Make the distribution wide enough to cover all bids
            
            prob_i = norm.cdf(i + 0.5, loc=mean_bid, scale=std_dev_bid) - norm.cdf(i - 0.5, loc=mean_bid, scale=std_dev_bid)
            prob_j = norm.cdf(j + 0.5, loc=mean_bid, scale=std_dev_bid) - norm.cdf(j - 0.5, loc=mean_bid, scale=std_dev_bid)

            #find probability of i and j both being between 0 and num_rounds
            overall_prob = norm.cdf(num_rounds + 0.5, loc=mean_bid, scale=std_dev_bid) - norm.cdf(-0.5, loc=mean_bid, scale=std_dev_bid)

            # Return the joint probability
            return (prob_i * prob_j)/overall_prob
        
        info_set = len(begin[player])
        for i in range(num_actions):
            parent[player].append(previous_seq[player][i])
            begin[player].append(next_s[player])
            next_s[player] += 1
            end[player].append(next_s[player])
            for j in range(num_actions):
                reach.append((player, info_set+i, previous_seq[opponent][j], _p_chance_bid(i, j)))
        
        def _pn(idx):
            t = [begin[player][info_set + i] + idx for i in range(num_rounds + 1)]
            if player == 0:
                return (t, previous_seq[1])
            return (previous_seq[0], t)
        
        for bid in range(num_rounds + 1):
            if opponent == 0:
                _build_play(b,bid,1, opponent, 0, _pn(bid))
            else:
                _build_bid(opponent, num_rounds, _pn(bid), bid)

    def _build_play(b0,b1,rnd, player, num_tricks_taken, previous_seq):
        opponent = 1 - player
        if player == 0 and rnd == 1: #  first action
            num_actions = num_rounds + 1
        else: num_actions = num_cards - (2*(rnd-1))

        info_set = len(begin[player])
        num_actions = num_ranks
        
        info_set = len(begin[player])
        for card_played in range(num_actions):
            parent[player].append(previous_seq[player][card_played])
            begin[player].append(next_s[player])
            next_s[player] += 1
            end[player].append(next_s[player])
            if player == 0 and rnd == 1:
                for opp_bet in range(num_rounds + 1):
                    reach.append((player, info_set + card_played, previous_seq[opponent][opp_bet], _p_chance(2)))
            else:
                for opponent_card in range(num_actions):
                    reach.append((player, info_set + card_played, previous_seq[opponent][opponent_card], _p_chance((rnd-1)*2)))

        def _pn(idx):
            t = [begin[player][info_set + card_played] + idx for card_played in range(num_actions)]
            if player == 0:
                return (t, previous_seq[1])
            return (previous_seq[0], t)
        
        if rnd < num_rounds:
            if opponent == 1:
                for card_played in range(num_actions):
                    if card_played > 0:
                        for i in range(2):
                            _build_play(b0,b1,rnd, opponent, num_tricks_taken+i, _pn(card_played))
                    else: _build_play(b0,b1,rnd, opponent, num_tricks_taken, _pn(card_played))
            else: 
                for card_played in range(num_actions):
                    if card_played > 0:
                        for i in range(2):
                            _build_play(b0,b1,rnd+1, opponent, num_tricks_taken+i, _pn(card_played))
                    else: _build_play(b0,b1,rnd+1, opponent, num_tricks_taken, _pn(card_played))
        else:
            for card_played in range(num_actions):
                _build_terminal(b0,b1,opponent, num_tricks_taken, _pn(card_played))

    def _build_terminal(b0,b1, player, num_tricks_taken, previous_seq):
        
        def _value(b0,b1,p0_tricks, p1_tricks):
            x = abs(b0-p0_tricks)
            y = abs(b1-p1_tricks)
            return y-x

        for i in range(num_ranks):
            for j in range(num_ranks):
                payoff.append((previous_seq[0][i], previous_seq[1][j],
                               _p_chance(num_rounds) * _value(i, j, num_tricks_taken, num_rounds - num_tricks_taken)))
                
    previous_seg = ([0] * num_ranks, [0] * num_ranks)
    _build_bid(0, num_rounds, previous_seg)
    payoff_matrix = lil_matrix(next_s[0], next_s[1])
    for i,j,payoff_value in payoff:
        payoff_matrix[i,j] += payoff_value
    reach_matrix = (lil_matrix(len(begin[0]), next_s[1]), lil_matrix(len(begin[1]), next_s[0]))
    for player, infoset, opponent_seq, prob in reach:
        reach_matrix[player][infoset, opponent_seq] += prob
    
    return efg.ExtensiveFormGame(
            'bozoj-%d' % num_ranks,
            payoff_matrix,
            begin,
            end,
            parent,
            prox_infoset_weights=prox_infoset_weights,
            prox_scalar=prox_scalar,
            reach=reach_matrix)