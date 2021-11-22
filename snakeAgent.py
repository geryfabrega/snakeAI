import DeepQ
import numpy as np
import snakeGame
import time
from curses import wrapper
from ann_visualizer.visualize import ann_viz
import curses
import random
import curses
import pygame
import matplotlib.pyplot as plt


learning_rate = .001
n_games = 500
# make snake game 

#Find out what input_dims is by looking at Gyms documentation 

    # agent = Agent(gamma=0.99, epsilon=1.0, lr=learning_rate,
    #               input_dims=env.observation_space.shape, n_actions=env.action_space.n, mem_size=1000000,
    #               batch_size=64, epsilon_end=0.01)



#   n_actions is what our Agent can do AKA up,down,left and Right
#   input_dims is what out Agents sees. AKA eat apple, DIE, or get closer to further from Apple
myGame = snakeGame.SnakeGame()

agent = DeepQ.Agent(gamma=.99, epsilon=1.0,lr=learning_rate, input_dims=[6], n_actions=4, mem_size=100000000,batch_size=2048, epsilon_end=0.01)

scores = []
epsilon_history = []

myGame = snakeGame.SnakeGame()

for i in range(10):
    myGame.gameStart()
    observation = [0,0,0,0,0,0]
    score = 0
    while myGame.running:
        action = agent.choose_action([0])
        observations_ = myGame.frameAdvance(action)
        reward = myGame.globalScore
        agent.store_transition(observation,action,reward,observations_,myGame.running)
        observation = observations_
        score += reward
        agent.learn()

    epsilon_history.append(agent.epsilon)
    scores.append(score)
    avg_score = np.mean(scores[-100:])
    print("Episode:", i, " Score %.2f" % score,
            "Average score %.2f" % avg_score,
            "epsilon %.2f" % agent.epsilon)

plt.plot(scores)
plt.title("A graph of the score increase over each episode of learning ASCII SNAKE GAME'")
plt.ylabel("score")
plt.xlabel("Episode")
plt.show()  # plots the scores

curses.endwin()