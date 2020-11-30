import pygame
import math
import matplotlib.pyplot as plt
import numpy as np
import time
from breakout import breakout
from dqn_tf import Agent, DeepQNetwork
from utils import plotLearning


def stack_frames(stacked_frames, frame,buffer_size):
    if stacked_frames is None:
        stacked_frames = np.zeros((buffer_size, *frame.shape))
        for idx,_ in enumerate(stacked_frames):
            stacked_frames[idx,:] = frame
    
    else:
        stacked_frames[0:buffer_size-1, :] = stacked_frames[1:, :]
        stacked_frames[buffer_size-1,:] = frame

    stacked_frames = stacked_frames.reshape(1, *frame.shape[0:2], buffer_size)
    return stacked_frames


if __name__ == '__main__':
    
    load_checkpoint = False
    agent = Agent(gamma=0.99, epsilon=1.0, alpha=0.00025, 
                  input_dims=(80,60,4), n_actions=3, mem_size=60000, batch_size=32)

    if load_checkpoint:
        agent.load_models()
    
    scores = []
    eps_history = []
    n_games = 25000
    stack_size = 4
    score = 0
    frame_count = 0

    while agent.mem_cntr < 60000: #16000
        env = breakout()
        stacked_frames = None
        brick_count = 40
        observation = env.reset()
        observation = stack_frames(stacked_frames, observation, stack_size)
        while env.is_running:
            env.render()
            action = np.random.choice([0,1,2])
            env.slider.action(action)
            env.ball.move()
            env.slider_collision()
            env.brick_collision()
            env.win()
            env.loss()
            # print(observation.shape)
            if frame_count % 20 == 0 or not env.loss() or not env.win() or env.slider_collision():
                reward = 0
                observation_ = env.extract_frame(frame_count//20)
                observation_ = stack_frames(stacked_frames, observation_, stack_size)
                # reward += (brick_count - len(env.bricklist))*1000 # no reward on breaking brick due to temporal gap
                # brick_count = len(env.bricklist)
                if not env.loss():
                    reward -= 20000
                if not env.win():
                    reward += 10000
                if env.slider_collision():
                    reward += 5000
                if env.near_slider():
                    reward += 500
                # reward -= abs(env.ball.x - env.slider.x + 65)
                # print(reward)
                agent.store_transition(observation, action, reward, observation_, int(env.is_running))
                observation = observation_
                # print('observation shape: ', observation.shape)
            frame_count += 1
        print(agent.mem_cntr)
    print('done with random gameplay')


    for ep in range(n_games):
        score = 0
        brick_count = 40

        env = breakout()
        stacked_frames = None
        observation = env.reset()
        observation = stack_frames(stacked_frames, observation, stack_size)

        while env.is_running:
            env.render()
            action = agent.choose_action(observation)
            env.slider.action(action)
            env.ball.move()
            env.slider_collision()
            env.brick_collision()
            env.win()
            env.loss()
            # print(observation.shape)
            if frame_count % 20 == 0 or not env.loss() or not env.win() or env.slider_collision():
                reward = 0
                observation_ = env.extract_frame(frame_count//20)
                observation_ = stack_frames(stacked_frames, observation_, stack_size)
                reward += (brick_count - len(env.bricklist))*1000
                brick_count = len(env.bricklist)
                if not env.loss():
                    reward -= 20000
                if not env.win():
                    reward += 10000
                if env.slider_collision(): # ball collide with slider
                    reward += 5000
                if env.near_slider():
                    reward += 500
                # reward -= abs(env.ball.x - env.slider.x + 65)
                # print(reward)
                score += reward
                agent.store_transition(observation, action, reward, observation_, int(env.is_running))
                observation = observation_
                agent.learn()
                # print('observation shape: ', observation.shape)
            
            frame_count += 1
        
        if ep%50 == 0 and ep>0:
            avg_score = np.mean(scores[max(0,ep-10):(ep+1)])
            print('episode', ep, 'score', score, 'average score', avg_score, 'epsilon', agent.epsilon)
            agent.save_models()
        else:
            print('episode', ep, 'score', score)
        
        scores.append(score)
        eps_history.append(agent.epsilon)
    
    filename = 'learning_plot.png'
    x = [i for i in range(1,n_games+1)]
    plotLearning(x, scores, eps_history, filename)
    
