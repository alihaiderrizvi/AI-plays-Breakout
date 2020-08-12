import pygame
import math
from constants import icon_path, slider_path, ball_path, brick1_path, brick2_path, bg_path, icon, slider_img, ball_img, brick1_img, brick2_img, brick3_img, brick4_img, brick5_img, brick6_img, brick7_img, brick8_img, bg, screen_size, caption, fill, is_running, sliderX, sliderY, sliderX_change, bgX, bgY, ballX, ballY, ballX_change, ballY_change

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
    for brick_pos, img in brick_list:
        screen.blit(img, brick_pos)

# create list of bricks
def form_bricks():
    lst = []
    for col in range(30, 191, 40):
        for row in range(0, 701, 100):
            lst.append((row, col))
    
    for i,_ in enumerate(lst):
        if i in (0,8,16,24,32):
            lst[i] = (lst[i], brick1_img)
        elif i in (1,9,17,25,33):
            lst[i] = (lst[i], brick2_img)
        elif i in (2,10,18,26,34):
            lst[i] = (lst[i], brick3_img)
        elif i in (3,11,19,27,35):
            lst[i] = (lst[i], brick4_img)
        elif i in (4,12,20,28,36):
            lst[i] = (lst[i], brick5_img)
        elif i in (5,13,21,29,37):
            lst[i] = (lst[i], brick6_img)
        elif i in (6,14,22,30,38):
            lst[i] = (lst[i], brick7_img)
        elif i in (7,15,23,31,39):
            lst[i] = (lst[i], brick8_img)
    
    print(lst)
    print(len(lst))
    return lst

# display ball
def ball(x,y):
    screen.blit(ball_img, (x,y))

# check collision with screen boundaries
def check_screen_collision(ballX, ballY, ballX_change, ballY_change):
    if ballY < 0:
        ballY_change = -1 * ballY_change
    if ballX < 0:
        ballX_change = -1 * ballX_change
    if ballX > 785:
        ballX_change = -1 * ballX_change

    return ballX_change, ballY_change

# check collision with slider
def check_slider_collision(ballX, ballY, ballX_change, ballY_change, sliderX, sliderY):
    if 525 <= ballY + 10 <= 530:
        if sliderX - 20 <= ballX <= sliderX:
            ballX_change = -6
            ballY_change = -2

        elif sliderX + 1 <= ballX <= sliderX + 24:
            ballX_change = -5
            ballY_change = -3
        
        elif sliderX + 25 <= ballX <= sliderX + 48:
            ballX_change = -4
            ballY_change = -3

        elif sliderX + 49 <= ballX <= sliderX + 72:
            ballY_change = -1 * ballY_change

        elif sliderX + 73 <= ballX <= sliderX + 96:
            ballX_change = 4
            ballY_change = -3

        elif sliderX + 97 <= ballX <= sliderX + 120:
            ballX_change = 5
            ballY_change = -3
        
        elif sliderX + 121 <= ballX <= sliderX + 140:
            ballX_change = 6
            ballY_change = -2
    
    return ballX_change, ballY_change

#checks collision with brick
def check_brick_collision(ballX, ballY, ballX_change, ballY_change):
    for pos, img in brick_list:
        #to do: change brick coordinate calculation for more precision
        if pos[0] <= ballX < pos[0]+100 and pos[1] <= ballY <= pos[1]+40:
            #delets the brick
            brick_list.remove((pos, img))

            # magnitude of velocity
            m = math.sqrt(ballX_change * ballX_change + ballY_change * ballY_change)

            #[nx,ny] is the collision normal  
            if ballY_change < 0:
                nx = 0
                ny = -1
            elif ballX_change < 0:
                nx = -1
                ny = 0
            elif ballX_change > 0:
                nx = 1
                ny = 0

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
    ballX_change, ballY_change = check_slider_collision(ballX, ballY, ballX_change, ballY_change, sliderX, sliderY)
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