import os
import sys
import random
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import numpy as np


# allow access to other folders (Algorithms, Utils)
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from Algorithms import LocalSearch, RandomSearch, HillClimbing, SimulatedAnnealing, GeneticAlgorithm, TabuSearch
from Utils.Utilities import Utils


class graph:
    
    FILE_PATH = os.path.join(os.path.dirname(__file__), '..', 'algeria_20_cities_xy.csv')
    ALGIERS_INDEX = 0  # Assuming Algiers is at index 0 in the CSV
    
    def __init__(self):
        self.data = Utils.readCSV(self.FILE_PATH)
        self.local = LocalSearch.localSearch()
        self.randomSearch = RandomSearch.randomSearch()
        self.hill = HillClimbing.hillClimbing()
        self.sa = SimulatedAnnealing.SimulatedAnnealing() 
        self.ga = GeneticAlgorithm.GeneticAlgorithm()
        self.tabu = TabuSearch.TabuSearch()


        self.fig = None
        self.ax = None
        self.line = None

    def drawInitialGraph(self):
        self.fig, self.ax = plt.subplots()

        self.x = self.data['x_km']
        self.y = self.data['y_km']
        self.lat = self.data['lat']
        self.lon = self.data['lon']

        plt.scatter(self.x, self.y, c='red', marker='s', label='city', edgecolors='k', alpha=0.8)
        
        # Highlight Algiers with a different color
        plt.scatter(self.x[self.ALGIERS_INDEX], self.y[self.ALGIERS_INDEX], 
                   c='green', marker='*', s=300, label='Algiers (Start/End)', 
                   edgecolors='k', alpha=1, zorder=5)
        
        cities = self.data['city']
        for xi, yi, name in zip(self.x, self.y, cities):
            plt.annotate(name, (xi, yi), xytext=(6, 0), textcoords='offset points',
                         fontsize=8, ha='left', va='bottom')
            
        self.ax.set_xlabel('x (km)')
        self.ax.set_ylabel('y (km)')
        self.ax.set_title('Représentation spatiale de 20 villes d\'Algérie')
        self.ax.legend()
        self.ax.grid(True, linestyle='--')

        self._add_buttons()

        plt.show()

    def _add_buttons(self):
        ax_random = self.fig.add_axes([0.01, 0.01, 0.15, 0.05])
        ax_local  = self.fig.add_axes([0.17, 0.01, 0.15, 0.05])
        ax_hill   = self.fig.add_axes([0.33, 0.01, 0.15, 0.05])
        ax_sa     = self.fig.add_axes([0.49, 0.01, 0.15, 0.05])
        ax_tabu   = self.fig.add_axes([0.65, 0.01, 0.15, 0.05])
        ax_ga     = self.fig.add_axes([0.81, 0.01, 0.15, 0.05])

        self.btn_random = Button(ax_random, 'Random')
        self.btn_local  = Button(ax_local, 'Local Search')
        self.btn_hill   = Button(ax_hill, 'Hill Climb')
        self.btn_sa     = Button(ax_sa, 'Simulated A.')
        self.btn_tabu   = Button(ax_tabu, 'Tabu Search')
        self.btn_ga     = Button(ax_ga, 'Genetic Algo')

        self.btn_random.on_clicked(self._on_random)
        self.btn_local.on_clicked(self._on_local)
        self.btn_hill.on_clicked(self._on_hill)
        self.btn_sa.on_clicked(self._on_sa)
        self.btn_tabu.on_clicked(self._on_tabu)
        self.btn_ga.on_clicked(self._on_ga)


    def drawRoute(self, route, delay=0.3):
        if self.line and self.line in self.ax.lines:
            self.line.remove()
            self.line = None
        
        # Add Algiers at the end to complete the circuit
        full_route = list(route) + [self.ALGIERS_INDEX]
        
        x_coords = self.x[full_route]
        y_coords = self.y[full_route]

        # Draw progressive path
        for i in range(1, len(full_route) + 1):
            if self.line:
                self.line.remove()
                self.line = None
            self.line, = self.ax.plot(x_coords[:i], y_coords[:i], color='blue', linewidth=1.5)
            plt.pause(delay)

        self.fig.canvas.draw()

    def _create_initial_route(self):
        """Create a random route that starts with Algiers"""
        # Get all cities except Algiers
        other_cities = [i for i in range(20) if i != self.ALGIERS_INDEX]
        random.shuffle(other_cities)
        # Start with Algiers
        return [self.ALGIERS_INDEX] + other_cities

    def _on_random(self, event):
        self.ax.set_title("Random Search")

        for route, dist in self.randomSearch.randomSearch(10):
            # Ensure route starts with Algiers
            if route[0] != self.ALGIERS_INDEX:
                # Find Algiers in the route and move it to the start
                algiers_pos = route.index(self.ALGIERS_INDEX)
                route = [self.ALGIERS_INDEX] + route[:algiers_pos] + route[algiers_pos+1:]
            
            self.drawRoute(route)
            print(f"new distance: {dist:.2f}")

        print("Done.")

    def _on_local(self, event):
        self.ax.set_title("Local Search")

        # Create an initial route starting from Algiers
        initial = self._create_initial_route()

        for route, dist in self.local.two_optt(initial):
            # Ensure Algiers stays at the start
            if route[0] != self.ALGIERS_INDEX:
                algiers_pos = route.index(self.ALGIERS_INDEX)
                route = [self.ALGIERS_INDEX] + route[:algiers_pos] + route[algiers_pos+1:]
            
            self.drawRoute(route)
            print(f"new distance: {dist:.2f}")
        
        print("Done.")

    def _on_hill(self, event):
        self.ax.set_title("Hill Climbing")

        # Create random starting route from Algiers
        initial = self._create_initial_route()

        for route, dist in self.hill.two_opt_hill_climbing_visual(initial):
            # Ensure Algiers stays at the start
            if route[0] != self.ALGIERS_INDEX:
                algiers_pos = route.index(self.ALGIERS_INDEX)
                route = [self.ALGIERS_INDEX] + route[:algiers_pos] + route[algiers_pos+1:]
            
            self.drawRoute(route)
            print(f"new distance: {dist:.2f}")

        print("Done.")

    def _on_sa(self, event):
        self.ax.set_title("Simulated Annealing")

        initial = self._create_initial_route()

        sampleNumber = 40
        delta_prob = 0.9
        alpha = 0.90
        minimalTemp = 0.01

        initialTemp = Utils.initial_temp(sampleNumber, initial, delta_prob)
        schema = Utils.generate_schema(initialTemp, alpha, minimalTemp)

        for route, dist in self.sa.simulated_annealing(initial, schema):

            if route[0] != self.ALGIERS_INDEX:
                algiers_pos = route.index(self.ALGIERS_INDEX)
                route = [self.ALGIERS_INDEX] + route[:algiers_pos] + route[algiers_pos+1:]

            self.drawRoute(route)   
            print(f"new distance: {dist:.2f}")

        print("Done.")

    def _on_tabu(self, event):
        self.ax.set_title("Tabu Search")

        initial = self._create_initial_route()

        for route, dist in self.tabu.tabu_search_visual(initial):

            if route[0] != self.ALGIERS_INDEX:
                algiers_pos = route.index(self.ALGIERS_INDEX)
                route = [self.ALGIERS_INDEX] + route[:algiers_pos] + route[algiers_pos+1:]

            self.drawRoute(route)   
            print(f"new distance: {dist:.2f}")

        print("Done.")

    def _on_ga(self, event):
        self.ax.set_title("Genetic Algorithm")

        initial = self._create_initial_route()

        population_size = 50
        crossover_rate = 0.8
        mutation_rate = 0.2
        max_generations = 50

        last_best = float("inf")

        for route, dist in self.ga.genetic_algorithm(
            initial,
            population_size,
            crossover_rate,
            mutation_rate,
            max_generations
        ):

            if dist < last_best:

                # Rotate so Algiers is first
                if route[0] != self.ALGIERS_INDEX:
                    pos = route.index(self.ALGIERS_INDEX)
                    route = route[pos:] + route[:pos]

                # Add Algiers again ONLY for drawing (start = end)
                route_to_draw = route + [self.ALGIERS_INDEX]

                self.drawRoute(route_to_draw)
                print(f"new distance: {dist:.2f}")

                last_best = dist

        print("Done.")
