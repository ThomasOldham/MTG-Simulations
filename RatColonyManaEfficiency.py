import ColorlessGoldfish
import Card
import Deck

RAT_COLONY = Card.Card(land=False, manaCost='1B')
SWAMP = Card.Card(land=True, manaEachTurn='B')

def deck():
    """ Constructs and returns a deck with 40 Rat Colonies and 20 Swamps """
    deck = Deck.Deck()
    for i in range(40):
        deck.add_card_to_top(RAT_COLONY)
    for i in range(20):
        deck.add_card_to_top(SWAMP)
    deck.shuffle()
    return deck

def simulation():
    """ Runs a simulation for the deck as described in ColorlessGoldfish.py
        and returns the results. """
    return ColorlessGoldfish.simulation(deck())

