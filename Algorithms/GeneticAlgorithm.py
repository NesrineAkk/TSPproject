from Utils.Utilities import Utils
import random


class GeneticAlgorithm:

    def __init__(self):
        pass

    def genetic_algorithm(self, initialRoute, population_size, crossover_rate, mutation_rate, max_generations):

        population = Utils.initialize_population(initialRoute, population_size)
        best_solution = population[0]
        best_distance = Utils.evaluateSolution(best_solution)

        for gen in range(max_generations):

            fitness_values = []
            for route in population:
                distance = Utils.evaluateSolution(route)
                fitness = 1 / (1 + distance)
                fitness_values.append(fitness)

                if distance < best_distance:
                    best_distance = distance
                    best_solution = route[:]

            selected_population = Utils.roulette_selection(population, fitness_values, population_size)

            new_population = []
            for i in range(0, population_size, 2):

                parent1 = selected_population[i]
                parent2 = selected_population[i+1] if i+1 < population_size else selected_population[0]

                if random.random() < crossover_rate:
                    child1, child2 = Utils.order_crossover(parent1, parent2)
                else:
                    child1, child2 = parent1[:], parent2[:]

                new_population.append(child1)
                new_population.append(child2)

            new_population = new_population[:population_size]

            for i in range(population_size):
                if random.random() < mutation_rate:
                    new_population[i] = Utils.swap_mutation(new_population[i])

            population = new_population

            # ✅ yield best solution at each generation
            yield best_solution, best_distance

