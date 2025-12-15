import pygame
import random
import math
from constants import *
from pipe import Pipe


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.animation_index = 0
        self.animation_speed = 0
        image1 = pygame.image.load('assets/Game Objects/yellowbird-downflap.png')
        image1 = pygame.transform.scale(image1, (image1.get_width() * 1.5, image1.get_height() * 1.5))
        image2 = pygame.image.load('assets/Game Objects/yellowbird-midflap.png')
        image2 = pygame.transform.scale(image2, (image2.get_width() * 1.5, image2.get_height() * 1.5))
        image3 = pygame.image.load('assets/Game Objects/yellowbird-upflap.png')
        image3 = pygame.transform.scale(image3, (image3.get_width() * 1.5, image3.get_height() * 1.5))
        self.images.append(image1)
        self.images.append(image2)
        self.images.append(image3)
        self.image = self.images[self.animation_index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.velocity = 0
        self.dead = False
        self.is_flapping = False
        self.decision = None
        self.fitness = 0.0
        self.time_alive = 0
        self.pipes_passed = 0
        self.weights = [
            random.uniform(-1, 1),
            random.uniform(-1, 1),
            random.uniform(-1, 1),
            random.uniform(-1, 1)
        ]

    def ground_collision(self):
        return bool(self.rect.bottom >= GROUND_LINE_Y)

    def sky_collision(self):
        return bool(self.rect.top < 0)

    def check_pipe_collision(self, pipe_group):
        return pygame.sprite.spritecollide(self, pipe_group, False)

    def jump(self):
        if not self.dead:
            self.velocity = -10
            self.is_flapping = True
            self.animation_index = 0

    def update(self, pipe_group=None):
        if not self.dead:
            is_colliding = self.ground_collision() or self.sky_collision()
            if pipe_group and self.check_pipe_collision(pipe_group):
                is_colliding = True
            if is_colliding:
                self.dead = True
                self.kill()

        if not self.dead:
            self.velocity += 0.5

            if self.velocity > 0:
                self.is_flapping = False

            if self.velocity > 10:
                self.velocity = 10
            self.rect.y += int(self.velocity)

            if pipe_group:
                self.time_alive += 1
                for pipe in pipe_group:
                    if isinstance(pipe, Pipe) and pipe.position == 0:
                        if self.rect.left > pipe.rect.right and not pipe.passed_by_bird:
                            self.pipes_passed += 1
                            pipe.passed_by_bird = True
                            break

            if self.ground_collision():
                self.rect.bottom = GROUND_LINE_Y
                self.dead = True
                self.kill()

            self.animation_speed += 1
            cd = 5
            if self.animation_speed > cd:
                self.animation_speed = 0
                self.animation_index += 1
                if self.animation_index >= len(self.images):
                    self.animation_index = 0
            self.image = self.images[self.animation_index]
            self.image = pygame.transform.rotate(self.images[self.animation_index], -self.velocity * 2)

        elif self.dead and self.rect.bottom < GROUND_LINE_Y:
            self.velocity += 0.5
            self.rect.y += int(self.velocity)
            if self.rect.bottom >= GROUND_LINE_Y:
                self.rect.bottom = GROUND_LINE_Y
                self.velocity = 0

    def sigmoid(self, x):
        if x < -500: return 0
        if x > 500: return 1
        return 1 / (1 + math.exp(-x))

    def get_inputs(self, pipe_group):
        next_pipe_pair = []

        pipe_sprites = pipe_group.sprites()
        if not pipe_sprites:
            return None

        for pipe in pipe_sprites:
            if pipe.rect.right > self.rect.left:
                if pipe.position == 1:
                    top_pipe = pipe
                    bottom_pipe = pipe_sprites[pipe_sprites.index(pipe) + 1]
                else:
                    bottom_pipe = pipe
                    top_pipe = pipe_sprites[pipe_sprites.index(pipe) - 1]

                next_pipe_pair = [top_pipe, bottom_pipe]
                break

        if not next_pipe_pair:
            return None

        top_pipe, bottom_pipe = next_pipe_pair

        i0 = self.rect.top - top_pipe.rect.bottom
        i1 = top_pipe.rect.left - self.rect.right
        i2 = bottom_pipe.rect.top - self.rect.bottom

        return [i0, i1, i2, 1]

    def think(self, pipe_group):
        inputs = self.get_inputs(pipe_group)
        if inputs is None or self.dead:
            return

        total = 0
        for w, i in zip(self.weights, inputs):
            total += w * i

        output = self.sigmoid(total)

        global FLAP_THRESHOLD

        if output > FLAP_THRESHOLD and self.velocity > 0 and not self.is_flapping:
            self.jump()

    def clone(self):
        clone = Bird(self.rect.x, self.rect.y)
        clone.weights = self.weights.copy()
        return clone

    def mutate(self, rate=0.2):
        self.weights = [w + random.uniform(-rate, rate) for w in self.weights]