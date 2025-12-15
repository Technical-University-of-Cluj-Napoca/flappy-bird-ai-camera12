import pygame
from constants import *

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, pos):
        pygame.sprite.Sprite.__init__(self)
        original_image = pygame.image.load(
            'assets/Game Objects/pipe-green.png'
        ).convert_alpha()
        width = original_image.get_width()
        self.image = pygame.transform.scale(original_image, (width * 1.5, 600))
        self.rect = self.image.get_rect()
        if pos == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(PIPE_GAP / 2)]
        elif pos == 0:
            self.rect.topleft = [x, y + int(PIPE_GAP / 2)]

    def update(self):
        self.rect.x -= SCROLL_SPEED
        if self.rect.right < 0:
            self.kill()

