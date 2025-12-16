import pygame
import random


class Ground:
    ground_level = 600
    base_img = pygame.image.load('Assets/base.png')
    base_img = pygame.transform.scale(base_img, (550, 120))

    def __init__(self, win_width):
        self.win_width = win_width
        self.x = 0
        self.y = Ground.ground_level
        self.rect = pygame.Rect(self.x, self.y, win_width, 5)
        self.scroll_speed = 1  # same as pipe speed

    def update(self):
        self.x -= self.scroll_speed
        if self.x <= -self.base_img.get_width():
            self.x = 0

    def draw(self, window):
        window.blit(self.base_img, (self.x, self.y))
        window.blit(self.base_img, (self.x + self.base_img.get_width(), self.y))


class Pipes:
    width = 50
    opening = 130
    bottom_pipe_img = pygame.image.load('Assets/pipe-green.png')
    bottom_pipe_img = pygame.transform.scale(bottom_pipe_img, (width, bottom_pipe_img.get_height()))
    top_pipe_img = pygame.transform.rotate(bottom_pipe_img, 180)
    def __init__(self, win_width):
        self.x = win_width
        self.bottom_height = random.randint(10, 300)
        self.top_height = Ground.ground_level - self.bottom_height - self.opening
        self.bottom_rect, self.top_rect = pygame.Rect(0, 0, 0, 0), pygame.Rect(0, 0, 0, 0)
        self.passed = False
        self.off_screen = False

    def draw(self, window):
        bottom_pipe_surface = pygame.transform.scale(self.bottom_pipe_img, (self.width, self.bottom_height))
        bottom_y = Ground.ground_level - self.bottom_height
        window.blit(bottom_pipe_surface, (self.x, bottom_y))
        self.bottom_rect = bottom_pipe_surface.get_rect(topleft=(self.x, bottom_y))
        top_pipe_surface = pygame.transform.scale(self.top_pipe_img, (self.width, self.top_height))
        top_y = 0
        window.blit(top_pipe_surface, (self.x, top_y))
        self.top_rect = top_pipe_surface.get_rect(topleft=(self.x, top_y))

    def update(self):
        self.x -= 1
        if self.x + Pipes.width <= 50:
            self.passed = True
        if self.x <= -self.width:
            self.off_screen = True
