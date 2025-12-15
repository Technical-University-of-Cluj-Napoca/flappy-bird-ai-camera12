import random
import pygame
from constants import *
from bird import Bird
from button import Button
from pipe import Pipe

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

font = pygame.font.Font(None, 40)

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
start_button = Button(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, start_button_img)

restart_button_img = pygame.image.load('assets/Game Objects/restart_btn.png').convert_alpha()
restart_button_img = pygame.transform.scale(restart_button_img, btn_size)
restart_button = Button(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, restart_button_img)

digits_imgs = []
for i in range(10):
    digit_img = pygame.image.load(f'assets/UI/Numbers/{i}.png')
    digit_img = pygame.transform.scale(digit_img, (30, 40))
    digits_imgs.append(digit_img)

class Species:
    def __init__(self, representative):
        self.representative = representative
        self.birds = [representative]
        self.fitness = 0.0

class Population:
    def __init__(self, size):
        self.birds = [Bird(100, int(SCREEN_HEIGHT / 2)) for _ in range(size)]
        self.size = size
        self.species = []
        self.generation = 1

    def update_live_birds(self, pipe_group):
        for bird in self.birds:
            if not bird.dead:
                bird.think(pipe_group)
                bird.update(pipe_group)

    def extiction(self):
        return all(bird.dead for bird in self.birds)

    def weight_difference(self, bird_a, bird_b):
        return sum(abs(wa - wb) for wa, wb in zip(bird_a.weights, bird_b.weights))

    def speciate(self):
        self.species = []
        for bird in self.birds:
            found_species = False
            for species in self.species:
                if self.weight_difference(bird, species.representative) < SPECIES_THRESHOLD:
                    species.birds.append(bird)
                    found_species = True
                    break
            if not found_species:
                self.species.append(Species(bird))

    def calculate_fitness(self):
        for bird in self.birds:
            bird.fitness = bird.time_alive + (bird.pipes_passed ** 2) * 100
        for species in self.species:
            total = sum(b.fitness for b in species.birds)
            species.fitness = total / len(species.birds)

    def sort_species(self):
        self.species.sort(key=lambda s: s.fitness, reverse=True)
        for species in self.species:
            species.birds.sort(key=lambda b: b.fitness, reverse=True)

    def next_generation(self):
        new_birds = []

        for species in self.species:
            champion = species.birds[0]
            new_birds.append(champion.clone())

        species_weights = [s.fitness for s in self.species]
        if sum(species_weights) == 0:
            species_weights = [1] * len(self.species)

        while len(new_birds) < self.size:
            species = random.choices(self.species, weights=species_weights, k=1)[0]
            breedable_birds = species.birds
            parent_weights = [b.fitness for b in breedable_birds]
            if sum(parent_weights) == 0:
                parent_weights = [1] * len(breedable_birds)
            parent = random.choices(breedable_birds, weights=parent_weights, k=1)[0]
            child = parent.clone()
            child.mutate(rate=0.5)
            new_birds.append(child)

        self.birds = new_birds
        for bird in self.birds:
            bird.rect.x = 100
            bird.rect.y = int(SCREEN_HEIGHT / 2)
            bird.dead = False
            bird.velocity = 0
            bird.animation_index = 0
            bird.time_alive = 0
            bird.pipes_passed = 0
            bird.is_flapping = False

        bird_group.empty()
        for bird in self.birds:
            bird_group.add(bird)

        self.generation += 1

population = Population(POPULATION_SIZE)
bird_group = pygame.sprite.Group()
for bird in population.birds:
    bird_group.add(bird)

pipe_group = pygame.sprite.Group()
last_pipe = pygame.time.get_ticks()

clock = pygame.time.Clock()
scroll = 0
running = True
game_started = False
game_over = False
score = 0
mode = 1

def draw_score(surface, text, y_pos):
    score_str = str(text)
    digit_width = digits_imgs[0].get_width()
    total_width = len(score_str) * digit_width
    start_x = SCREEN_WIDTH / 2 - (total_width / 2)
    for i, digit_char in enumerate(score_str):
        digit_img = digits_imgs[int(digit_char)]
        surface.blit(digit_img, (start_x + i * digit_width, y_pos))

def reset_game():
    pipe_group.empty()

while running:
    clock.tick(FPS)
    screen.blit(bg, (0, 0))
    bird_group.draw(screen)
    pipe_group.draw(screen)
    screen.blit(base, (scroll, 820))
    screen.blit(base, (scroll + base_width, 820))

    if not game_started and not game_over:
        if start_button.draw(screen):
            game_started = True

    if game_started and not game_over:
        current_time = pygame.time.get_ticks()
        if current_time - last_pipe > PIPE_FREQUENCY:
            pipe_height = random.randint(-100, 100)
            bottom_pipe = Pipe(SCREEN_WIDTH, int(SCREEN_HEIGHT / 2) + pipe_height, 0)
            top_pipe = Pipe(SCREEN_WIDTH, int(SCREEN_HEIGHT / 2) + pipe_height, 1)
            pipe_group.add(bottom_pipe)
            pipe_group.add(top_pipe)
            last_pipe = current_time

        if mode == 1:
            population.update_live_birds(pipe_group)

            live_birds = [b for b in population.birds if not b.dead]
            if live_birds:
                score = max(b.pipes_passed for b in live_birds)
            draw_score(screen, score, 50)

            gen_text = font.render(f"Gen: {population.generation}", True, (0, 0, 0))
            screen.blit(gen_text, (SCREEN_WIDTH / 2 - gen_text.get_width() / 2, 10))

        pipe_group.update()

        for bird in population.birds:
            if bird.dead and bird in bird_group:
                bird_group.remove(bird)

        if population.extiction():
            population.calculate_fitness()
            population.speciate()
            population.sort_species()
            population.next_generation()
            score = 0
            reset_game()

        scroll -= SCROLL_SPEED
        if scroll <= -base_width:
            scroll = 0

    elif game_over:
        if restart_button.draw(screen):
            game_over = False
            game_started = True
            reset_game()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()

pygame.quit()
