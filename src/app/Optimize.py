# Create ps
# Create swarm
# Initialoze swarm
# Run alogoritm
#
# Create function
#
import random
from app.Particle import Particle


class Optimize:
    swarm = []
    g_best_position = []
    g_best_fitness = []
    num_runs = 1
    iterations = 2000
    swarm_size = 35
    c1 = 1.4
    c2 = 1.4
    w = 0.7
# todo must be editable
    max_ambu = 5  # constraint
    num_depots = 3  # dimention
    max_x = 8
    min_x = 0

    def run(self):
        for i in range(self.num_runs):
            self.init_swarm(self)
            self.g_best_position = self.swarm[0].best_position
            self.g_best_fitness = self.swarm[0].best_fitness

            # run PSO
            for i in range(self.iterations):
                for j in range(len(self.swarm)):
                    curr_fitness = self.swarm[j].curr_fitness
                    if curr_fitness < self.swarm[j].best_fitness:
                        self.update_personal_best(self.swarm[j])

                    if self.swarm[j].best_fitness < self.g_best_fitness:
                        self.g_best_position = self.swarm[j].best_position
                        self.g_best_fitness = self.swarm[j].best_fitness

                for j in range(len(self.swarm)):
                    self.update_velocity(self, self.swarm[j])
                    self.update_position(self, self.swarm[j])

        print("Global best fitness : " + str(self.g_best_fitness))
        print("Global best position : ", self.g_best_position)
        return str(self.g_best_fitness), self.g_best_position

    def update_personal_best(self, p):
        curr_fitness = p.curr_fitness

        if (self.is_feasible(p)):
            p.best_fitness = curr_fitness
            p.best_position = p.curr_position

    def update_position(self, p):
     # todo calc fitness and update
        for i in range(self.num_depots):
            p.curr_position[i] = p.curr_position[i] + p.velocity[i]

    def update_velocity(self, p):
        for i in range(self.num_depots):
            r1 = random.random()
            r2 = random.random()
            p.velocity[i] = self.w * p.velocity[i] + self.c1 * r1 * \
                (p.best_position[i] - p.curr_position[i]) + self.c2 * \
                 r2 * (self.g_best_position[i] - p.curr_position[i])

    # todo must fix function to be accurate for simulation
    def get_fitness(p):
        fitness = 0
        for i in range(len(p.curr_position)):
            fitness += p.curr_position[i]*2

        return fitness

    def is_feasible(self, p):
        count = 0
        for i in range(len(p.curr_position)):
            count += p.curr_position[i]

        if count < self.max_ambu:
            return True
        else:
            return False

    def init_swarm(self):
        for i in range(self.swarm_size):
            self.swarm.append(Particle(self.get_fitness, self.max_ambu, self.num_depots))











