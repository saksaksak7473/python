import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("My pygame")
clock = pygame.time.Clock()

running = True
    
class Wall:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = (255, 255, 255) 
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)       
          
class Player:
    def __init__(self, x, y):
        self.dx = 0
        self.dy = 0
        self.x = x
        self.y = y
        self.speed = 5
        self.color = (255, 255, 255)
        self.rect = pygame.Rect(self.x, self.y, 50, 50)
        
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.dx -= self.speed
        if keys[pygame.K_s]:
            self.dx += self.speed
        if keys[pygame.K_a]:
            self.dy -= self.speed
        if keys[pygame.K_d]:
            self.dy += self.speed
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
    
    def collision(self, wall):
        self.rect.x += self.dx
        if self.rect.colliderect(wall.rect):
            if self.dx > 0:
                self.rect.right = wall.rect.left
            elif self.dx < 0:
                self.rect.left = wall.rect.right

player = Player(275, 275)

walls = [
    Wall(400, 300, 50, 200),
    Wall(100, 100, 500, 50)
]              
            
while running:
    
    screen.fill((0, 0, 0))
    player.update()
    for wall in walls:
        player.collision(wall)
    player.draw(screen)
        
    for wall in walls:
        wall.draw(screen)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    pygame.display.flip()
    clock.tick(60)

pygame.quit()