import numpy.random as r

class Deck:
    cards = []
    
    def draw(self):
        return self.cards.pop()
    
    def take_bottom_card(self):
        return self.cards.pop(0)
    
    def add_card_to_top(self, card):
        self.cards.append(card)
    
    def add_card_to_bottom(self, card):
        self.cards.insert(0, card)
    
    def shuffle(self):
        r.shuffle(self.cards)