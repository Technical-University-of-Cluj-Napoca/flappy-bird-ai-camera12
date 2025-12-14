import pygame
from constants import *
from bird import Bird
pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

bg = pygame.image.load('assets/Game Objects/background-day.png')
bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

base = pygame.image.load('assets/Game Objects/base.png')
base = pygame.transform.scale(base, (SCREEN_WIDTH + 30, 200))
base_width = base.get_width()

bird_group = pygame.sprite.Group()
faby= Bird(100, int(SCREEN_HEIGHT /2))
bird_group.add(faby)
scroll = 0
running = True

while running:
    clock.tick(FPS)

    screen.blit(bg, (0, 0))
    screen.blit(base, (scroll, 820))
    screen.blit(base, (scroll + base_width, 820))
    bird_group.draw(screen)
    bird_group.update()
    scroll -= SCROLL_SPEED
    if scroll <= -base_width:
        scroll = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()

pygame.quit()