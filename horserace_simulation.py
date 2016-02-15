#!/usr/bin/python

# Standard library
import math
import sys
from decimal import *
# Local application (see https://github.com/andyandy1992/Vose-Alias-Method)
from vose_sampler import VoseAlias as VA


def simulate_game(oH, oC, oD, oS):
    """ Runs a simulation for the horserace card game.
        Inputs: number of cards observed within the racetrack for each suit.
        Output: Letter referring to the winning suit. """

    # Remaining number of cards for each suit
    r = {}
    r["H"] = 13-oH-1 # remaining number of H (-1 for the "Ace of Hearts" horse)
    r["C"] = 13-oC-1
    r["D"] = 13-oD-1
    r["S"] = 13-oS-1
    N = r["H"]+r["C"]+r["D"]+r["S"] # total number of remaining cards in deck

    # Initialise counts for the number of flipped cards for each suit
    n = {}
    n["H"]=0
    n["C"]=0
    n["D"]=0
    n["S"]=0

    while n["H"]<6 and n["C"]<6 and n["D"]<6 and n["S"]<6:
        # Compute probability that each suit is flipped
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

    return card # the last chosen card is the winner


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print "\nERROR: 4 arguments required: oH oC oD oS [which denote the 'number of observed H, C, D, S respectively at the start of the race']"
        exit(1)

    oH = int(sys.argv[1]) # number of H observed at start (i.e. in the racetrack)
    oC = int(sys.argv[2])
    oD = int(sys.argv[3])
    oS = int(sys.argv[4])

    # Ensure only 6 cards given
    if (oH+oC+oD+oS) != 6:
        print "\nERROR: Number of cards observed in racetrack does not equal 6."
        exit(1)

    # Initialise counts for number of winnings simulations for each suit.
    wins = {}
    wins["H"]=0
    wins["C"]=0
    wins["D"]=0
    wins["S"]=0

    # Run simulations
    for i in range(1000):
        card = simulate_game(oH, oC, oD, oS)
        wins[card] += 1

    print wins
