from Utils.Utilities import Utils
from collections import deque
import random

class TabuSearch:
    def __init__(self):
        pass

    def tabu_search_visual(self, initialRoute, max_iter=400, max_no_improve=80):
        tabu_size = random.randint(5, 20)

        S = initialRoute[:]
        Best = S[:]
        fS = Utils.evaluateSolution(S)
        fBest = fS

        TabuList = deque(maxlen=tabu_size)
        no_improve = 0

        yield Best, fBest

        for iteration in range(max_iter):

            best_admissible = None
            best_admissible_cost = float('inf')
            best_move = None

            for i in range(1, len(S) - 2):
                for j in range(i + 1, len(S)):
                    if j - i == 1:
                        continue

                    move = (i, j)

                    S_prime = S[:]
                    S_prime[i:j] = reversed(S[i:j])
                    cost = Utils.evaluateSolution(S_prime)

                    if move in TabuList and cost >= fBest:
                        continue

                    if cost < best_admissible_cost:
                        best_admissible = S_prime
                        best_admissible_cost = cost
                        best_move = move

            if best_admissible is None:
                TabuList.clear()
                S = Best[:]
                no_improve += 1
                if no_improve >= max_no_improve:
                    break
                continue

            S = best_admissible
            fS = best_admissible_cost
            TabuList.append(best_move)

            if fS < fBest:
                Best = S[:]
                fBest = fS
                no_improve = 0
                yield Best, fBest
            else:
                no_improve += 1

            if no_improve >= max_no_improve:
                break

        yield Best, fBest
