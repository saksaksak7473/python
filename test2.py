import pygame

pygame.init() # initializing pygame

screen = pygame.display.set_mode((800, 600)) # create screen
pygame.display.set_caption("My First Game!!")
clock = pygame.time.Clock()

dirt_block = pygame.image.load('dirt_block.jpg').convert_alpha()
# make the white background transparent
for x in range(dirt_block.get_width()):
    for y in range(dirt_block.get_height()):
        r, g, b, a = dirt_block.get_at((x, y))
        if r > 220 and g > 220 and b > 220:
            dirt_block.set_at((x, y), (255, 255, 255, 0))

pic_surf = pygame.transform.smoothscale(dirt_block, (50, 50))
player = pic_surf.get_rect(center = (375, 275))

walls = [
    pygame.Rect(500, 100, 50, 300),
    pygame.Rect(100, 400, 300, 50),
    pygame.Rect(200, 200, 100, 100)
]

text_font = pygame.font.Font(None, 50)
text_surf = text_font.render('Hello', False, (255, 255, 255))
text_rect = text_surf.get_rect(center = (400, 50))

running = True
speed = 5

while running:

    for event in pygame.event.get(): # this is calls Event Loops: Checking all user possible input
        if event.type == pygame.QUIT: # user Close the Window
            running = False

    keys = pygame.key.get_pressed()
    dx = 0
    dy = 0

    if keys[pygame.K_a]:
        dx -= speed
    if keys[pygame.K_d]:
        dx += speed
    if keys[pygame.K_w]:
        dy -= speed
    if keys[pygame.K_s]:
        dy += speed

    player.x += dx
    for wall in walls:
        if player.colliderect(wall):
            if dx > 0:
                player.right = wall.left
            elif dx < 0:
                player.left = wall.right

    player.y += dy
    for wall in walls:
        if player.colliderect(wall):
            if dy < 0:
                player.top = wall.bottom
            elif dy > 0:
                player.bottom = wall.top

    screen.fill((0, 0, 0))
    screen.blit(pic_surf, player)
    for wall in walls:
        pygame.draw.rect(screen, (255, 255, 255), wall)
    screen.blit(text_surf, text_rect)
    pygame.display.flip() # Display the frame on screen
    clock.tick(60) # frame rates

pygame.quit()