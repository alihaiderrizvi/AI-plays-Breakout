import pygame

brick_height = 40
brick_width = 100

class brick:
    def __init__(self, x, y, img_path):
        self.x = x
        self.y = y
        self.img = pygame.image.load(img_path)
        self.height = brick_height
        self.width = brick_width