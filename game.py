import pygame
import math
from constants import icon_path, slider_path, ball_path, brick1_path, brick2_path, bg_path, icon, slider_img, ball_img, brick_img, bg, screen_size, caption, fill, is_running, sliderX, sliderY, sliderX_change, bgX, bgY, ballX, ballY, ballX_change, ballY_change

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
    print(lst)
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

#checks collision with brick
def check_brick_collision(ballX, ballY, ballX_change, ballY_change):
    for a,b in brick_list:
        #to do: change brick coordinate calculation for more precision
        if a-50 < ballX < a+50 and b-50< ballY < b+50:
            #delets the brick
            brick_list.remove((a,b))

            # magnitude of velocity
            m = math.sqrt(ballX_change * ballX_change + ballY_change * ballY_change)

            #[nx,ny] is the collision normal
            nx = 0
            ny = -1

            #vx and vy are the normalized velocity (magnitude of 1)
            vx = ballX_change/m
            vy = ballY_change /m

            #t is the cosine of the angle between v and n
            t = vx * nx + vy * ny
            if t > 0:
                ballX_change -= 2*nx*m*t
                ballY_change -= 2*ny*m*t

    return ballX_change, ballY_change




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
    ballX_change, ballY_change = check_brick_collision(ballX, ballY, ballX_change, ballY_change)

    
    
    # resetting position if slider goes out of screen
    if sliderX < 0:
        sliderX = 0
    elif sliderX >= 680:
        sliderX = 680
    
    slider(sliderX, sliderY) # display slider
    bricks(brick_list) # display bricks
    ball(ballX, ballY) # display ball
    pygame.display.update() # updating screen