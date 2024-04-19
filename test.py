import pygame
import sys
import os
from pygame.locals import *


os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,30)
pygame.init()
width = pygame.display.Info().current_w
height = pygame.display.Info().current_h
window = pygame.display.set_mode((600,600))   #width,height-30
pygame.display.set_caption("Game of life")

FPS = 10
Clock = pygame.time.Clock()

White = pygame.Color(255,255,255)
Black = pygame.Color(0,0,0,255)
window_x, window_y = pygame.display.get_window_size()
cell_size = 10
grid_layer = pygame.Surface((width,height))

def draw(cell_size):
    grid_layer.fill(White)
    for x in range(0,width,cell_size):
        pygame.draw.line(grid_layer, Black,(x,0),(x,width))
    for y in range(0,height, cell_size):
        pygame.draw.line(grid_layer, Black, (0,y), (height,y))
def update():
    window.blit(grid_layer,(0,0))


        

def cell (color, x, y, cell_size):
    pygame.draw.rect(window, color,(x,y,cell_size,cell_size))


cells = {}
dict_key = {}
clickdown = False
draw(cell_size)
update()


while True:
    mouse_x, mouse_y = pygame.mouse.get_pos() 
    x,y = (mouse_x//cell_size)*cell_size, (mouse_y//cell_size)*cell_size
    current_color = pygame.Surface.get_at(window,(x+1,y+1))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                clickdown = True
                if current_color == White:
                    cells[(x,y)] = "White"
                    # cell(Black, x*cell_size+1,y*cell_size+1, cell_size-1)
                else:
                    cells[(x,y)] = "Black"
                    # cell(White, x*cell_size+1,y*cell_size+1, cell_size-1)
        elif event.type == MOUSEBUTTONUP:
            if event.button == 1:
                clickdown = False
        elif event.type == MOUSEWHEEL:
            if event.y:
                cell_size+=event.y
                if cell_size>50:
                    cell_size=50
                elif cell_size <10:
                    cell_size=10
            updated_cells = {}
            for key, value in cells.items():
                updated_x = (key[0] // cell_size) * cell_size
                updated_y = (key[1] // cell_size) * cell_size
                updated_cells[(updated_x, updated_y)] = value
            cells = updated_cells
            draw(cell_size)
            update()
        if clickdown or event.type==MOUSEWHEEL:
            keys= cells.keys()
            values = cells.values()
            for key, value in cells.items():
                if value == "White":
                    dict_key[key] = 0
                    for i in dict_key.keys():
                        cell(Black, i[0]+1, i[1]+1, cell_size-1)
                elif value == "Black":
                    cell(White, key[0]+1, key[1]+1, cell_size-1)
                dict_key.clear()
            try:                
                for key in cells.keys():
                    for value in values:
                        if value == "Black":
                            del cells[key]
            except RuntimeError:
                pass

    pygame.display.update()
    Clock.tick(FPS)