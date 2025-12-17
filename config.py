import components
import pygame

SCREEN_HEIGHT = 720
SCREEN_WIDTH = 550
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
ground = components.Ground(SCREEN_WIDTH)
pipes = []