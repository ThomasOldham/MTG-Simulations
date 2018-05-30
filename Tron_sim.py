import numpy as np
from random import shuffle as sh

NON_LAND = 0
MINE = 1
POWER_PLANT = 2
TOWER = 3
SCOURS = 4
SURGICAL = 5

hp = 20
deck = []
hand = []
grave = []
tron = 0

"""
This function initializes the deck with given number of mind, plant, tower,
scours, and surgical
Total card is 38, because we assume we have 2 cards on hand, 1 scour,
and 1 surgical
"""
def init_deck(mine, plant, tower, scours, surgical):
    global deck
    deck = [0] * (40 - (mine + plant + tower + scours + surgical) - 2)
    mine_deck = [MINE] * mine
    plant_deck = [POWER_PLANT] * plant
    tower_deck = [TOWER] * tower
    scours_deck = [SCOURS] * scours
    surgical_deck = [SURGICAL] * surgical
    deck = deck + mine_deck + plant_deck + tower_deck + scours_deck + surgical_deck
    sh(deck)
    

"""
This function initial a hand with 2 cards scours, and surgical
Next, it draws 5 cards from deck.
"""
def init_hand():
    global deck, hand
    hand = [SURGICAL, SCOURS]

    for i in range(5):
        hand.append(deck.pop(0))
    


for i in range(10000):
    init_deck(4,4,4,3,3)        #assume we have a surgical in open hand
    #print(deck)
    #print(len(deck))
    init_hand()
    #print(hand)
    #print(len(hand))
    turn = 1
    while(turn <= 3):
        hand.append(deck.pop(0))
        if SCOURS in hand:
            hand.remove(SCOURS)
            grave.append(SCOURS)
            grave.append(deck.pop(0))
            grave.append(deck.pop(0))    
        if SURGICAL in hand:
            hand.remove(SURGICAL)
            grave.append(SURGICAL)
            if MINE in grave:
                hand.append(MINE)
                grave.remove(MINE)
            elif POWER_PLANT in grave:
                hand.append(POWER_PLANT)
                grave.remove(POWER_PLANT)
            elif TOWER in grave:
                hand.append(TOWER)
                grave.remove(TOWER)
            hp = hp - 2
        turn = turn + 1
            
    #print(deck)
    #print(hand)
    if MINE in hand and TOWER in hand and POWER_PLANT in hand:
        tron = tron + 1
    else:
        print(False)
print (tron)

"""
While loop to draw card until x turns
Cast scours, and surgical
Casting cards include taking card from hand and put into graveyard,
Draw new card, include taking a card from deck, put into hand.
if(hand contains 1,2,3)
    tron
    
Run 10000 times, calculate the percentage success tron

hp that we will be sacrify for this
percentage to get Tron in 10k times

"""