import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

class Player:
    def __init__(self, x, y, w, h):

        self.speed = 5
        self.gravity = 0
        self.jump_count = 2
        self.animations = {
            "idle" : [],
            "run" : [],
            "wall_impact" : []
        }
        for i in range(1, 7):
            frame = pygame.transform.smoothscale(pygame.image.load(f"idle/idle{i}.png").convert_alpha(), (w, h))
            self.animations["idle"].append(frame)
        for i in range(1, 9):
            frame = pygame.transform.smoothscale(pygame.image.load(f"walk/run{i}.png").convert_alpha(), (w, h))
            self.animations["run"].append(frame)
        for i in range(2, 5):
            frame = pygame.transform.smoothscale(pygame.image.load(f"wall_impact/wall_impact{i}.png").convert_alpha(), (w, h))
            self.animations["wall_impact"].append(frame)
        self.state = "idle"
        self.frame_index = 0
        self.ani_speed = 0
        self.flip = False
        self.frame = self.animations[self.state][self.frame_index]
        
        self.player = self.frame.get_rect(topleft = (x, y)) # Player Rect  <------------------
    
    def animate(self, screen):
        self.ani_speed += 1
        if self.frame_index >= len(self.animations[self.state]):
            self.frame_index = 0
        else:
            current_frame = self.animations[self.state][self.frame_index]
            if self.flip:
                self.frame = pygame.transform.flip(current_frame, True, False)
            else:
                self.frame = current_frame
            if self.ani_speed >= 10:
                self.ani_speed = 0
                self.frame_index += 1
            
        screen.blit(self.frame, self.player)
            
    
    def move(self, Maps, Frames, X, Y):
        dx = 0
        dv = 0
        self.gravity += 0.3
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LSHIFT]:
            dv += 5
        if keys[pygame.K_d]:
            dx += self.speed + dv
            self.flip = True
        if keys[pygame.K_a]:
            dx -= self.speed + dv
            self.flip = False
        if keys[pygame.K_s]:
            self.gravity = min(self.gravity + 1, 15)
        
        if dx != 0:
            self.state = "run"
        else:
            self.state = "idle"
        
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
                self.state = "wall_impact"
                if dx > 0:
                    self.player.right = frame.left
                elif dx < 0:
                    self.player.left = frame.right
                if self.player.right == frame.left or self.player.left == frame.right:
                    if self.gravity > 0:
                        self.gravity = min(self.gravity + 0.1, 1)
                    self.jump_count = 2
                    
        walls = Maps[0][Y][X]
        for wall in walls:
            if self.player.colliderect(wall.new_wall):
                self.state = "wall_impact"
                if dx > 0:
                    self.player.right = wall.new_wall.left
                elif dx < 0:
                    self.player.left = wall.new_wall.right
                if self.player.right == wall.new_wall.left or self.player.left == wall.new_wall.right:
                    if self.gravity > 0:
                        self.gravity = min(self.gravity + 0.1, 1)
                    self.jump_count = 2
                
        self.player.y += self.gravity    
        doors = Maps[1][Y][X]
        for door in doors:
            if self.player.colliderect(door.new_door):
                self.player.x, self.player.y = 10, 10
                if self.gravity > 0:
                    return X, Y + 1
                elif self.gravity < 0:
                    return X, Y - 1
                
        for frame in Frames:
            if self.player.colliderect(frame):
                if self.gravity > 0:
                    self.player.bottom = frame.top
                    self.gravity = 0
                    self.jump_count = 2
                elif self.gravity < 0:
                    self.player.top = frame.bottom
                    self.gravity = 0
                    
        walls = Maps[0][Y][X]
        for wall in walls:
            if self.player.colliderect(wall.new_wall):
                if self.gravity > 0:
                    self.player.bottom = wall.new_wall.top
                    self.gravity = 0
                    self.jump_count = 2
                elif self.gravity < 0:
                    self.player.top = wall.new_wall.bottom
                    self.gravity = 0
                    
        return X, Y

    def getJump(self, isJump):
        if isJump and self.jump_count > 0:
            self.gravity = -10
            self.jump_count -= 1

        
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
        
Frames = [
    pygame.Rect(0, 0, 5, HEIGHT - 5), 
    pygame.Rect(0, HEIGHT - 5, WIDTH - 5, 5), 
    pygame.Rect(WIDTH - 5, 0, 5, HEIGHT), 
    pygame.Rect(5, 0, WIDTH - 10, 5)
]
        
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

background = pygame.transform.smoothscale(pygame.image.load("Background.jpg").convert(), (800, 600))
background_rect = background.get_rect(topleft = (0, 0))
running = True
CurrentMapX = 0
CurrentMapY = 0

player = Player(10, 10, 75, 75)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.getJump(True)
        
    CurrentMapX, CurrentMapY = player.move(Maps, Frames, CurrentMapX, CurrentMapY)
    
    screen.fill((0, 0, 0))
    screen.blit(background, background_rect)
    player.animate(screen)
    
    for frame in Frames:
        pygame.draw.rect(screen, (255, 255, 255), frame)
    for walls in Maps[0][CurrentMapY][CurrentMapX]:
            walls.W_draw(screen)
    for doors in Maps[1][CurrentMapY][CurrentMapX]:
        doors.D_draw(screen)
    
    pygame.display.flip()
    clock.tick(60)
    
pygame.quit()