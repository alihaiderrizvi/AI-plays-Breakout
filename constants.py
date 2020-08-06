import pygame

icon_path = 'assets/icon.png'
slider_path = 'assets/slider.png'
ball_path = 'assets/ball.png'
brick1_path = 'assets/brick1.png'
brick2_path = 'assets/brick2.png'
bg_path = 'assets/background.png'

icon = pygame.image.load(icon_path)
slider_img = pygame.image.load(slider_path)
ball_img = pygame.image.load(ball_path)
brick_img = pygame.image.load(brick1_path)
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

