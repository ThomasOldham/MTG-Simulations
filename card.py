import mana as Mana

class Card:
    
    land = None
    manaCost = None
    manaFirstTurn = None
    manaEachTurn = None
    pseudoETBT = None
    damageFirstTurn = None
    damageEachTurn = None
    
    def __init__(self, land=False, manaCost='0', manaFirstTurn='0',
    manaEachTurn='0', pseudoETBT=False, payEachTurn='0', damageFirstTurn=0,
    damageEachTurn=0):
        self.land = land
        self.manaCost = Mana.fromString(manaCost)
        self.manaFirstTurn = Mana.fromString(manaFirstTurn)
        self.manaEachTurn = Mana.fromString(manaEachTurn)
        self.pseudoETBT = pseudoETBT
        self.payEachTurn = Mana.fromString(payEachTurn)
        self.damageFirstTurn = damageFirstTurn
        self.damageEachTurn = damageEachTurn
    
    def __str__(self):
        delim = '\n'
        ret = ''
        if self.land:
            ret = "Land"
        else:
            ret = "Spell"
        ret += delim + "Mana cost " + Mana.toString(self.manaCost)
        ret += delim + "Generates " + Mana.toString(self.manaFirstTurn) + " when cast"
        ret += delim + "Generates " + Mana.toString(self.manaEachTurn) + " each turn"
        if (self.pseudoETBT):
            ret += ", except the turn it is cast"
        ret += delim + "Does " + str(self.damageFirstTurn) + " when cast"
        ret += delim + "Does " + str(self.damageEachTurn) + " each turn"
        if (self.pseudoETBT):
            ret += ", except the turn it is cast"
        ret += delim + "Costs " + Mana.toString(self.payEachTurn) + " each turn"
        return ret