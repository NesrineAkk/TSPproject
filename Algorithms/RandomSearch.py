import random
from Utils.Evaluate import Utils


class randomSearch:

    def __init__(self):
        pass
    def randomSolution(self):
        solution = random.sample(range(0,20), 20)
        return solution

    def randomSearch(self, num: int):
        best = self.randomSolution()
        best_dist = Utils.evaluateSolution(best)
        yield best, best_dist 

        while num > 0:
            candidate = self.randomSolution()
            dist = Utils.evaluateSolution(candidate)
            if Utils.evaluateSolution(candidate) < Utils.evaluateSolution(best):
                best = candidate
                best_dist = dist
                yield best, best_dist 
            num -= 1
        yield best, best_dist    