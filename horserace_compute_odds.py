#!/usr/bin/python

# Standard library
import math
import sys
from decimal import *
from fractions import Fraction


def comb(n, r):
    """ Return the combination of n and r (i.e. the number of ways for positioning r cards within a total of
    n cards (where order doesn't matter). """
    f = math.factorial
    return f(n) / (f(r) * f(n-r))

def perm(n, r):
    """ Return the permutation of n and r (i.e. the number of ways for positioning r cards within a total of
    n cards (where order does matter)). """
    f = math.factorial
    return f(n) / f(n-r)

def prob_win(N, X, rX, rY1, rY2, rY3):
    """ Let X be in {H,C,D,S} be the horse to win and Y1,Y2,Y3 be in {H,C,D,S}\{X} be the losing horses.
    Return the probability that horse X wins the race.
    N:='number remaining cards (i.e. 42 in usual play)', rX:='number remaining cards for winning suit',
    rY1:='number remaining cards of first suit not to win', rY2:='number remaining cards of second suit
    not to win', rY3:='number remaining cards of third suit not to win' """

    nX = 6     # number of X flipped during race (for X to win)
    sum_probX = 0 # initial the sum representing the overall probability for X winning

    nY1 = 0    # number of Y1 flipped during the race (must be less than 6)
    while nY1 < 6:
        nY2 = 0
        while nY2 < 6:
            nY3 = 0
            while nY3 < 6:
                nFlip = nX+nY1+nY2+nY3 # total number of cards flipped
                nPos = nFlip-1         # total number of available positions for flipped cards (-1, noting that that last card must be X for X to win)

                # number of sequences for a combination of 5 X, nY1 Y1, nY2 Y2 and nY3 Y3
                nWays = comb(nPos,5) * comb(nPos-5,nY1) * comb(nPos-5-nY1,nY2) * comb(nPos-5-nY1-nY2,nY3)
#                print "Number of ways for choosing nX={0}, nY1={1}, nY2={2}, nY3={3} is: {4}".format(nX,nY1,nY2,nY3,nWays)

                # probability of observing nX X, nY1 Y1, nY2 Y2 and nY3 Y3 (any order)
                prob_cards = Decimal( perm(rX,nX) * perm(rY1,nY1) * perm(rY2,nY2) * perm(rY3,nY3) ) / Decimal( perm(N,nFlip) )
#                print "prob_cards is: {0}".format(prob_cards)
          
                # probability of X win given a combination of nX X, nY1 Y1, nY2 Y2 and nY3 Y3 (compare with binomial random variables)
                probX = nWays * prob_cards

                sum_probX += probX

                nY3 += 1
            nY2 += 1
        nY1 += 1

    return sum_probX

def pretty_prob(p):
    """ Return a fraction with a 'more sensible' denominator (to eventually create 'more sensible' odds) """
    # Initially try return a lower precision probability (but enventually a 'more sensible/bookie-like' odd)
    pretty_prob = Fraction(round_to(p)).limit_denominator()

    # If not precise enough, improve precision to prevent nonsense odds
    if pretty_prob == 0:
        pretty_prob = Fraction(round_to(p, precision=0.005)).limit_denominator()
    
    return pretty_prob

def round_to(p, precision=0.05):
    """ Return a given number p rounded to the nearest 'precision' """
    correction = 0.5 if p >= 0 else -0.5 # so int (i.e. floor rounds to correct)
    return int( Decimal(p) / Decimal(precision) + Decimal(correction) ) * precision

def prob2odds(p):
    """ Return the odds for a given probability p """
    # Note: in the case of the usual game, we do not have to handle impossible events (e.g if a horse cannot win), and so this equation will never result in
    #       divion by zero.
    return (1-p) / p


if __name__ == "__main__":
    # Let H:="Heart card(s)", C:="Club card(s)", D:="Diamond card(s)", S:="Spade card(s)"
    args_error = "\nERROR: 4 integer arguments required: oH oC oD oS [which denote the 'number of observed H, C, D, S respectively in the race track']"
    if len(sys.argv) != 5:
        print args_error
        exit(1)

    try:
        oH = int(sys.argv[1]) # number of H observed at start (i.e. in the race track)
        oC = int(sys.argv[2])
        oD = int(sys.argv[3])
        oS = int(sys.argv[4])
    except ValueError:
        print args_error
        exit(1)

    rH = 13-oH-1 # remaining number of H (-1 for the "Ace of Hearts" horse)
    rC = 13-oC-1
    rD = 13-oD-1
    rS = 13-oS-1

    # Quick check: number of remaining cards at the start should be 42 (for usual setup)
    N = rH+rC+rD+rS # number of remainng cards at the start
    if N != 42:
        print "\nERROR: Number of remaining cards at the start does not equal 42. Were the number of observed cards in the race track for each suit entered correctly?"
        exit(1)

    # Compute winning probability for each suit
    pH = prob_win(N, "H", rH, rC, rD, rS)
    pC = prob_win(N, "C", rC, rH, rD, rS)
    pD = prob_win(N, "D", rD, rH, rC, rS)
    pS = prob_win(N, "S", rS, rH, rC, rD)
    print "(More precise) winning probabilities: H={0}, C={1}, D={2}, S={3}".format(pH,pC,pD,pS)

	#Improve readability:
    pretty_pH = pretty_prob(pH)
    pretty_pC = pretty_prob(pC)
    pretty_pD = pretty_prob(pD)
    pretty_pS = pretty_prob(pS)
    print "(Rounded) winnings probabilities: H={0}, C={1}, D={2}, S={3}".format(pretty_pH, pretty_pC, pretty_pD, pretty_pS)
    #Check probs sum to 1
    total_sum = pH+pC+pD+pS
    if 1-total_sum > 0.05:
        print "\nERROR: Probabilities didn't sum to 1. total_sum={0}".format(total_sum)

    # Compute horse odds
    pretty_oddsH = prob2odds(pretty_pH)
    pretty_oddsC = prob2odds(pretty_pC)
    pretty_oddsD = prob2odds(pretty_pD)
    pretty_oddsS = prob2odds(pretty_pS)
    
    print "(Rounded) fair odds (where 3/1:='3 to 1 against'='stake 1 to win 3'):"
    print "H={0}/{1}, C={2}/{3}, D={4}/{5}, S={6}/{7}".format(pretty_oddsH.numerator, pretty_oddsH.denominator, pretty_oddsC.numerator, pretty_oddsC.denominator, pretty_oddsD.numerator, pretty_oddsD.denominator, pretty_oddsS.numerator, pretty_oddsS.denominator)
