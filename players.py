import random
import time
import pygame
import math
import numpy as np
from copy import deepcopy


class connect4Player(object):
    def __init__(self, position, seed=0):
        self.position = position
        self.opponent = None
        self.seed = seed
        random.seed(seed)

    def play(self, env, move):
        move = [-1]


class human(connect4Player):

    def play(self, env, move):
        move[:] = [int(input('Select next move: '))]
        while True:
            if int(move[0]) >= 0 and int(move[0]) <= 6 and env.topPosition[int(move[0])] >= 0:
                break
            move[:] = [int(input('Index invalid. Select next move: '))]


class human2(connect4Player):

    def play(self, env, move):
        done = False
        while (not done):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                    posx = event.pos[0]
                    if self.position == 1:
                        pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
                    else:
                        pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS)
                pygame.display.update()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    posx = event.pos[0]
                    col = int(math.floor(posx / SQUARESIZE))
                    move[:] = [col]
                    done = True


class randomAI(connect4Player):

    def play(self, env, move):
        possible = env.topPosition >= 0
        indices = []
        for i, p in enumerate(possible):
            if p: indices.append(i)
        move[:] = [random.choice(indices)]


class stupidAI(connect4Player):

    def play(self, env, move):
        possible = env.topPosition >= 0
        indices = []
        for i, p in enumerate(possible):
            if p: indices.append(i)
        if 3 in indices:
            move[:] = [3]
        elif 2 in indices:
            move[:] = [2]
        elif 1 in indices:
            move[:] = [1]
        elif 5 in indices:
            move[:] = [5]
        elif 6 in indices:
            move[:] = [6]
        else:
            move[:] = [0]


class minimaxAI(connect4Player):

    def play(self, env, move):
        move[:] = [3]
        env = deepcopy(env)
        env.visualize = False

        if np.array_equal(env.topPosition, [5, 5, 5, 5, 5, 5, 5]) or np.array_equal(env.topPosition, [5, 5, 5, 4, 5, 5, 5]):
            move[:] = [3]
            return

        depth = 3
        v, col = self.max_val(env, move, depth)
        move[:] = [col]

    def simulateMove(self, env, move, player):
        env.board[env.topPosition[move]][move] = player
        env.topPosition[move] -= 1
        env.history[0].append(move)

    def eval_fun(self, env, move):
        score = 0
        env_copy = deepcopy(env)

        # weighting array based on possible wins if there is a piece in this location
        weighting_matrix = [[3, 4, 5, 7, 5, 4, 3], [3, 6, 8, 10, 8, 6, 3], [3, 7, 14, 16, 14, 7, 3],
                            [3, 7, 14, 16, 14, 7, 3], [3, 6, 8, 10, 8, 6, 3], [3, 4, 5, 7, 5, 4, 3]]

        for row in range(env.shape[0]):  # for row in number of rows given in board_shape
            for col in range(env.shape[1]):  # for column in number of columns given in board_shape
                if env_copy.board[row][col] == 1:  # check if this index is player 1
                    score += weighting_matrix[row][
                        col]  # increment the score by the corresponding index location in weighting_array
                else:
                    score -= weighting_matrix[row][
                        col]  # decrement the score by the corresponding index location in weighting_array
        return score


    def max_val(self, env, move, depth):
        possible = env.topPosition >= 0
        if len(env.history[0]) != 0:
            if env.gameOver(env.history[0][-1], self.opponent.position):
                return -math.inf, None
            elif np.array_equal(possible, [False, False, False, False, False, False, False]):
                return 0, None
            elif depth == 0:
                return self.eval_fun(env, move), None
        v = -math.inf
        col = 3  # col = 0
        for i, p in enumerate(possible):
            if p:
                child = deepcopy(env)  # name child
                self.simulateMove(child, i, self.position)
                child_val = self.min_val(child, i, depth - 1)[0]
                if child_val > v:
                    v = child_val
                    col = i
        return v, col

    def min_val(self, env, move, depth):
        possible = env.topPosition >= 0
        if len(env.history[0]) != 0:
            if env.gameOver(env.history[0][-1], self.position):
                return math.inf, None
            elif np.array_equal(possible, [False, False, False, False, False, False, False]):
                return 0, None
            elif depth == 0:
                return self.eval_fun(env, move), None
        v = math.inf
        col = 3
        for i, p in enumerate(possible):
            if p:
                child = deepcopy(env)
                self.simulateMove(child, i, self.opponent.position)
                child_val = self.max_val(child, i, depth - 1)[0]
                if child_val < v:
                    v = child_val
                    col = i
        return v, col

class alphaBetaAI(connect4Player):
    def play(self, env, move):
        self.move_order = [3,2,1,4,5,6,0]
        env = deepcopy(env)
        env.visualize = False

        if np.array_equal(env.topPosition, [5, 5, 5, 5, 5, 5, 5]) or np.array_equal(env.topPosition, [5, 5, 5, 4, 5, 5, 5]):
            move[:] = [3]
            return

        depth = 3
        v, col = self.max_val(env, move, depth, -math.inf, math.inf)
        move[:] = [col]
        print("timeout")

    def simulateMove(self, env, move, player):
        env.board[env.topPosition[move]][move] = player
        env.topPosition[move] -= 1
        env.history[0].append(move)

    def eval_fun(self, env, move):
        score = 0
        env_copy = deepcopy(env)

        # weighting array based on possible wins if there is a piece in this location
        weighting_matrix = [[3, 4, 5, 7, 5, 4, 3], [3, 6, 8, 10, 8, 6, 3], [3, 7, 14, 16, 14, 7, 3], [3, 7, 14, 16, 14, 7, 3], [3, 6, 8, 10, 8, 6, 3], [3, 4, 5, 7, 5, 4, 3]]

        for row in range(env.shape[0]):  # for row in number of rows given in board_shape
            for col in range(env.shape[1]):  # for column in number of columns given in board_shape
                if env_copy.board[row][col] == 1:  # check if this index is player 1
                    score += weighting_matrix[row][col]  # increment the score by the corresponding index location in weighting_array
                else:
                    score -= weighting_matrix[row][col]  # decrement the score by the corresponding index location in weighting_array
        return score

    def max_val(self, env, move, depth, a, b):
        possible = env.topPosition >= 0
        if len(env.history[0]) != 0:
            if env.gameOver(env.history[0][-1], self.opponent.position):
                return -math.inf, None
            elif np.array_equal(possible, [False, False, False, False, False, False, False]):
                return 0, None
            elif depth == 0:
                return self.eval_fun(env, move), None
        v = -math.inf
        col = 3  # col = 0
        for i, p in enumerate(possible):
            if p:
                child = deepcopy(env)
                self.simulateMove(child, self.move_order[i], self.position)
                child_val = self.min_val(child, self.move_order[i], depth - 1, a, b)[0]
                if child_val > v:
                    v = child_val
                    col = self.move_order[i]
                a = max(a, v)
                if a >= b:
                    break
        return v, col

    def min_val(self, env, move, depth, a, b):
        possible = env.topPosition >= 0
        if len(env.history[0]) != 0:
            if env.gameOver(env.history[0][-1], self.position):
                return math.inf, None
            elif np.array_equal(possible, [False, False, False, False, False, False, False]):
                return 0, None
            elif depth == 0:
                return self.eval_fun(env, move), None
        v = math.inf
        col = 3  # col = 0
        for i, p in enumerate(possible):
            if p:
                child = deepcopy(env)
                self.simulateMove(child, self.move_order[i], self.opponent.position)
                child_val = self.max_val(child, self.move_order[i], depth - 1, a, b)[0]
                if child_val < v:
                    v = child_val
                    col = self.move_order[i]
                b = min(b, v)
                if b <= a:
                    break
        return v, col

SQUARESIZE = 100
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

ROW_COUNT = 6
COLUMN_COUNT = 7

pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE / 2 - 5)

screen = pygame.display.set_mode(size)
