from Utils.Utilities import Utils
import math
import random
class SimulatedAnnealing:
    def __init__(self):
        pass


    def simulated_annealing(self, initialState, schema):
        current = initialState
        current_cost = Utils.evaluateSolution(current)

        best = current
        best_cost = current_cost

        yield current, current_cost

        for t in schema:
            neighbor = Utils.two_opt_neighbor(current)
            neighbor_cost = Utils.evaluateSolution(neighbor)

            deltaE = neighbor_cost - current_cost

            if deltaE < 0 or math.exp(-deltaE / t) >= random.random():
                current = neighbor
                current_cost = neighbor_cost

                if current_cost < best_cost:
                    best = current
                    best_cost = current_cost

                yield current, current_cost

        yield best, best_cost
