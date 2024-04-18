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

White = pygame.Color(255,255,255,255)
Black = pygame.Color(0,0,0,255)
window_x, window_y = pygame.display.get_window_size()
cell_size = 10

def cell (surface, color, x, y, cell_size):
    pygame.draw.rect(surface, color,(x,y,cell_size,cell_size))
def grid (cell_size):
    for x in range(0,width,cell_size):
        pygame.draw.line(window, Black,(x,0),(x,width))
    for y in range(0,height, cell_size):
        pygame.draw.line(window, Black, (0,y), (height,y))

        
window.fill(White)
grid(cell_size)

while True:
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
                mouse_x, mouse_y = pygame.mouse.get_pos()
                x,y = mouse_x//cell_size, mouse_y//cell_size            
                current_color = pygame.Surface.get_at(window,(x*cell_size+1,y*cell_size+1))
                if current_color == White:
                    cell(window, Black, x*cell_size+1,y*cell_size+1, cell_size-1)
                else:
                    cell(window, White, x*cell_size+1,y*cell_size+1, cell_size-1)
        elif event.type == MOUSEWHEEL:
            event.y
    pygame.display.update()
    Clock.tick(FPS)