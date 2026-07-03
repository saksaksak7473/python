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
    
    def move(self, Maps, Frames, X, Y):
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
        doors = Maps[1][Y][X]
        for door in doors:
            if self.player.colliderect(door.new_door):
                self.player.x, self.player.y = 10, 10
                if dx > 0:
                    return X + 1, Y
                elif dx < 0:
                    return X - 1, Y
                
        for frame in Frames:
            if self.player.colliderect(frame):
                if dx > 0:
                    self.player.right = frame.left
                elif dx < 0:
                    self.player.left = frame.right
                    
        walls = Maps[0][Y][X]
        for wall in walls:
            if self.player.colliderect(wall.new_wall):
                if dx > 0:
                    self.player.right = wall.new_wall.left
                elif dx < 0:
                    self.player.left = wall.new_wall.right

        self.player.y += dy
        doors = Maps[1][Y][X]
        for door in doors:
            if self.player.colliderect(door.new_door):
                self.player.x, self.player.y = 10, 10
                if dy > 0:
                    return X, Y + 1
                elif dy < 0:
                    return X, Y - 1
                
        for frame in Frames:
            if self.player.colliderect(frame):
                if dy > 0:
                    self.player.bottom = frame.top
                elif dy < 0:
                    self.player.top = frame.bottom
                    
        walls = Maps[0][Y][X]
        for wall in walls:
            if self.player.colliderect(wall.new_wall):
                if dy > 0:
                    self.player.bottom = wall.new_wall.top
                elif dy < 0:
                    self.player.top = wall.new_wall.bottom

        return X, Y
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.player)
        
class Block:
    def __init__(self, x, y, w, h):
        self.new_wall = pygame.Rect(x, y, w, h)
        self.new_door = pygame.Rect(x, y, w, h)
        self.W_color = 'White'
        self.D_color = 'Red'
        
    def W_draw(self, screen):
        pygame.draw.rect(screen, self.W_color, self.new_wall)
        
    def D_draw(self, screen):
        pygame.draw.rect(screen, self.D_color, self.new_door)
        
Frames = [pygame.Rect(0, 0, 5, HEIGHT - 5), pygame.Rect(0, HEIGHT - 5, WIDTH - 5, 5), pygame.Rect(WIDTH - 5, 0, 5, HEIGHT), pygame.Rect(5, 0, WIDTH - 10, 5)]
        
Maps = [
    # Walls
    [
        [
            [Block(100, 100, 25, 300), Block(100, 100, 400, 25)], # Walls in Map 1
            [Block(200, 200, 400, 25), Block(200, 200, 25, 300)], # Walls in Map 2
            [Block(300, 300, 25, 300), Block(300, 300, 400, 25)] # Walls in Map 3
        ],
        [
            [Block(400, 400, 25, 300), Block(400, 400, 400, 25)], # Walls in Map 4
            [Block(500, 500, 400, 25), Block(500, 500, 25, 300)], # Walls in Map 5
            [Block(600, 400, 25, 300), Block(400, 400, 400, 25)] # Walls in Map 6
        ],
        [
            [Block(700, 300, 25, 300), Block(300, 300, 400, 25)], # Walls in Map 7
            [Block(600, 200, 400, 25), Block(200, 200, 25, 300)], # Walls in Map 8
            [Block(700, 100, 25, 300), Block(100, 100, 400, 25)] # Walls in Map 9
        ]
    ],
    # Doors
    [
        [
            [Block(350, HEIGHT - 5, 100, 5), Block(WIDTH - 5, 250, 5, 100)], # Doors in Map 1
            [Block(350, HEIGHT - 5, 100, 5), Block(WIDTH - 5, 250, 5, 100), Block(0, 250, 5, 100)], # Doors in Map 2
            [Block(0, 250, 5, 100), Block(350, HEIGHT - 5, 100, 5)] # Doors in Map 3
        ],
        [
            [Block(350, 0, 100, 5), Block(WIDTH - 5, 250, 5, 100), Block(350, HEIGHT - 5, 100, 5)], # Doors in Map 4
            [Block(350, HEIGHT - 5, 100, 5), Block(WIDTH - 5, 250, 5, 100), Block(0, 250, 5, 100), Block(350, 0, 100, 5)], # Doors in Map 5
            [Block(0, 250, 5, 100), Block(350, HEIGHT - 5, 100, 5), Block(350, 0, 100, 5)] # Doors in Map 6
        ],
        [
            [Block(350, 0, 100, 5), Block(WIDTH - 5, 250, 5, 100)], # Doors in Map 7
            [Block(350, 0, 100, 5), Block(0, 250, 5, 100), Block(WIDTH - 5, 250, 5, 100)], # Doors in Map 8
            [Block(0, 250, 5, 100), Block(350, 0, 100, 5)] # Doors in Map 9
        ]
    ]
]        

running = True
CurrentMapX = 0
CurrentMapY = 0

player = Player(10, 10, 25, 25)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
    # action
    CurrentMapX, CurrentMapY = player.move(Maps, Frames, CurrentMapX, CurrentMapY)
    
    # draw
    screen.fill((0, 0, 0))
    for frame in Frames:
        pygame.draw.rect(screen, (255, 255, 255), frame)
    player.draw(screen)
    for walls in Maps[0][CurrentMapY][CurrentMapX]:
            walls.W_draw(screen)
    for doors in Maps[1][CurrentMapY][CurrentMapX]:
        doors.D_draw(screen)
    
    pygame.display.flip()
    clock.tick(60)
    
pygame.quit()