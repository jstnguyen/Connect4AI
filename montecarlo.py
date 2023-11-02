import numpy as np
import random
import sys
import signal
from players import connect4Player
from copy import deepcopy

class monteCarloAI(connect4Player):

	def play(self, env, move):
		random.seed(self.seed)
		# Find legal moves
		env = deepcopy(env)
		env.visualize = False
		possible = env.topPosition >= 0 # boolean array, true where > 0 else false, this is possible moves otherwise you cannot make a move here (column all filled up)
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i) # copy and paste this code for my AI to see which columns are possible
		# Init fitness trackers
		vs = np.zeros(7) # which leads to most wins
		# Play until told to stop
		counter = 0
		while counter < 1000:
			first_move = random.choice(indices)
			turnout = self.playRandomGame(deepcopy(env), first_move)
			if turnout == self.position:
				vs[first_move] += 1
			elif turnout != 0:
				vs[first_move] -= 1
			if counter % 100 == 0: # what is the best move per every 100 moves? guarantees a move is returned even if time runs out
				move[:] = [np.argmax(vs)] # index position of the max number ex. np.argmax([2,23,3]) = 1
			counter += 1
		move[:] = [np.argmax(vs)]

	def playRandomGame(self, env, first_move):
		switch = {1:2,2:1}
		move = first_move
		player = self.position
		self.simulateMove(env, move, player)
		while not env.gameOver(move, player):
			player = switch[player]
			possible = env.topPosition >= 0
			indices = []
			for i, p in enumerate(possible):
				if p: indices.append(i)
			move = random.choice(indices)
			self.simulateMove(env, move, player)
		if len(env.history[0]) == 42: return 0
		return player

	def simulateMove(self, env, move, player): # likely needed similar function
		env.board[env.topPosition[move]][move] = player
		env.topPosition[move] -= 1
		env.history[0].append(move)

	def signal_handler(self):
		print("SIGTERM ENCOUNTERED")
		sys.exit(0)

