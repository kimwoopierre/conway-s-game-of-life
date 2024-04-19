import sys
import pygame
import os
from pygame.locals import *
FPS = 10
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,30)

pygame.init()
#display
display_info = pygame.display.Info()
display_width = display_info.current_w
display_height = display_info.current_h
print(display_width, display_height)
pygame.display.set_caption("game of life")
window = pygame.display.set_mode((display_width, display_height-30)) 
window_rect = window.get_rect()
window_rect.move_ip(0, 30)
clock = pygame.time.Clock()


class Layer(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.buttons = pygame.sprite.Group()
        self.grids = pygame.sprite.Group()
        self.texts = pygame.sprite.Group()
    def add_button(self, *buttons):
        for button in buttons:        
            self.buttons.add(button)
    def add_grid(self, grid):
        self.grids.add(grid)
    def remove_button(self, button):
        self.buttons.remove(button)
    def update(self):
        self.buttons.update()
        self.grids.update()
        self.texts.update()
    def draw(self, window):
        self.buttons.draw(window)
        self.grids.draw(window)
    def add_text(self, text):
        self.texts.add(text)

class GridSprite(pygame.sprite.Sprite):
    def __init__(self, width, height, color):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.grid_x = 0
        self.grid_y = 0
        self.max_x = display_width -width
        self.max_y = display_height - height
    def draw_grid(self, surface, cell_size):
        for x in range(self.grid_x, surface.get_width(), cell_size):
            pygame.draw.line(surface, (128, 128, 128), (x,0), (x,surface.get_height()))
        for y in range(self.grid_y, surface.get_height(), cell_size):
            pygame.draw.line(surface, (128, 128, 128), (0, y), (surface.get_width(), y))




class ButtonSprite(pygame.sprite.Sprite):
    def __init__(self,surface, x, y, width, height):
        super().__init__()
        self.surface = surface
        self.rect = pygame.Rect(x, y, width, height)
        self.visible = True
    def draw(self, color, radius):
        if self.visible:        
            pygame.draw.rect(self.surface, color, rect=self.rect, border_radius=radius)
   

Title = pygame.font.SysFont("arial", 100, True)
Show_title = Title.render("Game of life", True, (0,0,0))
descript = pygame.font.SysFont("arial", 30, True)
Show_descript = descript.render("For play the game, press enter(return) key", True, (50,50,50))
Run_text = pygame.font.SysFont("arial", 25, True)
Show_run = Run_text.render("Run", True, (255,255,255))
    
my_layer = Layer()
my_grid = GridSprite(300,300, (255,255,255))
my_button_R = ButtonSprite(window, 620, 480, 75,50)
my_button_Q = ButtonSprite(window, 720, 480, 75,50)

my_layer.add_grid(my_grid)
my_layer.add_button(my_button_Q, my_button_R)

cell_size = 10
cells = {}


def draw_cell(surface, row, col, color):
    cell_rect = pygame.Rect(row*cell_size+my_grid.grid_x, col*cell_size+my_grid.grid_y, cell_size, cell_size)
    pygame.draw.rect(surface, color, cell_rect)

num_cell_width = display_width//cell_size
num_cell_height = display_height//cell_size
grid_state = [[False for _ in range(num_cell_height)] for _ in range(num_cell_width)]


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.key == K_RETURN:
                print(cells)                
        elif event.type == MOUSEBUTTONUP:
            if event.button ==1:
                mouse_x, mouse_y = event.pos
                print(mouse_x//cell_size*cell_size, mouse_y//cell_size*cell_size)
                row = (mouse_x-my_grid.grid_x)//cell_size
                col = (mouse_y-my_grid.grid_y)//cell_size
                if 0<=row <len(grid_state) and 0<= col < len(grid_state[0]) and my_button_R.visible == False:                
                    grid_state[row][col] = not grid_state[row][col]
                if my_button_R.rect.collidepoint(mouse_x, mouse_y) and my_button_R.visible == True:
                    my_button_R.visible = False
                    my_button_Q.visible = False
                    print("non")
                elif my_button_Q.rect.collidepoint(mouse_x, mouse_y) and my_button_Q.visible == True:
                    pygame.quit()
                    sys.exit()
                
        elif event.type == MOUSEWHEEL and my_button_R.visible == False:
            if event.y>0:
                if cell_size>=70:
                    cell_size = 70
                else:
                    cell_size+=event.y
                print(cell_size)
            elif event.y<0:
                if cell_size<=10:
                    cell_size = 10
                else:                
                    cell_size+=event.y
                print(cell_size)

    window.fill((0,0,0))
    for row in range(len(grid_state)):
        for col in range(len(grid_state[0])):
            color = (0,0,0) if grid_state[row][col] else (255,255,255)
            cells[(row,col)] = color
            draw_cell(window, row, col, color)
    if my_button_R.visible == False:
        my_grid.draw_grid(window, cell_size)
        
    my_button_R.draw((50,50,50), 3)
    my_button_Q.draw((50,50,50), 3)
    window.blit(Show_title,(470,300))
    window.blit(Show_descript,(460,410))
    window.blit(Show_run,(640, 490)) #620, 480
    pygame.display.update()
    
    clock.tick(FPS)