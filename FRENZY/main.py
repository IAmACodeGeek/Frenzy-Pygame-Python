# Imports
import os

import pygame, time, sys
from pygame.locals import * 
import random

import snake
import tic_tac_toe
# Import the database
from Database.variables import *
import csv

# Increase recursion limit
sys.setrecursionlimit(5000)

pygame.init()

def transform(value, respect_to):
	value = int(value / 1920 * WINDOW_WIDTH) if respect_to == WINDOW_WIDTH else int(value / 1080 * WINDOW_HEIGHT)
	return value

current_page = 'LOADING'

CLOCK = pygame.time.Clock()
# Create display screen
DISPSURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Frenzy!!!')

# Loading images
MAIN_MENU_IMG = pygame.image.load('Images/others/menu_img.png').convert_alpha()
BLUR_BG_IMG = pygame.image.load('Images/others/blurred bg img.jpg').convert_alpha()
PLAY_ARROW_IMG = pygame.image.load('Images/Wooden_imgs/play_arrow.png').convert_alpha()
LONG_DOUBLE_ARROW_IMG = pygame.image.load('Images/Wooden_imgs/long_double_arrow.png').convert_alpha()
BOARD_IMG = pygame.image.load('Images/Wooden_imgs/board.png').convert_alpha()
RECTANGLE_IMG = pygame.image.load('Images/Wooden_imgs/rectangle_button.png').convert_alpha()
CROSS_IMG = pygame.image.load('Images/Wooden_imgs/cross.png').convert_alpha()
SETTINGS_IMG = pygame.image.load('Images/Wooden_imgs/setting.png').convert_alpha()
INFO_IMG = pygame.image.load('Images/Wooden_imgs/info.png').convert_alpha()
SOUND_ON_IMG = pygame.image.load('Images/Wooden_imgs/sound_on.png').convert_alpha()
SOUND_OFF_IMG = pygame.image.load('Images/Wooden_imgs/sound_off.png').convert_alpha()
CHECK_ON_IMG = pygame.image.load('Images/Wooden_imgs/check_on.png').convert_alpha()
CHECK_OFF_IMG = pygame.image.load('Images/Wooden_imgs/check_off.png').convert_alpha()
BACK_IMG = pygame.image.load('Images/Wooden_imgs/back_button.png').convert_alpha()
SNAKE_GAME_IMG = pygame.image.load('Images/snake/snake.png').convert_alpha()
TIC_TAC_TOE_IMG = pygame.image.load('Images/tic tac toe/tic tac toe.png').convert_alpha()

TTT_BOARD_IMG = pygame.image.load('Images/tic tac toe/tic tac toe board.png').convert_alpha()
FRENZY_IMG = pygame.image.load('Images/frenzy/frenzy.png').convert_alpha()


# Creating certain images and rects
board_image = pygame.transform.scale(BOARD_IMG, (transform(1500, WINDOW_WIDTH), transform(1000, WINDOW_HEIGHT))).convert_alpha()
board_image_rect = board_image.get_rect()
board_image_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

# Loading fonts
ALLOY_FONT60 = pygame.font.Font('Fonts/alloy_ink.ttf', transform(60, WINDOW_HEIGHT))
ALLOY_FONT100 = pygame.font.Font('Fonts/alloy_ink.ttf', transform(100, WINDOW_HEIGHT))
ALLOY_FONT130 = pygame.font.Font('Fonts/alloy_ink.ttf', transform(130, WINDOW_HEIGHT))
ALLOY_FONT140 = pygame.font.Font('Fonts/alloy_ink.ttf', transform(140, WINDOW_HEIGHT))
BRUSH_FONT270 = pygame.font.Font('Fonts/brush.ttf', transform(270, WINDOW_HEIGHT))
CURSIVE_FONT270 = pygame.font.Font('Fonts/cursive.ttf', transform(270, WINDOW_HEIGHT))
ALLOY_FONT210 = pygame.font.Font('Fonts/cursive.ttf', transform(350, WINDOW_HEIGHT))
MODERN_FONT40 = pygame.font.Font('Fonts/Modern1.ttf', transform(40, WINDOW_HEIGHT))

# Loading sounds
button_click_sound = pygame.mixer.Sound('Sounds/button_click.wav')
quit_game_sound = pygame.mixer.Sound('Sounds/game_quit.wav')
in_the_forest = pygame.mixer.music.load('Sounds/in_the_forest.mp3')
boing_sound = pygame.mixer.Sound("Sounds/boing.mp3")
blick_sound = pygame.mixer.Sound("Sounds/movement sound.wav")
fruit_eat_sound = pygame.mixer.Sound('Sounds/fruit eat sound.wav')
yay_sound = pygame.mixer.Sound('Sounds/yay.mp3')
sad_sound = pygame.mixer.Sound('Sounds/sad.wav')
ammo_reload_sound = pygame.mixer.Sound('Sounds/ammo reload.mp3')
bullet_shoot_sound = blick_sound
explode_sound = pygame.mixer.Sound('Sounds/grenade explode.wav')
health_gain_sound = pygame.mixer.Sound('Sounds/health regain.wav')
win_sound = pygame.mixer.Sound('Sounds/win.wav')
lose_sound = pygame.mixer.Sound('Sounds/lose sound.wav')
player_hit_sound = pygame.mixer.Sound('Sounds/player hit sound.wav')
enemy_hit_sound = pygame.mixer.Sound('Sounds/enemy hit sound.wav')



# Play bg music
if MUSIC_ON:
	pygame.mixer.music.set_volume(1)
else:
	pygame.mixer.music.set_volume(0)

if SOUND_ON:
	button_click_sound.set_volume(1)
	quit_game_sound.set_volume(1)
	ammo_reload_sound.set_volume(1)
	bullet_shoot_sound.set_volume(1)
	explode_sound.set_volume(1)
	health_gain_sound.set_volume(1)
	win_sound.set_volume(1)
	lose_sound.set_volume(1)
	player_hit_sound.set_volume(1)
	enemy_hit_sound.set_volume(1)

else:
	button_click_sound.set_volume(0)
	quit_game_sound.set_volume(0)
	ammo_reload_sound.set_volume(0)
	bullet_shoot_sound.set_volume(0)
	explode_sound.set_volume(0)
	health_gain_sound.set_volume(0)
	win_sound.set_volume(0)
	lose_sound.set_volume(0)
	player_hit_sound.set_volume(0)
	enemy_hit_sound.set_volume(0)
pygame.mixer.music.play(-1)

# Create bg_img for the main menu
bg_img = pygame.transform.scale(MAIN_MENU_IMG, (WINDOW_WIDTH, WINDOW_HEIGHT + transform(100, WINDOW_HEIGHT))).convert_alpha()
bg_img_rect = bg_img.get_rect()
bg_img_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

# Create images for buttons

gameplay_button_img = pygame.transform.scale(LONG_DOUBLE_ARROW_IMG, (transform(900, WINDOW_WIDTH), transform(220, WINDOW_HEIGHT))).convert_alpha()
gameplay_button_img_rect = gameplay_button_img.get_rect()

quit_button_img = pygame.transform.scale(CROSS_IMG, (transform(100, WINDOW_WIDTH), transform(100, WINDOW_WIDTH))).convert_alpha()
quit_button_img_rect = quit_button_img.get_rect()

settings_button_img = pygame.transform.scale(SETTINGS_IMG, (transform(140, WINDOW_WIDTH), transform(140, WINDOW_WIDTH))).convert_alpha()
settings_button_img_rect = settings_button_img.get_rect()

info_button_img = pygame.transform.scale(INFO_IMG, (transform(140, WINDOW_WIDTH), transform(140, WINDOW_WIDTH))).convert_alpha()
info_button_img_rect = info_button_img.get_rect()

snake_game_img = pygame.transform.scale(SNAKE_GAME_IMG, (transform(500, WINDOW_WIDTH), transform(500, WINDOW_HEIGHT))).convert_alpha()
snake_game_img_rect = snake_game_img.get_rect()

tic_tac_toe_img = pygame.transform.scale(TIC_TAC_TOE_IMG, (transform(500, WINDOW_WIDTH), transform(500, WINDOW_HEIGHT))).convert_alpha()
tic_tac_toe_img_rect = tic_tac_toe_img.get_rect()

frenzy_img = pygame.transform.scale(FRENZY_IMG, (transform(475, WINDOW_WIDTH), transform(475, WINDOW_HEIGHT))).convert_alpha()
frenzy_rect = frenzy_img.get_rect()

back_button_img = pygame.transform.scale(BACK_IMG, (transform(140, WINDOW_WIDTH), transform(140, WINDOW_WIDTH))).convert_alpha()
back_button_img_rect = back_button_img.get_rect()

blur_bg_img = pygame.transform.scale(BLUR_BG_IMG, (WINDOW_WIDTH, WINDOW_HEIGHT + transform(100, WINDOW_HEIGHT))).convert_alpha()
blur_bg_img_rect = blur_bg_img.get_rect()

# Create texts

play_text = ALLOY_FONT100.render('Play!', True, LEMON).convert_alpha()
play_text_rect = play_text.get_rect()

title_text = CURSIVE_FONT270.render('FRENZY!', True, LEMON).convert_alpha()
title_text_rect = title_text.get_rect()

title_bg_text = CURSIVE_FONT270.render('FRENZY!', True, BLACK).convert_alpha()
title_bg_text_rect = title_bg_text.get_rect()



def quit_game():
	# Initialize the quit board
	
	
	# Text on the board
	quit_text1 = ALLOY_FONT100.render('Are you sure', True, LEMON).convert_alpha()
	quit_text1_rect = quit_text1.get_rect()
	quit_text1_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2-transform(220, WINDOW_HEIGHT))
	
	quit_text2 = ALLOY_FONT100.render('To exit the game???', True, LEMON).convert_alpha()
	quit_text2_rect = quit_text2.get_rect()
	quit_text2_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2- transform(70, WINDOW_HEIGHT))
	
	# Text for yes
	yes_text = ALLOY_FONT130.render('yes', True, GREEN).convert_alpha()
	yes_text_rect = yes_text.get_rect()
	yes_text_rect.center = (transform(700, WINDOW_WIDTH), WINDOW_HEIGHT//2+ transform(130, WINDOW_HEIGHT))
	
	#Text for no
	no_text = ALLOY_FONT140.render('no', True, RED).convert_alpha()
	no_text_rect = no_text.get_rect()
	no_text_rect.center = (transform(1200, WINDOW_HEIGHT), WINDOW_HEIGHT//2+ transform(130, WINDOW_HEIGHT))
	
	# Blitting the image and texts
	
	DISPSURF.blit(board_image, board_image_rect)
	
	DISPSURF.blit(quit_text1, quit_text1_rect)
	
	DISPSURF.blit(quit_text2, quit_text2_rect)
	
	DISPSURF.blit(yes_text, yes_text_rect)
	
	DISPSURF.blit(no_text, no_text_rect)
	
	# Update the screen
	pygame.display.update()
	
	
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				quit_game_sound.play()
				time.sleep(0.2)
				pygame.quit()
				sys.exit()
			elif event.type == MOUSEBUTTONDOWN:
				# Quit event
				if yes_text_rect.collidepoint(event.pos):
					quit_game_sound.play()
					time.sleep(0.2)
					return True
				
				# Cancel event
				elif no_text_rect.collidepoint(event.pos):
					button_click_sound.play()
					return False
				
				# Cancel event
				elif not board_image_rect.collidepoint(event.pos):
					button_click_sound.play()
					return False
					

def main_menu_load():
	# Initialize the images, rectangles, texts
	global current_page, bg_img, bg_img_rect, gameplay_button_img, gameplay_button_img_rect, quit_button_img, quit_button_img_rect, settings_button_img, settings_button_img_rect, info_button_img, info_button_img_rect, play_text, play_text_rect, title_text, title_text_rect, title_bg_text, title_bg_text_rect
	
	current_page = 'MAIN MENU'
	
	
	# Animation loop
	for i in range(TRANSITION_SCALE + 1):
		
		# Position the buttons
		gameplay_button_img_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT - i/TRANSITION_SCALE*(WINDOW_HEIGHT - transform(500, WINDOW_HEIGHT)) )
			
		quit_button_img_rect.center = (WINDOW_WIDTH - i/TRANSITION_SCALE*transform(100, WINDOW_WIDTH),  i/TRANSITION_SCALE*transform(100, WINDOW_HEIGHT))
		
		settings_button_img_rect.center = (i/TRANSITION_SCALE*transform(125, WINDOW_WIDTH), transform(750, WINDOW_HEIGHT))
		
		info_button_img_rect.center = (i/TRANSITION_SCALE*transform(125, WINDOW_WIDTH), transform(450, WINDOW_HEIGHT))
		
		#Position the texts
		
		play_text_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT - i/TRANSITION_SCALE*(WINDOW_HEIGHT - transform(500, WINDOW_HEIGHT)))
		
		title_text_rect.center = (WINDOW_WIDTH//2, i/TRANSITION_SCALE*transform(180, WINDOW_HEIGHT))
		title_bg_text_rect.center = (WINDOW_WIDTH//2-transform(20, WINDOW_WIDTH), i/TRANSITION_SCALE*transform(180, WINDOW_HEIGHT))
		
		main_menu_screen()
		
		
		# Update display
		pygame.display.update()

def main_menu_screen():
	# Blit the images
		DISPSURF.blit(bg_img, bg_img_rect)
		
		DISPSURF.blit(gameplay_button_img, gameplay_button_img_rect)
		
		DISPSURF.blit(quit_button_img, quit_button_img_rect)
		
		DISPSURF.blit(settings_button_img, settings_button_img_rect)
		
		DISPSURF.blit(info_button_img, info_button_img_rect)
		
		# Blit the texts
		DISPSURF.blit(play_text, play_text_rect)
		
		DISPSURF.blit(title_bg_text, title_bg_text_rect)

		DISPSURF.blit(title_text, title_text_rect)

def music():
	global MUSIC_ON, music_image, music_image_rect, check_image1, check_image1_rect
	MUSIC_ON = not MUSIC_ON
	
	# Open database file for reading
	readfile = open('Database/variables.py', 'r')
	lines = readfile.readlines()
	# Open same file for writing
	writefile = open('Database/variables.py', 'w')
	
	if MUSIC_ON:
		music_image = pygame.transform.scale(SOUND_ON_IMG, (transform(140, WINDOW_WIDTH), transform(140, WINDOW_WIDTH))).convert_alpha()
		check_image1= pygame.transform.scale(CHECK_ON_IMG, (transform(100, WINDOW_WIDTH), transform(100, WINDOW_WIDTH))).convert_alpha()
		pygame.mixer.music.set_volume(1)
		
		for i in range(len(lines)):
			if 'MUSIC_ON = ' in lines[i]:
				lines[i] = 'MUSIC_ON = True\n'
				break
	else:
		music_image = pygame.transform.scale(SOUND_OFF_IMG, (transform(140, WINDOW_WIDTH), transform(140, WINDOW_WIDTH))).convert_alpha()
		check_image1= pygame.transform.scale(CHECK_OFF_IMG, (transform(100, WINDOW_WIDTH), transform(100, WINDOW_WIDTH))).convert_alpha()
		pygame.mixer.music.set_volume(0)
		
		for i in range(len(lines)):
			if 'MUSIC_ON = ' in lines[i]:
				lines[i] = 'MUSIC_ON = False\n'
				break
	
	writefile.write(''.join(lines))
	readfile.close()
	writefile.close()
	DISPSURF.blit(check_image1, check_image1_rect)
	DISPSURF.blit(music_image,music_image_rect )
	pygame.display.update()

def sound():
	global SOUND_ON, check_image2
	
	SOUND_ON = not SOUND_ON
	
	readfile = open('Database/variables.py', 'r')
	lines = readfile.readlines()
	writefile = open('Database/variables.py', 'w')
	
	
	if SOUND_ON:
		check_image2 = pygame.transform.scale(CHECK_ON_IMG, (transform(100, WINDOW_WIDTH), transform(100, WINDOW_WIDTH))).convert_alpha()
		button_click_sound.set_volume(1)
		quit_game_sound.set_volume(1)
		for i in range(len(lines)):
			if 'SOUND_ON =' in lines[i]:
				lines[i] = 'SOUND_ON = True\n'
				break
	
	else:
		check_image2 = pygame.transform.scale(CHECK_OFF_IMG, (transform(100, WINDOW_WIDTH), transform(100, WINDOW_WIDTH))).convert_alpha()
		button_click_sound.set_volume(0)
		quit_game_sound.set_volume(0)
		for i in range(len(lines)):
			if 'SOUND_ON =' in lines[i]:
				lines[i] = 'SOUND_ON = False\n'
				break
	readfile.close()
	writefile.write(''.join(lines))
	writefile.close()
	DISPSURF.blit(check_image2,check_image2_rect)
	pygame.display.update()

def sound_menu():
	global check_image1, check_image2, check_image1_rect, check_image2_rect
	# sound menu board
	
	check_image1 = pygame.transform.scale(CHECK_ON_IMG, (transform(100, WINDOW_WIDTH), transform(100, WINDOW_WIDTH))) if MUSIC_ON else pygame.transform.scale(CHECK_OFF_IMG, (transform(100, WINDOW_WIDTH), transform(100, WINDOW_WIDTH))).convert_alpha()
	check_image2 = pygame.transform.scale(CHECK_ON_IMG, (transform(100, WINDOW_WIDTH), transform(100, WINDOW_WIDTH))) if SOUND_ON else pygame.transform.scale(CHECK_OFF_IMG, (transform(100, WINDOW_WIDTH), transform(100, WINDOW_WIDTH))).convert_alpha() 
	check_image1 = check_image1.convert_alpha()
	check_image2 = check_image2.convert_alpha()
	
	
	sound_and_music_text = ALLOY_FONT130.render('SOUNDS AND MUSIC', True, LEMON).convert_alpha()
	music_text = ALLOY_FONT100.render('MUSIC', True, LEMON).convert_alpha()
	sound_text = ALLOY_FONT100.render('SOUND', True, LEMON).convert_alpha()
	effects_text = ALLOY_FONT100.render('EFFECTS', True, LEMON).convert_alpha()
	
	sound_and_music_rect = sound_and_music_text.get_rect()
	music_rect = music_text.get_rect()
	sound_rect = sound_text.get_rect()
	effects_rect = effects_text.get_rect()
	check_image1_rect = check_image1.get_rect()
	check_image2_rect = check_image2.get_rect()
	
	sound_and_music_rect.center = (WINDOW_WIDTH//2, transform(225, WINDOW_HEIGHT))
	music_rect.center = (transform(750, WINDOW_WIDTH), transform(450, WINDOW_HEIGHT))
	sound_rect.center = (transform(750, WINDOW_WIDTH), transform(650, WINDOW_HEIGHT))
	effects_rect.center = (transform(750, WINDOW_WIDTH), transform(750, WINDOW_HEIGHT))
	check_image1_rect.center = (transform(1200, WINDOW_WIDTH), transform(450, WINDOW_HEIGHT))
	check_image2_rect.center = (transform(1200, WINDOW_WIDTH), transform(650, WINDOW_HEIGHT))
	
	DISPSURF.blit(board_image, board_image_rect)
	
	DISPSURF.blit(sound_and_music_text, sound_and_music_rect)
	DISPSURF.blit(music_text, music_rect)
	DISPSURF.blit(sound_text, sound_rect)
	DISPSURF.blit(effects_text, effects_rect)
	DISPSURF.blit(check_image1, check_image1_rect)
	DISPSURF.blit(check_image2, check_image2_rect)
	
	pygame.display.update()
	while True:
		flag = False
		for event in pygame.event.get():
			if event.type == QUIT:
				
				quit_game_sound.play()
				time.sleep(0.2)
				pygame.quit()
				sys.exit()
			elif event.type == MOUSEBUTTONDOWN:
				if check_image1_rect.collidepoint(event.pos):
					button_click_sound.play()
					music()
				elif check_image2_rect.collidepoint(event.pos):
					button_click_sound.play()
					sound()
				elif not board_image_rect.collidepoint(event.pos):
					flag = True
					button_click_sound.play()
		if flag:
			break
	main_menu_screen()
	DISPSURF.blit(music_image, music_image_rect)
	pygame.display.update()
	
def settings_menu():
	# Animation start
	
	global music_image, music_image_rect, sound_image, sound_image_rect
	if MUSIC_ON:
		music_image = pygame.transform.scale(SOUND_ON_IMG, (transform(140, WINDOW_WIDTH), transform(140, WINDOW_WIDTH))).convert_alpha()
	else:
		music_image = pygame.transform.scale(SOUND_OFF_IMG, (transform(140, WINDOW_WIDTH), transform(140, WINDOW_WIDTH))).convert_alpha()
	music_image_rect = music_image.get_rect()
	for i in range(1, 3):
		music_image_rect.center = (transform(125, WINDOW_WIDTH), transform(750-i/2*150, WINDOW_HEIGHT))
		main_menu_screen()
		DISPSURF.blit(music_image,music_image_rect )
		
		
		pygame.display.update()
	# Animation over
	
	
	
	while True:
		flag = False
		for event in pygame.event.get():
			if event.type == MOUSEBUTTONDOWN:
				if music_image_rect.collidepoint(event.pos):
					button_click_sound.play()
					sound_menu()
				else:
					button_click_sound.play()
					flag = True
			elif event.type == QUIT:
				quit_game_sound.play()
				time.sleep(0.2)
				pygame.quit()
				sys.exit()
		if flag:
			break
		
	# Closing animation
	for i in range(1, -1, -1):
		music_image_rect.center = (transform(125,WINDOW_WIDTH), transform(750-i/2*150, WINDOW_HEIGHT))
		main_menu_screen()
		DISPSURF.blit(music_image,music_image_rect )
		DISPSURF.blit(settings_button_img, settings_button_img_rect)
		pygame.display.update()
	
def Main_menu():
	
	if current_page != 'MAIN MENU':
		main_menu_load()
	
	# Game loop
	while True:
		for event in pygame.event.get():
			if event.type == MOUSEBUTTONDOWN:
				# Quit button clicked
				if quit_button_img_rect.collidepoint(event.pos):
					button_click_sound.play()
					if quit_game():
						pygame.quit()
						sys.exit()
					else:
						main_menu_screen()
				
				elif gameplay_button_img_rect.collidepoint(event.pos):
					button_click_sound.play()
					play_menu()
					
				
				elif settings_button_img_rect.collidepoint(event.pos):
					button_click_sound.play()
					settings_menu()
			elif event.type == QUIT:
				quit_game_sound.play()
				time.sleep(0.2)
				pygame.quit()
				sys.exit()
				
		
		# Update the display
		pygame.display.update()

def play_menu():
	global blur_bg_img_rect
	blur_bg_img_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

	
	play_menu_load()

	
	#DISPSURF.blit(quit_button_img, quit_button_img_rect)
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				quit_game_sound.play()
				time.sleep(0.2)
				pygame.quit()
				sys.exit()
			elif event.type == MOUSEBUTTONDOWN:
				if back_button_img_rect.collidepoint(event.pos):
					button_click_sound.play()
					Main_menu()
				
				elif snake_game_img_rect.collidepoint(event.pos):
					button_click_sound.play()
					snake.Snake()
					play_menu()
				
				elif tic_tac_toe_img_rect.collidepoint(event.pos):
					button_click_sound.play()
					tic_tac_toe.Tic_tac_toe()
					play_menu()
				elif frenzy_rect.collidepoint(event.pos):
					button_click_sound.play()
					game(1)
					play_menu()

		


def play_menu_load():
	global current_page, snake_game_img, snake_game_img_rect, back_button_img_rect, back_button_img, tic_tac_toe_img_rect, tic_tac_toe_img

	current_page = 'PLAY MENU'

	for i in range(TRANSITION_SCALE + 1):
		snake_game_img_rect.center = (WINDOW_WIDTH//4, (WINDOW_HEIGHT//2 // TRANSITION_SCALE) * i)
		tic_tac_toe_img_rect.center = (WINDOW_WIDTH//2, (WINDOW_HEIGHT//2 // TRANSITION_SCALE) * i)
		frenzy_rect.center = (WINDOW_WIDTH//4 * 3, (WINDOW_HEIGHT//2 // TRANSITION_SCALE) * i)
		back_button_img_rect.center = (WINDOW_WIDTH - WINDOW_WIDTH//10 // TRANSITION_SCALE * i, WINDOW_HEIGHT//10 // TRANSITION_SCALE * i)
		
		play_menu_screen()

		pygame.display.update()

def play_menu_screen():
	DISPSURF.blit(blur_bg_img, blur_bg_img_rect)
	DISPSURF.blit(snake_game_img, snake_game_img_rect)
	DISPSURF.blit(tic_tac_toe_img, tic_tac_toe_img_rect)
	DISPSURF.blit(frenzy_img, frenzy_rect)
	DISPSURF.blit(back_button_img, back_button_img_rect)

def main():
	pygame.init()
	
	Main_menu()


class Enemy(pygame.sprite.Sprite):

	def __init__(self, pos_x, pos_y, img_scale, x_vel, vision_width, vision_height, walk_distance):
		pygame.sprite.Sprite.__init__(self)

		self.x, self.y = pos_x, pos_y

		self.image_scale = img_scale
		
		self.alive = True

		self.x_speed = x_vel
		self.y_speed = 0

		self.health = 100
		self.max_health = 100

		# Load the animation sprite sheets
		self.animation_list = []
		for i in range(len(os.listdir('Images/frenzy/enemy'))):
			img = pygame.image.load(f'Images/frenzy/enemy/enemy{i}.png')
			img = pygame.transform.scale(img, (TILESIZE, TILESIZE)).convert_alpha()
			self.animation_list.append(img)
		
		# Variable to check which animation image is currently required
		self.animation_phase = 0

		self.image = self.animation_list[self.animation_phase]
		self.rect = self.image.get_rect()
		self.rect.center = self.x, self.y
		self.width, self.height = self.image.get_width(), self.image.get_height()

		# 1 for right -1 for left
		self.direction = 1

		# for the enemy to change directions after certain distance
		self.move_counter = 0

		# To check if the enemy is moving or still
		self.is_idle = False
		# Counter to prevent the enemy from remaining idle forever
		self.idle_counter = 0

		# rect to handle the vision of the enemy
		self.vision_width, self.vision_height = vision_width, vision_height

		self.vision_rect = pygame.Rect(pos_x, pos_y, self.vision_width * self.direction, self.vision_height)

		# To limit the speed of shooting
		self.shoot_cooldown = 0

		# To reverse direction 
		self.walk_distance = walk_distance

		self.mirror_img = False

	def check_alive(self):
		if self.health <= 0:
			self.health = 0
			self.x_speed = 0
			self.alive = False
			

	def update(self):
		self.ai()
		if self.alive:
			self.check_alive()
		
		else: # kill animation
			
			if self.animation_phase >= len(os.listdir('Images/frenzy/enemy')):
				self.kill()
				player.kill_count += 1
				return
			else:
				self.animation_phase += 1
			self.image = self.animation_list[self.animation_phase-1]
			self.rect = self.image.get_rect()
			self.rect.centerx = self.x
			self.rect.top = self.y
			

		self.draw()
	
	def bullet_shoot(self):
		if self.shoot_cooldown == 0:
			self.shoot_cooldown = 20
			bullet = Bullet(self.rect.centerx + 0.7 * self.rect.size[0] * self.direction, self.rect.centery, self.direction)
			bullet_group.add(bullet)
		self.shoot_cooldown -= 1
		
			

	def ai(self):
		# Check if the player and the enemy are alive
		if self.alive and player.alive:
			# to randomly make the enemy become idle
			if self.is_idle == False and random.randint(1, 200) == 1:
				self.is_idle = True
				self.idle_counter = 50
			
			# Shoot if the player is within sight
			if self.vision_rect.colliderect(player.rect):
				self.bullet_shoot()
				
			else:
				# move the enemy if it is not idle
				if self.is_idle == False:
					if self.direction == 1:
						self.move_right = True
					else:
						self.move_right = False
					self.move_left = not self.move_right

					
					
					self.move_counter += 1
					
					# Reverse the direction
					if self.move_counter > self.walk_distance:
						self.direction *= -1
						self.move_right = not self.move_right
						self.move_left = not self.move_left
						self.move_counter = 0
					self.update_pos()
				# If enemy is idle
				else:
					self.idle_counter -= 1
					if self.idle_counter == 0:
						self.is_idle = False
		# Update the vision along with the enemy
		self.vision_rect.center = self.rect.centerx + self.vision_rect.width / 2 * self.direction + self.width//2 * self.direction, self.rect.centery

		# update scrolling of the enemies
		self.rect.x += screen_scroll

	def update_pos(self):
		dx, dy = 0, 0 # Variables to handle change in player movements

		dx = self.x_speed * self.direction

		# Whether or not flip the image
		self.mirror_img = self.move_right

		self.y_speed += GRAVITY

		dy = self.y_speed
		if self.y_speed > 10:
			self.y_speed = 10

		for tile in game_world.obstacles:
			#check for y collision
			if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
				#check for top collision
				if self.y_speed < 0:
					self.y_speed = 0
					dy = tile[1].bottom - self.rect.top
				elif self.y_speed >= 0:
					self.y_speed = 0
					self.in_air = False
					dy = tile[1].top - self.rect.bottom
			#check for x collision
			if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height//2):
				dx = 0
				# Reverse direction if enemy hits wall
				self.direction *= -1
				self.move_counter = 0
				break
		# Update the player positions
		self.rect.x += dx
		self.rect.y += dy
		self.x, self.y = self.rect.x, self.rect.y
	
	def draw(self):
		DISPSURF.blit(pygame.transform.flip(self.image, self.mirror_img, False), self.rect)
		
		


class Player(pygame.sprite.Sprite):

	
	def __init__(self, pos_x, pos_y, img_scale, x_vel, animation_time, bullet_count, grenade_count):
		pygame.sprite.Sprite.__init__(self)

		# Position of the player
		self.x = pos_x
		self.y = pos_y
		

		# To scale the imported player image
		self.image_scale = img_scale

		self.animation = []
		self.animation_phase = 0

		self.action = 1 # o for idle, 1 for running and 2 for jumping
		
		movements = ['idle', 'run', 'jump', 'die']
		for i in movements:
			list = []
			for j in range(len(os.listdir(f'Images/frenzy/{i}'))):
				img = pygame.image.load(f'Images/frenzy/{i}/{j}.png')
				img = pygame.transform.scale(img, (int(img.get_width() * self.image_scale), int(img.get_height() * self.image_scale))).convert_alpha()
				list.append(img)
			self.animation.append(list)
		
		self.image = self.animation[self.action][self.animation_phase]
		self.rect = self.image.get_rect()
		self.rect.center = self.x, self.y
		self.width, self.height = self.image.get_width(), self.image.get_height()

		self.animation_time = animation_time

		self.move_left, self.move_right, self.jump = False, False, False

		self.x_speed = x_vel
		self.y_speed = 0
		

		self.direction = 1
		self.mirror_img = False

		self.in_air = True

		self.health = 100
		self.max_health = 100

		self.shoot = False
		self.shoot_cooldown = 0

		self.grenade = False
		self.grenade_cooldown = 0

		self.ow_cooldown = 3

		self.grenade_count = grenade_count
		self.bullet_count = bullet_count

		self.alive = True

		self.health_bar = HealthBar(WINDOW_WIDTH//30, 10, self.health, self.max_health, self.max_health * 2, 30)

		self.kill_count = 0
		self.total_enemy = 0

		# Time to handle animations
		self.time = pygame.time.get_ticks()

	def check_win(self):
		if self.rect.right + bg_scroll > (COLS-1) * TILESIZE and self.kill_count >= 3/4 * self.total_enemy:
			# del player_group, enemy_group, world_map, game_world, 
			game(LEVEL + 1)

	def blit_player(self):
		DISPSURF.blit(pygame.transform.flip(self.image, self.mirror_img, False), self.rect)
		self.health_bar.draw(self.health)

	def player_pos_update(self):
        
		dx, dy = 0, 0 # Variables to handle change in player movements
		screen_scroll = 0

		if self.move_left:
			dx = -self.x_speed
			self.direction = -1
			self.mirror_img = True
			
		if self.move_right:
			dx = self.x_speed
			self.direction = 1
			self.mirror_img = False

		if self.jump:
			if not self.in_air:
				self.y_speed = -15
			self.jump = False
			self.in_air = True

		if self.in_air:
			self.action = 2
		elif self.move_left or self.move_right:
			self.action = 1
		else:
			self.action = 0
		
		if self.shoot:
			self.bullet_shoot()
		elif self.grenade:
			self.grenade_launch()

		self.y_speed += GRAVITY

		dy = self.y_speed
		if self.y_speed > 10:
			self.y_speed = 10

		global bg_scroll
		for tile in game_world.obstacles:
			#check for x collision
			if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
				dx = 0
			#check for y collision
			if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
				#check for top collision
				if self.y_speed < 0:
					self.y_speed = 0
					dy = tile[1].bottom - self.rect.top
				elif self.y_speed >= 0:
					self.y_speed = 0
					self.in_air = False
					dy = tile[1].top - self.rect.bottom
		if self.rect.x + dx <= 0 :
			dx = 0
		
		elif self.rect.x + bg_scroll > COLS * TILESIZE - TILESIZE:
			dx = 0 if dx > 0 else dx
			
		if pygame.sprite.spritecollide(self, enemy_group, False):
			self.health -= 0.5
			if self.ow_cooldown == 0:
				player_hit_sound.play()
				self.ow_cooldown = 100
			self.ow_cooldown -= 1
		else:
			if self.ow_cooldown > 3:
				self.ow_cooldown = 3


				
		
		# Update the player positions
		self.rect.x += dx
		self.rect.y += dy
		
		# Update the scrolling
		if (self.rect.right > WINDOW_WIDTH - SCROLL_START_DIST and not (bg_scroll + self.rect.x > COLS * TILESIZE - SCROLL_START_DIST)) or (self.rect.left < SCROLL_START_DIST and player.rect.x + bg_scroll - SCROLL_START_DIST > 0):
			self.rect.x -= dx
			screen_scroll = -dx
			
			bg_scroll -= screen_scroll
		return screen_scroll
	
	def grenade_launch(self):
		if self.grenade_cooldown == 0 and self.grenade_count > 0:
			self.grenade_cooldown = 50 
			grenade = Grenade(self.rect.centerx + 0.7 * self.rect.size[0] * self.direction, self.rect.centery - 0.7 * self.rect.size[1], self.direction)
			grenade_group.add(grenade)
			self.grenade_count -= 1
	
	def bullet_shoot(self):
		if self.shoot_cooldown == 0 and self.bullet_count > 0:
			self.shoot_cooldown = 20
			bullet = Bullet(self.rect.centerx + 0.8 * self.rect.size[0] * self.direction, self.rect.centery, self.direction)
			bullet_group.add(bullet)
			self.bullet_count -= 1
		

        
	def update(self):
		# if player is alive
		self.check_win()
		global screen_scroll
		if self.alive:
			screen_scroll = self.player_pos_update()
			self.change_animation()
			if self.shoot_cooldown > 0:
				self.shoot_cooldown -= 1
			if self.grenade_cooldown > 0:
				self.grenade_cooldown -= 1
			self.check_alive()

		else: # death animation
			if self.die_cooldown == 0:
				
				self.action = len(self.animation) - 1
				self.die_cooldown = 50
				self.image = self.animation[self.action][self.animation_phase]
				
				if self.animation_phase == len(self.animation[self.action]) - 1:
					self.kill()
				self.animation_phase += 1
			
			self.die_cooldown -= 1
		

		self.blit_player()

	def check_alive(self):
		if self.health <= 0 or self.rect.top >= WINDOW_HEIGHT:
			self.alive = False
			lose_sound.play()
			
			self.animation_phase = 0
		else:
			self.die_cooldown = 50

	def change_animation(self):
		if self.in_air:
			self.image = self.animation[self.action][0]
			return
		latest_time = pygame.time.get_ticks()
		if latest_time - self.time > self.animation_time[self.action]:
			self.time = latest_time
			self.animation_phase = (self.animation_phase + 1) % len(self.animation[self.action])
			self.image = self.animation[self.action][self.animation_phase]

class Bullet(pygame.sprite.Sprite):
	def __init__(self, x, y, direction):
		pygame.sprite.Sprite.__init__(self)

		self.x_speed = player.x_speed * 3
		
		self.image = bullet_img
		self.rect = self.image.get_rect()
		self.rect.center = x, y
		
		self.direction = direction
		bullet_shoot_sound.play()
	
	def update(self):
		# Move the bullet
		self.rect.x += self.direction * self.x_speed + screen_scroll

		# Check if the bullet left the screen
		if self.rect.centerx > WINDOW_WIDTH or self.rect.centerx < 0:
			# inbuilt method to delete sprites
			self.kill()
		for tile in game_world.obstacles:
			if tile[1].colliderect(self.rect):
				self.kill()
		# Check for collision with player and enemies
		for enemy in enemy_group:
			if pygame.sprite.spritecollide(enemy, bullet_group, False):
				if enemy.alive:
					self.kill()
					enemy.health -= 100/2.9
					enemy_hit_sound.play()
		if pygame.sprite.spritecollide(player, bullet_group, False):
			player.health -= 6
			if player.ow_cooldown == 0:
				player_hit_sound.play()
				player.ow_cooldown = 3
			player.ow_cooldown -= 1
			self.kill()

class Itembox(pygame.sprite.Sprite):

	def __init__(self, item_type, x, y, count):
		pygame.sprite.Sprite.__init__(self)

		self.item_type = item_type

		self.image = item_boxes[self.item_type]

		self.rect = self.image.get_rect()
		self.rect.topleft = x, y

		self.count = count

	def update(self):
		if pygame.sprite.collide_rect(self, player):
			if self.item_type == "Health":
				player.health += self.count
				health_gain_sound.play()
				if player.health > player.max_health:
					player.health = player.max_health
			elif self.item_type == "Grenade":
				player.grenade_count += self.count
				ammo_reload_sound.play()
			elif self.item_type == "Bullet":
				player.bullet_count += self.count
				ammo_reload_sound.play()
			self.kill()
		self.rect.x += screen_scroll

class Grenade(pygame.sprite.Sprite):
	def __init__(self, x, y, direction):

		pygame.sprite.Sprite.__init__(self)
		self.x_speed = player.x_speed * 1.5
		self.y_speed = -12
		self.timer = 100
		self.image = grenade_img
		self.rect = self.image.get_rect()
		self.rect.center = x, y
		self.direction = direction
		self.width, self.height = self.image.get_width(), self.image.get_height()
		bullet_shoot_sound.play()
	
	def update(self):
		self.y_speed += GRAVITY
		dx = self.x_speed * self.direction
		dy = self.y_speed
		
		for tile in game_world.obstacles:
			#check for x collision
			if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
				self.direction *= -1
				dx = self.x_speed * self.direction
			#check for y collision
			if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
				
				#check for top collision
				if self.y_speed < 0:
					self.y_speed = 0
					dy = tile[1].bottom - self.rect.top
				elif self.y_speed >= 0:
					self.y_speed = 0
					self.x_speed = 0
					self.in_air = False
					dy = tile[1].top - self.rect.bottom
		self.rect.centerx += dx
		self.rect.centery += dy
		if self.rect.centerx > WINDOW_WIDTH or self.rect.centerx < 0:
			self.y_speed = 0
			self.direction *= -1
			dx = self.x_speed * self.direction
		self.timer -= 1
		if self.timer <= 0:
			self.kill()
			explosion = Explosion(self.rect.centerx, self.rect.centery, 0.1)
			explosion_group.add(explosion)
			# do damage
			
			if abs(self.rect.centerx - player.rect.centerx) < TILESIZE * 2 and abs(self.rect.centery - player.rect.centery) < TILESIZE * 2:
				player.health -= 50
			for enemy in enemy_group:
				if abs(self.rect.centerx - enemy.rect.centerx) < TILESIZE * 2 and abs(self.rect.centery - enemy.rect.centery) < TILESIZE * 2:
					enemy.health -= 100
		self.rect.x += screen_scroll

			
class Explosion(pygame.sprite.Sprite):
	def __init__(self, x, y, image_scale):
		pygame.sprite.Sprite.__init__(self)
		self.animation_list = []
		self.animation_index = 0
		self.image_scale = image_scale
		for i in range(len(os.listdir('Images/frenzy/explosion'))):
			img = pygame.image.load(f'Images/frenzy/explosion/exp{i}.png')
			img = pygame.transform.scale(img, (img.get_width() * self.image_scale, img.get_height() * self.image_scale)).convert_alpha()
			self.animation_list.append(img)
		self.image = self.animation_list[self.animation_index]
		self.rect = self.image.get_rect()
		self.x, self.y = x, y
		self.rect.centerx = self.x
		self.rect.bottom = self.y
		self.counter = 0
		self.cooldown = 4
		explode_sound.play()

	def update(self):
		self.counter += 1
		if self.counter > self.cooldown:
			self.counter = 0
			self.animation_index += 1
			if self.animation_index >= len(os.listdir('Images/frenzy/explosion')):
				self.kill()
				return
			self.image = self.animation_list[self.animation_index]
			self.rect = self.image.get_rect()
			self.rect.centerx = self.x
			self.rect.bottom = self.y
		self.x += screen_scroll


class HealthBar:
	def __init__(self, x, y, health, max_health, width, height):
		self.x = x
		self.y = y
		self.health = health
		self.max_health = max_health
		self.border_width = 1
		self.width, self.height = width, height
		self.max_rect = (self.x - self.border_width, self.y - self.border_width, self.width + 2 * self.border_width, self.height + 2 * self.border_width)

	def draw(self, health):
		self.health = health
		pygame.draw.rect(DISPSURF, RED, self.max_rect)
		pygame.draw.rect(DISPSURF, GREEN, (self.x, self.y, self.health / self.max_health * self.width, self.height))
		pygame.draw.rect(DISPSURF, BLACK, self.max_rect, width = self.border_width)

def load(level):
    global world_map
    if f'{level}.csv' in os.listdir('Database/Levels'):
        with open(f'Database/Levels/{level}.csv', 'r', newline = '') as readfile:
            reader = csv.reader(readfile, delimiter = ',')
            rows = []
            for row in reader:
                row = list([int(i) for i in row])
                rows.append(row)
            world_map = rows
    

class World:
	def __init__(self):
		self.obstacles = []
	def process(self, data):
		total_enemies = 0
		for y, row in enumerate(data):
			for x, tile in enumerate(row):
				if tile >= 0:
					img = all_tiles[tile]
					img_rect = img.get_rect()
					img_rect.x = x * TILESIZE
					img_rect.y = y * TILESIZE
					tile_data = img, img_rect
					if tile >= 0 and tile <= 7:
						self.obstacles.append(tile_data)
					elif tile == 12:
						player = Player(x * TILESIZE, y * TILESIZE, 0.55, 5, (150, 120 , 350), 25, 8)#0.7, 5, (150, 120, 350), 20, 3)
						
					elif tile == 11:
						enemy = Enemy(x * TILESIZE, y * TILESIZE, 0.175, 1, TILESIZE * 3, TILESIZE, 4 * TILESIZE)#0.175, 1, 200, 50, 100)
						enemy_group.add(enemy)
						total_enemies += 1
					elif tile == 8:
						item_box = Itembox('Bullet', x * TILESIZE, y * TILESIZE, 6)
						item_box_group.add(item_box)
					elif tile == 9:
						item_box = Itembox('Grenade', x * TILESIZE, y * TILESIZE, 5)
						item_box_group.add(item_box)
					elif tile == 10:
						item_box = Itembox('Health', x * TILESIZE, y * TILESIZE, 25)
						item_box_group.add(item_box)
		return player, total_enemies
	
	def draw_and_scroll(self):
		for tile in self.obstacles:
			# Update screen scrolling
			tile[1].x += screen_scroll
			DISPSURF.blit(tile[0], tile[1])


boy_bg_img = pygame.image.load('Images/level loader/bg.png')
boy_bg_img = pygame.transform.scale(boy_bg_img, (WINDOW_WIDTH, WINDOW_HEIGHT)).convert_alpha()
def draw_bg():
	for i in range(3):
		DISPSURF.blit(boy_bg_img, (i * WINDOW_WIDTH - bg_scroll, 0))



def game(level):
	global item_boxes, all_tiles, grenade_img, bullet_img, health_box_img, grenade_box_img, bullet_box_img, health_box_img, game_world, world_map, item_box_group, bullet_group, player, enemy, grenade_group, explosion_group, enemy_group, TILESIZE, player_group, LEVEL, ROWS, COLS, TILE_TYPES, GRAVITY, SCROLL_START_DIST, screen_scroll, bg_scroll
	
	# Initialize all names
	
	GRAVITY = 0.75

	gameover = False
	
	LEVEL = level
	ROWS = 20
	COLS = 100
	TILESIZE = WINDOW_HEIGHT // ROWS
	TILE_TYPES = 13
	SCROLL_START_DIST = 350
	screen_scroll, bg_scroll = 0, 0

	bullet_group = pygame.sprite.Group()
	grenade_group = pygame.sprite.Group()
	explosion_group = pygame.sprite.Group()
	player_group = pygame.sprite.Group()
	enemy_group = pygame.sprite.Group()
	item_box_group = pygame.sprite.Group()
		
	# Create texts
	ammo_text = MODERN_FONT40.render('AMMO :  ', True, BLACK).convert_alpha()
	grenade_text = MODERN_FONT40.render('GRENADE :  ', True, BLACK).convert_alpha()

	ammo_count_posy = WINDOW_HEIGHT//20
	grenade_count_posy = WINDOW_HEIGHT//12

	world_map = [[-1] * COLS for i in range(ROWS)]

	
	all_tiles = []
	for i in range(TILE_TYPES):
		file_type = 'jpg' if i < 8 else 'png'
		img = pygame.image.load(f'Images/level loader/all tiles/{i}.{file_type}')
		img = pygame.transform.scale(img, (TILESIZE, TILESIZE)).convert_alpha()
		all_tiles.append(img)

	BULLET_IMG = pygame.image.load('Images/frenzy/bullet.png')
	bullet_img = pygame.transform.scale(BULLET_IMG, (transform(20, WINDOW_WIDTH), transform(20, WINDOW_HEIGHT))).convert_alpha()

	grenade_box_img = pygame.transform.scale(pygame.image.load('Images/level loader/all tiles/9.png'), (TILESIZE, TILESIZE)).convert_alpha()
	bullet_box_img = pygame.transform.scale(pygame.image.load('Images/level loader/all tiles/8.png'), (TILESIZE, TILESIZE)).convert_alpha()
	health_box_img = pygame.transform.scale(pygame.image.load('Images/level loader/all tiles/10.png'), (TILESIZE, TILESIZE)).convert_alpha()

	item_boxes = {
	'Health' : health_box_img,
	'Grenade' : grenade_box_img,
	'Bullet' : bullet_box_img
	}
	grenade_img = pygame.image.load('Images/frenzy/grenade.png').convert_alpha()
	grenade_img = pygame.transform.scale(grenade_img, (30, 25))


	# Load world
	load(level)

	game_world = World()
	player, player.total_enemy = game_world.process(world_map)
	player_group.add(player)

	global button_click_sound, quit_game_sound, ammo_reload_sound, bullet_shoot_sound, explode_sound, health_gain_sound, win_sound
	if SOUND_ON:
		button_click_sound.set_volume(1)
		quit_game_sound.set_volume(1)
		ammo_reload_sound.set_volume(1)
		bullet_shoot_sound.set_volume(1)
		explode_sound.set_volume(1)
		health_gain_sound.set_volume(1)
		win_sound.set_volume(1)
		lose_sound.set_volume(1)
		player_hit_sound.set_volume(1)
		enemy_hit_sound.set_volume(1)

	else:
		button_click_sound.set_volume(0)
		quit_game_sound.set_volume(0)
		ammo_reload_sound.set_volume(0)
		bullet_shoot_sound.set_volume(0)
		explode_sound.set_volume(0)
		health_gain_sound.set_volume(0)
		win_sound.set_volume(0)
		lose_sound.set_volume(0)
		player_hit_sound.set_volume(0)
		enemy_hit_sound.set_volume(0)


	while not gameover:
		CLOCK.tick(60)
		for event in pygame.event.get():
			if event.type == QUIT:
				quit_game_sound.play()
				time.sleep(0.2)
				pygame.quit()
				sys.exit()
			elif event.type == KEYDOWN:
				if event.key == K_LEFT:
					player.move_left = True
				elif event.key == K_RIGHT:
					player.move_right = True
				elif event.key == K_UP:
					player.jump = True
				elif event.key == K_SPACE:
					player.shoot = True
				elif event.key == K_LCTRL:
					player.grenade = True
				
				elif event.key == K_ESCAPE:
					gameover = True

			elif event.type == KEYUP:
				if event.key == K_LEFT:
					player.move_left = False
				elif event.key == K_RIGHT:
					player.move_right = False
				elif event.key == K_SPACE:
					player.shoot = False
				elif event.key == K_LCTRL:
					player.grenade = False

		if not player.alive:
			surface, yes_rect, no_rect = snake.create_snake_gameover()
			yes_rect.topleft = yes_rect.left + WINDOW_WIDTH//2 - snake.GRASS_TILE_TOTAL_LENGTH//2, yes_rect.top + WINDOW_HEIGHT//2 - snake.GRASS_TILE_TOTAL_LENGTH//2
			no_rect.topleft = no_rect.left + WINDOW_WIDTH//2 - snake.GRASS_TILE_TOTAL_LENGTH//2, no_rect.top + WINDOW_HEIGHT//2 - snake.GRASS_TILE_TOTAL_LENGTH//2
			DISPSURF.blit(surface, snake.snake_floor_coord)
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
							game(LEVEL)
						elif no_rect.collidepoint(event.pos):
							button_click_sound.play()
							pygame.mixer.music.play()
							return
							

				if gameover:
					break


		draw_bg()
		
		bullet_group.update()
		grenade_group.update()
		explosion_group.update()
		enemy_group.update()
		player_group.update()
		item_box_group.update()
		game_world.draw_and_scroll()
		bullet_group.draw(DISPSURF)
		grenade_group.draw(DISPSURF)
		explosion_group.draw(DISPSURF)
		
		
		item_box_group.draw(DISPSURF)
		
		DISPSURF.blit(ammo_text, (WINDOW_WIDTH//30, ammo_count_posy))
		DISPSURF.blit(grenade_text, (WINDOW_WIDTH//30, grenade_count_posy))

		#draw Ammo count
		for i in range(player.grenade_count):
			DISPSURF.blit(bullet_img, (200 + i * 20, grenade_count_posy + bullet_img.get_height()//1.5))
		for i in range(player.bullet_count):
			DISPSURF.blit(bullet_img, (200 + i * 20, ammo_count_posy + bullet_img.get_height()//1.5))

		pygame.display.update()



if __name__ == '__main__':
	main()
	
