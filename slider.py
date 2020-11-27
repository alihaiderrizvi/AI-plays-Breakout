import pygame


class slider:
    def __init__(self, x, y, img_path):
        self.x = x
        self.y = y
        self.img = pygame.image.load(img_path)
    
    def move(self, x):
        self.x += x
        if self.x < 0:
            self.x = 0
        elif self.x >= 860:
            self.x = 680

    def action(self, action=1):
        if action == 0: ## move left
            self.move(-8)
        elif action == 2: ## move right
            self.move(8)