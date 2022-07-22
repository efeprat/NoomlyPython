"""A model for the Noomly game.

This module provides a model for the Noomly game.  You can play
the original Noomly in https://noomly.surge.sh/.
"""

# Just lowercase letters to be allowed as digits
from string import digits, ascii_lowercase as letters

import re

SOL_LOWER = -1    # Solution < guess
SOL_EQUAL = 0     # Solution = guess
SOL_GREATER = +1  # Solution > guess

MIN_BASE = 2
MAX_BASE = 16

DIGITS = (digits + letters)[:MAX_BASE]


class ForbiddenCallError(Exception):
    pass


def is_in_base(str, base):
    # Does the string represent a number in this base?
    in_base_re = f"[{DIGITS[:base]}]+"
    return re.fullmatch(in_base_re, str) != None


class GuessHints:
    def __init__(self, ncorrect, nmisp, soldir):
        self.ncorrect = ncorrect  # Number of correct digits
        self.nmisp = nmisp        # Number of misplaced digits
        self.soldir = soldir      # Solution direction wrt the guess

    def get_ncorrect(self):
        return self.ncorrect

    def get_nmisp(self):
        return self.nmisp

    def get_soldir(self):
        return self.soldir

    def __str__(self):
        nc = self.ncorrect
        nm = self.nmisp
        if self.soldir == SOL_LOWER:
            comp_op = "<"
        elif self.soldir == SOL_EQUAL:
            comp_op = "="
        else:
            comp_op = ">"
        return f"NC: {nc}; NM: {nm}; S {comp_op} G"


class NoomlyGame:
    # A model for just one Noomly challenge
    def __init__(self, solution, base=10):

        if type(solution) is not str:
            raise TypeError(f"solution {repr(solution)} should be a string")
        if len(solution) == 0:
            raise ValueError("solution string shouldn't be empty")
        if type(base) is not int:
            raise TypeError(f"base {repr(base)} should be an integer")
        if not MIN_BASE <= base <= MAX_BASE:
            raise ValueError(f"base {base} should be between {MIN_BASE} and {MAX_BASE}")
        if not is_in_base(solution, base):
            raise ValueError(f"solution {solution} should represent a number in base {base}")

        self.solution = solution
        self.size = len(solution)
        self.base = base
        self.history = []
        self.solved = False

    def get_solution(self):

        if not self.solved:
            raise ForbiddenCallError("game still unsolved, so solution is a secret")

        return self.solution

    def get_size(self):
        return self.size

    def get_base(self):
        return self.base

    def get_history(self):
        return self.history

    def get_nguesses(self):
        return len(self.history)

    def is_solved(self):
        return self.solved

    def process_guess(self, guess):

        if type(guess) is not str:
            raise TypeError(f"guess {repr(solution)} should be a string")
        if len(guess) != self.size:
            raise ValueError(f"guess string size should be {self.size}")
        if not is_in_base(guess, self.base):
            raise ValueError(f"guess {guess} should represent a number in base {self.base}")
        if self.solved:
            raise ForbiddenCallError("game already solved, so no more guessing allowed")

        # Counting correct digits (in their correct places)
        nc = 0
        dic_g = {}
        dic_s = {}
        for i in range(self.size):
            gd = guess[i]
            sd = self.solution[i]
            if gd == sd:
                nc += 1
            else:
                dic_g[gd] = dic_g.get(gd, 0) + 1
                dic_s[sd] = dic_s.get(sd, 0) + 1
        self.solved = nc == self.size

        # Counting misplaced digits
        nm = 0
        if self.solved:
            soldir = SOL_EQUAL
        else:
            for d in dic_g:
                if d in dic_s:
                    nm += min(dic_g[d], dic_s[d])
            soldir = SOL_LOWER if self.solution < guess else SOL_GREATER

        response = GuessHints(nc, nm, soldir)
        self.history.append((guess, response))
        return response
