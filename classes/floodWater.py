import pygame
import classes.utils as const


class FloodWater(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        image = pygame.image.load('assets/image/floodWater.png')
        self.image = pygame.transform.scale(image, (const.tile_size, const.tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y