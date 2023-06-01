import pygame
import pickle
from os import path


pygame.init()

clock = pygame.time.Clock()
fps = 60

#game window
tile_size = 50
cols = 38
line = 21
margin = 100
screen_width = 1900
screen_height = 1050

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Level Editor')


#load images
sun_img = pygame.image.load('assets/image/sun.png')
sun_img = pygame.transform.scale(sun_img, (tile_size, tile_size))
bg_img = pygame.image.load('assets/image/sky.jpg')
bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height - margin))
dirt_img = pygame.image.load('assets/image/dirt.png')
grass_img = pygame.image.load('assets/image/grass.png')
grass1_img = pygame.image.load('assets/image/grass1.png')
grass2_img = pygame.image.load('assets/image/grass2.png')
grass3_img = pygame.image.load('assets/image/grass3.png')
grass4_img = pygame.image.load('assets/image/grass4.png')
grass5_img = pygame.image.load('assets/image/grass5.png')
grass6_img = pygame.image.load('assets/image/grass6.png')
grass7_img = pygame.image.load('assets/image/grass7.png')
grass8_img = pygame.image.load('assets/image/grass8.png')
grass9_img = pygame.image.load('assets/image/grass9.png')
grass10_img = pygame.image.load('assets/image/grass10.png')
grass11_img = pygame.image.load('assets/image/grass11.png')
grass12_img = pygame.image.load('assets/image/grass12.png')
grass13_img = pygame.image.load('assets/image/grass13.png')
grass14_img = pygame.image.load('assets/image/grass14.png')
grass15_img = pygame.image.load('assets/image/grass15.png')
grass16_img = pygame.image.load('assets/image/grass16.png')
grass17_img = pygame.image.load('assets/image/grass17.png')
grass18_img = pygame.image.load('assets/image/grass18.png')
grass19_img = pygame.image.load('assets/image/grass19.png')
grass20_img = pygame.image.load('assets/image/grass20.png')
grass21_img = pygame.image.load('assets/image/grass21.png')
grass22_img = pygame.image.load('assets/image/grass22.png')
grass23_img = pygame.image.load('assets/image/grass23.png')
grass24_img = pygame.image.load('assets/image/grass24.png')
grass25_img = pygame.image.load('assets/image/grass25.png')
grass26_img = pygame.image.load('assets/image/grass26.png')
grass27_img = pygame.image.load('assets/image/grass27.png')
grass28_img = pygame.image.load('assets/image/grass28.png')
grass29_img = pygame.image.load('assets/image/grass29.png')
grass30_img = pygame.image.load('assets/image/grass30.png')
grass31_img = pygame.image.load('assets/image/grass31.png')
grass32_img = pygame.image.load('assets/image/grass32.png')
grass33_img = pygame.image.load('assets/image/grass33.png')
grass34_img = pygame.image.load('assets/image/grass34.png')
grass35_img = pygame.image.load('assets/image/grass35.png')
grass36_img = pygame.image.load('assets/image/grass36.png')
grass37_img = pygame.image.load('assets/image/grass37.png')
grass38_img = pygame.image.load('assets/image/grass38.png')
grass39_img = pygame.image.load('assets/image/grass39.png')

grass3_invisible_img = pygame.image.load('assets/image/grass3_invisible.png')
grass4_invisible_img = pygame.image.load('assets/image/grass4_invisible.png')

enemy_img = pygame.image.load('assets/image/enemy.png')
platform_x_img = pygame.image.load('assets/image/platform_x.png')
platform_y_img = pygame.image.load('assets/image/platform_y.png')
floodWater_img = pygame.image.load('assets/image/floodWater.png')
floodWater2_img = pygame.image.load('assets/image/floodWater2.png')
coin_img = pygame.image.load('assets/image/coin.png')
exit_img = pygame.image.load('assets/image/exitLevel.png')


#define game variables
clicked = False
level = 1

#define colours
white = (255, 255, 255)
green = (144, 201, 120)

font = pygame.font.SysFont('Futura', 24)

#create empty tile list
world_data = [[1] * cols]
for row in range(line - 2):
	r = [1] + ([0] * (cols - 2)) + [1]
	world_data.append(r)
world_data.append([2] * cols)


#function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))


def draw_grid():
	for c in range(cols + 1):
		#vertical lines
		pygame.draw.line(screen, white, (c * tile_size, 0), (c * tile_size, screen_height - margin))
	for l in range(line + 1):
		# horizontal lines
		pygame.draw.line(screen, white, (0, l * tile_size), (screen_width, l * tile_size))


def draw_world():
	for row in range(line):
		for col in range(cols):
			if world_data[row][col] > 0:
				if world_data[row][col] == 1:
					#dirt blocks
					img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 2:
					#grass blocks
					img = pygame.transform.scale(grass_img, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 3:
					#enemy blocks
					img = pygame.transform.scale(enemy_img, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size + (tile_size * 0.25)))
				if world_data[row][col] == 4:
					#horizontally moving platform
					img = pygame.transform.scale(platform_x_img, (tile_size, tile_size // 2))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 5:
					#vertically moving platform
					img = pygame.transform.scale(platform_y_img, (tile_size, tile_size // 2))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 6:
					#lava
					img = pygame.transform.scale(floodWater_img, (tile_size, tile_size // 2))
					screen.blit(img, (col * tile_size, row * tile_size + (tile_size // 2)))
				if world_data[row][col] == 7:
					#coin
					img = pygame.transform.scale(coin_img, (tile_size // 2, tile_size // 2))
					screen.blit(img, (col * tile_size + (tile_size // 4), row * tile_size + (tile_size // 4)))
				if world_data[row][col] == 8:
					#exit
					img = pygame.transform.scale(exit_img, (int(tile_size * 0.75), int(tile_size * 0.75)))
					screen.blit(img, (col * tile_size, row * tile_size - (tile_size * -0.26)))
				if world_data[row][col] == 9:
					#grass blocks
					img = pygame.transform.scale(grass1_img, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 10:
					#grass blocks
					img = pygame.transform.scale(grass2_img, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 11:
					#grass blocks
					img = pygame.transform.scale(grass3_img, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 12:
					#grass blocks
					img = pygame.transform.scale(grass4_img, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 13:
					#grass blocks
					img = pygame.transform.scale(grass5_img, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 14:
					#grass blocks
					img = pygame.transform.scale(grass6_img, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 15:
					#grass blocks
					img = pygame.transform.scale(grass7_img, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 16:
					#grass blocks
					img = pygame.transform.scale(grass8_img, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 17:
					#grass blocks
					img = pygame.transform.scale(grass9_img, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 18:
					#grass blocks
					img = pygame.transform.scale(grass10_img, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 19:
					#grass blocks
					img = pygame.transform.scale(grass11_img, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 20:
					#grass blocks
					img = pygame.transform.scale(grass12_img, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 21:
					#grass blocks
					img = pygame.transform.scale(grass13_img, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 22:
					#grass blocks
					img = pygame.transform.scale(grass14_img, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 23:
					#grass blocks
					img = pygame.transform.scale(grass15_img, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 24:
					#grass blocks
					img = pygame.transform.scale(grass16_img, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 25:
					#grass blocks
					img = pygame.transform.scale(grass17_img, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 26:
					#grass blocks
					img = pygame.transform.scale(grass18_img, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 27:
					#grass blocks
					img = pygame.transform.scale(grass19_img, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 28:
					#grass blocks
					img = pygame.transform.scale(grass20_img, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 29:
					#grass blocks
					img = pygame.transform.scale(grass21_img, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 30:
					#grass blocks
					img = pygame.transform.scale(grass22_img, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 31:
					#grass blocks
					img = pygame.transform.scale(grass23_img, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 32:
					#grass blocks
					img = pygame.transform.scale(grass24_img, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 33:
					#grass blocks
					img = pygame.transform.scale(grass25_img, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 34:
					#grass blocks
					img = pygame.transform.scale(grass26_img, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 35:
					#grass blocks
					img = pygame.transform.scale(grass27_img, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 36:
					#grass blocks
					img = pygame.transform.scale(grass28_img, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 37:
					#grass blocks
					img = pygame.transform.scale(grass29_img, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 38:
					#grass blocks
					img = pygame.transform.scale(grass30_img, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 39:
					#grass blocks
					img = pygame.transform.scale(grass31_img, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 40:
					#grass blocks
					img = pygame.transform.scale(grass32_img, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 41:
					#grass blocks
					img = pygame.transform.scale(grass33_img, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 42:
					#grass blocks
					img = pygame.transform.scale(grass34_img, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 43:
					#grass blocks
					img = pygame.transform.scale(grass35_img, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 44:
					#grass blocks
					img = pygame.transform.scale(grass36_img, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 45:
					#grass blocks
					img = pygame.transform.scale(grass37_img, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 46:
					#grass blocks
					img = pygame.transform.scale(grass38_img, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 47:
					#grass blocks
					img = pygame.transform.scale(grass39_img, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 48:
					#grass blocks
					img = pygame.transform.scale(floodWater2_img, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 49:
					#grass blocks
					img = pygame.transform.scale(grass3_invisible_img, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 50:
					#grass blocks
					img = pygame.transform.scale(grass4_invisible_img, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))


#main game loop
run = True
while run:

	clock.tick(fps)

	#draw background
	screen.fill(green)
	screen.blit(bg_img, (0, 0))
	screen.blit(sun_img, (tile_size * 2, tile_size * 2))

	#show the grid and draw the level tiles
	draw_grid()
	draw_world()

	#text showing current level
	draw_text(f'Level: {level}', font, white, tile_size, screen_height - 60)
	draw_text('Aperte "Seta para Cima" ou "Seta para Baixo" para trocar de level', font, white, tile_size, screen_height - 40)
	draw_text('Aperte "S" para salvar o level ou "L" para carregar o level ja salvo', font, white, tile_size, screen_height - 20)

	#event handler
	for event in pygame.event.get():
		#quit game
		if event.type == pygame.QUIT:
			run = False
		#mouseclicks to change tiles
		if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
			clicked = True
			pos = pygame.mouse.get_pos()
			x = pos[0] // tile_size
			y = pos[1] // tile_size
			#check that the coordinates are within the tile area
			if x < cols and y < line:
				#update tile value
				if pygame.mouse.get_pressed()[0] == 1:
					world_data[y][x] += 1
					if world_data[y][x] > 50:
						world_data[y][x] = 0
				elif pygame.mouse.get_pressed()[2] == 1:
					world_data[y][x] -= 1
					if world_data[y][x] < 0:
						world_data[y][x] = 50
		if event.type == pygame.MOUSEBUTTONUP:
			clicked = False
		#up and down key presses to change level number
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				level += 1
			elif event.key == pygame.K_DOWN and level > 1:
				level -= 1
			elif event.key == pygame.K_s:
				# save level data
				pickle_out = open(f'level{level}_data', 'wb')
				pickle.dump(world_data, pickle_out)
				pickle_out.close()
			elif event.key == pygame.K_l:
				# load in level data
				if path.exists(f'level{level}_data'):
					pickle_in = open(f'level{level}_data', 'rb')
					world_data = pickle.load(pickle_in)
	#update game display window
	pygame.display.update()

pygame.quit()
