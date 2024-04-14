import pygame
import sys
import os
from pygame.locals import *

pygame.init()
display_info = pygame.display.Info()
display_width = display_info.current_w
display_height = display_info.current_h
print(display_width, display_height)
pygame.display.set_caption("game of life")
window = pygame.display.set_mode((600,600)) #display_width, display_height-30
window_rect = window.get_rect()
window_rect.move_ip(0, 30)
clock = pygame.time.Clock()
FPS = 10
Black = (0,0,0)
White = (256,256,256)


playground = pygame.Rect(50,50,500,500)
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
    window.fill(Black)
    pygame.draw.rect(window,White, rect=playground)
    pygame.display.update()
    clock.tick(FPS)