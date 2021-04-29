import numpy as np
import matplotlib.pyplot as plt
import random
from scipy.ndimage.filters import gaussian_filter


class GameOfLife():

    def __init__(self):
        self.width = 16
        self.height = 16
        self.blur = 1
        self.matrix = np.zeros((self.height, self.width))
        self.add_random_shapes()

    def load_start_shape(self):
        with open("gol_start_shape.txt") as f:
            shape = f.read().splitlines()
            shapelist = [indices.split(",") for indices in shape]

        for indices in shapelist:
            self.matrix[int(indices[0]), int(indices[1])] = 1

    def add_random_shapes(self):
        r_pentomino = [[0, 1], [0, 2], [1, 0], [1, 1], [2, 1]]
        minus = [[0, 0], [0, 1], [0, 2]]
        glider = [[0, 1], [1, 2], [2, 0], [2, 1], [2, 2]]

        shapelist = [r_pentomino, minus]
        offset = [random.randint(3, self.height-3), random.randint(3, self.width-3)]

        for indices in random.choice(shapelist):
            self.matrix[indices[0]+offset[0], indices[1]+offset[1]] = \
                self.matrix[indices[0]+offset[0], indices[1]+offset[1]] + 1

    def check_live_or_die(self):

        will_be_born = []
        will_die = []

        for loc, cell in np.ndenumerate(self.matrix):
            neighbors = self.matrix[loc[0] - 1:loc[0] + 2, loc[1] - 1:loc[1] + 2]
            count = np.sum(np.sum(neighbors, axis=0)) - cell
            if count == 3:
                will_be_born.append(loc)
            elif all((count < 2, len(neighbors > 0))):
                will_die.append(loc)
            elif all((1 < count < 3, cell == 1)):
                will_be_born.append(loc)
            elif count > 3:
                will_die.append(loc)

        return will_be_born, will_die

    def play_game(self):

        shape_adder = random.randint(0, 1)
        live, die = self.check_live_or_die()
        for born in live:
            self.matrix[born[0], born[1]] = 1

        for die in die:
            self.matrix[die[0], die[1]] = 0

        if shape_adder == 0:
            self.add_random_shapes()
        blurred_matrix = gaussian_filter(self.matrix, self.blur)
        return blurred_matrix