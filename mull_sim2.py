#==============================================================================
# Mulligan Simulator
# Simulates drawing opening hands and makes aggressive mulligan decisions
# based on land counts in opening hands.
#==============================================================================
import numpy as np
import matplotlib.pyplot as plt
import deck as Dk
import card as Cd

VERBOSE = False
V_VERBOSE = False

limited = True
num_sims = 10000
total_kept =[]
total_mulled = []
deck_length = 0

#Set deck size based on format
if limited:
    deck_length = 40
else:
    deck_length = 60
    
def keep_or_mull(hand):
    """ Keepable hand is defined as having land count between 2 and 4 cards. 
    Hands are not mulled to less than 5 
    Returns bool representing mulligan decision:
        True: hand satisfiess criteria
        False: hand fails criteria
    """
    land_count = 0
    
    #count land cards
    for i in range(len(hand)):
        if hand[i].is_land == True:
            land_count += 1
            
    if (land_count >= 2 and land_count <= 3) or len(hand) <= 4:
        if V_VERBOSE:
            print('Hand Kept')
        return True
    else:
        if V_VERBOSE:
            print('Hand Mulled')
        return False
    
def mull_sim_single(deck):
    """Shuffles the deck order and draws an opening 7 cards.
    Keepable hand is defined as having land count between 2 and 4 cards.
    
    Returns bool representing mulligan decision:
        True: hand satisfiess criteria
        False: hand fails criteria"""
    
    deck.shuffle()
    hand = deck.peep(8)    
    
    return keep_or_mull(hand)
        
#Set number of lands for simulation
for land_count in range(deck_length):
    deck = Dk.Deck()
    hands_kept = 0
    hands_mulled = 0
    
    for i in range(land_count):
        #fill deck with white land cards
        deck.add_card(Cd.Card(is_land=True, manaEachTurn = 'W'))
        
    for i in range(deck_length - land_count):
        #fill deck with generic non-land cards
        deck.add_card(Cd.Card(is_land=False))
        
    if VERBOSE:
        print('For Land Count ' + land_count + ':')
        
    for i in range(num_sims):
        if(mull_sim_single(deck)):
            hands_kept += 1
        else:
            hands_mulled += 1
            
    total_kept.append(hands_kept)
    total_mulled.append(hands_mulled)
    
    if VERBOSE:
        print('Hands Kept: ' + str(hands_kept))
        print('Hands Mulled: ' + str(hands_mulled))
        
    deck.clear()
    
#Plot of number of lands in deck (x) versus hands kept versus mulled (y)
if VERBOSE:
    print(total_kept)
    print(total_mulled)
x_axis = np.arange(deck_length)

ax = plt.gca()
ax.bar(x_axis, total_mulled,width=0.4,color='g',align='edge')
ax.bar(x_axis+0.4, total_kept,width=0.4,color='b',align='edge')
ax.legend(["Mulled","Kept"])
plt.title("Aggressive Limited Land Count VS Hands Kept or Mulled (2-3 Lands)")
plt.ylabel('Mulligans/Keeps')
plt.xlabel('Land Count')
plt.show()