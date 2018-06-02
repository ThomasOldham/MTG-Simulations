import ColorlessGoldfish
import card
import deck
import numpy as N
import numpy.ma as M
import mana
import warnings

RAT_COLONY = card.Card(is_land=False, manaCost='1B')
SWAMP = card.Card(is_land=True, manaEachTurn='B')
GOLDFISH_STARTING_LIFE = 20
DEBUG = False
GOOD_COLOR = (0x00, 0x00, 0xFF)
BAD_COLOR = (0xFF, 0x00, 0x00)
NO_DATA_COLOR = (0xFF, 0xFF, 0xFF)

DEBUG = False

def rats_deck():
    """ Constructs and returns a deck with 40 Rat Colonies and 20 Swamps """
    rats_deck = deck.Deck()
    for i in range(40):
        rats_deck.add_card(RAT_COLONY)
    for i in range(20):
        rats_deck.add_card(SWAMP)
    rats_deck.shuffle()
    return rats_deck

def simulation(hand_size = 7, num_turns = 5):
    """ Runs a simulation for the deck as described in ColorlessGoldfish.py
        and returns the results. """
    d = rats_deck()
    if DEBUG:
        print(len(d.cards))
    return ColorlessGoldfish.simulation(d, hand_size = hand_size, num_turns = num_turns)

def kill_turn():
    """ Runs a simulation and gets the turn when the goldfish is defeated.
        Returns -1 if goldfish is not defeated within 5 turns."""
    states = simulation()
    goldfish_life = GOLDFISH_STARTING_LIFE
    previous_rats = 0
    for i in range(len(states)):
        state = states[i]
        rats = 0
        for permanent in state.board:
            if not permanent.is_land:
                rats += 1
        goldfish_life -= (rats + 1) * previous_rats
        if goldfish_life <= 0:
            return i
        previous_rats = rats
    return -1

def mana_efficiency_and_num_lands(hand_size, num_turns = 5):
    """ Runs a simulation and gets the total amount of mana spent
        during the game and the number of lands in the opening hand.
    """
    states = simulation(hand_size = hand_size, num_turns = num_turns)
    final_state = states[-1]
    mana_count = 0
    for permanent in final_state.board:
        mana_count += mana.converted(permanent.manaCost)
    lands = 0
    first_state = states[0]
    for hand_card in first_state.hand:
        if hand_card.is_land:
            lands += 1
    if DEBUG:
        out = ""
        for hand_card in first_state.hand:
            out += " " + str(hand_card.is_land)
        print(out, lands)
    return mana_count, lands

def damage_and_num_lands(hand_size, num_turns = 5):
    """ Runs a simulation and gets the total amount of damage dealt
        during the game and the number of lands in the opening hand.
    """
    
    states = simulation(hand_size = hand_size, num_turns = num_turns)
    damage = 0
    previous_rats = 0
    for state in states:
        rats = 0
        for permanent in state.board:
            if not permanent.is_land:
                rats += 1
        damage += previous_rats * (rats + 2)
        previous_rats = rats
    first_state = states[0]
    lands = 0
    for hand_card in first_state.hand:
        if hand_card.is_land:
            lands += 1
    return damage, lands

def performance_by_hand(num_simulations_per_hand_size = 1000, \
max_hand_size = 7, num_turns = 5,
performance_and_num_lands = mana_efficiency_and_num_lands):
    """ Runs a given number of simulations and organizes them by number
        of card in starting hand and number of lands in starting hand.
        Returns a 2D masked array of performances (performance measured
        by a given metric, default mana efficienty) with the first index
        representing the number of cards and the second index representing
        the number of lands. Masked elements have no data. Last number of
        lands (one more than the number of cards) is instead the average
        across all land numbers. This type of array can be used with
        MulliganVisual to create a visual representation indicating when
        a mulligan is visual, and to what degree.
    """
    
    counts = N.zeros((max_hand_size + 1, max_hand_size + 2))
    sums = N.zeros((max_hand_size + 1, max_hand_size + 2))
    for hand_size in range(max_hand_size + 1):
        for iteration in range(num_simulations_per_hand_size):
            mana_count, lands = performance_and_num_lands(hand_size, num_turns = num_turns)
            if DEBUG:
                print(hand_size, lands)
            counts[hand_size, lands] += 1
            counts[hand_size, -1] += 1
            sums[hand_size, lands] += mana_count
            sums[hand_size, -1] += mana_count
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