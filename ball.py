import pygame

class ball:
    def __init__(self, x, y, img_path):
        self.x = x
        self.y = y
        self.img = pygame.image.load(img_path)
        self.x_change = 3
        self.y_change = 3
    
    def move(self):
        self.x += self.x_change
        self.y += self.y_change
        if self.x < 0 or self.x +20 >= 800:
            self.x_change = -self.x_change
        if self.y < 0:
            self.y_change = -self.y_change
    
    def slider_collision(self, slider):
        if 525 <= self.y + 10 <= 530:
            if slider.x - 20 <= self.x <= slider.x:
                self.x_change = -6
                self.y_change = -2

            elif slider.x + 1 <= self.x <= slider.x + 20:
                self.x_change = -5
                self.y_change = -3
            
            elif slider.x + 21 <= self.x <= slider.x + 50:
                self.x_change = -4
                self.y_change = -3

            elif slider.x + 51 <= self.x <= slider.x + 80:
                self.y_change = -1 * self.y_change

            elif slider.x + 81 <= self.x <= slider.x + 110:
                self.x_change = 4
                self.y_change = -3

            elif slider.x + 111 <= self.x <= slider.x + 130:
                self.x_change = 5
                self.y_change = -3
            
            elif slider.x + 131 <= self.x <= slider.x + 150:
                self.x_change = 6
                self.y_change = -2