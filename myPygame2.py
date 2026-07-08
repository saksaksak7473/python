import pygame

pygame.init()

WIDTH, HEIGHT = 1280, 800

class Player(pygame.sprite.Sprite):
    def __init__(self, groups, x, y, w, h):
        super().__init__(groups)
        self.speed = 3
        self.image = pygame.transform.smoothscale(pygame.image.load("Character.png"), (w, h))
        self.rect = self.image.get_rect(midbottom = (x, y))
        
    def update(self):
        dirX = 0
        dirY = 0
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d] or keys[pygame.K_a]:
            dirX += keys[pygame.K_d] - keys[pygame.K_a]
        if keys[pygame.K_s] or keys[pygame.K_w]:
            dirY += keys[pygame.K_s] - keys[pygame.K_w]
        self.rect.x += dirX * self.speed
        self.rect.y += dirY * self.speed
        
player_sprite = pygame.sprite.Group()
player = Player(player_sprite, 100, 100, 50, 50)
        

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    # Draw  
    screen.fill((0, 0, 0))
    player_sprite.draw(screen)
    
    # Update
    player_sprite.update()
    pygame.display.flip()
    clock.tick(60)
    
pygame.quit()