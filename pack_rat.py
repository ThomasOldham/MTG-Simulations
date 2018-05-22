# Owen Turtenwald Pack Rat Retrospective
# Simulates the case of PT2015 limited deck played by O. Turtenwald
# Determines the ideal mulligan limit with a changeable variable
# representing the number of times to mull. The question is if there 
# is any benefit to ceasing mulligans before going down to 2 cards in the 
# opening hand in order to increase the chances of drawing the Pack Rat by 
# the 5th turn (relevant for casting and activation cost). Runs a set of 
# 10,000 sims for each limit and assumes the play (no draw for 1st turn)
#==============================================================================
# Owen's deck consisted of 1 Pack Rat and 39 swamps.
# Pack Rat - 1B, */*
# Pack Rat's power and toughness are each equal to the number of Rats you
# control.
# 2B, Discard a card: Create a token that's a copy of Pack Rat
#------------------------------------------------------------------------------
import numpy as np
import numpy.random as r
import matplotlib.pyplot as plt

SWAMP = 0
PACK_RAT = 1
MULL_LIMIT = 7
NUM_SIMS = 10000
VERBOSE = False

#Init deck
deck = np.zeros(40)
#Add 1 Pack Rat
deck[9] = PACK_RAT

def sim_game(deck,SIM_MULL_LIM,MPL,OPL,DPL):
    """Simulates a game using the specified deck
    Returns 1 if a Pack Rat was found by turn 5,
    returns 0 otherwise"""
    if VERBOSE:
        print('New Hand')
    #shuffle and draw 7
    r.shuffle(deck)
    hand = deck[:7]
    if hand.sum() == PACK_RAT:
        if VERBOSE:
            print("Pack Rat in opener!")
        OPL[SIM_MULL_LIM] += 1
        return PACK_RAT
    #Mulligan logic, looking for Pack Rat
    for i in range(SIM_MULL_LIM,0,-1):
        if hand.sum() == PACK_RAT:
            if VERBOSE:
                print("Pack Rat in opener!")
            OPL[SIM_MULL_LIM] += 1
            return PACK_RAT
        else:
            MPL[SIM_MULL_LIM] += 1
            r.shuffle(deck)
            hand = deck[:i]
    #Check for Pack Rat after final mulligan
    if hand.sum() == PACK_RAT:
        if VERBOSE:
            print("Pack Rat in opener!")
        OPL[SIM_MULL_LIM] += 1
        return PACK_RAT
    #Pack Rat not found in opener, determine if it is in top 5 of the library
    if VERBOSE:
        print("Drawing to Pack Rat...")
    library = deck[len(hand)+1:len(hand)+6]
    if library.sum() == PACK_RAT:
        if VERBOSE:
            print('Pack Rat Drawn!')
        DPL[SIM_MULL_LIM] += 1
        return PACK_RAT
    else:
        if VERBOSE:
            print('Swamps only....')
        return 0
        
#List of return values from simulations
rat_found = np.zeros(MULL_LIMIT)
avg_mulls = np.zeros(MULL_LIMIT)
avg_rat_on_open = np.zeros(MULL_LIMIT)
avg_draws = np.zeros(MULL_LIMIT)
x_axis = range(7)

#Run simulations
for r_i in range(len(rat_found)):
    for s in range(NUM_SIMS):                
        rat_found[r_i] += sim_game(deck,r_i,avg_mulls,avg_rat_on_open,avg_draws)
        
print('Number of games with Pack Rat in opener + top 5')
print(rat_found)
print('Number of mulligans executed per limit')
print(avg_mulls)
print('Number of openers with Pack Rat per limit')
print(avg_rat_on_open)
print('Number of draws into Pack Rat per limit')
print(avg_draws)

plt.figure("Figure 1")
ax = plt.gca()
plt.title("Pack Rat Sim Averages for " + str(NUM_SIMS) + " Sims")
plt.plot(x_axis,rat_found,'y*--')
plt.plot(x_axis,avg_rat_on_open,'r+--')
plt.plot(x_axis,avg_draws,'kv--')
plt.ylabel("Average Count")
plt.xlabel("Mulligan Limits")
plt.legend(["Rat found by turn <5","Rat found on opener","Draws till rat found"], loc = 'upper center')

plt.figure("Figure 2")
plt.title("Average Mulls per Mull limit for " + str(NUM_SIMS) + " Sims")
plt.plot(x_axis,avg_mulls, 'bo--')
plt.ylabel("Average Count")
plt.xlabel("Mulligan Limits")

plt.show()