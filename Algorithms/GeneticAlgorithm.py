from Utils.Utilities import Utils
import random


class GeneticAlgorithm:

    def __init__(self):
        pass

    def generate_random_population(self, population_size):
        random_paths = []
    
        for _ in range(population_size):
            random_path = list(range(1, 20))
            random.shuffle(random_path)
            random_path = [0] + random_path
            random_paths.append(random_path)
        return random_paths

    def choose_survivors(self, old_generation):
        survivors = []
        random.shuffle(old_generation)
        midway = len(old_generation) // 2
        for i in range(midway):
            if Utils.evaluateSolution(old_generation[i]) < Utils.evaluateSolution(old_generation[i + midway]):
                survivors.append(old_generation[i])
            else:
                survivors.append(old_generation[i + midway])
        return survivors

    def create_offspring(self, parent_a, parent_b):
        offsprings =[]
        start = random.randint(0, len(parent_a)-1)
        finish = random.randint(start, len(parent_a))
        sub_path_a = parent_a[start:finish]
        remaining_path_b = list([item for item in parent_b if item not in sub_path_a])
        for i in range(0, len(parent_a)):
            if start <= i < finish:
                offsprings.append(sub_path_a.pop(0))
            else:
                offsprings.append(remaining_path_b.pop(0))

        return offsprings
    

    def create_crossovers(self, survivors):
        offsprings = []
        midway = len(survivors) // 2
        for i in range(midway):
            parent_a, parent_b = survivors[i], survivors[i + midway]
            for _ in range(2):
                offsprings.append(self.create_offspring(parent_a, parent_b))
                offsprings.append(self.create_offspring(parent_b, parent_a))
        return offsprings
    
    def apply_mutation(self, generation):
        mutated_gen = []
        for path in generation:
            if random.randint(0, 1000) < 9:
                index1, index2 = random.randint(1, len(path) - 1), random.randint(1, len(path) - 1)
                path[index1], path[index2] = path[index2], path[index1]
            mutated_gen.append(path)
        return mutated_gen
    
    def generate_new_population(self, old_generation):
        survivors = self.choose_survivors(old_generation)
        crossovers = self.create_crossovers(survivors)
        new_population = self.apply_mutation(crossovers)
        return new_population
    

    def genetic_algorithm_visual(self, population_size, generations):
        

        population = self.generate_random_population(population_size)
        best_solution = population[0]
        best_distance = Utils.evaluateSolution(best_solution)

        for gen in range(generations):

            population = self.generate_new_population(population)
            
            best = population[0]
            for p in population:
                if Utils.evaluateSolution(best) < Utils.evaluateSolution(p):
                    best = p
            
            best_dist = Utils.evaluateSolution(best)
            if best_distance > best_dist:
                best_solution = best
                best_distance = best_dist
                yield best, best_dist


        
    def genetic_algorithm_2(self, population_size, generations, fitness_function):
        population = self.generate_random_population(population_size)

        for gen in range(generations):

            fitnesses = [fitness_function(p) for p in population]
            survivors = self.roullette_wheel_selection(population, fitnesses, selection_size=population_size // 2)
            offspring = self.create_crossovers(survivors)
            offspring = self.apply_mutation(offspring)
            population = survivors + offspring

        final_fitnesses = [fitness_function(p) for p in population]
        best_index = final_fitnesses.index(max(final_fitnesses))
        return population[best_index], final_fitnesses[best_index]

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

            yield best_solution, best_distance

