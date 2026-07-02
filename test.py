import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("My First Pygame")
clock = pygame.time.Clock()

running = True

while running:
    for event in pygame.event.get():
        # Player close the window
        if event.type == pygame.QUIT: 
            running = False
    
    screen.fill((0, 0, 0)) # screen background color
    pygame.display.flip() # Show the frame on screen
    clock.tick(60)

pygame.quit()