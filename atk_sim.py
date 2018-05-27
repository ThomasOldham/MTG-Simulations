# Average Turn Kill Simulator - Muck Rats
# Deck is 15 swamps and 45 Muck Rats. Performs no mulligan actions and assumes 
# the play (no card drawn on first turn). Incorporates psuedo and quasi goldfish 
# behavior. Psuedo-goldfish interacts based on conditional criteria and 
# interaction counts. Quasi-goldfish interacts based on stochastic outcome. 
#
# Muck Rats 
#   cost - 1 Black Mana
#   creature - Rat
#   damage - 1
#   defense - 1
#==============================================================================
# Muck Rat - B, 1/1
# Vanilla creature (no abilities)
#------------------------------------------------------------------------------
import numpy as np
import numpy.random as r
import deck as Dk
import card as Cd
import mana as Mana
import mull_sim as Mull
import copy

p_goldfish = False        #Set to true to enable psuedo-goldfish behavior
q_goldfish = False        #Set to true to enable quais-goldfish behavior
q_goldfish_prob = .05     #Chance quasi-goldfish has to interact 
deck_size = 60
land_count = 15
goldfish_interactions = 0 #Number of interactions goldfish has access to
VERBOSE = False            #Set to true to enable verbose messaging
NUM_SIMS = 100            #Number of goldfish simulations to run

def cal_kill_turn(deck):  
    """ Calculates the kill turn for a deck
    
    Assumes all creatures in deck require only one mana type. Assumes only 
    creatures and land in deck.
    """ 
    #Init board/game state
    goldfish_life = 20
    turn = 0        
    
    #lands in hand
    lands_in_hand = []
    #spell count in hand
    spells_in_hand = []
    #lands in play
    lands_in_play = []
    #creatures in play
    spells_in_play = []
    #creatures' in play power
    #creature_pwr = 1
    
    #shuffle and draw 7 cards, mulls if hand bad
    hand = None
    keep_hand = False
    hand_count = 8
    while keep_hand == False:
        hand_count = hand_count - 1
        deck.shuffle()
        hand = deck.peep(hand_count)
        keep_hand = Mull.keep_or_mull(hand)
    hand = deck.draw_hand(num = hand_count)        
        
    #Init Hand state
    for card in hand:
        if card.is_land == True:
            lands_in_hand.append(card)
        else:
            spells_in_hand.append(card)   
        
    #SIMULATE GOLDFISH KILL
    while(goldfish_life >= 0 and deck.size() > 0):            
        if VERBOSE:
            print("+++++++++++++ Turn " + str(turn) + "++++++++++++++")           
            print("    Goldfish life = " + str(goldfish_life))
            
            print("    Lands in play")
            for card in lands_in_play:
                print(card)
            print("    Spells in play")
            for card in spells_in_play:
                print(card)
            print("    Lands in hand")
            for card in lands_in_hand:
                print(card)
            print("    Creatures in hand")
            for card in spells_in_hand:
                print(card)            
            
        # Draw a card if not first turn
        if turn > 0:
            card_to_draw = deck.draw()           
            if card_to_draw.is_land == True:                
                lands_in_hand.append(copy.deepcopy(card_to_draw))
            else:                
                spells_in_hand.append(copy.deepcopy(card_to_draw))                

        #MAIN PHASE 1 play land card if we have any
        if len(lands_in_hand) > 0:            
            lowest_cost = None
            land_to_play = None
            #Play the land card that has the lowest cost creature in hand
            for land in lands_in_hand[:]:
                for creature in spells_in_hand[:]:
                    if land.manaEachTurn == creature.manaCost:
                        # this land card has a playable creature
                        if land_to_play != None:
                            temp_cost = creature.manaCost
                            if temp_cost < lowest_cost:
                                if len(np.where(temp_cost > 0)[0]) <= \
                                    len(np.where(lowest_cost > 0)[0]): 
                                        # play the land that corresponds to
                                        # the creatures that require the 
                                        # least different types
                                    land_to_play = land
                                    lowest_cost = temp_cost
                        else:
                            #first land card, we store it to play
                            land_to_play = land
                            lowest_cost = creature.manaCost
            if land_to_play == None: #No spell cards in hand
                land_to_play = lands_in_hand[0] #play first land card
                           
            lands_in_play.append(copy.deepcopy(land_to_play))            
            lands_in_hand.pop(lands_in_hand.index(land_to_play))           
            
        #ATTACK GOLDFISH 
        for creature in spells_in_play:
            goldfish_life = goldfish_life - creature.damageEachTurn
        if goldfish_life <= 0:
            if VERBOSE:
                print('Goldfish killed on turn ' + str(turn))
            return turn
            
        #MAIN PHASE 2 play spells
        if len(spells_in_hand) > 0 and len(lands_in_play) > 0:            
            #Spells in hand and mana available --> play a creature
            #GOLDFISH LOGIC
            if p_goldfish:
                if goldfish_interactions > 0:
                    pass
            if q_goldfish:
                if r.random(1) < q_goldfish_prob:
                    if goldfish_interactions > 0:
                        pass
            #Check mana pool
            mana_pool = np.array([0] * Mana.MANA_TYPES)
            for card in lands_in_play:
                mana_pool += card.manaEachTurn
                
            for creature in spells_in_hand:
                temp_pool = np.array(mana_pool - \
                    np.array(creature.manaCost))
                if len(np.where(temp_pool < 0)[0]) == 0: 
                    #can afford to play card
                    mana_pool = temp_pool[:]
                    spells_in_play.append(copy.deepcopy(creature))
                    spells_in_hand.remove(creature)
        if VERBOSE:
            print("++++++++++++ End Turn " + str(turn) + "++++++++++")   
        turn += 1 
    #End Gold Fish kill    
    
    if VERBOSE:
        print('Goldfish killed on turn ' + str(turn))
    return turn

def cal_average_kill_turns(deck):
    """ Calculates and returns the average kill turn, lowest kill turn, and
     highest kill turn. Works for decks with one or more land types and 
     creatures that use only one land type each. Creatures may not all use
     the same land type
    """
    #Results array
    turn_results = np.zeros(NUM_SIMS)
    
    #Simulation loop
    for i in range(NUM_SIMS):   
        if VERBOSE:
            print('Running simulation ' + str(i + 1))     
        turn_results[i] = cal_kill_turn(copy.deepcopy(deck))
    #End of Simulations
    
    #DETERMINE ATK
    average_kill_turn = np.average(turn_results)
    min_kill_turn = np.min(turn_results)
    max_kill_turn = np.max(turn_results)
        
    return average_kill_turn, min_kill_turn, max_kill_turn

#Init deck
deck = Dk.Deck()

#Add black land cards
for i in range(land_count):
    deck.add_card(Cd.Card(is_land=True, manaEachTurn = 'B'))

for i in range(deck_size - land_count):
    #fill deck with Much Rats
    deck.add_card(Cd.Card(is_land=False, manaCost = 'B', damageEachTurn = 1))

#UNCOMMENT FOR NEXT CARD TYPE
#Add 2 drops
#for i in range(deck_size - land_count):
#    deck.add_card(Cd.Card(land=False, ManaCost = 'B', damageEachTurn = 2))
    
# Determine kill turns
ATK, min_ATK, max_ATK = cal_average_kill_turns(deck)

#output
print('Average Turn Kill')
print(ATK)
print('Lowest Turn Kill')
print(min_ATK)
print('Highest Turn Kill')
print(max_ATK)
