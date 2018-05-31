import numpy as np
from random import shuffle as sh
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

NON_LAND = 0
MINE = 1
POWER_PLANT = 2
TOWER = 3
SCOURS = 4
SURGICAL = 5

my_deck = []
my_hand = []
opp_deck = []

tron_stopped = np.zeros(5)

"""
This function initializes the deck with given number of mine, plant, tower,
scours, and surgical
Total card is 38, because we assume we have 2 cards on hand, 1 scour,
and 1 surgical
"""
def init_deck(mine, plant, tower, scours):
    global my_deck, opp_deck
    
    #my_deck
    my_deck = [0] * (40 - (mine + plant + tower + scours) - 1)
    mine_deck = [MINE] * mine
    plant_deck = [POWER_PLANT] * plant
    tower_deck = [TOWER] * tower
    scours_deck = [SCOURS] * scours
    my_deck = my_deck + mine_deck + plant_deck + tower_deck + scours_deck
    sh(my_deck)
    
    #opp_deck
    opp_deck = [0] * (40 - (mine + plant + tower)) + opp_deck + mine_deck + plant_deck + tower_deck
    sh(opp_deck)
    

"""
This function initial a hand with 2 cards scours, and surgical
Next, it draws 5 cards from deck.
"""
def init_hand(num_scours):
    global my_deck, my_hand
    for i in range(6 - num_scours):
        my_hand.append(my_deck.pop(0))
    temp = ([SCOURS] * num_scours) 
    my_hand = my_hand + temp + [SURGICAL]

"""
Run 1k sims
While loop to draw card until x turns
Cast scours, and surgical
Casting cards include taking card from hand and put into graveyard,
Draw new card, include taking a card from deck, put into hand.
If there is a MINE or POWER_PLANT or TOWER in grave,
we can use SURGICAL. Exile a tron piece and all cards with the same name
from opponent deck and graveyard
Successfully breaking the tron deck.
"""

"""   
0 Scours in hand
"""
    


for i in range(1000):
    init_deck(4,4,4,4)        #assume we have a surgical in open hand
    #print(my_deck)
    #print(len(my_deck))
    #print(opp_deck)
    #print(len(opp_deck))
    init_hand(0)
    #print(my_hand)
    #print(len(my_hand))
    
    grave = []
    turn = 1
    while(turn <= 3):
        my_hand.append(my_deck.pop(0))
        if SCOURS in my_hand:
            my_hand.remove(SCOURS)
            grave.append(opp_deck.pop(0))
            grave.append(opp_deck.pop(0))
            opp_deck.pop(0)
        if MINE in grave or POWER_PLANT in grave or TOWER in grave:
            #my_hand.remove(SURGICAL)
            
            
            tron_stopped[0] = tron_stopped[0] + 1
            break 
            
        turn = turn + 1
        
    #print(deck)
    #print(hand)

"""
1 Scours in hand
"""  
for i in range(1000):
    init_deck(4,4,4,4)        #assume we have a surgical in open hand
    #print(my_deck)
    #print(len(my_deck))
    #print(opp_deck)
    #print(len(opp_deck))
    init_hand(1)
    #print(my_hand)
    #print(len(my_hand))
    
    grave = []
    turn = 1
    while(turn <= 3):
        my_hand.append(my_deck.pop(0))
        if SCOURS in my_hand:
            my_hand.remove(SCOURS)
            grave.append(opp_deck.pop(0))
            grave.append(opp_deck.pop(0))
            opp_deck.pop(0)
        if MINE in grave or POWER_PLANT in grave or TOWER in grave:
            #my_hand.remove(SURGICAL)
            
            
            tron_stopped[1] = tron_stopped[1] + 1
            break 
            
        turn = turn + 1
        
    #print(deck)
    #print(hand)


"""
2 Scours in hand
"""
for i in range(1000):
    init_deck(4,4,4,4)        #assume we have a surgical in open hand
    #print(my_deck)
    #print(len(my_deck))
    #print(opp_deck)
    #print(len(opp_deck))
    init_hand(2)
    #print(my_hand)
    #print(len(my_hand))
    
    grave = []
    turn = 1
    while(turn <= 3):
        my_hand.append(my_deck.pop(0))
        if SCOURS in my_hand:
            my_hand.remove(SCOURS)
            grave.append(opp_deck.pop(0))
            grave.append(opp_deck.pop(0))
            opp_deck.pop(0)
        if MINE in grave or POWER_PLANT in grave or TOWER in grave:
            #my_hand.remove(SURGICAL)
            
            
            
            tron_stopped[2] = tron_stopped[2] + 1
            break
            
        turn = turn + 1
        
    #print(deck)
    #print(hand)


"""
3 scours in hand
"""
for i in range(1000):
    init_deck(4,4,4,4)        #assume we have a surgical in open hand
    #print(my_deck)
    #print(len(my_deck))
    #print(opp_deck)
    #print(len(opp_deck))
    init_hand(3)
    #print(my_hand)
    #print(len(my_hand))
    
    grave = []
    turn = 1
    while(turn <= 3):
        my_hand.append(my_deck.pop(0))
        if SCOURS in my_hand:
            my_hand.remove(SCOURS)
            grave.append(opp_deck.pop(0))
            grave.append(opp_deck.pop(0))
            opp_deck.pop(0)
        if MINE in grave or POWER_PLANT in grave or TOWER in grave:
            #my_hand.remove(SURGICAL)
            
            
            tron_stopped[3] = tron_stopped[3] + 1
            break 
            
        turn = turn + 1
        
    #print(deck)
    #print(hand)


"""
4 scours in hand
"""
for i in range(1000):
    init_deck(4,4,4,4)        #assume we have a surgical in open hand
    #print(my_deck)
    #print(len(my_deck))
    #print(opp_deck)
    #print(len(opp_deck))
    init_hand(4)
    #print(my_hand)
    #print(len(my_hand))
    
    grave = []
    turn = 1
    while(turn <= 3):
        my_hand.append(my_deck.pop(0))
        if SCOURS in my_hand:
            my_hand.remove(SCOURS)
            grave.append(opp_deck.pop(0))
            grave.append(opp_deck.pop(0))
            opp_deck.pop(0)
        if MINE in grave or POWER_PLANT in grave or TOWER in grave:
            #my_hand.remove(SURGICAL)
            
            
            
            tron_stopped[4] = tron_stopped[4] + 1
            break
            
        turn = turn + 1
        
    #print(deck)
    #print(hand)


print (tron_stopped)
x = np.arange(5)
plt.bar(x, tron_stopped)
plt.xticks(x, ('0 Scours', '1 Scours', '2 Scours', '3 Scours', '4 Scours'))
plt.show()
