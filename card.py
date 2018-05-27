import mana as Mana

class Card:
    
    is_land = None
    manaCost = None
    manaFirstTurn = None
    manaEachTurn = None
    is_pseudoETBT = None
    damageFirstTurn = None
    damageEachTurn = None
    
    def __init__(self, is_land=False, manaCost='0', manaFirstTurn='0',
    manaEachTurn='0', is_pseudoETBT=False, payEachTurn='0', damageFirstTurn=0,
    damageEachTurn=0):
        self.is_land = is_land
        self.manaCost = Mana.fromString(manaCost)
        self.manaFirstTurn = Mana.fromString(manaFirstTurn)
        self.manaEachTurn = Mana.fromString(manaEachTurn)
        self.is_pseudoETBT = is_pseudoETBT
        self.payEachTurn = Mana.fromString(payEachTurn)
        self.damageFirstTurn = damageFirstTurn
        self.damageEachTurn = damageEachTurn
    
    def __str__(self):
        delim = '\n'
        ret = ''
        if self.is_land:
            ret = "Land"
        else:
            ret = "Spell"
        ret += delim + "Mana cost " + Mana.toString(self.manaCost)
        ret += delim + "Generates " + Mana.toString(self.manaFirstTurn) + " when cast"
        ret += delim + "Generates " + Mana.toString(self.manaEachTurn) + " each turn"
        if (self.is_pseudoETBT):
            ret += ", except the turn it is cast"
        ret += delim + "Does " + str(self.damageFirstTurn) + " when cast"
        ret += delim + "Does " + str(self.damageEachTurn) + " each turn"
        if (self.is_pseudoETBT):
            ret += ", except the turn it is cast"
        ret += delim + "Costs " + Mana.toString(self.payEachTurn) + " each turn"
        return ret