# Imports
import pygame, time, sys
from pygame.locals import * 
import random

# Import the database
from Database.variables import *

pygame.init()


def transform(value, respect_to):
	value = int(value / 1920 * WINDOW_WIDTH) if respect_to == WINDOW_WIDTH else int(value / 1080 * WINDOW_HEIGHT)
	return value

CLOCK = pygame.time.Clock()

DISPSURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('ROMERO 3 GAMES!!!')

BACK_IMG = pygame.image.load('Images/Wooden_imgs/back_button.png').convert_alpha()
BLUR_BG_IMG = pygame.image.load('Images/others/blurred bg img.jpg').convert_alpha()
SNAKE_GAME_IMG = pygame.image.load('Images/snake/snake.png').convert_alpha()
DARK_GRASS_IMG = pygame.image.load('Images/snake/dark grass.jpg').convert_alpha()
LIGHT_GRASS_IMG = pygame.image.load('Images/snake/light grass.jpg').convert_alpha()
SNAKE_HEAD_IMG = pygame.image.load('Images/snake/snake_head.png').convert_alpha() 
SNAKE_BODY_IMG = pygame.image.load('Images/snake/snake body1.png').convert_alpha()
FRUIT_IMG = pygame.image.load('Images/snake/fruit.png').convert_alpha()

# Loading sounds
button_click_sound = pygame.mixer.Sound('Sounds/button_click.wav')
quit_game_sound = pygame.mixer.Sound('Sounds/game_quit.wav')
in_the_forest = pygame.mixer.music.load('Sounds/in_the_forest.mp3')
boing_sound = pygame.mixer.Sound("Sounds/boing.mp3")
blick_sound = pygame.mixer.Sound("Sounds/movement sound.wav")
fruit_eat_sound = pygame.mixer.Sound('Sounds/fruit eat sound.wav')
yay_sound = pygame.mixer.Sound('Sounds/yay.mp3')
sad_sound = pygame.mixer.Sound('Sounds/sad.wav')

# Play bg music
if MUSIC_ON:
	pygame.mixer.music.set_volume(1)
else:
	pygame.mixer.music.set_volume(0)


# Play bg music
if MUSIC_ON:
	pygame.mixer.music.set_volume(1)
else:
	pygame.mixer.music.set_volume(0)

if SOUND_ON:
	button_click_sound.set_volume(1)
	quit_game_sound.set_volume(1)
	boing_sound.set_volume(1)
	blick_sound.set_volume(1)
	fruit_eat_sound.set_volume(1)
	yay_sound.set_volume(1)
	sad_sound.set_volume(1)

else:
	button_click_sound.set_volume(0)
	quit_game_sound.set_volume(0)
	boing_sound.set_volume(0)
	blick_sound.set_volume(0)
	fruit_eat_sound.set_volume(0)
	yay_sound.set_volume(0)
	sad_sound.set_volume(0)

pygame.mixer.music.play(-1)

blur_bg_img = pygame.transform.scale(BLUR_BG_IMG, (WINDOW_WIDTH, WINDOW_HEIGHT + transform(100, WINDOW_HEIGHT))).convert_alpha()
blur_bg_img_rect = blur_bg_img.get_rect()
blur_bg_img_rect.center = WINDOW_WIDTH//2, WINDOW_HEIGHT//2

back_button_img = pygame.transform.scale(BACK_IMG, (transform(140, WINDOW_WIDTH), transform(140, WINDOW_WIDTH))).convert_alpha()
back_button_img_rect = back_button_img.get_rect()
back_button_img_rect.center = (WINDOW_WIDTH - WINDOW_WIDTH//10, WINDOW_HEIGHT//10)

NO_OF_TILES = 17
GRASS_TILE_TOTAL_LENGTH = WINDOW_HEIGHT//1.2
GRASS_TILE_WIDTH = GRASS_TILE_TOTAL_LENGTH//NO_OF_TILES
GRASS_TILE_TOTAL_LENGTH = NO_OF_TILES * GRASS_TILE_WIDTH
dark_grass_img = pygame.transform.scale(DARK_GRASS_IMG, (GRASS_TILE_WIDTH, GRASS_TILE_WIDTH)).convert_alpha()
light_grass_img = pygame.transform.scale(LIGHT_GRASS_IMG, (GRASS_TILE_WIDTH, GRASS_TILE_WIDTH)).convert_alpha()

# Create images for snake game
snake_head_img = pygame.transform.scale(SNAKE_HEAD_IMG, (GRASS_TILE_WIDTH + transform(5, WINDOW_WIDTH), GRASS_TILE_WIDTH + transform(5, WINDOW_HEIGHT))).convert_alpha()
snake_head_img_rect = snake_head_img.get_rect()
snake_head_left = snake_head_img.convert_alpha()
snake_head_right = pygame.transform.rotate(snake_head_img, 180).convert_alpha()
snake_head_up = pygame.transform.rotate(snake_head_img, -90).convert_alpha()
snake_head_down = pygame.transform.rotate(snake_head_img, 90).convert_alpha()
snake_head_left_rect = snake_head_left.get_rect()
snake_head_right_rect = snake_head_right.get_rect()
snake_head_up_rect = snake_head_up.get_rect()
snake_head_down_rect = snake_head_down.get_rect()

snake_body_img = pygame.transform.scale(SNAKE_BODY_IMG, (GRASS_TILE_WIDTH, GRASS_TILE_WIDTH)).convert_alpha()
snake_body_img_rect = snake_body_img.get_rect()

fruit_img = pygame.transform.scale(FRUIT_IMG, (GRASS_TILE_WIDTH, GRASS_TILE_WIDTH)).convert_alpha()
fruit_img_rect = fruit_img.get_rect()

# Loading fonts
ALLOY_FONT60 = pygame.font.Font('Fonts/alloy_ink.ttf', transform(60, WINDOW_HEIGHT))
ALLOY_FONT100 = pygame.font.Font('Fonts/alloy_ink.ttf', transform(100, WINDOW_HEIGHT))
ALLOY_FONT140 = pygame.font.Font('Fonts/alloy_ink.ttf', transform(140, WINDOW_HEIGHT))
snake_floor_coord = (WINDOW_WIDTH//2 -GRASS_TILE_TOTAL_LENGTH//2, WINDOW_HEIGHT//2 - GRASS_TILE_TOTAL_LENGTH//2)
def Snake():

	global current_page, snake_head_img_rect, snake_head_img, snake_floor_coord
	current_page = 'SNAKE GAME'
	
	press_permit = True
	
	cycle_no = 1

	score = 0
	
	gameover = False
	
	snake_dir = 'up'
	
	snake_head_img, snake_head_img_rect = snake_head_up, snake_head_up_rect
	
	snake_length = 3
	
	snake_array = [[NO_OF_TILES//2, NO_OF_TILES//2], [NO_OF_TILES//2, NO_OF_TILES//2 + 1], [NO_OF_TILES//2, NO_OF_TILES//2 + 2]]
	
	snake_floor = create_snake_floor()
	gameover_surface, yes_rect, no_rect = create_snake_gameover()
	
	yes_rect.topleft = yes_rect.left + WINDOW_WIDTH//2 - GRASS_TILE_TOTAL_LENGTH//2, yes_rect.top + WINDOW_HEIGHT//2 - GRASS_TILE_TOTAL_LENGTH//2
	no_rect.topleft = no_rect.left + WINDOW_WIDTH//2 - GRASS_TILE_TOTAL_LENGTH//2, no_rect.top + WINDOW_HEIGHT//2 - GRASS_TILE_TOTAL_LENGTH//2
	print(yes_rect.topleft, no_rect.topleft)
	
	DISPSURF.blit(blur_bg_img, blur_bg_img_rect)
	
	snake_floor_coord = (WINDOW_WIDTH//2 -GRASS_TILE_TOTAL_LENGTH//2, WINDOW_HEIGHT//2 - GRASS_TILE_TOTAL_LENGTH//2)
	
	border_rect = (DISPSURF, LEMON, (snake_floor_coord[0] - transform(10, WINDOW_WIDTH), snake_floor_coord[1] - transform(10, WINDOW_WIDTH), GRASS_TILE_TOTAL_LENGTH + transform(20, WINDOW_WIDTH), GRASS_TILE_TOTAL_LENGTH + transform(20, WINDOW_WIDTH)))
	
	fruit_coord = [random.randint(0, NO_OF_TILES - 1), random.randint(0, NO_OF_TILES - 1)]
	fruit_img_rect.topleft = fruit_coord[0] * GRASS_TILE_WIDTH + WINDOW_WIDTH//2 - GRASS_TILE_TOTAL_LENGTH//2, fruit_coord[1] * GRASS_TILE_WIDTH + WINDOW_HEIGHT//2 - GRASS_TILE_TOTAL_LENGTH//2
	while fruit_coord in snake_array:
		fruit_coord = [random.randint(0, NO_OF_TILES - 1), random.randint(0, NO_OF_TILES - 1)]
		fruit_img_rect.topleft = fruit_coord[0] * GRASS_TILE_WIDTH + WINDOW_WIDTH//2 - GRASS_TILE_TOTAL_LENGTH//2, fruit_coord[1] * GRASS_TILE_WIDTH + WINDOW_HEIGHT//2 - GRASS_TILE_TOTAL_LENGTH//2

	score_text = ALLOY_FONT100.render("SCORE", True, BLACK).convert_alpha()
	score_text_rect = score_text.get_rect()
	score_text_rect.center = (WINDOW_WIDTH//6.5, WINDOW_HEIGHT//2.5)


	score_value_text = ALLOY_FONT100.render(f"{score}", True, BLACK).convert_alpha()
	score_value_rect = score_value_text.get_rect()
	score_value_rect.center = (WINDOW_WIDTH//6.5, WINDOW_HEIGHT//2)
	
	esc_press = False

	while not gameover:
		FPS = 60 + score * 0.5
		
		for event in pygame.event.get():
			if event.type == QUIT:
				quit_game_sound.play()
				time.sleep(0.2)
				pygame.quit()
				sys.exit()
			elif event.type == MOUSEBUTTONDOWN:
				if back_button_img_rect.collidepoint(event.pos):
					button_click_sound.play()
					gameover = True
					
					esc_press = True

		if gameover:
			break

		snake_dir, press_permit, gameover = snake_direction(snake_dir, press_permit)

		if cycle_no % (20) == 0:
			snake_array, press_permit = snake_movement(snake_array, snake_dir, snake_length)
			
			DISPSURF.blit(blur_bg_img, blur_bg_img_rect)
			pygame.draw.rect(*border_rect)
			DISPSURF.blit(snake_floor, snake_floor_coord)
			DISPSURF.blit(back_button_img, back_button_img_rect)
			DISPSURF.blit(fruit_img, fruit_img_rect)
			snake_head_img_rect.topleft = snake_array[0][0] * GRASS_TILE_WIDTH + WINDOW_WIDTH//2 - GRASS_TILE_TOTAL_LENGTH//2, snake_array[0][1] * GRASS_TILE_WIDTH + WINDOW_HEIGHT//2 - GRASS_TILE_TOTAL_LENGTH//2
			DISPSURF.blit(snake_head_img, snake_head_img_rect)
			DISPSURF.blit(score_text, score_text_rect)
			DISPSURF.blit(score_value_text, score_value_rect)
			


			for i in range(1, snake_length):
				snake_body_img_rect.topleft = snake_array[i][0] * GRASS_TILE_WIDTH + WINDOW_WIDTH//2 - GRASS_TILE_TOTAL_LENGTH//2, snake_array[i][1] * GRASS_TILE_WIDTH + WINDOW_HEIGHT//2 - GRASS_TILE_TOTAL_LENGTH//2
				DISPSURF.blit(snake_body_img, snake_body_img_rect)

		# Gameover condition
		if snake_array[0][0] < 0 or snake_array[0][0] > NO_OF_TILES - 1 or snake_array[0][1] < 0 or snake_array[0][1] > NO_OF_TILES - 1:  
			gameover = True
			pygame.mixer.music.pause()
			boing_sound.play()
			if score < 250:
				sad_sound.play()
			else:
				yay_sound.play()
			time.sleep(0.5)
		for i in range(1, snake_length):
			if snake_array[0] == snake_array[i]:
				gameover = True
				pygame.mixer.music.pause()
				boing_sound.play()
				if score < 250:
					sad_sound.play()
				else:
					yay_sound.play()
				time.sleep(0.5)
		
		if snake_array[0] == fruit_coord:
			fruit_eat_sound.play()
			score += 10
			score_value_text = ALLOY_FONT100.render(f"{score}", True, BLACK)
			score_value_rect = score_value_text.get_rect()
			score_value_rect.center = (WINDOW_WIDTH//6.5, WINDOW_HEIGHT//2)

			snake_length += 1
			snake_array.append(list())

			fruit_coord = [random.randint(0, NO_OF_TILES - 1), random.randint(0, NO_OF_TILES - 1)]
			fruit_img_rect.topleft = fruit_coord[0] * GRASS_TILE_WIDTH + WINDOW_WIDTH//2 - GRASS_TILE_TOTAL_LENGTH//2, fruit_coord[1] * GRASS_TILE_WIDTH + WINDOW_HEIGHT//2 - GRASS_TILE_TOTAL_LENGTH//2
			while fruit_coord in snake_array:
				fruit_coord = [random.randint(0, NO_OF_TILES - 1), random.randint(0, NO_OF_TILES - 1)]
				fruit_img_rect.topleft = fruit_coord[0] * GRASS_TILE_WIDTH + WINDOW_WIDTH//2 - GRASS_TILE_TOTAL_LENGTH//2, fruit_coord[1] * GRASS_TILE_WIDTH + WINDOW_HEIGHT//2 - GRASS_TILE_TOTAL_LENGTH//2

			
		pygame.display.update()
		cycle_no +=1
		CLOCK.tick(FPS)
	
	if esc_press:
		return
	DISPSURF.blit(blur_bg_img, blur_bg_img_rect)
	DISPSURF.blit(score_text, score_text_rect)
	DISPSURF.blit(score_value_text, score_value_rect)
	pygame.draw.rect(*border_rect)
	DISPSURF.blit(gameover_surface, snake_floor_coord)
	
	pygame.display.update()
	
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				quit_game_sound.play()
				time.sleep(0.2)
				pygame.quit()
				sys.exit()
			elif event.type == pygame.MOUSEBUTTONDOWN:
				
				if yes_rect.collidepoint(event.pos):

					button_click_sound.play()
					pygame.mixer.music.play()
					Snake()
				elif no_rect.collidepoint(event.pos):
					button_click_sound.play()
					pygame.mixer.music.play()
					return

		
	
def snake_direction(snake_dir, press_permit):
	
	keys = pygame.key.get_pressed()
	if keys[K_UP] and snake_dir != 'down' and press_permit:
		snake_dir = 'up'
		press_permit = False
		
	
	if keys[K_LEFT] and snake_dir != 'right' and press_permit:
		snake_dir = 'left'
		press_permit = False
		
		
	if keys[K_RIGHT] and snake_dir != 'left' and press_permit:
		snake_dir = 'right'
		press_permit = False
		
		
	if keys[K_DOWN] and snake_dir != 'up' and press_permit:
		snake_dir = 'down'
		press_permit = False
	
	if keys[K_SPACE]:
		button_click_sound.play()
		while True:
			keys1 = pygame.key.get_pressed()
			if keys1[K_LCTRL]:
				break
			for event in pygame.event.get():
				if event.type == QUIT:
					quit_game_sound.play()
					time.sleep(0.2)
					pygame.quit()
					sys.exit()
				elif event.type == MOUSEBUTTONDOWN:
					if back_button_img_rect.collidepoint(event.pos):
						return snake_dir, press_permit, True
		
		
		
	return snake_dir, press_permit, False

def snake_movement(snake_array, snake_dir, snake_length):
	global snake_head_img, snake_head_img_rect
	
	press_permit = True
	blick_sound.play()
	for i in range(snake_length-1, 0, -1):# [10, 10] [10, 11] [10, 12] range(2,0) 2,1
		
		snake_array[i] = list(snake_array[i - 1]) #2 becomes 1 and 1 becomes zero
		
	
	
	if snake_dir == 'up':
		snake_array[0][1] -= 1
		snake_head_img, snake_head_img_rect = snake_head_up, snake_head_up_rect
	elif snake_dir == 'down':
		snake_array[0][1] += 1
		snake_head_img, snake_head_img_rect = snake_head_down, snake_head_down_rect
	elif snake_dir == 'left':
		snake_array[0][0] -= 1
		snake_head_img, snake_head_img_rect = snake_head_left, snake_head_left_rect
	elif snake_dir == 'right':
		snake_array[0][0] += 1
		snake_head_img, snake_head_img_rect = snake_head_right, snake_head_right_rect
	
	return snake_array, press_permit

def create_snake_floor():
	snake_floor = pygame.Surface((GRASS_TILE_TOTAL_LENGTH, GRASS_TILE_TOTAL_LENGTH))
	floor_left_coord = WINDOW_WIDTH//2 - GRASS_TILE_TOTAL_LENGTH//2
	floor_top_coord = WINDOW_HEIGHT//2 - GRASS_TILE_TOTAL_LENGTH//2
	for i in range(NO_OF_TILES):
		for j in range(NO_OF_TILES):
			blitting_rect = pygame.Rect(j * GRASS_TILE_WIDTH, i * GRASS_TILE_WIDTH, GRASS_TILE_WIDTH, GRASS_TILE_WIDTH)
			snake_floor.blit(dark_grass_img if (i+j)%2 == 0 else light_grass_img, blitting_rect)
	return snake_floor.convert_alpha()

def create_snake_gameover():
	surface = pygame.Surface((int(GRASS_TILE_TOTAL_LENGTH), int(GRASS_TILE_TOTAL_LENGTH)))
	gameover_text = ALLOY_FONT140.render('Game Over!', True, LEMON).convert_alpha()
	gameover_rect = gameover_text.get_rect()
	gameover_rect.center = GRASS_TILE_TOTAL_LENGTH//2, GRASS_TILE_TOTAL_LENGTH//5
	play_again_text = ALLOY_FONT100.render("Play again???", True, LEMON).convert_alpha()
	play_again_rect = play_again_text.get_rect()
	play_again_rect.center = GRASS_TILE_TOTAL_LENGTH//2, GRASS_TILE_TOTAL_LENGTH//2
	
	yes_text = ALLOY_FONT60.render('Yes', True, GREEN).convert_alpha()
	no_text = ALLOY_FONT60.render('No', True, RED).convert_alpha()

	yes_rect = yes_text.get_rect()
	no_rect = no_text.get_rect()
	
	yes_rect.center = GRASS_TILE_TOTAL_LENGTH//3, GRASS_TILE_TOTAL_LENGTH//1.5
	no_rect.center = GRASS_TILE_TOTAL_LENGTH * 2 //3, GRASS_TILE_TOTAL_LENGTH//1.5
	
	surface.blit(gameover_text, gameover_rect)
	surface.blit(play_again_text, play_again_rect)
	surface.blit(no_text, no_rect)
	surface.blit(yes_text, yes_rect)
	return surface.convert_alpha(), yes_rect, no_rect

if __name__ == '__main__':
    Snake()
