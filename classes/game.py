import pygame
import pickle
from os import path
from classes.mainMenu import MainMenu
from classes.optionsMenu import OptionsMenu
from classes.creditsMenu import CreditsMenu
from classes.player import Player
from classes.healthBar import HealthBar
from classes.world import World
from classes.coin import Coin
import classes.utils as const


def draw_text(text, font, text_col, x, y):
    image = font.render(text, True, text_col)
    Game.screen.blit(image, (x, y))


# Função para resetar a fase
def reset_level(game):
    game.player.reset(100, const.screen_height - 130)
    game.enemy_group.empty()
    game.platform_group.empty()
    game.flood_water_group.empty()
    game.exit_group.empty()

    # Cria um objeto World com dados de mapa em 'world_data'
    if not path.exists(f'assets/level_data/level{game.level}_data'):
        quit()
    pickle_in = open(f'assets/level_data/level{game.level}_data', 'rb')
    world_data = pickle.load(pickle_in)
    world = World(world_data, game.enemy_group, game.platform_group, game.flood_water_group, game.coin_group, game.exit_group, game.screen)

    return world


class Game:
    # Crie uma janela do Pygame com as dimensões especificadas anteriormente
    screen = pygame.display.set_mode((const.screen_width, const.screen_height))
    clock = pygame.time.Clock()
    fps = 60

    def __init__(self):
        # Inicialize o Pygame para que possa ser utilizado
        pygame.init()
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
        # Defina a largura e a altura da tela do jogo
        self.display = pygame.Surface((const.screen_width, const.screen_height))
        # Carregue as imagens a partir do diretório especificado
        self.sun_image = pygame.image.load('assets/image/sun.png')
        self.background_image = pygame.image.load('assets/image/sky.png')
        #Defina o título da janela do jogo
        pygame.display.set_caption('SurviveNature')
        # Definido fonte.
        self.font = pygame.font.SysFont('Bauhaus 93', 70)
        self.font_score = pygame.font.SysFont('Bauhaus 93', 30)
        self.font_menu = 'assets/font/8-BIT WONDER.TTF'
        # Opções do menu
        self.main_menu = MainMenu(self)
        self.options = OptionsMenu(self)
        self.credits = CreditsMenu(self)
        self.curr_menu = self.main_menu
        #
        self.world = None
        self.enemy_group = pygame.sprite.Group()
        self.platform_group = pygame.sprite.Group()
        self.flood_water_group = pygame.sprite.Group()
        self.coin_group = pygame.sprite.Group()
        self.exit_group = pygame.sprite.Group()
        # Cria um objeto Player com posição inicial
        self.player = Player(100, const.screen_height - 130, self)
        self.vida = HealthBar((const.tile_size // 2) - 15, 15, self.player.lives)
        # Carregue os sons do jogo
        self.coin_effect = pygame.mixer.Sound('assets/audio/coin.wav')
        self.coin_effect.set_volume(0.5)
        #
        self.max_levels = 7
        self.game_over = 0
        self.main_menu = True
        self.level = 7
        self.score = 0

    def game_loop(self):
        self.world = reset_level(self)
        while self.playing:
            self.check_events()
            if self.START_KEY:
                self.playing = False

            Game.clock.tick(self.fps)

            # Carregue as imagens a partir do diretório especificado
            Game.screen.blit(self.background_image, (0, 0))
            Game.screen.blit(self.sun_image, (100, 100))

            if self.main_menu:
                self.main_menu = False
            else:
                # Desenha o mundo na tela
                self.world.draw()

                # Se o jogador estiver vivo
                if self.game_over == 0:
                    self.enemy_group.update()
                    self.platform_group.update()
                    # Atualizando a pontuação
                    # Verifica se o item foi coletado
                    print('player.lives = ' + str(self.player.lives))
                    if pygame.sprite.spritecollide(self.player, self.coin_group, True):
                        self.score += 1
                        self.coin_effect.play()
                    # Criando moeda fictícia para mostrar na pontuação
                    score_coin = Coin((const.tile_size // 2) + 5, 3.5 * (const.tile_size // 2))
                    self.coin_group.add(score_coin)
                    draw_text(' X ' + str(self.score), self.font_score, const.white, const.tile_size - 5, const.tile_size + 21)

                self.enemy_group.draw(Game.screen)
                self.platform_group.draw(Game.screen)
                self.flood_water_group.draw(Game.screen)
                self.coin_group.draw(Game.screen)
                self.exit_group.draw(Game.screen)
                self.vida.draw(Game.screen, self.player.lives)

                self.game_over = self.player.update(self.game_over)

                # Se o jogador perder uma vida
                if self.game_over == -1:
                    self.player.lives -= 1
                    if self.player.lives > 0:
                        self.world = reset_level(self)
                        self.game_over = 0
                    else:
                        score = 0
                        # if restart_button.draw():

                # Se o jogador ganhar a fase
                if self.game_over == 1:
                    # Resetar o jogo e ir para a proxima fase
                    self.level += 1
                    if self.level <= self.max_levels:
                        # Resetar fase
                        self.world = reset_level(self)
                        self.game_over = 0
                        self.player.score += score
                        score = 0
                    else:
                        draw_text('Você Ganhou!', self.font, const.blue, (const.screen_width // 2) - 200, const.screen_height // 2)
                        # Resetar o jogo
                        if const.restart_button.draw():
                            self.level = 1
                            # Resetar fase
                            self.world = reset_level(self)
                            self.game_over = 0
                            score = 0

            pygame.display.update()
            self.reset_keys()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False

    def draw_text(self, text, size, x, y, color):
        font = pygame.font.Font(self.font_menu, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)
