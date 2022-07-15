import random
from datetime import date
from string import digits

from noomlygame import *

HARD = False
SIZE = 4

today_string = date.today().isoformat()

random.seed(today_string)

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
            guess = input("Guess #{:02d}> ".format(game.get_nguesses()+1))
            response = game.process_guess(guess)
            guess_ok = True
        except ValueError:
            print("INVALID GUESS VALUE!!! Please retry...")
    print(11*" "+"{} --- {}".format(guess, response))

print("WELL DONE!!! Bye!")
