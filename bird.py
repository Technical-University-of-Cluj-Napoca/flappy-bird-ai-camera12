import pygame

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.animation_index = 0
        self.animation_speed = 0
        image1 = pygame.image.load('assets/Game Objects/yellowbird-downflap.png')
        image1 = pygame.transform.scale(image1, (image1.get_width() * 1.5, image1.get_height()*1.5))
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
        self.mouse_pressed=False

    def update(self):

        self.velocity += 0.5

        if self.velocity > 10:
            self.velocity = 10

        if self.rect.bottom < 810:
            self.rect.y += int(self.velocity)

        if pygame.mouse.get_pressed()[0] == 1 and self.mouse_pressed == False:
            self.mouse_pressed = True
            self.velocity = -10

        if pygame.mouse.get_pressed()[0] == 0 :
            self.mouse_pressed = False

        self.animation_speed += 1
        cd=5
        if self.animation_speed > cd:
            self.animation_speed = 0
            self.animation_index += 1
            if self.animation_index >= len(self.images):
                self.animation_index = 0
        self.image = self.images[self.animation_index]
        self.image = pygame.transform.rotate(self.images[self.animation_index], -self.velocity*2)

