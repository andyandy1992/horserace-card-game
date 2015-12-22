#!/usr/bin/python

#LIBRARIES:
# Standard library
import math
from decimal import *
#Local application (see https://github.com/andyandy1992/Vose-Alias-Method)
from vose_sampler import VoseAlias as VA

oH = 0 # number of H observed at start (i.e. in the racetrack)
oC = 2
oD = 2
oS = 2

wins = {}
wins["H"]=0
wins["C"]=0
wins["D"]=0
wins["S"]=0

for i in range(1000):
    
    r = {}
    r["H"] = 13-oH-1 # remaining number of H (-1 for the "Ace of Hearts"    horse)
    r["C"] = 13-oC-1
    r["D"] = 13-oD-1
    r["S"] = 13-oS-1

    N = r["H"]+r["C"]+r["D"]+r["S"] # number of remaining cards

    n = {}
    n["H"]=0
    n["C"]=0
    n["D"]=0
    n["S"]=0

#    print "\n NEW:"

    while n["H"]<6 and n["C"]<6 and n["D"]<6 and n["S"]<6:

        pH = Decimal(r["H"])/Decimal(N)
        pC = Decimal(r["C"])/Decimal(N)
        pD = Decimal(r["D"])/Decimal(N)
        pS = Decimal(r["S"])/Decimal(N)

#        print "pH="+str(pH)+",pC="+str(pC)+",pD="+str(pD)+",pS="+str(pS)

        cards_dist = {"H":pH, "C":pC, "D":pD, "S":pS}
 
        # generate random card
        VA_cards = VA(cards_dist)
        card = VA_cards.alias_generation()
        n[card] += 1
        r[card] -= 1
        N -= 1

    wins[card] += 1 #the last chosen card is a winner.

print wins
