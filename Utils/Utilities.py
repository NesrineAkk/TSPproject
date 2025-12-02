import numpy as np
import os
import math
import random

class Utils:
    
    @staticmethod
    def readCSV(file_path):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(base_dir, '..', file_path)
        full_path = os.path.normpath(full_path)  

        data = np.genfromtxt(full_path, delimiter=',', names=True, dtype=None, encoding='utf-8')
        return data

    @staticmethod
    def evaluateSolution(solution):
        evaluation = 0
        
        data = Utils.readCSV('algeria_20_cities_xy.csv')

        for i in range(len(solution) - 1):
            city1 = solution[i]
            city2 = solution[i + 1]
            dist = np.sqrt(
                (data['x_km'][city1] - data['x_km'][city2])**2 +
                (data['y_km'][city1] - data['y_km'][city2])**2
            )
            evaluation += dist

        return evaluation
    

    @staticmethod
    def two_opt_neighbor(node):

        n = len(node)
        i, j = sorted(random.sample(range(n), 2))

        neighbor = node[:i] + list(reversed(node[i:j+1])) + node[j+1:]

        return neighbor

    @staticmethod
    def deltas_average(sampleNumber, initialNode):
        deltas = []

        for _ in range(sampleNumber):
            n = Utils.two_opt_neighbor(initialNode)
            deltaE = Utils.evaluateSolution(initialNode) - Utils.evaluateSolution(n)

            if deltaE > 0:
                deltas.append(deltaE)

        if len(deltas) == 0:
            return 0
        return sum(deltas) / len(deltas)
    
    @staticmethod
    def generate_schema(initialTemp, alpha, minimalTemp):
        schema = []
        T = initialTemp

        while T >= minimalTemp:
            schema.append(T)
            T = alpha * T
        
        return schema

    @staticmethod
    def initial_temp(sampleNumber, initialNode, initialProbability):
        deltaAvg = Utils.deltas_average(sampleNumber, initialNode)

        if deltaAvg == 0:
            return 1
        initial_temp = -deltaAvg / math.log(initialProbability)

        return initial_temp
    
    def initialize_population(initialRoute, population_size):
        pop = []
        for _ in range(population_size):
            r = initialRoute[:]
            random.shuffle(r)
            pop.append(r)
        return pop
    

    @staticmethod
    def roulette_selection(population, fitness_values, selection_size):
        total_fitness = sum(fitness_values)
        selected = []
        probabilities = [f / total_fitness for f in fitness_values]

        for _ in range(selection_size):
            r = random.random()
            cumulative = 0
            for i, prob in enumerate(probabilities):
                cumulative += prob
                if r <= cumulative:
                    selected.append(population[i][:])
                    break
        return selected


    @staticmethod
    def order_crossover(parent1, parent2):
        size = len(parent1)
        child1 = [None] * size
        child2 = [None] * size

        start, end = sorted(random.sample(range(size), 2))

        child1[start:end] = parent1[start:end]
        child2[start:end] = parent2[start:end]

        Utils.fill_child(child1, parent2, start, end)
        Utils.fill_child(child2, parent1, start, end)

        return child1, child2


    @staticmethod
    def fill_child(child, parent, start, end):
        size = len(child)
        pos_parent = end
        pos_child = end

        while None in child:
            gene = parent[pos_parent % size]
            if gene not in child:
                child[pos_child % size] = gene
                pos_child += 1
            pos_parent += 1


    @staticmethod
    def swap_mutation(route):
        i, j = random.sample(range(len(route)), 2)
        mutated = route[:]
        mutated[i], mutated[j] = mutated[j], mutated[i]
        return mutated