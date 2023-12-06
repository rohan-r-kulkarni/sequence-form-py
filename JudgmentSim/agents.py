class Agent:
    """
    This is a base class for an Agent that will be used to simulate a player in the game.
    The classes that inherit from this should implement the bid() and play_card() methods.
    """
    def bid(self, hand):
        raise NotImplementedError("Subclasses should implement this method")

    def play_card(self, hand, round_number):
        raise NotImplementedError("Subclasses should implement this method")

# We'll also create two simple agents that inherit from Agent class for testing purposes.
class RandomAgent(Agent):
    """
    An agent that bids and plays cards randomly.
    """
    import random

    def bid(self, hand):
        return self.random.randint(0, len(hand))

    def play_card(self, hand, round_number):
        return self.random.choice(hand)
    
class AggressiveAgent(Agent):
    """
    An aggressive agent that always bids the number of cards in their hand with a rank higher than 10,
    and always plays the maximum card.
    """
    def bid(self, hand):
        # Count the number of cards with rank higher than 10 ('J', 'Q', 'K', 'A')
        high_cards = sum(1 for card in hand if card in ['J', 'Q', 'K', 'A'])
        return high_cards

    def play_card(self, hand, round_number):
        # Play the maximum card
        rank_values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
        max_card = max(hand, key=lambda card: rank_values[card])
        return max_card

class SlyAgent(Agent):
    """
    A sly agent that saves their large cards for later in the game, bidding zero and playing the minimum card initially.
    """
    def bid(self, hand):
        # Bid zero initially
        return 0

    def play_card(self, hand, round_number):
        # Save larger cards for later, play the minimum card
        rank_values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
        # If we are in the last rounds, start using the high cards
        if round_number >= len(hand) / 2:
            min_card = max(hand, key=lambda card: rank_values[card])
        else:
            min_card = min(hand, key=lambda card: rank_values[card])
        return min_card