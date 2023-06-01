import pygame

# Defina as variáveis do jogo
screen_width = 1900
screen_height = 1050
tile_size = 50

# Defina as cores
white = (255, 255, 255)
blue = (0, 0, 255)
dark_blue = (0, 0, 156, .5)
black = (0, 0, 0)

# Carregue as imagens a partir do diretório especificado
restart_image = pygame.image.load('assets/image/restart_button.png')
start_image = pygame.image.load('assets/image/start_button.png')
