import pygame
from slider import slider
from ball import ball
from brick import brick
from constants import icon_path, slider_path, ball_path, brick1_path, brick2_path, bg_path, icon, slider_img, ball_img, brick1_img, brick2_img, brick3_img, brick4_img, brick5_img, brick6_img, brick7_img, brick8_img, bg, screen_size, caption, fill, is_running, sliderX, sliderY, sliderX_change, bgX, bgY, ballX, ballY, ballX_change, ballY_change, frame_count, rgb_weights
import math
from PIL import Image
import numpy as np

class breakout:
    def __init__(self):
        self.screen = None
        self.bg = pygame.image.load(bg_path)
        self.slider = slider(390, 530, 'assets/slider.png')
        self.ball = ball(200, 250, 'assets/ball.png')
        self.bricklist = []
        self.is_running = True

        for col in range(30, 191, 40):
            for row in range(0, 701, 100):
                self.bricklist.append(brick(row,col, 'assets/Brick1.png'))
    
    def extract_frame(self, frame_count):
        snap = pygame.surfarray.array3d(pygame.display.get_surface())
        snap = np.dot(snap, rgb_weights).astype(int) #convert to grayscale
        snap = snap.reshape((1, 80, 10, 60, 10)).max(4).max(2)[0] #resize
        snap = Image.fromarray(snap).convert('LA')
        snap.save('snap' + str(frame_count//30)+ '.png', 'PNG')

    def render(self):
        self.screen = pygame.display.set_mode(screen_size)
        self.screen.blit(self.bg, (0, 0))
        self.screen.blit(self.slider.img, (self.slider.x, self.slider.y))
        self.screen.blit(self.ball.img, (self.ball.x, self.ball.y))
        for brick in self.bricklist:
            self.screen.blit(brick.img, (brick.x, brick.y))
        pygame.display.update()
    
    def slider_collision(self):
        if 525 <= self.ball.y + 10 <= 530:
            if self.slider.x - 20 <= self.ball.x <= self.slider.x:
                self.ball.x_change = -6
                self.ball.y_change = -2

            elif self.slider.x + 1 <= self.ball.x <= self.slider.x + 20:
                self.ball.x_change = -5
                self.ball.y_change = -3
            
            elif self.slider.x + 21 <= self.ball.x <= self.slider.x + 50:
                self.ball.x_change = -4
                self.ball.y_change = -3

            elif self.slider.x + 51 <= self.ball.x <= self.slider.x + 80:
                self.ball.y_change = -self.ball.y_change

            elif self.slider.x + 81 <= self.ball.x <= self.slider.x + 110:
                self.ball.x_change = 4
                self.ball.y_change = -3

            elif self.slider.x + 111 <= self.ball.x <= self.slider.x + 130:
                self.ball.x_change = 5
                self.ball.y_change = -3
            
            elif self.slider.x + 131 <= self.ball.x <= self.slider.x + 150:
                self.ball.x_change = 6
                self.ball.y_change = -2

    def brick_collision(self):
        for brick in self.bricklist:
            #to do: change brick coordinate calculation for more precision
            if brick.x <= self.ball.x < brick.x+100 and brick.y <= self.ball.y <= brick.y+40:
                #delets the brick
                self.bricklist.remove(brick)

                # magnitude of velocity
                m = math.sqrt(self.ball.x_change**2 + self.ball.y_change**2)

                #[nx,ny] is the collision normal  
                if self.ball.y_change < 0:
                    nx = 0
                    ny = -1
                elif self.ball.x_change < 0:
                    nx = -1
                    ny = 0
                elif self.ball.x_change > 0:
                    nx = 1
                    ny = 0

                #vx and vy are the normalized velocity (magnitude of 1)
                vx = self.ball.x_change/m
                vy = self.ball.y_change/m

                #t is the cosine of the angle between v and n
                t = vx * nx + vy * ny
                if t > 0:
                    self.ball.x_change -= 2*nx*m*t
                    self.ball.y_change -= 2*ny*m*t


    def loss(self):
        if self.ball.y > 800:
            self.is_running = False
    
    def win(self):
        if self.bricklist == []:
            self.is_running = False
