import pygame

#initialize pygame
pygame.init()

#create screen
screen = pygame.display.set_mode((800,600))

#Title and Icon
pygame.display.set_caption("AI plays Brick Breaker")
icon = pygame.image.load('assets/icon.png')
pygame.display.set_icon(icon)

#setting game state
is_running = True

#game loop
while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False