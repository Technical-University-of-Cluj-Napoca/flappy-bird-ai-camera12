import random
import pygame

from constants import *
from bird import Bird
from button import Button
from pipe import Pipe

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

#Images imports
bg = pygame.image.load('assets/Game Objects/background-day.png')
bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
base = pygame.image.load('assets/Game Objects/base.png')
base = pygame.transform.scale(base, (SCREEN_WIDTH, 200))
base_width = base.get_width()

start_button_img_original = pygame.image.load('assets/Game Objects/start_btn.png').convert_alpha()
btn_width = int(start_button_img_original.get_width() / 2)
btn_height = int(start_button_img_original.get_height() / 2)
btn_size = (btn_width, btn_height)
start_button_img = pygame.transform.scale(start_button_img_original, btn_size)
start_button = Button(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, start_button_img)
restart_button_img = pygame.image.load('assets/Game Objects/restart_btn.png').convert_alpha()
restart_button_img = pygame.transform.scale(restart_button_img, btn_size)
restart_button = Button(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, restart_button_img)
digits_imgs = []
for i in range(10):
    digit_img = pygame.image.load('assets/UI/Numbers/{i}.png'.format(i=i))
    digit_img = pygame.transform.scale(digit_img, (30, 40))
    digits_imgs.append(digit_img)


#Groups initialization
bird_group = pygame.sprite.Group()
faby= Bird(100, int(SCREEN_HEIGHT / 2))
bird_group.add(faby)
pipe_group = pygame.sprite.Group()
last_pipe = pygame.time.get_ticks()

clock = pygame.time.Clock()
scroll = 0
running = True
game_started = False
game_over = False
pass_pipe=False
score = 0

def draw_score(surface):
    score_str = str(score)
    digit_width = digits_imgs[0].get_width()
    total_width = len(score_str) * digit_width
    start_x = SCREEN_WIDTH/2 - (total_width / 2)
    for i, digit_char in enumerate(score_str):
        digit_index = int(digit_char)
        digit_img = digits_imgs[digit_index]
        pos_x = start_x + i * digit_width
        pos_y = 50
        surface.blit(digit_img, (pos_x, pos_y))
def reset_game():
    pipe_group.empty()
    faby.rect.x = 100
    faby.rect.y = int(SCREEN_HEIGHT / 2)
    global score
    score = 0
while running:
    clock.tick(FPS)
    screen.blit(bg, (0, 0))
    bird_group.draw(screen)
    pipe_group.draw(screen)
    screen.blit(base, (scroll, 820))
    screen.blit(base, (scroll + base_width, 820))

    #Score calculation
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right and pass_pipe == False:
            pass_pipe = True
        if pass_pipe:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False
    draw_score(screen)

    if not game_started and not game_over:
        if start_button.draw(screen):
            game_started = True

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

    elif game_over:
        if restart_button.draw(screen):
            game_over = False
            game_started = True
            reset_game()

    if faby.rect.bottom >= 810 or faby.rect.top < 0:
        game_started = False
        game_over = True
        faby.dead = True

    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False):
        game_started = False
        game_over = True
        faby.dead = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    pygame.display.update()


pygame.quit()