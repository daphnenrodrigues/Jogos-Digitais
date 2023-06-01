import pygame
import classes.utils as const


class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        image = pygame.image.load('assets/image/exitLevel.png')
        self.image = pygame.transform.scale(image, (const.tile_size, int(const.tile_size * 1.5)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
