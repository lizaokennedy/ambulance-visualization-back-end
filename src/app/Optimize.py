# Create ps
# Create population
# Initialoze population
# Run alogoritm
#
# Create function
#
from operator import pos
from random import randint, random
from app.Individual import Individual
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor
import numpy as np


class Optimize:
    population = []
    best_individual = None
    num_runs = 1
    iterations = 2000
    population_size = 30
    # todo must be editable
    max_ambu = 20 # constraint
    num_depots = 7  # dimention
    max_x = 8
    min_x = 0
    cross_prob = 0.7
    mutate_prob = 0.15
    penalty = 30*max_ambu
    retrain_prob = 0.002
    retrain_count = 0

    def run(self):
        for n in range(self.num_runs):
            self.init_population()
            print("Starting population")
            for i in self.population:
                print(i.fitness, i.position)
            print()
            for i in range(self.iterations):
                # print(i)
                if random() < self.retrain_prob:
                    self.trainSVM()
                    self.retrain_count += 1
                new_population = []
                for j in range(len(self.population)):
                    new_population.append(self.create_offspring())

                self.population = self.select_population(new_population)
                self.best_individual = self.population[0]
                if i == 0:
                    print("Best starting fitness")
                    print(self.best_individual.fitness)
            
            print("Best end fitness")
            print(self.best_individual.fitness)
            for i in self.population:
                print(i.fitness, i.position)
        print("Retrained", self.retrain_count, "Times")
        print("Global best fitness : " + str(self.best_individual.fitness))
        print("Global best position : ", self.best_individual.position)
        print("Actual Fitness:", self.expensive_eval(self.best_individual))
        return str(self.best_individual.fitness),self.best_individual.position

    def create_offspring(self):
        # create new individual by applying mutation operator
        p1 = self.population[randint(0, len(self.population) - 1)]
        p2 = self.population[randint(0, len(self.population) - 1)]

        c1, c2 = self.crossover(p1, p2)
        self.mutate(c1)
        self.mutate(c2)

        self.expensive_eval(c1)
        self.expensive_eval(c2)

        if c1.fitness < c2.fitness:
            return c1
        else:
            return c2

    def crossover(self, p1, p2):
        c1 = p1.clone()
        c2 = p2.clone()
        for i in range(len(p1.position)):
            if random() < self.cross_prob:
                temp = c1.position[i]
                c1.position[i] = c2.position[i]
                c2.position[i] = temp

        return c1, c2

    def mutate(self, c):
        for i in range(len(c.position)):
            if random() < self.mutate_prob:
                if random() < 0.5:
                    c.position[i] += random()*(self.max_x - c.position[i])
                else: 
                    c.position[i] += random()*(c.position[i] - self.min_x)

        return c

    def easy_eval(self, c):
        # check feasibility
        if not self.is_feasible(c.position):
            c.set_fitness(self.svm.predict([c.position])[0] + (self.penalty))
        else:
            c.set_fitness(self.svm.predict([c.position])[0])
        return c.fitness

    def expensive_eval(self, c):
        # check feasibility
        # set fitness score
        # call sumo
        fitness = 0
        if not self.is_feasible(c.position):
            fitness = self.penalty

        for i in range(1, len(c.position) + 1):
            fitness += (c.position[i-1])**2

        c.set_fitness(fitness)
        return fitness
      

    def select_population(self, new_population):
        sortedList = sorted(new_population, key=lambda x : x.fitness)

        if len(self.population) > 0:
            bestParent = sorted(self.population, key=lambda x : x.fitness)
            for i in range(7):
                sortedList[self.population_size - (i+1)] = bestParent[i]

        sortedList = sorted(sortedList, key=lambda x : x.fitness)
        return sortedList[:self.population_size]

    def init_population(self):
        start_population = []
        positions = []
        fitnesses = []
        for i in range(self.population_size * 10):
            start_population.append(Individual(self.max_ambu, self.num_depots))
            self.expensive_eval(start_population[i])
            positions.append(start_population[i].position)
            fitnesses.append(start_population[i].fitness)

        self.svm = SVR(kernel="rbf", C=100, gamma=0.1, epsilon=0.1)
        # self.svm = RandomForestRegressor(n_estimators=10)
        positions = np.array(positions)
        self.svm.fit(positions, fitnesses)

        self.population = self.select_population(start_population)
        for i in start_population:
            print(i.fitness, i.position)

    def trainSVM(self):
        positions = []
        fitnesses = []
        for i in range(len(self.population)):
            positions.append(self.population[i].position)
            fitnesses.append(self.expensive_eval(self.population[i]))
        self.svm = SVR(kernel="rbf", C=100, gamma=0.1, epsilon=0.1)
        # self.svm = RandomForestRegressor(n_estimators=10)
        self.svm.fit(positions, fitnesses)

    def is_feasible(self, pos):
        total = 0
        for i in range(len(pos)):
            total += pos[i]
        
        if total <= self.max_ambu:
            return True
        else:
            return False

if __name__ == "__main__":
    opt = Optimize()
    opt.run()
