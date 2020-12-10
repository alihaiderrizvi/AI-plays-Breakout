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
    
    load_checkpoint = True
    agent = Agent(gamma=0.99, epsilon=0.05, alpha=0.001,
                  input_dims=(80,60,4), n_actions=3, mem_size=50000, batch_size=32)

    if load_checkpoint:
        agent.load_models()
    
    scores = []
    eps_history = []
    times = []
    n_games = 3000
    stack_size = 4
    score = 0
    frame_count = 0

##    while agent.mem_cntr < 10000: #16000
##        env = breakout()
##        stacked_frames = None
##        brick_count = 40
##        observation = env.reset()
##        observation = stack_frames(stacked_frames, observation, stack_size)
##        while env.is_running:
##            env.render()
##            if env.ball.x+10 < env.slider.x+30:
##                action = 0
##            elif env.ball.x+10 > env.slider.x+100:
##                action = 2
##            else:
##                action = 1
##
####            action = np.random.choice([0,1,2])
##            env.slider.action(action)
##            env.ball.move()
##            env.slider_collision()
##            env.brick_collision()
##            env.win()
##            env.loss()
##            # print(observation.shape)
##            if frame_count % 20 == 0 or not env.loss() or not env.win() or env.slider_collision():
##                reward = 0
##                observation_ = env.extract_frame(frame_count//20)
##                observation_ = stack_frames(stacked_frames, observation_, stack_size)
##                # reward += (brick_count - len(env.bricklist))*1000 # no reward on breaking brick due to temporal gap
##                # brick_count = len(env.bricklist)
##                if not env.loss():
##                    reward -= 10000
##                if not env.win():
##                    reward += 10000
##                if env.slider_collision(): # ball collide with slider
##                    reward += 1000
##                if env.near_slider():
##                    reward += 1000
##                if env.ball_over_slider(): # ball.x match with slider.x
##                    reward += 1000
##                if not env.ball_over_slider(): # ball.x not over slider
##                    reward -= 100
##                # reward -= abs(env.ball.x - env.slider.x + 65)
##                # print(reward)
##                agent.store_transition(observation, action, reward, observation_, int(env.is_running))
##                observation = observation_
##                # print('observation shape: ', observation.shape)
##            frame_count += 1
##        print(agent.mem_cntr)
##    print('done with random gameplay')

    start = time.time()
    for ep in range(n_games):
        score = 0
        brick_count = 40

        env = breakout()
        stacked_frames = None
        observation = env.reset()
        observation = stack_frames(stacked_frames, observation, stack_size)

        while env.is_running:
            env.render()
            if env.ball.x+10 < env.slider.x+30:
                ideal = 0
            elif env.ball.x+10 > env.slider.x+100:
                ideal = 2
            else:
                ideal = 1
            action = agent.choose_action(observation, ideal)
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
##                reward += (brick_count - len(env.bricklist))*1000
##                brick_count = len(env.bricklist)
                if not env.loss():
                    reward -= 10000
                if not env.win():
                    reward += 10000
                if env.slider_collision(): # ball collide with slider
                    reward += 1000
                if env.near_slider():
                    reward += 1000
                if env.ball_over_slider(): # ball.x match with slider.x
                    reward += 1000
                if not env.ball_over_slider(): # ball.x not over slider
                    reward -= 300
                # reward -= abs(env.ball.x - env.slider.x + 65)
                # print(reward)
                score += reward
                agent.store_transition(observation, action, reward, observation_, int(env.is_running))
                observation = observation_
                agent.learn()
                # print('observation shape: ', observation.shape)
            
            frame_count += 1
        
        if ep%10 == 0 and ep>0:
            avg_score = np.mean(scores[max(0,ep-10):(ep+1)])
            print('episode', ep, 'score', score, 'average score', avg_score, 'epsilon', agent.epsilon)
            agent.save_models()
        else:
            print('episode', ep, 'score', score, 'epsilon', agent.epsilon)
        
        scores.append(score)
        eps_history.append(agent.epsilon)

        if ep%2 == 0:
            stop = time.time()
            times.append(stop-start)
            start = time.time()

        
    print(scores)
    print(eps_history)
    print(times)
    
    f = open('text.txt', 'w')

    write_scores = ', '.join(list(map(str, scores)))
    write_scores = '[' + write_scores + ']'
    f.write('scores = ')
    f.write(write_scores)

    f.write('\n\n')

    write_eps = ', '.join(list(map(str, eps_history)))
    write_eps = '[' + write_eps + ']'
    f.write('eps_history = ')
    f.write(write_eps)

    f.write('\n\n')

    write_times = ', '.join(list(map(str, times)))
    write_times = '[' + write_times + ']'
    f.write('times = ')
    f.write(write_times)
    
    f.close()
    
    filename = 'learning_plot.png'
    x = [i for i in range(1,n_games+1)]
    plotLearning(x, scores, eps_history, filename)
    
