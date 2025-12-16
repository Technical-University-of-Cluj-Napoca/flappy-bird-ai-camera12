import brain
import random
import pygame
import config


class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.animation_index = 0
        self.animation_speed = 0
        image1 = pygame.image.load('Assets/yellowbird-downflap.png')
        image2 = pygame.image.load('Assets/yellowbird-midflap.png')
        image3 = pygame.image.load('Assets/yellowbird-upflap.png')
        self.images.append(image1)
        self.images.append(image2)
        self.images.append(image3)
        self.image = self.images[self.animation_index]
        self.x, self.y = 50, 200
        self.rect = self.image.get_rect()
        self.color = random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)
        self.vel = 0
        self.flap = False
        self.alive = True
        self.lifespan = 0

        # AI
        self.decision = None
        self.vision = [0.5, 1, 0.5]
        self.fitness = 0
        self.inputs = 3
        self.brain = brain.Brain(self.inputs)
        self.brain.generate_net()

    def draw(self, window):
        window.blit(self.image, self.rect)

    def ground_collision(self, ground):
        return pygame.Rect.colliderect(self.rect, ground)

    def sky_collision(self):
        return bool(self.rect.y < 30)

    def pipe_collision(self):
        for p in config.pipes:
            return pygame.Rect.colliderect(self.rect, p.top_rect) or pygame.Rect.colliderect(self.rect, p.bottom_rect)

    def update(self, ground):
        if not (self.ground_collision(ground) or self.pipe_collision()):
            self.vel += 0.25
            self.rect.y += self.vel
            if self.vel > 5:
                self.vel = 5
            self.lifespan += 1
        else:
            self.alive = False
            self.flap = False
            self.vel = 0

        if self.vel >= 3:
            self.flap = False

        self.animation_speed += 1
        cd = 5
        if self.animation_speed > cd:
            self.animation_speed = 0
            self.animation_index += 1
            if self.animation_index >= len(self.images):
                self.animation_index = 0
        self.image = self.images[self.animation_index]
        self.image = pygame.transform.rotate(self.images[self.animation_index], -self.vel * 3)

    def bird_flap(self, manual = False):
        if not self.sky_collision():
            if manual:
                self.vel = -4
            else:
                if not self.flap:
                    self.flap = True
                    self.vel = -5

    @staticmethod
    def closest_pipe():
        for p in config.pipes:
            if not p.passed:
                return p

    # AI related functions
    def look(self, draw_lines = False):
        if config.pipes:
            self.vision[0] = max(0, self.rect.center[1] - self.closest_pipe().top_rect.bottom) / 500
            self.vision[1] = max(0, self.closest_pipe().x - self.rect.center[0]) / 500
            self.vision[2] = max(0, self.closest_pipe().bottom_rect.top - self.rect.center[1]) / 500

            if draw_lines:
                pygame.draw.line(config.window, self.color, self.rect.center,(self.rect.center[0], config.pipes[0].top_rect.bottom))
                pygame.draw.line(config.window, self.color, self.rect.center,(config.pipes[0].x, self.rect.center[1]))
                pygame.draw.line(config.window, self.color, self.rect.center,(self.rect.center[0], config.pipes[0].bottom_rect.top))

    def think(self):
        self.decision = self.brain.feed_forward(self.vision)
        if self.decision > 0.73:
            self.bird_flap()

    def calculate_fitness(self):
        self.fitness = self.lifespan

    def clone(self):
        clone = Bird()
        clone.fitness = self.fitness
        clone.brain = self.brain.clone()
        clone.brain.generate_net()
        return clone











