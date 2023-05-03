import pygame
from pygame.locals import *

pygame.init()

screen_width = 1000
screen_height = 1000

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('SurviveNature')

sun_image = pygame.image.load('assets/image/sun.png')
background_image = pygame.image.load('assets/image/sky.png')

run = True
while run:

    screen.blit(background_image, (0, 0))
    screen.blit(sun_image, (100, 100))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()