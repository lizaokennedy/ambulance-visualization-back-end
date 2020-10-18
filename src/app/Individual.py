import random

class Individual:
    # curr_position = [] 
    # best_position = []
    # velocity = []
    # curr_fitness = 0
    # best_fitness = 0
    # get_fitness = []
    # min_x = 0
    # max_x = 0
    # dimention = 0

    def __init__(self, max_x, dimention, first=False):
        self.dimention = dimention
        self.max_x = max_x
        self.position = []
        self.fitness = 0
        self.init_position(first)
        

    def init_position(self, first):
        allocated = 0
        if first:
            for i in range(self.dimention):
                self.position.append(0)
        else:
            for i in range(self.dimention):
                randomInt = random.randint(0, self.max_x - allocated)
                allocated += randomInt
                self.position.append(randomInt)
            random.shuffle(self.position)



    def set_fitness(self, fitness):
        self.fitness = fitness
    
    def set_position(self, position):
        self.position = position.copy()


    def clone(self):
        c = Individual(self.max_x, self.dimention)
        c.position = self.position.copy()
        return c
