import pygame


class Player:
    def __init__(self, x, y, game):
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
        # Carregue os sons do jogo
        self.jump_effect = pygame.mixer.Sound('assets/audio/jump.wav')
        self.jump_effect.set_volume(0.5)
        self.game_over_effect = pygame.mixer.Sound('assets/audio/game_over.wav')
        self.game_over_effect.set_volume(0.5)
        self.game = game
        self.death_time = None

    def update(self, game_over):
        dx = 0
        dy = 0
        walk_cooldown = 5
        col_thresh = 20

        if game_over == 0:
            # Verifica se alguma tecla foi pressionada
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False:
                self.jump_effect.play()
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
            if self.counter > walk_cooldown and self.death_time is None:
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
            for tile_num, (_, tile_rect) in self.game.world.tile_list:
                if tile_num == 50 or tile_num == 49:
                    continue
                # Verificando colisão no eixo x
                if tile_rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                # Verificando colisão no eixo y
                if tile_rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    # Verificando se abaixo do solo, ou seja, pulando
                    if self.vel_y < 0:
                        dy = tile_rect.bottom - self.rect.top
                        self.vel_y = 0
                    # Verificando se está acima do solo, ou seja, caindo
                    elif self.vel_y >= 0:
                        dy = tile_rect.top - self.rect.bottom
                        self.vel_y = 0
                        self.in_air = False

            # Adicionando colisão com os inimigos
            if pygame.sprite.spritecollide(self, self.game.enemy_group, False):
                game_over = -1
                self.game_over_effect.play()

            # Adicionando colisão com a água-suja
            if pygame.sprite.spritecollide(self, self.game.flood_water_group, False):
                game_over = -1
                self.game_over_effect.play()

            # Adicionando colisão com a porta de troca de level
            if pygame.sprite.spritecollide(self, self.game.exit_group, False):
                game_over = 1

            # Verificando colisão com as plataformas
            for platform in self.game.platform_group:
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

        # Carrega o jogador na tela
        self.game.screen.blit(self.image, self.rect)
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
