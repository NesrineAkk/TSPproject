import random
from Utils.Evaluate import Utils

class localSearch:

    def __init__(self):
        pass

    def isNeighbor(self, c1, c2):
        pass
    
    def neighbors(self, solution):
        pass
    
    def localSearch(self, initialSolution):

        best = initialSolution
        condition = True

        while condition:
            condition = False
            candidateSolutions = self.neighbors(best)
            for s in candidateSolutions:
                if Utils.evaluateSolution(s) < Utils.evaluateSolution(best):
                    best = s
                    condition = True
                    break

        return best

    def two_optt(self, initialRoute):
        best = initialRoute
        best_dist = Utils.evaluateSolution(best)
        improved = True
    
        yield best, best_dist

        while improved:
            improved = False
            
            for i in range(1, len(initialRoute) - 2):
                for j in range(i + 1, len(initialRoute)):
                    if j - i == 1: 
                        continue
                    
                    new_route = initialRoute[:]
                    
                    new_route[i:j] = initialRoute[j-1:i - 1:-1] 
                    new_dist = Utils.evaluateSolution(new_route)

                    if Utils.evaluateSolution(new_route) < Utils.evaluateSolution(best):
                        best = new_route
                        best_dist = new_dist
                        improved = True
                        initialRoute = best
                        yield best, best_dist

            yield best, best_dist
