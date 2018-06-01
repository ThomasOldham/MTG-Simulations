import copy
import mana
import numpy.random as r

DEBUG = False
TURN_OPTIONS_DEBUG = False
VALID_TURNS_DEBUG = False
NUM_ITERATIONS_DEBUG = False
LIST_INDEX_DEBUG = False
KOZILEK_DEBUG = False
DECK_OUT_DEBUG = False

class IntSet:
    """ Hashable set of integers.
        To read or write the contents, use the public member variable "contents."
        Changing what the reference points to is fine, but if you do so and
        then change the set from outside the class, it will of course change
        the contents of the IntSet object as well.
        Hash function is not very optimized.
    """
    contents = None
    
    def __init__(self):
        self.contents = set()
    
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
    """ A game state including the player's deck, hand, and field. """
    
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
    """ Uses an AI (defined by this function) to play a turn, attempting
        to use the available resources as well as it can, and returns the
        updated state.
    """
    
    ret = copy.deepcopy(state)
    if DECK_OUT_DEBUG:
        print(len(ret.deck.cards), "cards in deck")
    # Draw a card
    ret.hand.append(ret.deck.draw())
    # Calculate mana available
    mana_count = 0
    for card in ret.board:
        mana_count += mana.converted(card.manaEachTurn)
    # Get all possible turns
    possible_turns = set()
    _turn_options(ret.hand, mana_count, possible_turns, IntSet(), False)
    # Get all options tied for most mana spent
    best_turn_mana = 0
    for turn in possible_turns:
        turn_mana = 0
        for cardIndex in turn.contents:
            if LIST_INDEX_DEBUG:
                print(cardIndex, len(ret.hand))
            card = ret.hand[cardIndex]
            turn_mana += abs(mana.converted(card.manaCost) -
            mana.converted(card.manaFirstTurn))
        best_turn_mana = max(turn_mana, best_turn_mana)
    if KOZILEK_DEBUG:
        print(possible_turns)
    best_turns = []
    for turn in possible_turns:
        turn_mana = 0
        for cardIndex in turn.contents:
            card = ret.hand[cardIndex]
            turn_mana += abs(mana.converted(card.manaCost) -
            mana.converted(card.manaFirstTurn))
        if turn_mana == best_turn_mana:
            best_turns.append(turn)
        if KOZILEK_DEBUG:
            print(turn_mana, best_turn_mana)
    if KOZILEK_DEBUG:
        print(best_turn_mana, best_turns)
    # Among tied options, get all options tied for highest increase in
    # available mana
    best_mana_increase = 0
    for turn in best_turns:
        mana_increase = 0
        for cardIndex in turn.contents:
            card = ret.hand[cardIndex]
            mana_increase += mana.converted(card.manaEachTurn)
        best_mana_increase = max(best_mana_increase, mana_increase)
    best_mana_increase_turns = []
    for turn in best_turns:
        mana_increase = 0
        for cardIndex in turn.contents:
            card = ret.hand[cardIndex]
            mana_increase += mana.converted(card.manaEachTurn)
        if mana_increase == best_mana_increase:
            best_mana_increase_turns.append(turn)
    if KOZILEK_DEBUG:
        print(best_mana_increase_turns)
    # Among tied options, choose at random
    chosen_turn = best_mana_increase_turns[
    r.randint(0, high=len(best_mana_increase_turns))]
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

def _turn_options(hand, mana_count, tested_options, chosen_indices, played_land):
    """ Determines all options for how to play a turn.
        The current hand should be provided in hand as a list of cards.
        The amount of mana available should be provided in mana as an int.
        Whether or not a land has already been played should be provided
        in played_land.
        IntSets are of card indices in hand are used to represent possible
        turns.
        tested_options contains as IntSets any options that are already known
        to be allowed. After calling this method, it will include all possible
        turn options.
        chosen_indices should be an IntSet with any cards required to be played.
    """
    
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
        mana.converted(card.manaCost) <= mana_count and \
        ((not played_land) or not card.land):
            new_chosen_indices = copy.deepcopy(chosen_indices)
            new_chosen_indices.contents.add(i)
            new_mana = mana_count - mana.converted(card.manaCost) + \
            mana.converted(card.manaFirstTurn)
            if not card.pseudoETBT:
                new_mana += mana.converted(card.manaEachTurn)
            _turn_options(hand, new_mana, tested_options,
            new_chosen_indices, played_land or card.land)

def simulation(deck, hand_size = 7, num_turns = 5):
    """ Runs a simulated game using the given deck, hand size (default 7), and
        max number of turns (default 5).
        Returns a list of the game state after each turn.
    """
    
    deck.shuffle()
    state = SimState(deck)
    states = [state]
    for i in range(hand_size):
        state.hand.append(state.deck.draw())
    for i in range(num_turns):
        if DECK_OUT_DEBUG:
            print("turn",i)
        if NUM_ITERATIONS_DEBUG:
            print(i)
        states.append(_play_turn(states[-1]))
    return states