import pygame

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.animation_index = 0
        self.animation_speed = 0
        image1 = pygame.image.load('assets/Game Objects/yellowbird-downflap.png')
        image2 = pygame.image.load('assets/Game Objects/yellowbird-midflap.png')
        image3 = pygame.image.load('assets/Game Objects/yellowbird-upflap.png')
        self.images.append(image1)
        self.images.append(image2)
        self.images.append(image3)
        self.image = self.images[self.animation_index]
        self.rect = self.image.get_rect()
        self.rect.center=[x, y]

    def update(self):
        self.animation_speed += 1
        cd=5
        if self.animation_speed > cd:
            self.animation_speed = 0
            self.animation_index += 1
            if self.animation_index >= len(self.images):
                self.animation_index = 0
        self.image = self.images[self.animation_index]
