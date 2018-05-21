# Average Turn Kill Simulator - Muck Rats
# Deck is 15 swamps and 45 Muck Rats. Performs no mulligan actions and assumes 
# the play (no card drawn on first turn). Incorporates psuedo and quasi goldfish 
# behavior. Psuedo-goldfish interacts based on conditional criteria and 
# interaction counts. Quasi-goldfish interacts based on stochastic outcome. 
#==============================================================================
# Muck Rat - B, 1/1
# Vanilla creature (no abilities)
#------------------------------------------------------------------------------
import numpy as np
import numpy.random as r
import matplotlib.pyplot as plt

p_goldfish = False        #Set to true to enable psuedo-goldfish behavior
q_goldfish = False        #Set to true to enable quais-goldfish behavior
q_goldfish_prob = .05     #Chance quasi-goldfish has to interact 
goldfish_interactions = 0 #Number of interactions goldfish has access to
VERBOSE = False           #Set to true to enable verbose messaging
NUM_SIMS = 100            #Number of goldfish simulations to run

#DO NOT ALTER LAND/SPELL VALS!
LAND = 1
SPELL = 0

#Init deck
deck = np.zeros(60)

#Add 15 lands
for i in range(15):
    deck[i] = 1

#UNCOMMENT FOR NEXT CARD TYPE
#Add 2 drops
#for i in range(45, 60):
#    deck[i] = 2

if VERBOSE:
    print('Using Deck: ')
    print(deck)

#Results array
turn_results = np.zeros(NUM_SIMS)

#Simulation loop
for i in range(NUM_SIMS):
    if VERBOSE:
        print('Running simulation ' + str(i + 1))
    #Init board/game state
    goldfish_life = 20
    turn = 0
    
    #lands in play
    lands_play = 0
    #lands in hand
    lands_hand = 0
    #spell count in hand
    spells_hand = 0
    #creatures in play
    spells_play = 0
    #creatures' in play power
    creature_pwr = 1
    
    #shuffle and draw 7
    r.shuffle(deck)
    hand = deck[:7]
    
    #Init Hand state
    for card in range(len(hand)):
        if hand[card] == 1:
            lands_hand += 1
        if hand[card] == 0:
            spells_hand += 1

    #Draw cursor to index what card will be drawn next
    draw_cur = 7
    #SIMULATE GOLDFISH KILL
    while(goldfish_life >= 0):
        turn += 1
        #CARD DRAW LOGIC GOES HERE!
        if turn > 1:
            card_to_draw = deck[draw_cur]
            if card_to_draw == LAND:
                lands_hand += 1
            if card_to_draw == SPELL:
                spells_hand += 1
            draw_cur += 1

        #MAIN PHASE 1
        if lands_hand > 0:
            #play a land
            lands_hand -= 1
            lands_play += 1
            
        #ATTACK GOLDFISH 
        goldfish_life -= spells_play*creature_pwr
            
        #MAIN PHASE 2
        mana_available = lands_play
        while spells_hand > 0 and mana_available > 0:
            #spells in hand, mana available --> play a creature
            #GOLDFISH LOGIC GOES HERE!
            if p_goldfish:
                if goldfish_interactions > 0:
                    pass
            if q_goldfish:
                if r.random(1) < q_goldfish_prob:
                    if goldfish_interactions > 0:
                        pass
            #Play a creature in Main Phase 2
            spells_hand -= 1
            spells_play += 1
            mana_available -= 1   
        #EOL
    #Goldfish died on turn, record result in array
    if VERBOSE:
        print('Goldfish killed on turn ' + str(turn))
    turn_results[i] = turn
    
#DETERMINE ATK
ATK = np.average(turn_results)
min_ATK = np.min(turn_results)
max_ATK = np.max(turn_results)

#output
print('Average Turn Kill')
print(ATK)
print('Lowest Turn Kill')
print(min_ATK)
print('Highest Turn Kill')
print(max_ATK)
