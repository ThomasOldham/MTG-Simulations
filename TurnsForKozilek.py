""" The contents of this file mostly do not work. """

import ColorlessGoldfish
from card import Card
from deck import Deck
import mana
import warnings
import numpy as N
import numpy.ma as M
import copy

def edhrec_deck():
    """ Constructs a Kozilek Commander deck equal to the average deck on
        EDHRec as of May 27, 2018.
    """
    
    one_mana_land = Card(is_land = True, manaEachTurn = '1')
    two_mana_land = Card(is_land = True, manaEachTurn = '2')
    cards = [
    Card(manaCost = '9'), # Artisan of Kozilek
    Card(manaCost = '7'), # Bane of Bala Ged
    Card(manaCost = '12'), # Blightsteel Colossus
    Card(manaCost = '3', manaEachTurn = '2', pseudoETBT = True), # Burnished Hart, ignoring activation cost
    Card(manaCost = '6', manaEachTurn = '2'), # Conduit of Ruin
    Card(manaCost = '6'), # Duplicant
    Card(manaCost = '9'), # Emrakul, the Promised End, assuming 4 card types in grave
    Card(manaCost = '6'), # Endbringer
    Card(manaCost = '12'), # It That Betrays
    Card(manaCost = '5', manaEachTurn = '5', pseudoETBT = True), # Kozilek's Channeler
    Card(manaCost = '10'), # Kozilek, the Great Distortion
    Card(manaCost = '5'), # Kuldotha Forgemaster
    Card(manaCost = '3', manaEachTurn = '4', pseudoETBT = True), # Metalworker, assuming two artifacts in hand
    Card(manaCost = '6'), # Oblivion Sower
    Card(manaCost = '3', manaEachTurn = '2', pseudoETBT = True), # Palladium Myr
    Card(manaCost = '4', manaEachTurn = '1', pseudoETBT = True), # Solemn Simulacrum
    Card(manaCost = '6'), # Steel Hellkite
    Card(manaCost = '10'), # Ulamog, the Ceaseless Hunger
    Card(manaCost = '11'), # Ulamog, the Infinite Gyte
    Card(manaCost = '9'), # Void Winnower
    Card(manaCost = '7'), # Scour from Existence
    Card(manaCost = '2', manaFirstTurn = '1'), # Warping Wail
    Card(manaCost = '7'), # All is Dust
    Card(manaCost = '3', manaFirstTurn = '3'), # Basalt Monolith
    Card(manaCost = '5', manaEachTurn = '5', pseudoETBT = True), # Blinkmoth Urn, assuming five artifacts
    Card(manaCost = '4', manaEachTurn = '2'), # Clock of Omens, guessing at how much mana it's worth based on experience using it for ramp
    Card(manaCost = '9'), # Darksteel Forge
    Card(manaCost = '2', manaEachTurn = '2'), # Doubling Cube, assuming 8 mana before paying its cost, because that's what's needed to reach Kozilek
    Card(manaCost = '6', manaEachTurn = '3'), # Dreamstone Hedron
    Card(manaCost = '2', manaEachTurn = '1'), # Everflowing Chalice, assuming X=1
    Card(manaCost = '2', manaEachTurn = '1'), # Expediton Map, taking the greater of casting cost and activation cost, and assuming target land generates 2 mana per turn while the player would have otherwise played a 1-mana-per-turn land
    Card(manaCost = '5', manaEachTurn = '3'), # Gilded Lotus
    Card(manaCost = '2', manaFirstTurn = '3'), # Grim Monolith
    Card(manaCost = '4', manaEachTurn = '2'), # Hedron Archive
    Card(manaCost = '2'), # Lightning Greaves
    Card(manaEachTurn = '2'), # Mana Crypt
    Card(manaCost = '1', manaFirstTurn = '3'), # Mana Vault
    Card(manaCost = '2', manaEachTurn = '1'), # Mind Stone
    Card(manaCost = '5'), # Mind's Eye
    Card(manaCost = '3', manaEachTurn = '1'), # Mirage Mirror, assuming it copies a Gilded Lotus or Dreamstone Hedron
    Card(manaEachTurn = '1'), # Mox Opal
    Card(manaEachTurn = '5'), # Paradox Engine
    Card(manaCost = '8'), # Planar Bridge
    Card(manaCost = '3'), # Rings of Brighthearth
    Card(manaCost = '3', manaEachTurn = '2'), # Sculpting Steel, assuming it copies a mid-range mana rock, as a compromise between early-game and mid-to-late-game characteristics
    Card(manaCost = '1'), # Sensei's Divining Top
    Card(manaCost = '4', manaEachTurn = '2'), # Sisay's Ring
    Card(manaCost = '1', manaEachTurn = '2'), # Sol Ring
    Card(manaCost = '7'), # Spine of Ish Sah
    Card(manaCost = '6'), # Staff of Nin
    Card(manaCost = '2'), # Strionic Resonator
    Card(manaCost = '2'), # Swiftfoot Boots
    Card(manaCost = '2', manaEachTurn = '1'), # Thought Vessel
    Card(manaCost = '4', manaEachTurn = '3'), # Thran Dynamo
    Card(manaCost = '2'), # Torpor Orb
    Card(manaCost = '4'), # Trading Post
    Card(manaCost = '4'), # Unwinding Clock
    Card(manaCost = '4', manaEachTurn = '2'), # Ur-Golem's Eye
    Card(manaCost = '1', manaEachTurn = '1'), # Voltaic Key, assuming it untaps a mid-range mana rock, as a compromise between early-game and mid-to-late-game characteristics
    Card(manaCost = '3', manaEachTurn = '2', pseudoETBT = True), # Worn Powerstone
    Card(manaCost = '8'), # Ugin, the Spirit Dragon
    Card (is_land = True, manaEachTurn = '2') # Eye of Ugin, assuming one Eldrazi per turn
    ]
    cards += [two_mana_land] * 2 + [one_mana_land] * 34
    ret = Deck()
    for card in cards:
        ret.add_card(card)
    return ret

def simulation(deck, hand_size = 7, num_turns = 5):
    """ Simulates a game with the given deck and returns all states between turns. """
    return ColorlessGoldfish.simulation(deck, hand_size = hand_size, num_turns = num_turns)

def starting_lands_and_mana_available(deck, hand_size = 7, turns = 5):
    """ Runs a simulation and returns both the number of lands in the starting
        hand and the amount of mana available after the final turn.
    """
    
    states = simulation(deck, hand_size = hand_size, num_turns = turns)
    lands = 0
    for card in states[0].hand:
        if card.is_land:
            lands += 1
    mana_count = 0
    for card in states[-1].board:
        mana_count += mana.converted(card.manaEachTurn)
    return lands, mana

def mana_by_hand(deck, num_simulations_per_hand_size = 1000, \
max_hand_size = 7, num_turns = 5):
    """ Runs many simulations of each possible hand size <= the
        provided max, and organizes the mana available after the final turn
        in a numpy array by hand size in the first index and number of lands
        in the second index, with the final index of the second index holding
        the average value across all land counts, as required for
        MulliganVisual.
    """
    
    counts = N.zeros((max_hand_size + 1, max_hand_size + 2))
    sums = N.zeros((max_hand_size + 1, max_hand_size + 2))
    for hand_size in range(max_hand_size + 1):
        for iteration in range(num_simulations_per_hand_size):
            lands, mana = starting_lands_and_mana_available(copy.deepcopy(deck), \
            hand_size = hand_size, turns = num_turns)
            counts[hand_size, lands] += 1
            counts[hand_size, -1] += 1
            sums[hand_size, lands] += mana
            sums[hand_size, -1] += mana
    
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