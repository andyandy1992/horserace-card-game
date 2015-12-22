#!/usr/bin/python

#LIBRARIES:
# Standard library
import math
import sys
from decimal import *
from fractions import Fraction


def choose(n, x):
    """ Compute 'n choose x' (i.e. the number of ways of choose r objects from a set of n
    objects where order is unimportant='combination'). """
    f = math.factorial
    return Decimal(f(n) / (f(x) * f(n-x)))

def perm(n, x):
    """ Compute the permutation of n and c (i.e. the number of ways of choose r objects from a set of n
    objects where order is important). """
    f = math.factorial
    return Decimal(f(n) / f(n-x))

def round_to(n, precision=0.05):
    """ Rounds a given number to the nearest 'precision' """
    correction = 0.5 if n >= 0 else -0.5 # so int (i.e. floor rounds to correct)
    return int( n/Decimal(precision)+Decimal(correction) ) * precision


def prob_win(N, X, rX, rY1, rY2, rY3):
    """ Let X\in{H, C, D, S} be the horse to win and Y1,Y2,Y3\in{H, C, D, S}\{X} be the losing horses.
    This function returns the probability that horse X wins the race. 
    N:='number remaining cards (i.e. 42 in usual play)', rX:='number remaining cards for suit to win',
    rY1:='number remaining cards of first suit not to win', rY2:='number remaining cards of second suit
    not to win', rY3:='number remaining cards of third suit not to win'
    """   
    nX = 6 #number of X flipped during race (for X to win)
    sum_pX = 0 # probability of X winning (summing over all possible winning arrangements)

    nY1 = 0 # number of Y1 observed during the race
    while nY1 < 6:
        nY2 = 0
        while nY2 < 6:
            nY3 = 0
            while nY3 < 6:
                nFlip = nX+nY1+nY2+nY3 #number of cards flipped
                nPos = nFlip-1 # number of possible positions for 5 X, nY1 Y1, nY2 Y2 and nY3 Y3 (noting that that last card must be X for X to win)
                nWays = choose(nPos,5)*choose(nPos-5,nY1)*choose(nPos-5-nY1,nY2)*choose(nPos-5-nY1-nY2,nY3) # number of ways of selecting the 5 X, nY1 Y1, nY2 Y2 and nY3 Y3
#                print "nWays of choosing nX="+str(nX)+", nY1="+str(nY1)+", nY2="+str(nY2)+", nY3="+str(nY3)+" is: "+str(nWays)
                pCards = (perm(rX,nX)*perm(rY1,nY1)*perm(rY2,nY2)*perm(rY3,nY3))/perm(N,nFlip) # probability of observing nX X, nY1 Y1, nY2 Y2 and nY3 Y3
#                print "pCards is: "+str(pCards)
          
                pX = nWays*pCards # probability of X win for this possible arrangement of cards (compare with binomial random variables).
                sum_pX += pX

                nY3 += 1
            nY2 += 1
        nY1 += 1

    return sum_pX


if __name__ == "__main__":
    #Let H:="Heart card(s)", C:="Club card(s)", D:="Diamond card(s)", S:="Spade card(s)"
    if len(sys.argv) != 5:
        print "ERROR: 4 arguments required: oH oC oD oS [which denote the 'number of observed H, C, D, S respectively at the start of the race']"
        exit(1)

    oH = int(sys.argv[1]) # number of H observed at start (i.e. in the racetrack)
    oC = int(sys.argv[2])
    oD = int(sys.argv[3])
    oS = int(sys.argv[4])

    rH = 13-oH-1 # remaining number of H (-1 for the "Ace of Hearts" horse)
    rC = 13-oC-1
    rD = 13-oD-1
    rS = 13-oS-1

    #Quick check: number of remaining cards at the start should be 42 (for usual setup)
    N = rH+rC+rD+rS # number of remainng cards at the start
    if N != 42:
        print "Number of remainng cards at the start does not equal 42. Were the number of observed cards for each suit entered corerectly?"
        exit(1)

    #Compute winning probability for each suit
    pH = prob_win(N, "H", rH, rC, rD, rS)
    pC = prob_win(N, "C", rC, rH, rD, rS)
    pD = prob_win(N, "D", rD, rH, rC, rS)
    pS = prob_win(N, "S", rS, rH, rC, rD)

#    print "Probability of H win="+str(pH)+", C win="+str(pC)+", D win="+str(pD)+", S win="+str(pS)
    total_sum = pH+pC+pD+pS
    if 1-total_sum > 0.05:
        print "ERROR: Probabilities didn't sum to 1. total_sum="+str(total_sum)

    #Compute horse odds (formula from https://www.google.co.uk/search?q=convert+probabilities+to+odds&oq=convert+probabilities+to+&gs_l=serp.3.0.0i22i30l10.80129.87682.0.88889.18.17.0.0.0.0.109.1340.16j1.17.0....0...1c.1.64.serp..9.9.731.TNXR5ahlXlk)
    odds_H = Fraction(round_to(pH/(1-pH))).limit_denominator()
    odds_C = Fraction(round_to(pC/(1-pC))).limit_denominator()
    odds_D = Fraction(round_to(pD/(1-pD))).limit_denominator()
    odds_S = Fraction(round_to(pS/(1-pS))).limit_denominator()
    print "Odds (e.g. 7/10='10 to 7 against'=stake 7 to win 10):"
    print "H win="+str(odds_H)+", C win="+str(odds_C)+", D win="+str(odds_D)+", S win="+str(odds_S)
    
