import pygame

icon_path = 'assets/icon.png'
slider_path = 'assets/slider.png'
ball_path = 'assets/ball.png'
brick1_path = 'assets/Brick1.png'
brick2_path = 'assets/Brick2.png'
brick3_path = 'assets/Brick3.png'
brick4_path = 'assets/Brick4.png'
brick5_path = 'assets/Brick5.png'
brick6_path = 'assets/Brick6.png'
brick7_path = 'assets/Brick7.png'
brick8_path = 'assets/Brick8.png'

bg_path = 'assets/background.png'

icon = pygame.image.load(icon_path)
slider_img = pygame.image.load(slider_path)
ball_img = pygame.image.load(ball_path)
brick1_img = pygame.image.load(brick1_path)
brick2_img = pygame.image.load(brick2_path)
brick3_img = pygame.image.load(brick3_path)
brick4_img = pygame.image.load(brick4_path)
brick5_img = pygame.image.load(brick5_path)
brick6_img = pygame.image.load(brick6_path)
brick7_img = pygame.image.load(brick7_path)
brick8_img = pygame.image.load(brick8_path)
bg = pygame.image.load(bg_path)

screen_size = (800, 600)
caption = 'AI plays Brick Breaker'
fill = (255, 255, 255)

is_running = True

sliderX, sliderY = 390, 530
sliderX_change = 0
bgX, bgY = (0, 0)
ballX, ballY = (200, 250)
ballX_change, ballY_change = 3, 3