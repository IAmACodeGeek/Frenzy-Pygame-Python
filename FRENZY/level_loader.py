import pygame, os

from pygame.locals import *
from Database.variables import *
import csv

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = WINDOW_WIDTH, WINDOW_HEIGHT
LOW_MARGIN = 100
SIDE_MARGIN = 300

DISPSURF = pygame.display.set_mode((1300 + SIDE_MARGIN, 600 + LOW_MARGIN))
pygame.display.set_caption('Level Designer!!!')

clock = pygame.time.Clock()
FPS = 60

# Variables
ROWS = 20
MAX_COLS = 100
TILESIZE = SCREEN_HEIGHT / ROWS
TILETYPES = 13
current_tile = -1
LEVEL = 1
world_map = [[-1 for i in range(MAX_COLS)] for j in range(ROWS)]

scroll_left, scroll_right, scroll = False, False, 0
scroll_speed = 1

#load the images
bg_img = pygame.image.load('Images/level loader/bg.png')
bg_img = pygame.transform.scale(bg_img, (bg_img.get_width(), SCREEN_HEIGHT)).convert_alpha()
save_img = pygame.image.load('Images/level loader/save img.png').convert_alpha()
save_rect = save_img.get_rect()
save_rect.bottomright = SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT + LOW_MARGIN
reset_img = pygame.image.load('Images/level loader/reset.png')
reset_img = pygame.transform.scale(reset_img, (150, 150)).convert_alpha()
reset_rect = reset_img.get_rect()
reset_rect.center = save_rect.centerx, 550

MODERN_FONT40 = pygame.font.Font('Fonts/Modern1.ttf', 40)

blick_sound = pygame.mixer.Sound("Sounds/movement sound.wav")
blick_sound.set_volume(1)

img_list = []
for i in range(TILETYPES):
    file_type = 'jpg' if i < 8 else 'png'
    img = pygame.image.load(f'Images/level loader/all tiles/{i}.{file_type}')
    img = pygame.transform.scale(img, (TILESIZE, TILESIZE)).convert_alpha()
    img_list.append(img)

rect_list = []
current_index = 0
for i in range(4):
    for j in range(3):
        rect = pygame.Rect(SCREEN_WIDTH + 10 + j * (TILESIZE + 84), 10 + i * (TILESIZE + 70), TILESIZE, TILESIZE)
        rect_list.append(rect)
        current_index += 1
rect_list.append(pygame.Rect(SCREEN_WIDTH + 10 + 0 * (TILESIZE + 84), 10 + 4 * (TILESIZE + 70), TILESIZE, TILESIZE))
del current_index
options_rect = pygame.Rect(SCREEN_WIDTH, 0, SIDE_MARGIN, SCREEN_HEIGHT)
map_rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

def draw_options():
    if current_tile > -1:
        pygame.draw.rect(DISPSURF, RED, (rect_list[current_tile].x - 2, rect_list[current_tile].y - 2, TILESIZE + 4, TILESIZE + 4), 2)
    for index, img in enumerate(img_list):
        DISPSURF.blit(img, rect_list[index])

def draw_bg():
    DISPSURF.fill(WHITE)
    img_width = bg_img.get_width()
    for i in range(4):
        DISPSURF.blit(bg_img, (-scroll + i * img_width, 0))
    draw_grid()
    draw_tiles()
    pygame.draw.rect(DISPSURF, WHITE, options_rect)
    draw_options()
    
    draw_save()
    draw_level()

def draw_grid():
    for i in range(1, ROWS + 1):
        pygame.draw.line(DISPSURF, WHITE, (0 - scroll, i * TILESIZE), (150 * TILESIZE - scroll, i * TILESIZE))
    for i in range(1, MAX_COLS + 1):
        pygame.draw.line(DISPSURF, WHITE, (i * TILESIZE - scroll, 0), (i * TILESIZE- scroll, SCREEN_HEIGHT))
def draw_save():
    DISPSURF.blit(save_img, save_rect)
    DISPSURF.blit(reset_img, reset_rect)

def find(x,y):
    col = (x + scroll) // TILESIZE
    row = y // TILESIZE
    return int(row), int(col)

def draw_tiles():
    for i in range(ROWS):
        for j in range(MAX_COLS):
            if world_map[i][j] != -1:
                DISPSURF.blit(img_list[world_map[i][j]], (j * TILESIZE - scroll, i * TILESIZE))

def draw_level():
    level_text = MODERN_FONT40.render(f'LEVEL :  {LEVEL}  PRESS UP AND DOWN ARROWS TO CHANGE LEVEL', True, BLACK)
    DISPSURF.blit(level_text, (50, 770))

def save(level, map):
    with open(f'Database/Levels/{level}.csv', 'w', newline = '') as file:
        writer = csv.writer(file, delimiter = ',')
        for row in map:
            writer.writerow(row)
def load(level):
    global world_map
    if f'{level}.csv' in os.listdir('Database/Levels'):
        with open(f'Database/Levels/{level}.csv', 'r', newline = '') as readfile:
            reader = csv.reader(readfile, delimiter = ',')
            # for x, row in enumerate(reader):
            #     for y, tile in enumerate(row):
            #         world_map[x][y] = int(tile)
            rows = []
            for row in reader:
                row = list([int(i) for i in row])
                rows.append(row)
            world_map = rows
            
    else:
        world_map = [[-1 for i in range(MAX_COLS)] for j in range(ROWS)]

run = True
load(LEVEL)
MOUSE_ACTIVE = False
while run:
    
    clock.tick(FPS)
    # Scroll the screen
    if scroll_left:
        scroll -= 5 * scroll_speed
        if scroll < 0:
            scroll = 0
        
    if scroll_right:
        scroll += 5 * scroll_speed
        if TILESIZE * MAX_COLS - scroll < SCREEN_WIDTH:
            scroll = TILESIZE * MAX_COLS - SCREEN_WIDTH 



    draw_bg()
    
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                scroll_left = True
            if event.key == K_RIGHT:
                scroll_right = True
            if event.key == K_RSHIFT:
                scroll_speed = 5
            if event.key == K_UP:
                LEVEL += 1
                load(LEVEL)
            if event.key == K_DOWN and LEVEL > 1:
                LEVEL -= 1
                load(LEVEL)
        
        elif event.type == KEYUP:
            if event.key == K_LEFT:
                scroll_left = False
            if event.key == K_RIGHT:
                scroll_right = False
            if event.key == K_RSHIFT:
                scroll_speed = 1

        elif event.type == MOUSEBUTTONDOWN:
            if map_rect.collidepoint(event.pos):
                MOUSE_ACTIVE = True
                
                blick_sound.play()
            if save_rect.collidepoint(event.pos):
                save(LEVEL, world_map)
            elif reset_rect.collidepoint(event.pos):
                world_map = [[-1 for i in range(MAX_COLS)] for j in range(ROWS)]
                
            elif options_rect.collidepoint(event.pos):
                for index, rect in enumerate(rect_list):
                    if rect.collidepoint(event.pos):
                        current_tile = index
                        print(current_tile)
                        break
                else:
                    current_tile = -1
            elif map_rect.collidepoint(event.pos):
                row, col = find(*event.pos)
                world_map[row][col] = current_tile

        elif event.type == MOUSEMOTION and MOUSE_ACTIVE:
            if map_rect.collidepoint(event.pos):
                row, col = find(*event.pos)
                world_map[row][col] = current_tile

        elif event.type == MOUSEBUTTONUP:
            MOUSE_ACTIVE = False
        

            
            
                
        


                
    pygame.display.update()

pygame.quit()