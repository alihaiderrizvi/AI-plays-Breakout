import pygame
import math
import matplotlib.pyplot as plt
import numpy as np

import time
from breakout import breakout

n_games = 3


for ep in range(n_games):
    game = breakout()
    frame_count = 0
    while game.is_running:
        game.render()
        if frame_count%30 == 0:
            game.extract_frame(frame_count)
        
        game.ball.move()
        game.slider_collision()
        game.brick_collision()
        game.win()
        game.loss()
        frame_count += 1
    
    


