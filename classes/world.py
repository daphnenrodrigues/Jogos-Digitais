import pygame
import classes.utils as const
from classes.enemy import Enemy
from classes.platform import Platform
from classes.floodWater import FloodWater
from classes.coin import Coin
from classes.exit import Exit


class World:
    def __init__(self, data, enemy_group, platform_group, flood_water_group, coin_group, exit_group, screen):
        self.tile_list = []
        self.screen = screen

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
                    img = pygame.transform.scale(dirt_image, (const.tile_size, const.tile_size))
                    # Obtém o retângulo da imagem
                    img_rect = img.get_rect()
                    # Define a posição x e y do retângulo do bloco de terra
                    img_rect.x = col_count * const.tile_size
                    img_rect.y = row_count * const.tile_size
                    # Cria uma tupla com a imagem e o retângulo e adiciona na lista de blocos
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                # Verifica se o valor da posição atual é 2, ou seja, se o bloco é de grama
                if tile == 2:
                    img = pygame.transform.scale(grass_image, (const.tile_size, const.tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * const.tile_size
                    img_rect.y = row_count * const.tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    enemy = Enemy(col_count * const.tile_size, row_count * const.tile_size + 15)
                    enemy_group.add(enemy)
                if tile == 4:
                    platform = Platform(col_count * const.tile_size, row_count * const.tile_size, 1, 0)
                    platform_group.add(platform)
                if tile == 5:
                    platform = Platform(col_count * const.tile_size, row_count * const.tile_size, 0, 1)
                    platform_group.add(platform)
                if tile == 6:
                    flood_water = FloodWater(col_count * const.tile_size, row_count * const.tile_size + (const.tile_size // 2))
                    flood_water_group.add(flood_water)
                if tile == 7:
                    coin = Coin(col_count * const.tile_size + (const.tile_size // 2), row_count * const.tile_size + (const.tile_size // 2))
                    coin_group.add(coin)
                if tile == 8:
                    exit = Exit(col_count * const.tile_size, row_count * const.tile_size - (const.tile_size // 2))
                    exit_group.add(exit)

                col_count += 1
            row_count += 1

    # Desenha cada tile na tela usando as coordenadas de posição e a imagem associada
    def draw(self):
        for tile in self.tile_list:
            self.screen.blit(tile[0], tile[1])
            #pygame.draw.rect(Game.screen, (255, 255, 255), tile[1], 2)
