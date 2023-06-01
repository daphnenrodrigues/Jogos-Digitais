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
        images = {1: pygame.image.load('assets/image/dirt.png'),
                  2: pygame.image.load('assets/image/grass.png'),
                  9: pygame.image.load('assets/image/grass1.png'),
                  10: pygame.image.load('assets/image/grass2.png'),
                  11: pygame.image.load('assets/image/grass3.png'),
                  12: pygame.image.load('assets/image/grass4.png'),
                  13: pygame.image.load('assets/image/grass5.png'),
                  14: pygame.image.load('assets/image/grass6.png'),
                  15: pygame.image.load('assets/image/grass7.png'),
                  16: pygame.image.load('assets/image/grass8.png'),
                  17: pygame.image.load('assets/image/grass9.png'),
                  18: pygame.image.load('assets/image/grass10.png'),
                  19: pygame.image.load('assets/image/grass11.png'),
                  20: pygame.image.load('assets/image/grass12.png'),
                  21: pygame.image.load('assets/image/grass13.png'),
                  22: pygame.image.load('assets/image/grass14.png'),
                  23: pygame.image.load('assets/image/grass15.png'),
                  24: pygame.image.load('assets/image/grass16.png'),
                  25: pygame.image.load('assets/image/grass17.png'),
                  26: pygame.image.load('assets/image/grass18.png'),
                  27: pygame.image.load('assets/image/grass19.png'),
                  28: pygame.image.load('assets/image/grass20.png'),
                  29: pygame.image.load('assets/image/grass21.png'),
                  30: pygame.image.load('assets/image/grass22.png'),
                  31: pygame.image.load('assets/image/grass23.png'),
                  32: pygame.image.load('assets/image/grass24.png'),
                  33: pygame.image.load('assets/image/grass25.png'),
                  34: pygame.image.load('assets/image/grass26.png'),
                  35: pygame.image.load('assets/image/grass27.png'),
                  36: pygame.image.load('assets/image/grass28.png'),
                  37: pygame.image.load('assets/image/grass29.png'),
                  38: pygame.image.load('assets/image/grass30.png'),
                  39: pygame.image.load('assets/image/grass31.png'),
                  40: pygame.image.load('assets/image/grass32.png'),
                  41: pygame.image.load('assets/image/grass33.png'),
                  42: pygame.image.load('assets/image/grass34.png'),
                  43: pygame.image.load('assets/image/grass35.png'),
                  44: pygame.image.load('assets/image/grass36.png'),
                  45: pygame.image.load('assets/image/grass37.png'),
                  46: pygame.image.load('assets/image/grass38.png'),
                  47: pygame.image.load('assets/image/grass39.png'),
                  48: pygame.image.load('assets/image/floodWater2.png'),
                  49: pygame.image.load('assets/image/grass3.png'),
                  50: pygame.image.load('assets/image/grass4.png')}


        # Laço de repetição para percorrer as colunas da matriz 'world_data'
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 3:
                    enemy = Enemy(col_count * const.tile_size, row_count * const.tile_size + 15)
                    enemy_group.add(enemy)
                elif tile == 4:
                    platform = Platform(col_count * const.tile_size, row_count * const.tile_size, 1, 0)
                    platform_group.add(platform)
                elif tile == 5:
                    platform = Platform(col_count * const.tile_size, row_count * const.tile_size, 0, 1)
                    platform_group.add(platform)
                elif tile == 6:
                    flood_water = FloodWater(col_count * const.tile_size, row_count * const.tile_size + (const.tile_size // 2))
                    flood_water_group.add(flood_water)
                elif tile == 7:
                    coin = Coin(col_count * const.tile_size + (const.tile_size // 2), row_count * const.tile_size + (const.tile_size // 2))
                    coin_group.add(coin)
                elif tile == 8:
                    exit = Exit(col_count * const.tile_size, row_count * const.tile_size - (const.tile_size * -0.26))
                    exit_group.add(exit)
                elif tile in images.keys():
                    # Carrega a imagem do bloco de terra e redimensiona para o tamanho do bloco
                    img = pygame.transform.scale(images[tile], (const.tile_size, const.tile_size))
                    # Obtém o retângulo da imagem
                    img_rect = img.get_rect()
                    # Define a posição x e y do retângulo do bloco de terra
                    img_rect.x = col_count * const.tile_size
                    img_rect.y = row_count * const.tile_size
                    # Cria uma tupla com a imagem e o retângulo e adiciona na lista de blocos
                    self.tile_list.append((tile, (img, img_rect)))
                col_count += 1
            row_count += 1

    # Desenha cada tile na tela usando as coordenadas de posição e a imagem associada
    def draw(self):
        for _, tile in self.tile_list:
            self.screen.blit(*tile)
            #pygame.draw.rect(Game.screen, (255, 255, 255), tile[1], 2)
