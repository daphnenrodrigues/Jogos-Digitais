# Importe o módulo Pygame para utilizar suas funcionalidades
import pygame
import pickle
from os import path
from pygame import mixer

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()

# Defina as variáveis do jogo
tile_size = 50
game_over = 0
main_menu = True
level = 7
max_levels = 7
score = 0

# Definindo cores
white = (255, 255, 255)
blue = (0, 0, 255)

# Carregue as imagens a partir do diretório especificado
sun_image = pygame.image.load('assets/image/sun.png')
background_image = pygame.image.load('assets/image/sky.png')
restart_image = pygame.image.load('assets/image/restart_button.png')
start_image = pygame.image.load('assets/image/start_button.png')

# Carregue os sons do jogo
pygame.mixer.music.load('assets/audio/music.wav')
pygame.mixer.music.play(-1, 0.0, 5000)
coin_effect = pygame.mixer.Sound('assets/audio/coin.wav')
coin_effect.set_volume(0.5)
jump_effect = pygame.mixer.Sound('assets/audio/jump.wav')
jump_effect.set_volume(0.5)
game_over_effect = pygame.mixer.Sound('assets/audio/game_over.wav')
game_over_effect.set_volume(0.5)


# Desenha uma grade na tela do jogo de 50x50 pixels
def draw_grid():
    for line in range(0, 20):
        pygame.draw.line(Game.screen, (255, 255, 255), (0, line * tile_size), (Game.screen_width, line * tile_size))
        pygame.draw.line(Game.screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, Game.screen_height))


def draw_text(text, font, text_col, x, y):
    image = font.render(text, True, text_col)
    Game.screen.blit(image, (x, y))


# Função para resetar a fase
def reset_level(level):
    player.reset(100, Game.screen_height - 130)
    enemy_group.empty()
    platform_group.empty()
    flood_water_group.empty()
    exit_group.empty()

    # Cria um objeto World com dados de mapa em 'world_data'
    if path.exists(f'assets/level_data/level{level}_data'):
        pickle_in = open(f'assets/level_data/level{level}_data', 'rb')
        world_data = pickle.load(pickle_in)
    world = World(world_data)

    return world


class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False

        # Pegando a posição do mouse
        pos = pygame.mouse.get_pos()

        # Verificar as condições de clicar e se ele está em cima do botão
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # Adicionar botão na tela
        Game.screen.blit(self.image, self.rect)

        return action


class Player:
    def __init__(self, x, y):
        self.images_right = None
        self.images_left = None
        self.counter = None
        self.image = None
        self.dead_image = None
        self.index = None
        self.rect = None
        self.width = None
        self.height = None
        self.vel_y = None
        self.jumped = None
        self.direction = None
        self.in_air = None
        self.reset(x, y)
        self.lives = 5
        self.score = 0

    def update(self, game_over):
        dx = 0
        dy = 0
        walk_cooldown = 5
        col_thresh = 20

        if game_over == 0:
            # Verifica se alguma tecla foi pressionada
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False:
                jump_effect.play()
                self.vel_y = -15
                self.jumped = True
            if not key[pygame.K_SPACE]:
                self.jumped = False
            if key[pygame.K_LEFT]:
                dx -= 5
                self.counter += 1
                self.direction = -1
            if key[pygame.K_RIGHT]:
                dx += 5
                self.counter += 1
                self.direction = 1
            if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
                self.counter = 0
                self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            # Animação
            if self.counter > walk_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            # Adiciona a gravidade à velocidade vertical do jogador e limita em 10
            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y

            # Adicionando colisão
            self.in_air = True
            for tile in world.tile_list:
                # Verificando colisão no eixo x
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                # Verificando colisão no eixo y
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    # Verificando se abaixo do solo, ou seja, pulando
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    # Verificando se está acima do solo, ou seja, caindo
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.in_air = False

            # Adicionando colisão com os inimigos
            if pygame.sprite.spritecollide(self, enemy_group, False):
                game_over = -1
                game_over_effect.play()

            # Adicionando colisão com a água-suja
            if pygame.sprite.spritecollide(self, flood_water_group, False):
                game_over = -1
                game_over_effect.play()

            # Adicionando colisão com a porta de troca de level
            if pygame.sprite.spritecollide(self, exit_group, False):
                game_over = 1

            # Verificando colisão com as plataformas
            for platform in platform_group:
                # Colisão na direção do eixo x
                if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                # Colisão na direção do eixo y
                if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    # Verifique se está abaixo da plataforma
                    if abs((self.rect.top + dy) - platform.rect.bottom) < col_thresh:
                        self.vel_y = 0
                        dy = platform.rect.bottom - self.rect.top
                    # Verifique se está acima da plataforma
                    elif abs((self.rect.bottom + dy) - platform.rect.top) < col_thresh:
                        self.rect.bottom = platform.rect.top - 1
                        self.in_air = False
                        dy = 0
                    # Mover player lateralmente com a plataforma
                    if platform.move_x != 0:
                        self.rect.x += platform.move_direction

            # Atualiza as coordenadas do jogador
            self.rect.x += dx
            self.rect.y += dy

        elif game_over == -1:
            self.image = self.dead_image
            draw_text('Você Perdeu!', Game.font, blue, (Game.screen_width // 2) - 200, Game.screen_height // 2)
            if self.rect.y > 200:
                self.rect.y -= 5

        # Carrega o jogador na tela
        Game.screen.blit(self.image, self.rect)
        #pygame.draw.rect(Game.screen, (255, 255, 255), self.rect, 2)

        return game_over

    def reset(self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        # Carrega as imagens do jogador e redimensiona a imagem para 40x80 pixels
        for num in range(1, 5):
            image_right = pygame.image.load(f'assets/animation/player/player{num}.png')
            image_right = pygame.transform.scale(image_right, (40, 80))
            image_left = pygame.transform.flip(image_right, True, False)
            self.images_right.append(image_right)
            self.images_left.append(image_left)
        self.dead_image = pygame.image.load('assets/image/ghost.png')
        self.image = self.images_right[self.index]
        # Cria um retângulo para o jogador e posiciona-o nas coordenadas x e y especificadas
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        # Define a velocidade vertical do jogador como 0
        self.vel_y = 0
        self.jumped = False
        self.direction = 0
        self.in_air = True


class World:
    def __init__(self, data):
        self.tile_list = []

        # Carregue as imagens a partir do diretório especificado
        dirt_image = pygame.image.load('assets/image/dirt.png')
        grass_image = pygame.image.load('assets/image/grass.png')

        # Laço de repetição para percorrer as colunas da matriz 'world_data'
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                # Verifica se o valor da posição atual é 1, ou seja, se o bloco é de terra
                if tile == 1:
                    # Carrega a imagem do bloco de terra e redimensiona para o tamanho do bloco
                    img = pygame.transform.scale(dirt_image, (tile_size, tile_size))
                    # Obtém o retângulo da imagem
                    img_rect = img.get_rect()
                    # Define a posição x e y do retângulo do bloco de terra
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    # Cria uma tupla com a imagem e o retângulo e adiciona na lista de blocos
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                # Verifica se o valor da posição atual é 2, ou seja, se o bloco é de grama
                if tile == 2:
                    img = pygame.transform.scale(grass_image, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    enemy = Enemy(col_count * tile_size, row_count * tile_size + 15)
                    enemy_group.add(enemy)
                if tile == 4:
                    platform = Platform(col_count * tile_size, row_count * tile_size, 1, 0)
                    platform_group.add(platform)
                if tile == 5:
                    platform = Platform(col_count * tile_size, row_count * tile_size, 0, 1)
                    platform_group.add(platform)
                if tile == 6:
                    flood_water = FloodWater(col_count * tile_size, row_count * tile_size + (tile_size // 2))
                    flood_water_group.add(flood_water)
                if tile == 7:
                    coin = Coin(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2))
                    coin_group.add(coin)
                if tile == 8:
                    exit = Exit(col_count * tile_size, row_count * tile_size - (tile_size // 2))
                    exit_group.add(exit)

                col_count += 1
            row_count += 1

    # Desenha cada tile na tela usando as coordenadas de posição e a imagem associada
    def draw(self):
        for tile in self.tile_list:
            Game.screen.blit(tile[0], tile[1])
            #pygame.draw.rect(Game.screen, (255, 255, 255), tile[1], 2)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/image/enemy.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, move_x, move_y):
        pygame.sprite.Sprite.__init__(self)
        image = pygame.image.load('assets/image/platform.png')
        self.image = pygame.transform.scale(image, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_counter = 0
        self.move_direction = 1
        self.move_x = move_x
        self.move_y = move_y

    def update(self):
        self.rect.x += self.move_direction * self.move_x
        self.rect.y += self.move_direction * self.move_y
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1


class FloodWater(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        image = pygame.image.load('assets/image/floodWater.png')
        self.image = pygame.transform.scale(image, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        image = pygame.image.load('assets/image/coin.png')
        self.image = pygame.transform.scale(image, (tile_size // 2, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


class HealthBar(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images_live = []
        for num in range(0, 6):
            image_live = pygame.image.load(f'assets/animation/health/coracao{num}.png')
            image_live = pygame.transform.scale(image_live, (tile_size * 2.9, tile_size))
            self.images_live.append(image_live)
        self.image = self.images_live[player.lives]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, screen):
        self.image = self.images_live[player.lives]
        screen.blit(self.image, self.rect)
        #pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)


class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        image = pygame.image.load('assets/image/exitLevel.png')
        self.image = pygame.transform.scale(image, (tile_size, int(tile_size * 1.5)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Game:
    # Crie uma janela do Pygame com as dimensões especificadas anteriormente
    screen_width = 1920
    screen_height = 1080
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    fps = 60

    def __init__(self):
        # Inicialize o Pygame para que possa ser utilizado
        pygame.init()
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
        # Defina a largura e a altura da tela do jogo
        self.display = pygame.Surface((self.screen_width, self.screen_height))
        #Defina o título da janela do jogo
        pygame.display.set_caption('SurviveNature')
        # Definido fonte
        self.font = pygame.font.SysFont('Bauhaus 93', 70)
        self.font_score = pygame.font.SysFont('Bauhaus 93', 30)
        self.font_menu = 'assets/font/8-BIT WONDER.TTF'
        # Opções do menu
        self.main_menu = MainMenu(self)
        self.options = OptionsMenu(self)
        self.credits = CreditsMenu(self)
        self.curr_menu = self.main_menu

    '''
    # Cria um objeto Player com posição inicial
    player = Player(100, screen_height - 130)
    vida = HealthBar((tile_size // 2) - 15, 15)

    enemy_group = pygame.sprite.Group()
    platform_group = pygame.sprite.Group()
    flood_water_group = pygame.sprite.Group()
    coin_group = pygame.sprite.Group()
    exit_group = pygame.sprite.Group()

    # Criando moeda fictícia para mostrar na pontuação
    score_coin = Coin((tile_size // 2) + 5, 3.5 * (tile_size // 2))
    coin_group.add(score_coin)

    # Cria um objeto World com dados de mapa em 'world_data'
    if path.exists(f'assets/level_data/level{level}_data'):
        pickle_in = open(f'assets/level_data/level{level}_data', 'rb')
        world_data = pickle.load(pickle_in)
    world = World(world_data)

    restart_button = Button(screen_width // 2 - 50, screen_height // 2 + 100, restart_image)
    start_button = Button(screen_width // 2 - 350, screen_height // 2, start_image)
    exit_button = Button(screen_width // 2 + 150, screen_height // 2, exit_image)

    run = True
    while run:

        clock.tick(fps)

        # Carregue as imagens a partir do diretório especificado
        screen.blit(background_image, (0, 0))
        screen.blit(sun_image, (100, 100))

        if main_menu:
            if exit_button.draw():
                run = False
            if start_button.draw():
                main_menu = False
        else:
            # Desenha o mundo na tela
            world.draw()

            # Se o jogador estiver vivo
            if game_over == 0:
                enemy_group.update()
                platform_group.update()
                # Atualizando a pontuação
                # Verifica se o item foi coletado
                print('player.lives = ' + str(player.lives))
                if pygame.sprite.spritecollide(player, coin_group, True):
                    score += 1
                    coin_effect.play()
                draw_text(' X ' + str(score), font_score, white, tile_size - 5, tile_size + 21)

            enemy_group.draw(screen)
            platform_group.draw(screen)
            flood_water_group.draw(screen)
            coin_group.draw(screen)
            exit_group.draw(screen)
            vida.draw(screen)

            game_over = player.update(game_over)

            # Se o jogador morrer
            if game_over == -1:
                player.lives -= 1
                if player.lives > 0:
                    world_data = []
                    world = reset_level(level)
                    game_over = 0
                else:
                    score = 0
                    #if restart_button.draw():

            # Se o jogador ganhar a fase
            if game_over == 1:
            # Resetar o jogo e ir para a proxima fase
                level += 1
                if level <= max_levels:
                    # Resetar fase
                    world_data = []
                    world = reset_level(level)
                    game_over = 0
                    player.score += score
                    score = 0
                else:
                    draw_text('Você Ganhou!', font, blue, (screen_width // 2) - 200, screen_height // 2)
                    # Resetar o jogo
                    if restart_button.draw():
                        level = 1
                        # Resetar fase
                        world_data = []
                        world = reset_level(level)
                        game_over = 0
                        score = 0

        # Desenha o grid das imagens
    #	draw_grid()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

    pygame.quit()
    '''

    def game_loop(self):
        global world
        global game_over
        global score
        global level
        while self.playing:
            self.check_events()
            if self.START_KEY:
                self.playing = False

            Game.clock.tick(Game.fps)

            # Carregue as imagens a partir do diretório especificado
            Game.screen.blit(background_image, (0, 0))
            Game.screen.blit(sun_image, (100, 100))

            if self.main_menu:
                self.main_menu = False
            else:
                # Desenha o mundo na tela
                world.draw()

                # Se o jogador estiver vivo
                if game_over == 0:
                    enemy_group.update()
                    platform_group.update()
                    # Atualizando a pontuação
                    # Verifica se o item foi coletado
                    print('player.lives = ' + str(player.lives))
                    if pygame.sprite.spritecollide(player, coin_group, True):
                        score += 1
                        coin_effect.play()
                    draw_text(' X ' + str(score), self.font_score, white, tile_size - 5, tile_size + 21)

                enemy_group.draw(Game.screen)
                platform_group.draw(Game.screen)
                flood_water_group.draw(Game.screen)
                coin_group.draw(Game.screen)
                exit_group.draw(Game.screen)
                vida.draw(Game.screen)

                game_over = player.update(game_over)

                # Se o jogador morrer
                if game_over == -1:
                    player.lives -= 1
                    if player.lives > 0:
                        world_data = []
                        world = reset_level(level)
                        game_over = 0
                    else:
                        score = 0
                        # if restart_button.draw():

                # Se o jogador ganhar a fase
                if game_over == 1:
                    # Resetar o jogo e ir para a proxima fase
                    level += 1
                    if level <= max_levels:
                        # Resetar fase
                        world_data = []
                        world = reset_level(level)
                        game_over = 0
                        player.score += score
                        score = 0
                    else:
                        draw_text('Você Ganhou!', self.font, blue, (Game.screen_width // 2) - 200, Game.screen_height // 2)
                        # Resetar o jogo
                        if restart_button.draw():
                            level = 1
                            # Resetar fase
                            world_data = []
                            world = reset_level(level)
                            game_over = 0
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

    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(self.font_menu, size)
        text_surface = font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)


class Menu:
    def __init__(self, game):
        self.game = game
        self.screen_width_mid, self.screen_height_mid = self.game.screen_width / 2, self.game.screen_height / 2
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
        self.game.draw_text('*', 40, (self.cursor_rect.x - 100), self.cursor_rect.y)

    def blit_screen(self):
        self.game.screen.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()


class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Iniciar'
        self.startx, self.starty = self.screen_width_mid, self.screen_height_mid + 55
        self.optionsx, self.optionsy = self.screen_width_mid, self.screen_height_mid + 100
        self.creditsx, self.creditsy = self.screen_width_mid, self.screen_height_mid + 150
        self.exitsx, self.exitsy = self.screen_width_mid, self.screen_height_mid + 200
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.draw_background()
            self.game.draw_text('Survive Nature', 80, self.game.screen_width / 2, self.game.screen_height / 2 - 250)
            self.game.draw_text('Iniciar', 40, self.startx, self.starty)
            self.game.draw_text('Opcoes', 40, self.optionsx, self.optionsy)
            self.game.draw_text('Creditos', 40, self.creditsx, self.creditsy)
            self.game.draw_text('Sair', 40, self.exitsx, self.exitsy)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'Iniciar':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Opcoes'
            elif self.state == 'Opcoes':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Creditos'
            elif self.state == 'Creditos':
                self.cursor_rect.midtop = (self.exitsx + self.offset, self.exitsy)
                self.state = 'Sair'
            elif self.state == 'Sair':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Iniciar'
        elif self.game.UP_KEY:
            if self.state == 'Iniciar':
                self.cursor_rect.midtop = (self.exitsx + self.offset, self.exitsy)
                self.state = 'Sair'
            elif self.state == 'Opcoes':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Iniciar'
            elif self.state == 'Creditos':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Opcoes'
            elif self.state == 'Sair':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Creditos'

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 'Iniciar':
                self.game.playing = True
            elif self.state == 'Opcoes':
                self.game.curr_menu = self.game.options
            elif self.state == 'Creditos':
                self.game.curr_menu = self.game.credits
            elif self.state == 'Sair':
                self.game.running = False
            self.run_display = False


class OptionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Volume'
        self.volx, self.voly = self.screen_width_mid, self.screen_height_mid + 55
        self.controlsx, self.controlsy = self.screen_width_mid, self.screen_height_mid + 10
        self.cursor_rect.midtop = (self.volx + self.offset, self.voly)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.draw_background()
            self.game.draw_text('Opcoes    ( Em Breve )', 80, self.game.screen_width / 2, self.game.screen_height / 2 - 250)
            self.game.draw_text('Volume', 40, self.volx, self.voly)
            self.game.draw_text('Controles', 40, self.controlsx, self.controlsy)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.UP_KEY or self.game.DOWN_KEY:
            if self.state == 'Volume':
                self.state = 'Controles'
                self.cursor_rect.midtop = (self.controlsx + self.offset, self.controlsy)
            elif self.state == 'Controles':
                self.state = 'Volume'
                self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
        elif self.game.START_KEY:
            # TO-DO: Create a Volume Menu and a Controls Menu
            pass


class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.draw_background()
            self.game.draw_text('Creditos', 80, self.game.screen_width / 2, self.game.screen_height / 2 - 250)
            self.game.draw_text('Breno Ferreira Pinho          ( 41932110 )', 40, self.game.screen_width / 2, self.game.screen_height / 2 + 55)
            self.game.draw_text('Bruno Nardelli Santiago   ( 41933613 )', 40, self.game.screen_width / 2, self.game.screen_height / 2 + 100)
            self.game.draw_text('Daphne Nanni Rodrigues    ( 32123655 )', 40, self.game.screen_width / 2, self.game.screen_height / 2 + 150)
            self.blit_screen()


# Cria um objeto Player com posição inicial
player = Player(100, Game.screen_height - 130)
vida = HealthBar((tile_size // 2) - 15, 15)

enemy_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
flood_water_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

# Criando moeda fictícia para mostrar na pontuação
score_coin = Coin((tile_size // 2) + 5, 3.5 * (tile_size // 2))
coin_group.add(score_coin)

# Cria um objeto World com dados de mapa em 'world_data'
if path.exists(f'assets/level_data/level{level}_data'):
    pickle_in = open(f'assets/level_data/level{level}_data', 'rb')
    world_data = pickle.load(pickle_in)
else:
    quit()
world = World(world_data)

restart_button = Button(Game.screen_width // 2 - 50, Game.screen_height // 2 + 100, restart_image)
start_button = Button(Game.screen_width // 2 - 350, Game.screen_height // 2, start_image)

game = Game()

while game.running:
    game.curr_menu.display_menu()
    game.game_loop()
