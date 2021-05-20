import numpy as np
import random
from scipy.ndimage.filters import gaussian_filter

class Particle():
    def __init__(self):
        self.width = 72
        self.height = 72
        self.x = 38
        self.y = 38
        self.particle_size = 1
        self.momentum = self.particle_size + 2 * random.random()
        self.dx = -1 + 2 * random.random()
        self.dy = -1 + 2 * random.random()
        self.matrix = np.zeros((self.height, self.width))
        self.decay = 0.8
        self.blur = 6
        self.blurred_matrix = gaussian_filter(self.matrix, self.blur)
        self.age = 0
        self.max_age = random.randint(300, 500) #in frames

    def move_particle(self):

        #Get slightly randomized direction values
        dx_new = self.dx + (-1 + 2 * random.random())
        dy_new = self.dy + (-1 + 2 * random.random())
        
        #normalize and factor in momentum
        vec_length = np.sqrt(dx_new**2 + dy_new**2)
        dx_new = (dx_new/vec_length*self.momentum)*0.8
        dy_new = (dy_new/vec_length*self.momentum)*0.8
        
        #Plan move in the direction
        x_plan = self.x + dx_new
        y_plan = self.y + dy_new

        #Check for collision
        x_condition = (x_plan > self.height-self.particle_size, x_plan < self.particle_size)
        y_condition = (y_plan > self.height-self.particle_size, y_plan < self.particle_size)
        if all((any(x_condition), any(y_condition))):
            self.dx = -dx_new*2
            self.dy = -dy_new*2
        elif any(x_condition):
            self.dx = -dx_new*2
        elif any(y_condition):
            self.dy = -dy_new*2
        else:
            self.dx = dx_new
            self.dy = dy_new

        #Move
        self.x = int(np.round(self.x + self.dx))
        self.y = int(np.round(self.y + self.dy))

    def update_matrix(self):
        x_min = self.x - self.particle_size
        x_max = self.x + self.particle_size
        y_min = self.y - self.particle_size
        y_max = self.y + self.particle_size
        self.matrix = self.matrix*(1 - self.decay)
        self.matrix[x_min:x_max, y_min:y_max] = 1
        
    def ageing(self):
        self.age += 1
        if self.age > self.max_age:
            self.x = int(np.floor(self.height/2))
            self.y = int(np.floor(self.width/2))
            self.age = random.randint(300,500)

    def engine(self):
        self.move_particle()
        self.update_matrix()
        self.blurred_matrix = gaussian_filter(self.matrix, self.blur)
        self.ageing()

