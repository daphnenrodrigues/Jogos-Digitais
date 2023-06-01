import pygame
import classes.utils as const


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        image = pygame.image.load('assets/image/coin.png')
        self.image = pygame.transform.scale(image, (const.tile_size // 2, const.tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
