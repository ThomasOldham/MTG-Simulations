# Class representing a deck in Magic the Gathering
import numpy.random as r

class Deck:
    cards = None
    
    def __init__(self):
        self.cards = []
    
    def draw_hand(self):
        """ Draws and returns the top 7 cards in the deck. Cards are removed 
        from the deck
        """
        hand = []
        for i in range(8):
            hand.append(self.draw())
        return hand
        
    def peep(self,num):
        """ Looks at the first 'num' cards at the top of the deck. The cards are 
        not removed from the deck
        """
        return self.cards[:num]
        
    def draw(self):
        """ Draws a single card from the deck
        """
        return self.cards.pop()
    
    def take_bottom_card(self):
        return self.cards.pop(0)
    
    def add_card(self, card):
        self.cards.append(card)
    
    def add_card_to_bottom(self, card):
        self.cards.insert(0, card)
        
    def clear(self):
        """ Empties the deck
        """
        del self.cards[:]
    
    def shuffle(self):
        r.shuffle(self.cards)