import numpy as np
import matplotlib.pyplot as plt


class GameOfLife():

    def __init__(self):
        self.width = 8
        self.height = 8
        self.matrix = np.zeros((self.width, self.height))
        self.load_start_shape()

    def load_start_shape(self):
        with open("gol_start_shape.txt") as f:
            shape = f.read().splitlines()
            shapelist = [indices.split(",") for indices in shape]

        for indices in shapelist:
            self.matrix[int(indices[0]), int(indices[1])] = 1

    def play_game(self):
        game_is_on = True
        i = 0
        while game_is_on:
            plt.figure(i+1)
            plt.matshow(self.matrix)

            i += 1
            will_be_born = []
            will_die = []

            for loc, cell in np.ndenumerate(self.matrix):
                neighbors = self.matrix[loc[0]-1:loc[0]+2, loc[1]-1:loc[1]+2]
                print(neighbors)
                count = np.sum(np.sum(neighbors, axis=0))-cell
                print(count)
                if count == 3:
                    will_be_born.append(loc)
                elif all((count < 2, len(neighbors > 0))):
                    will_die.append(loc)
                elif all((1 < count < 3, cell == 1)):
                    will_be_born.append(loc)
                elif count > 3:
                    will_die.append(loc)

            for born in will_be_born:
                self.matrix[born[0], born[1]] = 1

            for die in will_die:
                self.matrix[die[0], die[1]] = 0


            if i > 10:
                game_is_on = False
        plt.show()

gol = GameOfLife()
gol.play_game()
print("hello")
