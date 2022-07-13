SOL_LOWER = -1
SOL_EQUAL = 0
SOL_GREATER = +1

MIN_BASE = 2
MAX_BASE = 16

class GuessHints:
    def __init__(self, ncorrect, nmissp, soldir):
        self.ncorrect = ncorrect
        self.nmissp = nmissp
        self.soldir = soldir

    def get_ncorrect(self):
        return self.ncorrect

    def get_nmissp(self):
        return self.nmissp

    def get_soldir(self):
        return self.soldir

class NoomlyGame:
    def __init__(self, solution, base=10):
        self.solution = solution
        self.size = len(solution)
        self.base = base
        self.guesses = []
        self.solved = False

        if type(solution) is not str:
            raise TypeError("solution {} should be a string".format(repr(solution)))
        if self.size == 0:
            raise ValueError("solution string shouldn't be empty")
        if type(base) is not int:
            raise TypeError("base {} should be an integer".format(repr(base)))
        if not MIN_BASE <= base <= MAX_BASE:
            raise ValueError("base {} should be between {} and {}".format(base, MIN_BASE, MAX_BASE))
        if not is_in_base(solution, base):
            raise ValueError("solution {} should represent a number in base {}".format(solution, base))
