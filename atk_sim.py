#Average Turn Kill Simulator
#Assumes all spells are 1/1 for 1 mana (1 drops)

import numpy as np
import numpy.random as r
import matplotlib.pyplot as plt

p_goldfish = False
q_goldfish = False

LAND = 1
SPELL = 0

#Init deck
deck = np.zeros(60)
deck = deck.tolist()

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
#creatures in play's power
creature_pwr = 1
#current card position to draw from deck, to be reset to 7 if deck shuffle
current_draw = 7

#shuffle and draw 7
r.shuffle(deck)
hand = deck[:7]
print(deck)
deck = np.delete(deck, [0,1,2,3,4,5,6])

#Init Hand state
for card in range(len(hand)):
    if hand[card] == 1:
        lands_hand += 1
    if hand[card] == 0:
        spells_hand += 1

#Simulate goldfish kill
while(goldfish_life >= 0):
    print('Before play a card' + str(hand))
    turn += 1
    #take first card out to play
    current_card_play = hand[0]
    hand = np.delete(hand, 0)
    #Draw card if not turn 1#########################
    #CARD DRAW LOGIC GOES HERE!!!!!!!!!!!!!!!!!!!!!!!
    if turn != 1:
        hand = np.append(hand, deck[0])
        deck = np.delete(deck, 0)
        current_draw += 1
        print('After' + str(hand))
    #################################################
    if LAND in hand:
        #print('Land')
        #play a land
        lands_hand -= 1
        lands_play += 1
        #remove land from hand#######################
        
    #ATTACK GOLDFISH 
    for i in range(spells_play):
        goldfish_life -= creature_pwr
        
    #MAIN PHASE 2
    if SPELL in hand:
        #print('Spell')
        #play a creature
        if p_goldfish:
            pass
        if q_goldfish:
            pass
        #GOLDFISH LOGIC GOES HERE!!!!!!!!!!!!!!!!!!!!
        #############################################
        spells_hand -= 1
        spells_play += 1
        #remove creature from hand###################
        #REPEAT PROCESS until all spells that can be played, are played!    

#DETERMINE ATK
