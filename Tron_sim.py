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
This function initializes the deck with given number of mine, plant, tower, scours
Total card is 39, because we assume we have 1 surgical card on hand 
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
This function initial a hand with surely a Surgical card
Then it draws a number of card equal to 6 - num_scours
Parameter:
    num_scours - number of Thought Scours to initialize
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
Casting cards include taking card from hand and exile it
Draw new card, include taking a card from deck, put into hand.
If there is a MINE or POWER_PLANT or TOWER in grave,
we can use SURGICAL. Exile a tron piece and all cards with the same name
from opponent deck and graveyard
Successfully breaking the tron deck.
"""

"""   
This function run the similation 1000 times
A while loop to simulate the first 3 turn of the game

The goal here is to see how effective Thought Scours can be against Tron deck
The opponent's deck have tron pieces, which we will try to destroy.
Our deck contain non_land and Thought Scours

For every turn, we draw 1 card from our deck. For every Thought Scours played, 
opponent puts 2 cards in graveyard, and draw a card from its deck.

The second if statement check whether we should use Surgical. Only use Surgical
when there is any Tron piece in the graveyard.

A Tron piece in the graveyard means the Tron deck is broken.

Parameter:
    scours - the initial number of scours in hand.
"""
    
def thought_scours(scours):
    for i in range(1000):
        #Initialize hands & decks & and grave yard
        init_deck(4,4,4,4)        
        #print(my_deck)
        #print(len(my_deck))
        #print(opp_deck)
        #print(len(opp_deck))
        init_hand(scours)
        #print(my_hand)
        #print(len(my_hand)
        grave = []
        
        #Simulation
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
                
                
                tron_stopped[scours] = tron_stopped[scours] + 1
                break 
                
            turn = turn + 1
            
        #print(deck)
        #print(hand)



thought_scours(0)
thought_scours(1)
thought_scours(2)
thought_scours(3)
thought_scours(4)

"""
Total Runtime: 5 minutes
This bar graph displays the percentage of succeed in breaking the Tron deck.
From the graph, there is a huge different between having the Thought Scours in
opener and without one.
"""
print (tron_stopped)
x = np.arange(5)
plt.bar(x, tron_stopped)
plt.xticks(x, ('0 Scours', '1 Scours', '2 Scours', '3 Scours', '4 Scours'))
plt.show()
