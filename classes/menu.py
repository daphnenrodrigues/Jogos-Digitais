import pygame
import classes.utils as const


class Menu:
    def __init__(self, game):
        self.game = game
        self.screen_width_mid, self.screen_height_mid = const.screen_width / 2, const.screen_height / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = - 100
        self.images = {'mist1': pygame.image.load('assets/animation/parallax/01_Mist.png').convert_alpha(),
                       'bushes2': pygame.image.load('assets/animation/parallax/02_Bushes.png').convert_alpha(),
                       'particles3': pygame.image.load('assets/animation/parallax/03_Particles.png').convert_alpha(),
                       'forest4': pygame.image.load('assets/animation/parallax/04_Forest.png').convert_alpha(),
                       'particles5': pygame.image.load('assets/animation/parallax/05_Particles.png').convert_alpha(),
                       'forest6': pygame.image.load('assets/animation/parallax/06_Forest.png').convert_alpha(),
                       'forest7': pygame.image.load('assets/animation/parallax/07_Forest.png').convert_alpha(),
                       'forest8': pygame.image.load('assets/animation/parallax/08_Forest.png').convert_alpha(),
                       'forest9': pygame.image.load('assets/animation/parallax/09_Forest.png').convert_alpha(),
                       'sky10': pygame.image.load('assets/animation/parallax/10_Sky.png').convert_alpha()}
        self.pos_images = {key: (0, 0) for key in self.images.keys()}
        self.vel_images = {key: 2 + (1 - n) * (2 / 9) for n, key in enumerate(self.images.keys(), 1)}
        # Carregue os sons do jogo
        self.menu_button = pygame.mixer.Sound('assets/audio/button_change.wav')
        self.menu_button.set_volume(0.5)

    def draw_background(self):
        # Efeito parallax
        for key in reversed(self.images.keys()):
            # Adiciona a rolagem em paralaxe aos planos de fundo
            rel_x = self.pos_images[key][0] % self.images[key].get_rect().width
            self.game.display.blit(self.images[key], (rel_x - self.images[key].get_rect().width, self.pos_images[key][1]))
            self.game.display.blit(self.images[key], (rel_x, self.pos_images[key][1]))
            # Move os planos de fundo
            self.pos_images[key] = (self.pos_images[key][0] - self.vel_images[key], self.pos_images[key][1])

    def draw_cursor(self):
        self.game.draw_text('*', 40, (self.cursor_rect.x - 100), self.cursor_rect.y, const.black)

    def blit_screen(self):
        self.game.screen.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()
