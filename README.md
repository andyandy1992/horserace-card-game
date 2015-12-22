#Computing the odds for the horserace card game
Python implementation for computing the odds in the horserace card game:

![Example of the horserace card game in progress](/images/horserace.jpeg?raw=true "Example of the horserace card game in progress")

1. The 4 aces ("horses") are laid face-up at one end of the table.
2. 6 cards face-up are laid ("race track") in a straight line perpendicular to the aces.
3. The race proceeds by flipping the remaining deck, & the ace matching that suit advances one step until a winner reaches the finish line (card 6).

Solution explained: [Quora](https://www.quora.com/What-are-the-odds-for-the-horserace-card-game)

##<a name="depends-on">Depends on:</a>
- The Python Standard Library, https://docs.python.org/2/library/
- Python versions 2.7+ (tested on Python 2.7.9 

## Example usage:
To compute the odds for a race that shows 2 club cards, 2 diamond cards and 2 spade cards:
```python horserace_compute_odds.py 0 2 2 2```

You can also simulate n races of the horserace card game for a given set of observed cards in the race track with (edit within file directly - currently set to run 1000 races that show 2 club cards, 2 diamond cards and 2 spade cards in the racetrack):
```python horserace_simulation.py```
