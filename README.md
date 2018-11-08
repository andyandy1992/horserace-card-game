# Computing the odds for the horserace card game
Python implementation for computing the odds in the horserace card game:

![Example of the horserace card game in progress](/images/horserace.jpeg?raw=true "Example of the horserace card game in progress")

1. The 4 aces ("horses") are laid face-up at one end of the table.
2. 6 cards face-up are laid ("race track") in a straight line perpendicular to the aces.
3. The race proceeds by flipping the remaining deck, & the ace matching that suit advances one step until a winner reaches the finish line (card 6).

Solution explained: [Medium](https://medium.com/@asmith9992/what-are-the-odds-for-the-horse-race-card-game-939a67602d2e)

## <a name="depends-on">Depends on:</a>
- The Python Standard Library, https://docs.python.org/2/library/
- Python versions 2.7 (tested on Python 2.7.11)

## Example usage:
To compute the odds for a race that shows 2 club cards, 2 diamond cards and 2 spade cards:

```python horserace_compute_odds.py 0 2 2 2```

You can also simulate 1000 races of the horserace card game for a given set of observed cards in the racetrack with:

```python horserace_simulation.py 0 2 2 2```
