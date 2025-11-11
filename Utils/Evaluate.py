import numpy as np
import os

class Utils:
    
    @staticmethod
    def readCSV(file_path):
        # Build an absolute path relative to this file
        base_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(base_dir, '..', file_path)
        full_path = os.path.normpath(full_path)  # normalize ".." etc.

        data = np.genfromtxt(full_path, delimiter=',', names=True, dtype=None, encoding='utf-8')
        return data

    @staticmethod
    def evaluateSolution(solution):
        evaluation = 0
        
        # ✅ only the filename (not 'TSP project/...') since we fixed the path
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
