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

TIC_TAC_TOE_IMG = pygame.image.load('Images/tic tac toe/tic tac toe.png').convert_alpha()
TTT_BOARD_IMG = pygame.image.load('Images/tic tac toe/tic tac toe board.png').convert_alpha()
CROSS_IMG = pygame.image.load('Images/Wooden_imgs/cross.png').convert_alpha()
CHECK_ON_IMG = pygame.image.load('Images/Wooden_imgs/check_on.png').convert_alpha()
CHECK_OFF_IMG = pygame.image.load('Images/Wooden_imgs/check_off.png').convert_alpha()

NO_OF_TILES = 17
GRASS_TILE_TOTAL_LENGTH = WINDOW_HEIGHT//1.2
GRASS_TILE_WIDTH = GRASS_TILE_TOTAL_LENGTH//NO_OF_TILES
GRASS_TILE_TOTAL_LENGTH = NO_OF_TILES * GRASS_TILE_WIDTH
TTT_TOTAL_LENGTH = GRASS_TILE_TOTAL_LENGTH + transform(150, WINDOW_WIDTH)
NEW_TTT_TOTAL_LENGTH = TTT_TOTAL_LENGTH + transform(50, WINDOW_WIDTH)

ALLOY_FONT100 = pygame.font.Font('Fonts/alloy_ink.ttf', transform(100, WINDOW_HEIGHT))
ALLOY_FONT130 = pygame.font.Font('Fonts/alloy_ink.ttf', transform(130, WINDOW_HEIGHT))

# Loading sounds
button_click_sound = pygame.mixer.Sound('Sounds/button_click.wav')
quit_game_sound = pygame.mixer.Sound('Sounds/game_quit.wav')
in_the_forest = pygame.mixer.music.load('Sounds/in_the_forest.mp3')
boing_sound = pygame.mixer.Sound("Sounds/boing.mp3")
blick_sound = pygame.mixer.Sound("Sounds/movement sound.wav")
fruit_eat_sound = pygame.mixer.Sound('Sounds/fruit eat sound.wav')
yay_sound = pygame.mixer.Sound('Sounds/yay.mp3')
sad_sound = pygame.mixer.Sound('Sounds/sad.wav')

ttt_board_img = pygame.transform.scale(TTT_BOARD_IMG, (NEW_TTT_TOTAL_LENGTH, NEW_TTT_TOTAL_LENGTH)).convert_alpha()
ttt_board_img_rect = ttt_board_img.get_rect()
ttt_board_img_rect.center = WINDOW_WIDTH//2, WINDOW_HEIGHT//2

cross_img = pygame.transform.scale(CROSS_IMG, (TTT_TOTAL_LENGTH//5, TTT_TOTAL_LENGTH//5))
o_img = pygame.transform.scale(CHECK_ON_IMG, (TTT_TOTAL_LENGTH//5, TTT_TOTAL_LENGTH//5))

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

back_button_img = pygame.transform.scale(BACK_IMG, (transform(140, WINDOW_WIDTH), transform(140, WINDOW_WIDTH))).convert_alpha()
back_button_img_rect = back_button_img.get_rect()
back_button_img_rect.center = (WINDOW_WIDTH - WINDOW_WIDTH//10, WINDOW_HEIGHT//10)

class TTTPlayer():
	def __init__(self, img):
		self.hold = []
		self.img = img
		self.row_hold = [0, 0, 0]
		self.col_hold = [0, 0, 0]
	def check_victory(self):
		for i in range(3):
			if self.row_hold[i] == 3 or self.col_hold[i] == 3:
				return True
		else:
			if ([0, 0] in self.hold and [1,1] in self.hold and [2,2] in self.hold) or ([2,0] in self.hold and [1,1] in self.hold and [0,2] in self.hold):
				return True
		return False

def Tic_tac_toe():
	global current_page
	current_page = 'TIC TAC TOE'
	cycle_no = 0
	DISPSURF.blit(blur_bg_img, blur_bg_img_rect)
	DISPSURF.blit(ttt_board_img, ttt_board_img_rect)
	DISPSURF.blit(back_button_img, back_button_img_rect)
	
	gameover = False
	players = [TTTPlayer(cross_img), TTTPlayer(o_img)]
	current_player = 0
	
	pygame.display.update()
	
	pygame.mixer.music.pause()
	while not gameover:	
		for event in pygame.event.get():
			if event.type == QUIT:
				quit_game_sound.play()
				time.sleep(0.2)
				pygame.quit()
				sys.exit()
			elif event.type == MOUSEBUTTONDOWN:
				if ttt_board_img_rect.collidepoint(event.pos):
					blick_sound.play()
					tile_x = (event.pos[0] - WINDOW_WIDTH//2 + NEW_TTT_TOTAL_LENGTH//2) // (NEW_TTT_TOTAL_LENGTH//3)
					tile_y = (event.pos[1] - WINDOW_HEIGHT//2 + NEW_TTT_TOTAL_LENGTH//2) // (NEW_TTT_TOTAL_LENGTH//3)
					tile_x, tile_y = int(tile_x), int(tile_y)
					if [tile_y, tile_x] not in players[0].hold and [tile_y, tile_x] not in players[1].hold:
						players[current_player].hold.append([tile_y, tile_x])
						players[current_player].row_hold[tile_y] += 1
						players[current_player].col_hold[tile_x] += 1
						DISPSURF.blit(players[current_player].img, (tile_x * TTT_TOTAL_LENGTH/3 + WINDOW_WIDTH//2 - TTT_TOTAL_LENGTH//2 + TTT_TOTAL_LENGTH//6 - TTT_TOTAL_LENGTH//10, tile_y * TTT_TOTAL_LENGTH/3 + WINDOW_HEIGHT//2 - TTT_TOTAL_LENGTH//2 + TTT_TOTAL_LENGTH//6 - TTT_TOTAL_LENGTH//10))
						cycle_no += 0.5
						if cycle_no >= 2:
							gameover = players[current_player].check_victory()

						if not gameover and cycle_no==4.5:
							pygame.display.update()
							time.sleep(1)
							Tic_tac_toe()
						current_player = (current_player + 1) % 2
						
						
						pygame.display.update()
						
				elif back_button_img_rect.collidepoint(event.pos):
					button_click_sound.play()
					pygame.mixer.music.play(-1)
					return
	
	else:
		fruit_eat_sound.play()
		time.sleep(0.6)
		DISPSURF.blit(blur_bg_img, blur_bg_img_rect)

		winner = 'x' if current_player == 1 else 'o'
		winner_text = ALLOY_FONT130.render(winner + '  wins!!!', True, BLACK)
		winner_text_rect = winner_text.get_rect()
		winner_text_rect.center = WINDOW_WIDTH//2, WINDOW_HEIGHT// 3.5
		
		play_again_text = ALLOY_FONT100.render("Play again???", True, BLACK)
		play_again_rect = play_again_text.get_rect()
		play_again_rect.center = WINDOW_WIDTH//2, WINDOW_HEIGHT//2

		yes_text = ALLOY_FONT100.render('Yes', True, GREEN)
		yes_rect = yes_text.get_rect()
		yes_rect.center = WINDOW_WIDTH// 3 * 1.25, WINDOW_HEIGHT//1.6
		no_text = ALLOY_FONT100.render('No', True, RED)
		no_rect = yes_text.get_rect()
		no_rect.center = WINDOW_WIDTH// 3 * 1.75, WINDOW_HEIGHT//1.6
		

		DISPSURF.blit(play_again_text, play_again_rect)
		DISPSURF.blit(winner_text, winner_text_rect)
		DISPSURF.blit(yes_text, yes_rect)
		DISPSURF.blit(no_text, no_rect)
		pygame.display.update()
		while True:
			for event in pygame.event.get():
				if event.type == QUIT:
					quit_game_sound.play()
					time.sleep(0.2)
					pygame.quit()
					sys.exit()
				elif event.type == MOUSEBUTTONDOWN:
					if yes_rect.collidepoint(event.pos):
						button_click_sound.play()
						Tic_tac_toe()
					elif no_rect.collidepoint(event.pos):
						button_click_sound.play()
						pygame.mixer.music.play()
						return

if __name__ == '__main__':
    Tic_tac_toe()
