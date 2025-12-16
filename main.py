import pygame
from sys import exit
import components
from population import *
from config import *
from button import *

pygame.init()
pygame.display.set_caption("Flappy bird")
clock = pygame.time.Clock()

digits_imgs = []
for i in range(10):
    digit_img = pygame.image.load(f'Assets/UI/Numbers/{i}.png').convert_alpha()
    digit_img = pygame.transform.scale(digit_img, (30, 40))
    digits_imgs.append(digit_img)

def generate_pipes():
    pipes.append(components.Pipes(win_width))

def draw_score(surface, score, y_pos):
    score_str = str(score)
    digit_width = digits_imgs[0].get_width()
    total_width = len(score_str) * digit_width
    start_x = win_width / 2 - (total_width / 2)
    for i, digit_char in enumerate(score_str):
        digit_img = digits_imgs[int(digit_char)]
        surface.blit(digit_img, (start_x + i * digit_width, y_pos))

class GroundScroll:
    def __init__(self, ground_obj):
        self.ground = ground_obj
        self.x = 0
        self.y = self.ground.y
        self.scroll_speed = 1

    def update(self):
        self.x -= self.scroll_speed
        if self.x <= -self.ground.base_img.get_width():
            self.x = 0

    def draw(self, window):
        window.blit(self.ground.base_img, (self.x, self.y))
        window.blit(self.ground.base_img, (self.x + self.ground.base_img.get_width(), self.y))

def main():
    pipes_spawn_time = 10
    bg = pygame.image.load('Assets/background-day.png').convert()
    bg = pygame.transform.scale(bg, (win_width, win_height))
    start_img = pygame.image.load('Assets/start_btn.png').convert_alpha()
    start_img = pygame.transform.scale(start_img, (start_img.get_width()//2, start_img.get_height()//2))
    start_button = Button(win_width // 2, win_height // 2, start_img)
    show_vision = False
    game_started = False
    mode = None
    population = None
    score = 0
    scrolling_ground = GroundScroll(ground)

    while True:
        window.blit(bg, (0, 0))
        scrolling_ground.update()
        scrolling_ground.draw(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    show_vision = not show_vision
                elif not game_started:
                    if event.key == pygame.K_a:
                        mode = 'auto'
                    elif event.key == pygame.K_m:
                        mode = 'manual'

        if not game_started:
            if start_button.draw(window):
                if mode is None:
                    mode = 'auto'
                if mode == 'manual':
                    population = Population(1)
                else:
                    population = Population(100)
                game_started = True

            font = pygame.font.SysFont(None, 30)
            text = font.render("Press A for Auto, M for Manual, then click Start", True, (255, 255, 255))
            window.blit(text, (win_width // 2 - text.get_width() // 2, win_height // 2 - 100))
            draw_score(window, score, 20)
            pygame.display.flip()
            clock.tick(60)
            continue

        if pipes_spawn_time <= 0:
            generate_pipes()
            pipes_spawn_time = 200
        pipes_spawn_time -= 1

        for p in pipes:
            p.draw(window)
            p.update()
            if p.off_screen:
                pipes.remove(p)
                score += 1

        if population and not population.extinct():
            if mode == 'manual' and pygame.mouse.get_pressed()[0]:
                for b in population.birds:
                    if b.alive:
                        b.bird_flap(manual=True)
            manual = (mode == 'manual')
            population.update_live_birds(draw_vision=show_vision, manual=manual)
        else:
            pipes.clear()
            if population:
                population.natural_selection()
                score = 0

        draw_score(window, score, 20)
        pygame.display.flip()
        clock.tick(60)

main()
