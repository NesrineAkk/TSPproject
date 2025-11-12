import random
from Utils.Evaluate import Utils

class localSearch:

    def __init__(self):
        pass

    def isNeighbor(self, c1, c2):
        pass
    
    def swap(self, tour, i, j):
        new_tour = tour.copy()
        new_tour[i], new_tour[j] = new_tour[j], new_tour[i]
        return new_tour
    
    def localSearch(self, initialSolution):

        trajet = initialSolution
        dist = Utils.evaluateSolution(trajet)
        ameliore = True
    
        while ameliore:
            ameliore = False
            for i in range(1, len(trajet) - 1):
                for j in range(i + 1, len(trajet)):
                    nouveau_trajet = self.swap(trajet, i, j)
                    nouvelle_dist = Utils.evaluateSolution(nouveau_trajet)
                    if nouvelle_dist < dist:
                        trajet = nouveau_trajet
                        dist = nouvelle_dist
                        ameliore = True
                        yield trajet, dist
    
        yield trajet, dist

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
