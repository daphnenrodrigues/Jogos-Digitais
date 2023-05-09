# Importe o módulo Pygame para utilizar suas funcionalidades
import pygame
from pygame.locals import *

# Inicialize o Pygame para que possa ser utilizado
pygame.init()

clock = pygame.time.Clock()
fps = 60

# Defina a largura e a altura da tela do jogo
screen_width = 1000
screen_height = 1000

# Crie uma janela do Pygame com as dimensões especificadas anteriormente e defina o título da janela do jogo
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('SurviveNature')

# Defina as variáveis do jogo
tile_size = 50
game_over = 0

# Carregue as imagens a partir do diretório especificado
sun_image = pygame.image.load('assets/image/sun.png')
background_image = pygame.image.load('assets/image/sky.png')


# Desenha uma grade na tela do jogo de 50x50 pixels
def draw_grid():
	for line in range(0, 20):
		pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (screen_width, line * tile_size))
		pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, screen_height))


class Player():
	def __init__(self, x, y):
		self.images_right = []
		self.images_left = []
		self.index = 0
		self.counter = 0
		# Carrega as imagens do jogador e redimensiona a imagem para 40x80 pixels
		for num in range(1, 5):
			image_right = pygame.image.load(f'assets/image/player{num}.png')
			image_right = pygame.transform.scale(image_right, (40, 80))
			image_left = pygame.transform.flip(image_right, True, False)
			self.images_right.append(image_right)
			self.images_left.append(image_left)
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

	def update(self):
		dx = 0
		dy = 0
		walk_cooldown = 5

		# Verifica se alguma tecla foi pressionada
		key = pygame.key.get_pressed()
		if key[pygame.K_SPACE] and self.jumped == False:
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
		for tile in world.tile_list:
			# Verificando colisão no eixo x
			if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
				dx = 0
			# Verificando colisão no eixo y
			if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
				# Verificando if below the ground i.e. jumping
				if self.vel_y < 0:
					dy = tile[1].bottom - self.rect.top
					self.vel_y = 0
				# Verificando if above the ground i.e. falling
				elif self.vel_y >= 0:
					dy = tile[1].top - self.rect.bottom
					self.vel_y = 0


		# Atualiza as coordenadas do jogador
		self.rect.x += dx
		self.rect.y += dy

		if self.rect.bottom > screen_height:
			self.rect.bottom = screen_height
			dy = 0

		# Carrega o jogador na tela
		screen.blit(self.image, self.rect)
		pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)


class World():
	def __init__(self, data):
		self.tile_list = []

		# Carregue as imagens a partir do diretório especificado
		dirt_image = pygame.image.load('assets/image/dirt.png')
		grass_image = pygame.image.load('assets/image/grass.png')

		# Laço de repetição para percorrer as colunas da matriz "world_data"
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
				if tile == 6:
					flood_water = FloodWater(col_count * tile_size, row_count * tile_size + (tile_size // 2))
					flood_water_group.add(flood_water)

				col_count += 1
			row_count += 1

	# Desenha cada tile na tela usando as coordenadas de posição e a imagem associada
	def draw(self):
		for tile in self.tile_list:
			screen.blit(tile[0], tile[1])
			pygame.draw.rect(screen, (255, 255, 255), tile[1], 2)


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


class FloodWater(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		image = pygame.image.load('assets/image/floodWater.png')
		self.image = pygame.transform.scale(image, (tile_size, tile_size // 2))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y



# Matrix referente ao mapa, onde cada número representa uma imagem
world_data = [
	[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 1],
	[1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 2, 2, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 7, 0, 5, 0, 0, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 1],
	[1, 7, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 7, 0, 0, 0, 0, 1],
	[1, 0, 2, 0, 0, 7, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 2, 0, 0, 4, 0, 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 7, 0, 0, 0, 0, 2, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 2, 2, 2, 2, 2, 1],
	[1, 0, 0, 0, 0, 0, 2, 2, 2, 6, 6, 6, 6, 6, 1, 1, 1, 1, 1, 1],
	[1, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
	[1, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
	[1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# Cria um objeto Player com posição inicial
player = Player(100, screen_height - 130)

enemy_group = pygame.sprite.Group()
flood_water_group = pygame.sprite.Group()

# Cria um objeto World com dados de mapa em 'world_data'
world = World(world_data)

run = True
while run:

	clock.tick(fps)

	# Carregue as imagens a partir do diretório especificado
	screen.blit(background_image, (0, 0))
	screen.blit(sun_image, (100, 100))

	# Desenha o mundo na tela e atualiza a posição do jogador
	world.draw()

	enemy_group.update()
	enemy_group.draw(screen)

	flood_water_group.draw(screen)

	player.update()
	# Desenha o grid das imagens
#	draw_grid()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	pygame.display.update()

pygame.quit()
