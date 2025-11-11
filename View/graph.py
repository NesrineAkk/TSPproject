import random
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import numpy as np
from Algorithms import LocalSearch, RandomSearch, HillClimbing
from Utils.Evaluate import Utils



class graph:
    FILE_PATH = 'TSPproject/algeria_20_cities_xy.csv'

    def __init__(self):
        self.data = Utils.readCSV(self.FILE_PATH)
        self.local = LocalSearch.localSearch()
        self.randomSearch = RandomSearch.randomSearch()
        self.hill = HillClimbing.hillClimbing()

        self.fig = None
        self.ax = None
        self.line = None

    

    def drawInitialGraph(self):
        self.fig, self.ax = plt.subplots()

        self.x = self.data['x_km']
        self.y = self.data['y_km']
        self.lat = self.data['lat']
        self.lon = self.data['lon']
        # need to add size propotional to lon * lat for better visualization
        # prod = np.abs(lat * lon)

        plt.scatter(self.x, self.y, c='red', marker='s', label='city', edgecolors='k', alpha=0.8)
        cities = self.data['city']
        for xi, yi, name in zip(self.x, self.y, cities):
            plt.annotate(name, (xi, yi), xytext=(6, 0), textcoords='offset points',
                         fontsize=8, ha='left', va='bottom')
            
        self.ax.set_xlabel('x (km)')
        self.ax.set_ylabel('y (km)')
        self.ax.set_title('Représentation spatiale de 20 villes d’Algérie')
        self.ax.legend()
        self.ax.grid(True, linestyle='--')

        self._add_buttons()

        plt.show()


        

    def _add_buttons(self):
        ax_random = self.fig.add_axes([0.1, 0.01, 0.2, 0.05])
        ax_local = self.fig.add_axes([0.4, 0.01, 0.2, 0.05])
        ax_hill = self.fig.add_axes([0.7, 0.01, 0.2, 0.05])

        # Create buttons
        self.btn_random = Button(ax_random, 'Random Search')
        self.btn_local = Button(ax_local, 'Local Search')
        self.btn_hill = Button(ax_hill, 'Hill Climbing')

        # Connect callbacks
        self.btn_random.on_clicked(self._on_random)
        self.btn_local.on_clicked(self._on_local)
        self.btn_hill.on_clicked(self._on_hill)

    def drawRoute(self, route, delay=0.3):
        if self.line and self.line in self.ax.lines:
            self.line.remove()
            self.line = None
        

        x_coords = self.x[route]
        y_coords = self.y[route]

        # Draw progressive path
        for i in range(1, len(route) + 1):
            if self.line:
                self.line.remove()
                self.line = None
            self.line, = self.ax.plot(x_coords[:i], y_coords[:i], color='blue', linewidth=1.5)
            plt.pause(delay)

        self.fig.canvas.draw()

    def _on_random(self, event):
        plt.title("Local Search:")

        for route, dist in self.randomSearch.randomSearch(10):
            self.drawRoute(route)
            print(f"new distance: {dist:.2f}")

        print("Done.")

    def _on_local(self, event):
        plt.title("Local Search:")

        # create an initial route
        initial = list(range(0, 20))
        random.shuffle(initial)


        for route, dist in self.local.two_optt(initial):
            self.drawRoute(route)
            print(f"new distance: {dist:.2f}")
        
        print("Done.")

    def _on_hill(self, event):
        plt.title("Hill Climbing:")

    # Create random starting route
        initial = list(range(0, 20))
        random.shuffle(initial)

        for route, dist in self.hill.two_opt_hill_climbing_visual(initial):
            self.drawRoute(route)
            print(f"new distance: {dist:.2f}")

        print("Done.")


    