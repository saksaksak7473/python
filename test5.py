import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

class Player:
    def __init__(self, x, y, w, h):
        self.player = pygame.Rect(x, y, w, h)
        self.color = 'Blue'
        self.speed = 5
    
    def move(self, Maps, Frames, index):
        dx = 0
        dy = 0
        dv = 0
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LSHIFT]:
            dv += 5
        if keys[pygame.K_d]:
            dx += self.speed + dv
        if keys[pygame.K_a]:
            dx -= self.speed + dv
        if keys[pygame.K_w]:
            dy -= self.speed + dv
        if keys[pygame.K_s]:
            dy += self.speed + dv
        
        self.player.x += dx
        for doors in Maps[1][index]:
            if self.player.colliderect(doors.new_door):
                self.player.x, self.player.y = 10, 10
                if dx > 0:
                    return index + 1
                elif dx < 0:
                    return index - 1
        for frame in Frames:
            if self.player.colliderect(frame):
                if dx > 0:
                    self.player.right = frame.left
                elif dx < 0:
                    self.player.left = frame.right
        for walls in Maps[0][index]:
            if self.player.colliderect(walls.new_wall):
                if dx > 0:
                    self.player.right = walls.new_wall.left
                elif dx < 0:
                    self.player.left = walls.new_wall.right

        self.player.y += dy
        for doors in Maps[1][index]:
            if self.player.colliderect(doors.new_door):
                self.player.x, self.player.y = 10, 10
                if dy > 0:
                    return index + 1
                elif dy < 0:
                    return index - 1
        for frame in Frames:
            if self.player.colliderect(frame):
                if dy > 0:
                    self.player.bottom = frame.top
                elif dy < 0:
                    self.player.top = frame.bottom
        for walls in Maps[0][index]:
            if self.player.colliderect(walls.new_wall):
                if dy > 0:
                    self.player.bottom = walls.new_wall.top
                elif dy < 0:
                    self.player.top = walls.new_wall.bottom

        return index
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.player)
        
class Block:
    def __init__(self, x, y, w, h):
        self.new_wall = pygame.Rect(x, y, w, h)
        self.new_door = pygame.Rect(x, y, w, h)
        self.W_color = 'White'
        self.D_color = 'Green'
        
    def W_draw(self, screen):
        pygame.draw.rect(screen, self.W_color, self.new_wall)
        
    def D_draw(self, screen):
        pygame.draw.rect(screen, self.D_color, self.new_door)
        
Frames = [pygame.Rect(0, 0, 5, HEIGHT - 5), pygame.Rect(0, HEIGHT - 5, WIDTH - 5, 5), pygame.Rect(WIDTH - 5, 0, 5, HEIGHT), pygame.Rect(5, 0, WIDTH - 10, 5)]
        
Maps = [
    # Walls
    [
        [Block(100, 100, 25, 300), Block(200, 300, 400, 25)],
        [Block(200, 500, 400, 25), Block(400, 200, 25, 300)]
    ],
    # Doors
    [
        [Block(350, HEIGHT - 5, 100, 5), Block(WIDTH - 5, 250, 5, 100)],
        [Block(350, HEIGHT - 5, 100, 5), Block(WIDTH - 5, 250, 5, 100), Block(0, 250, 5, 100)]
    ]
]        

running = True
CurrentMap = 0

player = Player(10, 10, 25, 25)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            pass
    # action
    CurrentMap = player.move(Maps, Frames, CurrentMap)
    
    # draw
    screen.fill((0, 0, 0))
    for frame in Frames:
        pygame.draw.rect(screen, (255, 255, 255), frame)
    player.draw(screen)
    for walls in Maps[0][CurrentMap]:
        walls.W_draw(screen)
    for doors in Maps[1][CurrentMap]:
        doors.D_draw(screen)
    
    pygame.display.flip()
    clock.tick(60)
    
pygame.quit()