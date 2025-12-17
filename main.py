import pygame
from sys import exit
import components
from population import *
from config import *
from button import *
from images import *

pygame.init()
pygame.display.set_caption("Flappy bird")
clock = pygame.time.Clock()

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

def get_medal(score):
    if score > 40:
        return platinum_img
    elif score > 30:
        return gold_img
    elif score > 20:
        return silver_img
    elif score > 10:
        return bronze_img
    return None

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
    start_button = Button(win_width // 2, win_height // 2, start_img)
    restart_button = Button(win_width // 2, win_height // 2 + 80, restart_img)
    show_vision = False
    game_started = False
    mode = None
    mode_text = ""
    mode_text_timer = 0
    manual_and_dead = False
    population = None
    score = 0
    best_score = 0
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
                        mode_text = "Automatic mode selected"
                        mode_text_timer = 120
                    elif event.key == pygame.K_m:
                        mode = 'manual'
                        mode_text = "Manual mode selected"
                        mode_text_timer = 120

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
            if mode_text_timer > 0:
                font = pygame.font.SysFont(None, 36)
                text_surface = font.render(mode_text, True, (255, 255, 255))
                window.blit(
                    text_surface,
                    (win_width // 2 - text_surface.get_width() // 2, win_height - 180)
                )
                mode_text_timer -= 1
            pygame.display.flip()
            clock.tick(60)
            continue

        if not manual_and_dead:
            if pipes_spawn_time <= 0:
                generate_pipes()
                pipes_spawn_time = 200
            pipes_spawn_time -= 1

        for p in pipes:
            p.draw(window)
            if not manual_and_dead:
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
            if score > best_score:
                best_score = score
            if mode == 'manual':
                manual_and_dead = True
            else:
                pipes.clear()
                if population:
                    population.natural_selection()
                    score = 0

        draw_score(window, score, 20)

        if mode == 'manual' and manual_and_dead:
            game_over_rect = game_over_img.get_rect(center=(win_width // 2, win_height // 2 - 120))
            window.blit(game_over_img, game_over_rect)

            medal = get_medal(score)
            if medal:
                medal_rect = medal.get_rect(center=(win_width // 2, win_height // 2 - 40))
                window.blit(medal, medal_rect)

            font = pygame.font.SysFont(None, 30)
            score_text = font.render(f"Score: {score}", True, (255, 255, 255))
            best_text = font.render(f"Best: {best_score}", True, (255, 255, 255))
            window.blit(score_text, (win_width // 2 - score_text.get_width() // 2, restart_button.rect.centery - 90))
            window.blit(best_text, (win_width // 2 - best_text.get_width() // 2, restart_button.rect.centery - 70))

            if restart_button.draw(window):
                pipes.clear()
                population = Population(1)
                score = 0
                manual_and_dead = False


        pygame.display.flip()
        clock.tick(60)

main()
