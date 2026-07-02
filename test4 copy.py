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
        
    def move(self, walls , map_gen , entrances):
        keys = pygame.key.get_pressed()
        dx = 0
        if keys[pygame.K_d]:
            dx += self.speed
        if keys[pygame.K_a]:
            dx -= self.speed
        for entrance in entrances:
            if self.rect.colliderect(entrance.rect):
                tol = 30
                if abs(self.rect.bottom - entrance.rect.top) <= tol:
                    map_gen.switchMap("Down")
                elif abs(self.rect.top - entrance.rect.bottom) <= tol:
                    map_gen.switchMap("Top")
                elif abs(self.rect.right - entrance.rect.left) <= tol:
                    map_gen.switchMap("Right")
                elif abs(self.rect.left - entrance.rect.right) <= tol:
                    map_gen.switchMap("Left")
                self.rect.y = 100
                self.rect.x = 100
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
       self.Maps = [
           [
            # Map1: entrances = right, bottom
            # Walls: right entrance horizontal caps at (680,480)/(680,720)
            #        bottom entrance vertical posts at (280,700)/(520,700)
            {"Map1": [
                Wall(100, 200, 200, 50), Wall(100, 500, 400, 100), Wall(580, 0, 320, 500), Wall(580, 720, 220, 80),
                Wall(680, 480, 120, 20), Wall(680, 720, 120, 20), Wall(280, 700, 20, 100), Wall(520, 700, 20, 100)
            ]},
            # Map2: entrances = left, right, bottom
            # Walls: left entrance horizontal caps at (0,480)/(0,720)
            #        right entrance horizontal caps at (680,480)/(680,720)
            #        bottom entrance vertical posts at (280,700)/(520,700)
            {"Map2": [
                Wall(0, 720, 220, 80), Wall(580, 0, 500, 220), Wall(100, 200, 400, 50), Wall(100, 500, 400, 100), Wall(580, 0, 320, 500), Wall(580, 720, 300, 80),
                Wall(0, 480, 120, 20), Wall(0, 720, 120, 20), Wall(680, 480, 120, 20), Wall(680, 720, 120, 20), Wall(280, 700, 20, 100), Wall(520, 700, 20, 100)
            ]},
            # Map3: entrances = left, bottom
            # Walls: left entrance horizontal caps at (0,480)/(0,720)
            #        bottom entrance vertical posts at (280,700)/(520,700)
            {"Map3": [
                Wall(0, 720, 220, 80), Wall(100, 200, 200, 50), Wall(100, 500, 400, 100), Wall(580, 0, 320, 500), Wall(580, 720, 220, 80),
                Wall(0, 480, 120, 20), Wall(0, 720, 120, 20), Wall(280, 700, 20, 100), Wall(520, 700, 20, 100)
            ]}
           ],
           [
            # Map4: entrances = right, top, bottom
            # Walls: right entrance horizontal caps at (680,480)/(680,720)
            #        top entrance vertical posts at (280,0)/(520,0)
            #        bottom entrance vertical posts at (280,700)/(520,700)
            {"Map4": [
                Wall(100, 200, 200, 50), Wall(100, 500, 400, 100), Wall(580, 0, 320, 500), Wall(580, 720, 220, 80),
                Wall(680, 480, 120, 20), Wall(680, 720, 120, 20), Wall(280, 700, 20, 100), Wall(520, 700, 20, 100), Wall(280, 0, 20, 100), Wall(520, 0, 20, 100)
            ]},
            # Map5: entrances = left, right, top, bottom
            # Walls: left caps (0,480)/(0,720), right caps (680,480)/(680,720), top posts (280,0)/(520,0), bottom posts (280,700)/(520,700)
            {"Map5": [
                Wall(0, 720, 220, 80), Wall(100, 200, 200, 50), Wall(100, 500, 400, 100), Wall(580, 0, 320, 500), Wall(580, 720, 220, 80),
                Wall(0, 480, 120, 20), Wall(0, 720, 120, 20), Wall(680, 480, 120, 20), Wall(680, 720, 120, 20), Wall(280, 700, 20, 100), Wall(520, 700, 20, 100), Wall(280, 0, 20, 100), Wall(520, 0, 20, 100)
            ]},
            # Map6: entrances = left, top, bottom
            # Walls: left caps (0,480)/(0,720), top posts (280,0)/(520,0), bottom posts (280,700)/(520,700)
            {"Map6": [
                Wall(0, 720, 220, 80), Wall(100, 200, 200, 50), Wall(100, 500, 400, 100), Wall(580, 0, 320, 500), Wall(580, 720, 220, 80),
                Wall(0, 480, 120, 20), Wall(0, 720, 120, 20), Wall(280, 700, 20, 100), Wall(520, 700, 20, 100), Wall(280, 0, 20, 100), Wall(520, 0, 20, 100)
            ]}
           ],
           [
            # Map7: entrances = right, top
            # Walls: right caps (680,480)/(680,720), top posts (280,0)/(520,0)
            {"Map7": [
                Wall(100, 200, 200, 50), Wall(100, 500, 400, 100), Wall(580, 0, 320, 500), Wall(580, 720, 220, 80),
                Wall(680, 480, 120, 20), Wall(680, 720, 120, 20), Wall(280, 0, 20, 100), Wall(520, 0, 20, 100)
            ]},
            # Map8: entrances = left, right, top
            # Walls: left caps (0,480)/(0,720), right caps (680,480)/(680,720), top posts (280,0)/(520,0)
            {"Map8": [
                Wall(0, 720, 220, 80), Wall(100, 200, 200, 50), Wall(100, 500, 400, 100), Wall(580, 0, 320, 500), Wall(580, 720, 220, 80),
                Wall(0, 480, 120, 20), Wall(0, 720, 120, 20), Wall(680, 480, 120, 20), Wall(680, 720, 120, 20), Wall(280, 0, 20, 100), Wall(520, 0, 20, 100)
            ]},
            # Map9: entrances = left, top
            # Walls: left caps (0,480)/(0,720), top posts (280,0)/(520,0)
            {"Map9": [
                Wall(0, 720, 220, 80), Wall(100, 200, 200, 50), Wall(100, 500, 400, 100), Wall(580, 0, 320, 500), Wall(580, 720, 220, 80),
                Wall(0, 480, 120, 20), Wall(0, 720, 120, 20), Wall(280, 0, 20, 100), Wall(520, 0, 20, 100)
            ]}
           ]
       ]
       # normalize entrance locations so every entrance uses the same coords
       self.MapEntrance = [
           [
               {"Map1": [Wall(790,500,12,220), Wall(300,790,220,10)]},
               {"Map2": [Wall(0,500,10,220), Wall(790,500,12,220), Wall(300,790,220,10)]},
               {"Map3": [Wall(0,500,10,220), Wall(300,790,220,10)]}
           ],
           [
               {"Map4": [Wall(790,500,12,220), Wall(300,10,220,10), Wall(300,790,220,10)]},
               {"Map5": [Wall(0,500,10,220), Wall(790,500,12,220), Wall(300,10,220,10), Wall(300,790,220,10)]},
               {"Map6": [Wall(0,500,10,220), Wall(300,10,220,10), Wall(300,790,220,10)]}
           ],
           [
               {"Map7": [Wall(790,500,12,220), Wall(300,10,220,10)]},
               {"Map8": [Wall(0,500,10,220), Wall(790,500,12,220), Wall(300,10,220,10)]},
               {"Map9": [Wall(0,500,10,220), Wall(300,10,220,10)]}
           ]
       ]
       self.current_map = "Map1"
       self.v = [
           ["Map1","Map2","Map3"],
           ["Map4","Map5","Map6"],
           ["Map7","Map8","Map9"]
                 ]
       self.CurrentMapX = 0
       self.CurrentMapY = 0
    def switchMap(self , direction):
        rows = len(self.v)
        cols = len(self.v[0]) if rows > 0 else 0
        new_x = self.CurrentMapX
        new_y = self.CurrentMapY
        if direction == "Top":
            new_x = max(0, self.CurrentMapX - 1)
        elif direction == "Down":
            new_x = min(rows - 1, self.CurrentMapX + 1)
        elif direction == "Right":
            new_y = min(cols - 1, self.CurrentMapY + 1)
        elif direction == "Left":
            new_y = max(0, self.CurrentMapY - 1)
        self.CurrentMapX = new_x
        self.CurrentMapY = new_y
        self.current_map = self.v[self.CurrentMapX][self.CurrentMapY]
        print(self.current_map)
    def FindRowAndColumn(self):
        for i, row in enumerate(self.v):
            for j, name in enumerate(row):
                if name == self.current_map:
                    self.CurrentMapX = i
                    self.CurrentMapY = j
                    return
    def giveRowAndColumn(self):
        self.FindRowAndColumn()
        return (self.CurrentMapX , self.CurrentMapY)
            
player = Player(375.00, 275.00)
MainMap = MapGeneration()

while running:
    MainMap.FindRowAndColumn()
    rows , columns = MainMap.giveRowAndColumn()
    screen.fill((0, 0, 0))
    walls = MainMap.Maps[rows][columns][MainMap.current_map]
    entrances = MainMap.MapEntrance[rows][columns][MainMap.current_map]
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
            if event.key == pygame.K_SPACE:
                player.jump(True)
     
    pygame.display.flip()
    clock.tick(60)  # 10 FPS is also very choppy/laggy for movement

pygame.quit()
