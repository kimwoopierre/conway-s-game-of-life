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
window = pygame.display.set_mode((600,600)) #display_width, display_height-30
window_rect = window.get_rect()
window_rect.move_ip(0, 30)
clock = pygame.time.Clock()

class Layer(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.buttons = pygame.sprite.Group()
        self.grids = pygame.sprite.Group()
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
    def draw(self, window):
        self.buttons.draw(window)
        self.grids.draw(window)

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
    def move(self, dx, dy):
        self.grid_x +=dx
        self.grid_y +=dy
        if self.grid_x ==0:
            self.grid_x = 0
        elif self.grid_x >0:
            if dx>0:            
                self.grid_x+=dx
            elif dx<0:
                while self.grid_x==0:
                    self.grid_x=-self.grid_x+dx
        if self.grid_y ==0:
            self.grid_y = 0
        elif self.grid_y >0:
            if dy>0:
                self.grid_y+=dy
            elif dx<0:
                while self.grid_y==0:
                    self.grid_y=-self.grid_y +dy
        # if self.grid_x >0:
        
        #     self.grid_x =0
        # elif self.grid_x < -display_width+600:
        #     self.grid_x = -display_width +600
        # if self.grid_y>0:
        #     self.grid_y =0
        # elif self.grid_y < -display_height+600:
        #     self.grid_y = -display_height +600

class ButtonSprite(pygame.sprite.Sprite):
    def __init__(self,surface, x, y, width, height):
        super().__init__()
        self.surface = surface
        self.rect = pygame.Rect(x, y, width, height)
        self.visible = True
    def draw(self, color, radius):
        if self.visible:        
            pygame.draw.rect(self.surface, color, rect=self.rect, border_radius=radius)
   


    
my_layer = Layer()
my_grid = GridSprite(300,300, (255,255,255))
my_button_R = ButtonSprite(window, 200, 250, 75,50)
my_button_Q = ButtonSprite(window, 300, 250, 75,50)
my_layer.add_grid(my_grid)
my_layer.add_button(my_button_Q, my_button_R)
# grid_x = 0
# grid_y = 0
cell_size = 10
#grid_size = (display_width//cell_size, display_height//cell_size)


def draw_cell(surface, row, col, color):
    cell_rect = pygame.Rect(row*cell_size+my_grid.grid_x, col*cell_size+my_grid.grid_y, cell_size, cell_size)
    pygame.draw.rect(surface, color, cell_rect)

num_cell_width = display_width//cell_size
num_cell_height = display_height//cell_size
grid_state = [[False for _ in range(num_cell_height)] for _ in range(num_cell_width)]
dragging = False


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
        elif event.type == MOUSEBUTTONUP:
            if event.button ==1:
                mouse_x, mouse_y = event.pos
                print(mouse_x//cell_size, mouse_y//cell_size) ----
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
            elif event.button ==3:
                dragging = False

        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 3 and my_button_Q.visible == False:
                dragging = True
            # if display_width >= grid_size[0] * cell_size and display_height >= grid_size[1] * cell_size:
            #     dragging = True
            #     drag_start_x, drag_start_y = event.pos
        elif event.type == MOUSEMOTION:
            if dragging:                
                dx, dy = event.rel
                fx, fy = event.pos
                print(dx, dy)
                my_grid.move(dx, dy)

                
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
            draw_cell(window, row, col, color)   
    my_grid.draw_grid(window, cell_size)
    my_button_R.draw((50,50,50), 3)
    my_button_Q.draw((50,50,50), 3)
    pygame.display.update()
    
    clock.tick(FPS)