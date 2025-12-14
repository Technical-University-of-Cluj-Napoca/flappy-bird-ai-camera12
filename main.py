import random

import pygame
import pygame_widgets
from pygments.lexers import q

from constants import *
from bird import Bird
from button import Button
from pipe import Pipe


pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

bg = pygame.image.load('assets/Game Objects/background-day.png')
bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

base = pygame.image.load('assets/Game Objects/base.png')
base = pygame.transform.scale(base, (SCREEN_WIDTH, 200))
base_width = base.get_width()

start_button_img = pygame.image.load('assets/Game Objects/start_btn.png').convert_alpha()
start_button_img = pygame.transform.scale(start_button_img, (start_button_img.width/2, start_button_img.height/2))
start_button = Button(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, start_button_img)

bird_group = pygame.sprite.Group()
faby= Bird(100, int(SCREEN_HEIGHT / 2))
bird_group.add(faby)

pipe_group = pygame.sprite.Group()
last_pipe = pygame.time.get_ticks()

scroll = 0
running = True
game_started = False
game_over = False


while running:
    clock.tick(FPS)
    screen.blit(bg, (0, 0))
    screen.blit(base, (scroll, 820))
    screen.blit(base, (scroll + base_width, 820))

    if not game_started and not game_over:
        if start_button.draw(screen):
            game_started = True

    bird_group.draw(screen)
    pipe_group.draw(screen)

    if game_started and not game_over:
        current_time = pygame.time.get_ticks()
        if current_time - last_pipe > PIPE_FREQUENCY:
            pipe_height = random.randint(-100, 100)
            bottom_pipe = Pipe(SCREEN_WIDTH, int(SCREEN_HEIGHT / 2) + pipe_height, 0)
            pipe_group.add(bottom_pipe)
            top_pipe = Pipe(SCREEN_WIDTH, int(SCREEN_HEIGHT/ 2) + pipe_height, 1)
            pipe_group.add(top_pipe)
            last_pipe = current_time

        bird_group.update()
        pipe_group.update()

        scroll -= SCROLL_SPEED
        if scroll <= -base_width:
            scroll = 0
    else:
        start_button.draw(screen)

    if faby.rect.bottom >= 810:
        game_started = False
        game_over = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and start_button.button_pressed == True and game_started == False and game_over == False:
            game_started = True
            start_button.button_pressed = False

    pygame.display.update()


pygame.quit()