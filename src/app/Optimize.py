# Create ps
# Create population
# Initialoze population
# Run alogoritm
#
# Create function
#
from random import randint, random
from app.Individual import Individual
from sklearn.svm import SVR

class Optimize:
    population = []
    best_individual = None
    num_runs = 1
    iterations = 2000
    population_size = 20
    # todo must be editable
    max_ambu = 5  # constraint
    num_depots = 3  # dimention
    max_x = 8
    min_x = 0
    cross_prob = 0.7
    mutate_prob = 0.15

    def run(self):
        # 5 * population size
        # hard_eval for each indiv
        # create svm from pop_size best individuals


        for i in range(self.num_runs):
            
            self.init_population(self)
            for i in range(self.iterations):
                new_population = []
                for j in range(len(self.population)):
                    new_population.append(self.create_offspring())

                self.best_individual = self.select_population(new_population)

        print("Global best fitness : " + str(self.g_best_fitness))
        print("Global best position : ", self.g_best_position)
        return str(self.g_best_fitness), self.g_best_position

    def select_population(self, new_population):
        return

    def create_offspring(self):
        # create new individual by applying mutation operator
        p1 = self.population[randint(0, len(self.population) - 1)]
        p2 = self.population[randint(0, len(self.population) - 1)]

        c1, c2 = self.crossover(p1, p2)
        self.mutate(c1)
        self.mutate(c2)

        self.easy_eval(c1)
        self.easy_eval(c2)

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
        c.set_fitness(self.svm.predict(c.position))

    def expensive_eval(self):
        # set fitness score
        # call sumo
        return

    def select_population(self, new_population):
        sortedList = sorted(self.population + new_population, key=lambda x : x.fitness)
        return sortedList[:self.population_size]

    def init_population(self):
        start_population = []
        positions = []
        fitnesses = []
        for i in range(self.population_size * 5):
            start_population.append(Individual(self.max_ambu, self.num_depots))
            start_population[i].set_fitness(self.expensive_eval(start_population[i]))
            positions.append(start_population[i].position)
            fitnesses[i].append(start_population[i].fitness)

        self.svm = SVR()
        self.svm.fit(positions, fitnesses)

        self.population = self.select_population(start_population)