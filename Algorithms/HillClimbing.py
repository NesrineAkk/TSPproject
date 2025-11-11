from Utils.Evaluate import Utils

class hillClimbing:

    def __init__(self):
        pass
    def two_opt_hill_climbing_visual(self, initialRoute):
        best = initialRoute
        best_distance = Utils.evaluateSolution(best)
        improved = True

        yield best, best_distance 

        while improved:
            improved = False
            best_neighbor = best
            best_neighbor_dist = best_distance

            for i in range(1, len(best) - 2):
                for j in range(i + 1, len(best)):
                    if j - i == 1:
                        continue
                    new_route = best[:]
                    new_route[i:j] = best[j-1:i - 1:-1]
                    new_distance = Utils.evaluateSolution(new_route)

                    if new_distance < best_neighbor_dist:
                        best_neighbor = new_route
                        best_neighbor_dist = new_distance
                        improved = True
            if improved:
                best = best_neighbor
                best_distance = best_neighbor_dist
                yield best, best_distance  

        yield best, best_distance