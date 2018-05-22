import ColorlessGoldfish
import Card
import Deck
import numpy as N
import numpy.ma as M
import Mana
from PIL import Image
import warnings

RAT_COLONY = Card.Card(land=False, manaCost='1B')
SWAMP = Card.Card(land=True, manaEachTurn='B')
GOLDFISH_STARTING_LIFE = 20
DEBUG = False
GOOD_COLOR = (0x00, 0x00, 0xFF)
BAD_COLOR = (0xFF, 0x00, 0x00)
NO_DATA_COLOR = (0xFF, 0xFF, 0xFF)

def deck():
    """ Constructs and returns a deck with 40 Rat Colonies and 20 Swamps """
    deck = Deck.Deck()
    for i in range(40):
        deck.add_card_to_top(RAT_COLONY)
    for i in range(20):
        deck.add_card_to_top(SWAMP)
    deck.shuffle()
    return deck

def simulation(hand_size = 7):
    """ Runs a simulation for the deck as described in ColorlessGoldfish.py
        and returns the results. """
    return ColorlessGoldfish.simulation(deck(), hand_size = hand_size)

def kill_turn():
    """ Runs a simulation and gets the turn when the goldfish is defeated. """
    states = simulation()
    goldfish_life = GOLDFISH_STARTING_LIFE
    previous_rats = 0
    for i in range(len(states)):
        state = states[i]
        rats = 0
        for card in state.board:
            if not card.land:
                rats += 1
        goldfish_life -= (rats + 1) * previous_rats
        if goldfish_life <= 0:
            return i
        previous_rats = rats
    return len(states)

def mana_efficiency_and_num_lands(hand_size):
    """ Runs a simulation and gets the total amount of mana spent
        during the game and the number of lands in the opening hand.
    """
    states = simulation()
    final_state = states[-1]
    mana = 0
    for card in final_state.board:
        mana += Mana.converted(card.manaCost)
    lands = 0
    first_state = states[0]
    for card in first_state.hand:
        if card.land:
            lands += 1
    return mana, lands

def mana_efficiency_by_hand(num_simulations_per_hand_size = 1000, \
max_hand_size = 7):
    """ Runs a given number of simulations and organizes them by number
        of card in starting hand and number of lands in starting hand.
        Returns a 2D masked array of mana efficiencies with the first index
        representing the number of cards and the second index representing
        the number of lands. Masked elements have no data. Last number of
        lands (one more than the number of cards) is instead the average
        across all land numbers.
    """
    
    counts = N.zeros((max_hand_size + 1, max_hand_size + 2))
    sums = N.zeros((max_hand_size + 1, max_hand_size + 2))
    for hand_size in range(max_hand_size + 1):
        for iteration in range(num_simulations_per_hand_size):
            mana, lands = mana_efficiency_and_num_lands(hand_size)
            if DEBUG:
                print(hand_size, lands)
            counts[hand_size, lands] += 1
            counts[hand_size, -1] += 1
            sums[hand_size, lands] += mana
            sums[hand_size, -1] += mana
    if DEBUG:
        print(counts)
        print(sums)
    
    mask = []
    for column in counts:
        mask.append([])
        for value in column:
            mask[-1].append(value == 0)
    averages = None
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        # https://stackoverflow.com/questions/14463277/how-to-disable-python-warnings
        averages = M.masked_array(sums / counts, mask=mask)
    return averages

def hand_performance_picture(test_results):
    """ Not implemented. """
    pass