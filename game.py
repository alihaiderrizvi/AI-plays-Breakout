import pygame
from constants import *

# initialize pygame
pygame.init()

# create screen
screen = pygame.display.set_mode(screen_size)

# title and icon
pygame.display.set_caption(caption)
pygame.display.set_icon(icon)

# display slider
def slider(x,y):
    screen.blit(slider_img, (x, y))

# display bricks
def bricks(brick_list):
    for brick_pos in brick_list:
        screen.blit(brick_img, brick_pos)

# create list of bricks
def form_bricks():
    lst = []
    for col in range(30, 191, 40):
        for row in range(0, 801, 100):
            lst.append((row, col))
    return lst

# display ball
def ball(x,y):
    screen.blit(ball_img, (x,y))

# check collision with screen boundaries
def check_screen_collision(ballX, ballY, ballX_change, ballY_change):
    if ballY < 0:
        ballY_change = 3
    if ballX < 0:
        ballX_change = 3
    if ballX > 785:
        ballX_change = -1 * ballX_change

    return ballX_change, ballY_change

# check collision with slider
def check_slider_collision(ballX, ballY, ballX_change, ballY_change, sliderX, sliderY):
    if 525 <= ballY + 10 <= 530 and sliderX <= ballX + 20 <= sliderX + 140:
        ballY_change = -1 * ballY_change
    
    return ballY_change

# initialize brick list
brick_list = form_bricks()

# game loop
while is_running: #game state

    # set background color
    screen.fill(fill) # (Red, Green, Blue)
    screen.blit(bg, (bgX, bgY))
    for event in pygame.event.get():
        # check game quit
        if event.type == pygame.QUIT:
            is_running = False
        
        
        if event.type == pygame.KEYDOWN:
            # check left
            if event.key == pygame.K_LEFT:
                sliderX_change = -4
            
            # check right
            if event.key == pygame.K_RIGHT:
                sliderX_change = 4
        
        if event.type == pygame.KEYUP:
            if (event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):
                 sliderX_change = 0
        
    sliderX += sliderX_change
    ballX += ballX_change
    ballY += ballY_change

    ## basic collision - will change it later
    ballX_change, ballY_change = check_screen_collision(ballX, ballY, ballX_change, ballY_change)
    ballY_change = check_slider_collision(ballX, ballY, ballX_change, ballY_change, sliderX, sliderY)
    #check_brick_collision() ## todo ##
    
    
    # resetting position if slider goes out of screen
    if sliderX < 0:
        sliderX = 0
    elif sliderX >= 680:
        sliderX = 680
    
    slider(sliderX, sliderY) # display slider
    bricks(brick_list) # display bricks
    ball(ballX, ballY) # display ball
    pygame.display.update() # updating screen