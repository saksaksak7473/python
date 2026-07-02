import pygame

pygame.init()

screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()

class Player:
    def __init__(self, x, y):
        self.speed = 10
        self.gravity = 10
        self.jump_power = -15  # negative = upward
        self.max_fall_speed = 20
        self.on_ground = False
        self.color = (255, 255, 255)
        self.rect = pygame.Rect(x, y, 50, 50)
        self.jumpcount = 2
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        
    def move(self, walls , Map , entrances):
        keys = pygame.key.get_pressed()
        dx = 0
        if keys[pygame.K_d]:
            dx += self.speed
        if keys[pygame.K_a]:
            dx -= self.speed
        for entrance in entrances:
            if self.rect.colliderect(entrance.rect):
                self.rect.x = 100
                self.rect.y = 100
                Map.switchMap(entrance)
        self.rect.x += dx
        
        for wall in walls:         
            if self.rect.colliderect(wall.rect):
                if dx > 0:
                    self.rect.right = wall.rect.left
                elif dx < 0:
                    self.rect.left = wall.rect.right

        # jump
        # fast fall / drop down while held
        if keys[pygame.K_s] and not self.on_ground:
            self.gravity = self.max_fall_speed
        # gravity
        self.rect.y += self.gravity
        self.gravity = min(self.gravity + 0.5, self.max_fall_speed)

        self.on_ground = False
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if self.gravity > 0:
                    self.rect.bottom = wall.rect.top
                    self.on_ground = True
                    self.jumpcount = 2
                    self.gravity = 0
                elif self.gravity < 0:
                    self.rect.top = wall.rect.bottom
                    self.gravity = 0
    def jump(self, Jump):
        if Jump and self.jumpcount > 0:
            self.gravity = self.jump_power
            self.on_ground = False
            self.jumpcount -= 1

class Wall:
    def __init__(self, x, y, w, h):
        self.wall = (255, 0, 255)
        self.entrance = (0 , 50  , 0)
        self.rect = pygame.Rect(x, y, w, h)

    def draw1(self, screen):
        pygame.draw.rect(screen, self.wall, self.rect)
        
    def draw2(self , screen):
        pygame.draw.rect(screen, self.entrance, self.rect)

running = True
class MapGeneration:
    def __init__(self):
       self.Maps = {}
       self.Maps["Map1"] = [Wall(100, 200, 200, 50), Wall(100, 500, 400, 100) , Wall(580,0,320,500) , Wall(580,720,220,80)]
       self.Maps["Map2"] = [Wall(0,720,220,80),Wall(100, 200, 200, 50), Wall(100, 500, 400, 100) , Wall(580,0,320,500) , Wall(580,720,220,80)]
       self.Maps["Map3"] = [Wall(0,720,220,80),Wall(100, 200, 200, 50), Wall(100, 500, 400, 100) , Wall(580,0,320,500) , Wall(580,720,220,80)]
       self.current_map = "Map1"
       self.MapEntrance = {}
       self.MapEntrance["Map1"] = [Wall(790,500,12,220)]
       self.MapEntrance["Map2"] = [Wall(0,500,10,220),Wall(790,500,15,220)]
       self.MapEntrance["Map3"] = [Wall(0,500,15,220)]
       self.v = []
       for Map in self.Maps.keys():
           self.v.append(Map)
    def switchMap(self , Entrance):
        index = 0
        while(self.MapEntrance[self.current_map][index] != Entrance):
            index += 1
            
        if index == 1:
            self.current_map = self.v[self.v.index(self.current_map) + index]
            print(self.current_map)
        elif self.current_map == "Map1":
            self.current_map = self.v[self.v.index(self.current_map) + 1]
            print(self.current_map)
        elif index == 0 and self.current_map != "Map1":
            self.current_map = self.v[self.v.index(self.current_map) - 1]
            print(self.current_map)

            
        
                        
                        
                
                        
       
       
    
    

player = Player(375.00, 275.00)
MainMap = MapGeneration()
while running:
    screen.fill((0, 0, 0))
    walls = MainMap.Maps[MainMap.current_map]
    entrances = MainMap.MapEntrance[MainMap.current_map]
    player.move(walls , MainMap , entrances)
    player.draw(screen)
    for wall in walls:
        wall.draw1(screen)
    for entrance in entrances:
        entrance.draw2(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                Jump = True
                player.jump(Jump)
     
    pygame.display.flip()
    clock.tick(60)  # 10 FPS is also very choppy/laggy for movement

pygame.quit()
