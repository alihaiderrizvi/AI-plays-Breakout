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

# slider
slider_img = pygame.image.load('assets/slider.png')
sliderX = 250
sliderY = 530
sliderX_change = 0

def slider(x,y):
    screen.blit(slider_img, (x, y))

#game loop
while is_running:

    #Set background color
    screen.fill((255, 255, 255)) # (Red, Green, Blue)

    for event in pygame.event.get():
        #check game quit
        if event.type == pygame.QUIT:
            is_running = False
        
        
        if event.type == pygame.KEYDOWN:
            #check left
            if event.key == pygame.K_LEFT:
                sliderX_change = -0.2
            
            #check left
            if event.key == pygame.K_RIGHT:
                sliderX_change = 0.2
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                sliderX_change = 0
        
    sliderX += sliderX_change
    
    #resetting position if slider goes out of screen
    if sliderX < 0:
        sliderX = 0
    elif sliderX >= 545:
        sliderX = 545
    
    slider(sliderX, sliderY) # display slider
    
    pygame.display.update() # updating screen