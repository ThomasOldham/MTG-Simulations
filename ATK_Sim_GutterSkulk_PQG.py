# Average Turn Kill Simulator - Gutter Skulk
# Alters Land and Gutter Skulk counts. Performs no mulligan actions and assumes 
# the play (no card drawn on first turn). Incorporates psuedo and quasi goldfish 
# behavior. Psuedo-goldfish interacts based on conditional criteria and 
# interaction counts. Quasi-goldfish interacts based on stochastic outcome. 
#==============================================================================
# Gutter Skulk - 1B, 2/2
# Vanilla creature (no abilities)
#------------------------------------------------------------------------------
import numpy as np
import numpy.random as r
import matplotlib.pyplot as plt

p_goldfish = False        #Set to true to enable psuedo-goldfish behavior
q_goldfish = False        #Set to true to enable quais-goldfish behavior
q_goldfish_prob = .50     #Chance quasi-goldfish has to interact 
GF_CNT = 3                #Number of interactions goldfish has access to
VERBOSE = False           #Set to true to enable verbose messaging
NUM_SIMS = 10000            #Number of goldfish simulations to run

#DO NOT ALTER LAND/SPELL VALS!
LAND = 1
SPELL = 0

def sim_goldfish(deck):
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
        #spell mana cost
        spells_cost = 2
        #creatures' in play power
        creature_pwr = 2
        #number of counters/removal goldfish has access to
        goldfish_interactions = GF_CNT
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
        while(goldfish_life >= 0 and turn < 20):
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
            while spells_hand > 0 and mana_available > 1:
                #spells in hand, mana available --> play a creature
                #GOLDFISH LOGIC GOES HERE!
                if p_goldfish:
                    if goldfish_interactions > 0:
                        #Effectively instant speed discard and mana denial
                        #Simulates spell countering
                        spells_hand -= 1
                        mana_available -= spells_cost
                        goldfish_interactions -= 1
                if q_goldfish:
                    if r.random(1) < q_goldfish_prob:
                        if goldfish_interactions > 0:
                            #Effectively instant speed discard and mana denial
                            #Simulates spell countering
                            spells_hand -= 1
                            mana_available -= spells_cost
                            goldfish_interactions -= 1
                #Play a creature in Main Phase 2
                if spells_hand > 0:
                    if mana_available >= spells_cost:
                        spells_hand -= 1
                        spells_play += 1
                        mana_available -= spells_cost  
            #EOL
        #Goldfish died on turn, record result in array
        if VERBOSE:
            print('Goldfish killed on turn ' + str(turn))
        turn_results[i] = turn
    #DETERMINE ATK
    ATK = np.average(turn_results)
    #min_ATK = np.min(turn_results)
    #max_ATK = np.max(turn_results)
    return ATK#,min_ATK,max_ATK

#Init deck
deck = np.zeros(60)
atk_results = np.zeros(50)
#Add lands
for i in range(5,55):
    deck = np.zeros(60)
    for j in range(i):
        #fill deck with lands
        deck[j] = 1
    atk_results[i-5] = sim_goldfish(deck)  
    
#output
print(atk_results)
#print('Average Turn Kill')
#print(ATK)
#print('Lowest Turn Kill')
#print(min_ATK)
#print('Highest Turn Kill')
#print(max_ATK)
x_axis = np.arange(5,55)-5
# -----------------Output and Plotting -----------------------------------------
ax = plt.gca()
ax.plot(x_axis, atk_results,color='red')
plt.title("Average Turn Kill for Gutter Skulk VS Land Count (10K)")
plt.ylabel('Average Turn Kill vs Goldfish')
plt.xlabel('Land Count')
plt.show()
