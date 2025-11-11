import numpy as np

class Utils:
    
    @staticmethod
    def readCSV (file_path):
        data = np.genfromtxt(str(file_path), delimiter=',', names=True, dtype=None, encoding='utf-8')
        return data

    @staticmethod
    def evaluateSolution(solution):
        evaluation = 0
        data = Utils.readCSV('TSPproject/algeria_20_cities_xy.csv')

        for i in range(len(solution) - 1):
            city1 = solution[i]
            city2 = solution[i + 1]
            dist = np.sqrt((data['x_km'][city1] - data['x_km'][city2])**2 + (data['y_km'][city1] - data['y_km'][city2])**2)
            evaluation += dist

        return evaluation