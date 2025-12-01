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



        