import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

player = pygame.Rect(100, 100, 50, 50)

walls = [
    pygame.Rect(300, 100, 50, 300),
    pygame.Rect(100, 350, 400, 50),
]

speed = 5
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
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

    # Move left/right first
    player.x += dx
    for wall in walls:
        if player.colliderect(wall):
            if dx > 0:
                player.right = wall.left
            elif dx < 0:
                player.left = wall.right

    # Then move up/down
    player.y += dy
    for wall in walls:
        if player.colliderect(wall):
            if dy > 0:
                player.bottom = wall.top
            elif dy < 0:
                player.top = wall.bottom

    screen.fill((0, 0, 0))

    pygame.draw.rect(screen, (255, 255, 255), player)
    for wall in walls:
        pygame.draw.rect(screen, (0, 150, 0), wall)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()