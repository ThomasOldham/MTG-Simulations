#Average Turn Kill Simulator
#Assumes all spells are 1/1 for 1 mana (1 drops)

import numpy as np
import numpy.random as r
import matplotlib.pyplot as plt

p_goldfish = False
q_goldfish = False
q_goldfish_prob = .05 #Chance quasi-goldfish has to interact
goldfish_interactions = 0 #Number of interactions goldfish has access to

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
    
print(deck)


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

#Simulate goldfish kill
while(goldfish_life >= 0):
    turn += 1
    #Draw card if not turn 1#########################
    #CARD DRAW LOGIC GOES HERE!!!!!!!!!!!!!!!!!!!!!!!
    #################################################
    #MAIN PHASE 1
    if lands_hand > 0:
        #play a land
        lands_hand -= 1
        lands_play += 1
        #remove land from hand#######################
        
    #ATTACK GOLDFISH 
    goldfish_life -= spells_play*creature_pwr
        
    #MAIN PHASE 2
    mana_available = lands_play
    while spells_hand > 0 and mana_available > 0:
        #play a creature
        if p_goldfish:
            if goldfish_interactions > 0:
                pass
        if q_goldfish:
            if r.random(1) < q_goldfish_prob:
                if goldfish_interactions > 0:
                    pass
        #GOLDFISH LOGIC GOES HERE!!!!!!!!!!!!!!!!!!!!
        #############################################
        spells_hand -= 1
        spells_play += 1
        #remove creature from hand###################
        #REPEAT PROCESS until all spells that can be played, are played!    

#DETERMINE ATK
