# Importe o módulo Pygame para utilizar suas funcionalidades
import pygame
from pygame import mixer
from classes.game import Game
from classes.button import Button
import classes.utils as const

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()

# Carregue os sons do jogo
coin_effect = pygame.mixer.Sound('assets/audio/coin.wav')
coin_effect.set_volume(0.5)


pygame.mixer.music.load('assets/audio/music.wav')
pygame.mixer.music.play(-1, 0.0, 5000)

game = Game()


# Desenha uma grade na tela do jogo de 50x50 pixels
def draw_grid():
    for line in range(0, 20):
        pygame.draw.line(Game.screen, (255, 255, 255), (0, line * const.tile_size), (const.screen_width, line * const.tile_size))
        pygame.draw.line(Game.screen, (255, 255, 255), (line * const.tile_size, 0), (line * const.tile_size, const.screen_height))


restart_button = Button(const.screen_width // 2 - 50, const.screen_height // 2 + 100, const.restart_image)
start_button = Button(const.screen_width // 2 - 350, const.screen_height // 2, const.start_image)


while game.running:
    game.curr_menu.display_menu()
    game.game_loop()
