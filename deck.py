import numpy.random as r

class Deck:
    """ Represents a deck of cards, but you can put any data type in.
        You can build a deck using either the add_card_to_top and
        add_card_to_bottom methods or by directly manipulating the "cards"
        attribute.
    """
    
    cards = None
    
    def __init__(self):
        self.cards = []
    
    def draw(self):
        """ Removes and returns the top card. """
        return self.cards.pop()
    
    def take_bottom_card(self):
        """ Removes and returns the bottom card. """
        return self.cards.pop(0)
    
    def add_card_to_top(self, card):
        """ Adds a card to the top of the deck. """
        self.cards.append(card)
    
    def add_card_to_bottom(self, card):
        """ Adds a card to the bottom of the deck."""
        self.cards.insert(0, card)
    
    def shuffle(self):
        """ Randomly reorders the cards in the deck. """
        r.shuffle(self.cards)