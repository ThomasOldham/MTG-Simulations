import mana

class Card:
    """ Represents a Magic the Gathering card. Can be a land or not a land,
        has a manaCost to play it, provides manaFirstTurn mana the turn it is
        played, and does damageFirstTurn damage the turn it is played.
        Generates manaEachTurn mana and does damageEachTurn damage each turn,
        except for the turn it is played if the pseudoETBT flag is set.
    """
    
    land = None
    manaCost = None
    manaFirstTurn = None
    manaEachTurn = None
    pseudoETBT = None
    damageFirstTurn = None
    damageEachTurn = None
    
    def __init__(self, is_land=False, manaCost='0', manaFirstTurn='0',
    manaEachTurn='0', pseudoETBT=False, payEachTurn='0', damageFirstTurn=0,
    damageEachTurn=0):
        self.is_land = is_land
        self.manaCost = mana.fromString(manaCost)
        self.manaFirstTurn = mana.fromString(manaFirstTurn)
        self.manaEachTurn = mana.fromString(manaEachTurn)
        self.pseudoETBT = pseudoETBT
        self.payEachTurn = mana.fromString(payEachTurn)
        self.damageFirstTurn = damageFirstTurn
        self.damageEachTurn = damageEachTurn
    
    def __str__(self):
        delim = '\n'
        ret = ''
        if self.is_land:
            ret = "Land"
        else:
            ret = "Spell"
        ret += delim + "Mana cost " + mana.toString(self.manaCost)
        ret += delim + "Generates " + mana.toString(self.manaFirstTurn) + " when cast"
        ret += delim + "Generates " + mana.toString(self.manaEachTurn) + " each turn"
        if (self.pseudoETBT):
            ret += ", except the turn it is cast"
        ret += delim + "Does " + str(self.damageFirstTurn) + " when cast"
        ret += delim + "Does " + str(self.damageEachTurn) + " each turn"
        if (self.pseudoETBT):
            ret += ", except the turn it is cast"
        ret += delim + "Costs " + mana.toString(self.payEachTurn) + " each turn"
        return ret