import random

class Particle:
    # curr_position = [] 
    # best_position = []
    # velocity = []
    # curr_fitness = 0
    # best_fitness = 0
    # get_fitness = []
    # min_x = 0
    # max_x = 0
    # dimention = 0

    def __init__(self, get_fitness, max_x, dimention):
        self.dimention = dimention
        self.max_x = max_x
        self.curr_position = []
        self.velocity = []
        self.init_position()
        self.curr_fitness = get_fitness(self)
        self.best_position = self.curr_position
        self.best_fitness = self.curr_fitness
        self.get_fitness = get_fitness
        self.init_velocity()

    def init_position(self):
        for i in range(self.dimention):
            self.curr_position.append(random.randint(0, self.max_x))
            
        print(self.curr_position)

    def init_velocity(self):
        for i in range(self.dimention):
            self.velocity.append(0)

    def set_velocity(self, velocity):
        self.velocity = velocity

    def set_curr_position(self, curr_position):
        self.curr_position = curr_position

    def set_best_position(self, best_position):
        self.best_position = best_position

    def set_curr_fitness(self, fitness):
        self.curr_fitness = fitness
    
    def set_best_fitness(self, fitness):
        self.best_fitness = fitness
