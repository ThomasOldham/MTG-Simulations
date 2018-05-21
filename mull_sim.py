#Mulligan Simulator
#Simulates drawing opening hands and makes a mulligan decision based on 
#land counts in opening hands
#Uses binary arrays to represent lands as 1, spells as 0

import numpy as np
import numpy.random as r
import matplotlib.pyplot as plt

VERBOSE = False
V_VERBOSE = False

limited = False
num_sims = 10000
total_kept =[]
total_mulled = []
deck_length = 0

#Set deck size based on format
if limited:
    deck_length = 40
else:
    deck_length = 60
    
def keep_or_mull(deck):
    """Shuffles the deck order and draws an opening 7 cards.
    Keepable hand is defined as having land count between 2 and 4 cards.
    
    Returns bool representing mulligan decision:
        True: hand satisfiess criteria
        False: hand fails criteria"""
    
    r.shuffle(deck)
    hand = deck[:8]
    land_count = hand.sum()
    if land_count >= 2 and land_count <= 4:
        if V_VERBOSE:
            print('Hand Kept')
        return True
    else:
        if V_VERBOSE:
            print('Hand Mulled')
        return False
        
#Set number of lands for simulation
#propose changing var names i,j to d_size, lands respectively
for land_count in range(deck_length):
    deck = np.zeros(deck_length)
    hands_kept = 0
    hands_mulled = 0
    
    for i in range(land_count):
        #fill deck with lands
        deck[i] = 1
        
    if VERBOSE:
        print('For Land Count ' + land_count + ':')
        
    for i in range(num_sims):
        if(keep_or_mull(deck)):
            hands_kept += 1
        else:
            hands_mulled += 1
            
    total_kept.append(hands_kept)
    total_mulled.append(hands_mulled)
    
    if VERBOSE:
        print('Hands Kept: ' + str(hands_kept))
        print('Hands Mulled: ' + str(hands_mulled))
    
#Plot of number of lands in deck (x) versus hands kept versus mulled (y)
if VERBOSE:
    print(total_kept)
    print(total_mulled)
x_axis = np.arange(deck_length)

ax = plt.gca()
ax.bar(x_axis, total_mulled,width=0.4,color='g',align='edge')
ax.bar(x_axis+0.4, total_kept,width=0.4,color='b',align='edge')
ax.legend(["Mulled","Kept"])
plt.title("Number of Lands in Deck VS Hands Kept or Mulled")
plt.ylabel('Card count')
plt.xlabel('Land count')
plt.show()
