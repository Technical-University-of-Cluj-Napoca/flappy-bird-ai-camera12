import pygame


class Button():
    def __init__(self, x, y, img):
        self.img = img
        self.rect = self.img.get_rect()
        self.rect.center = (x, y)
        self.button_pressed = False

    def draw(self, screen):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.button_pressed == False:
                self.button_pressed = True
                action = True

            if pygame.mouse.get_pressed()[0] == 0:
                self.button_pressed = False
        screen.blit(self.img, self.rect)
        return action
