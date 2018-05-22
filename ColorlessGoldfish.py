import copy
import Mana
import numpy.random as r

DEBUG = False
TURN_OPTIONS_DEBUG = False
VALID_TURNS_DEBUG = True

class IntSet:
    """ Hashable set of integers """
    contents = set()
    
    def __hash__(self):
        ret = 1
        for num in self.contents:
            ret *= num
        return ret
    
    def __eq__(self, item):
        if len(self.contents) != len(item.contents):
            return False
        for element in self.contents:
            if element not in item.contents:
                return False
        return True
    
    def __ne__(self, item):
        return not self.__eq__(item)

class SimState:
    deck = None
    hand = None
    board = None
    goldfish_life = None
    
    def __init__(self, deck, goldfish_life = 20):
        self.deck = deck
        self.hand = []
        self.board = []
        self.goldfish_life = goldfish_life

def _play_turn(state):
    ret = copy.deepcopy(state)
    # Draw a card
    ret.hand.append(ret.deck.draw())
    # Calculate mana available
    mana = 0
    for card in ret.board:
        mana += Mana.converted(card.manaEachTurn)
    # Get all possible turns
    possible_turns = set()
    _turn_options(ret.hand, mana, possible_turns, IntSet(), False)
    # Get all options tied for most mana spent
    best_turn_mana = 0
    for turn in possible_turns:
        turn_mana = 0
        for cardIndex in turn.contents:
            card = ret.hand[cardIndex]
            turn_mana += Mana.converted(card.manaCost)
        best_turn_mana = max(turn_mana, best_turn_mana)
    if DEBUG:
        print(len(possible_turns))
    best_turns = []
    for turn in possible_turns:
        turn_mana = 0
        for cardIndex in turn.contents:
            card = ret.hand[cardIndex]
            turn_mana += abs(Mana.converted(card.manaCost) -
            Mana.converted(card.manaFirstTurn))
        if turn_mana == best_turn_mana:
            best_turns.append(turn)
    # Among tied options, get all options tied for highest increase in
    # available mana
    best_mana_increase = 0
    for turn in best_turns:
        mana_increase = 0
        for cardIndex in turn.contents:
            card = ret.hand[cardIndex]
            mana_increase += Mana.converted(card.manaEachTurn)
        best_mana_increase = max(best_mana_increase, mana_increase)
    best_mana_increase_turns = []
    for turn in best_turns:
        mana_increase = 0
        for cardIndex in turn.contents:
            card = ret.hand[cardIndex]
            mana_increase += Mana.converted(card.manaEachTurn)
        if mana_increase == best_mana_increase:
            best_mana_increase_turns.append(turn)
    # Among tied options, choose at random
    chosen_turn = best_mana_increase_turns[
    r.randint(len(best_mana_increase_turns))]
    if DEBUG:
        print(chosen_turn.contents)
    # Play turn.
    if VALID_TURNS_DEBUG:
        print(len(ret.hand), chosen_turn.contents)
    for cardIndex in chosen_turn.contents:
        card = ret.hand[cardIndex]
        ret.hand[cardIndex] = None
        ret.board.append(card)
    while None in ret.hand:
        ret.hand.remove(None)
    return ret

def _turn_options(hand, mana, tested_options, chosen_indices, played_land):
    if TURN_OPTIONS_DEBUG:
        print(tested_options)
    if chosen_indices in tested_options:
        return
    tested_options.add(chosen_indices)
    if TURN_OPTIONS_DEBUG:
        print(tested_options)
    for i in range(len(hand)):
        card = hand[i]
        if (i not in chosen_indices.contents) and \
        Mana.converted(card.manaCost) <= mana and \
        ((not played_land) or not card.land):
            new_chosen_indices = copy.deepcopy(chosen_indices)
            new_chosen_indices.contents.add(i)
            new_mana = mana - Mana.converted(card.manaCost) + \
            Mana.converted(card.manaFirstTurn)
            if not card.pseudoETBT:
                new_mana += Mana.converted(card.manaEachTurn)
            _turn_options(hand, new_mana, tested_options,
            new_chosen_indices, played_land)

def simulation(deck, hand_size = 7, num_turns = 5):
    """ Runs a simulated game using the given deck, hand size (default 7), and
        max number of turns (default 5)
    """
    state = SimState(deck)
    states = [state]
    for i in range(hand_size):
        state.hand.append(state.deck.draw())
    for i in range(num_turns):
        states.append(_play_turn(states[-1]))
    return states