import pygame
import classes.utils as const


class HealthBar(pygame.sprite.Sprite):
    def __init__(self, x, y, player_lives):
        pygame.sprite.Sprite.__init__(self)
        self.images_live = []
        for num in range(0, 6):
            image_live = pygame.image.load(f'assets/animation/health/coracao{num}.png')
            image_live = pygame.transform.scale(image_live, (const.tile_size * 2.9, const.tile_size))
            self.images_live.append(image_live)
        self.image = self.images_live[player_lives]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, screen, lives):
        self.image = self.images_live[lives]
        screen.blit(self.image, self.rect)
        #pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)
