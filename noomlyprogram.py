"""Noomly with a text interface.

This program provides an interface for playing Noomly
in a text console.  It's a text-only view for the model
in the noomlygame module.  You can play the original
Noomly in https://noomly.surge.sh/.
"""

import random
from datetime import date
from string import digits

from noomlygame import *

HARD = False  # In hard mode, solution may contain repeated digits
SIZE = 4

today_string = date.today().isoformat()

random.seed(today_string)  # Just one different challenge each day

if HARD:
    sample = random.choices(digits, k=SIZE)
else:
    sample = random.sample(digits, SIZE)

solution = "".join(sample)

game = NoomlyGame(solution)

while not game.is_solved():
    guess_ok = False
    while not guess_ok:
        try:
            guess = input(f"Guess #{game.get_nguesses()+1:02d}> ")
            response = game.process_guess(guess)
            guess_ok = True
        except ValueError:
            print("INVALID GUESS VALUE!!! Please retry...")
    print(11*" " + f"{guess} --- {response}")

total_guesses = game.get_nguesses()
guesses_word = "guess" + ("" if total_guesses == 1 else "es")

print("WELL DONE!!!")
print(f"Number found in {total_guesses} {guesses_word}")
print("Bye!")
