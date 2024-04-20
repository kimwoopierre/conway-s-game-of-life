import sys
import pygame
import os
import pygame.freetype
from pygame.locals import *
from time import sleep
FPS = 25
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,30)

pygame.init()
#display
display_info = pygame.display.Info()
display_width = display_info.current_w
display_height = display_info.current_h
# print(display_width, display_height)
pygame.display.set_caption("game of life")
window = pygame.display.set_mode((display_width, display_height-30)) 
window_rect = window.get_rect()
window_rect.move_ip(0, 30)
clock = pygame.time.Clock()
White = (255,255,255)
Black = (0,0,0)
user_text = " "
speed = 1
cell_size = 10
cells = {}
num_cell_width = display_width//cell_size
num_cell_height = display_height//cell_size
grid_state = [[False for _ in range(num_cell_height)] for _ in range(num_cell_width)]
Running = False
draw_bool = False
erase_bool = False
is_dragging = False
clicked_cell = None

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
        # window.fill((255,255,255))
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

def draw_cell(surface, row, col, color):
    cell_rect = pygame.Rect(row*cell_size+my_grid.grid_x+1, col*cell_size+my_grid.grid_y+1, cell_size-1, cell_size-1)
    pygame.draw.rect(surface, color, cell_rect)

def erase_cell (cells):
    for keys in cells.keys():
        for key in keys:
            if cells.get(key) == (0,0,0):
                cells[key] = (255,255,255)

def run(grid_state,speed):
    while Running:
        next_state = [[False for _ in range(len(grid_state[0]))] for _ in range(len(grid_state))]
        for x, cell_color in cells.items():
            row, col = x
            cnt = 0
            # 주변 셀 검사
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i == 0 and j == 0:
                        continue  # 현재 셀은 제외
                    new_row = row + i
                    new_col = col + j
                    if (0 <= new_row < len(grid_state)) and (0 <= new_col < len(grid_state[0])):
                        if cells[(new_row, new_col)] == Black:
                            cnt += 1
            # 현재 셀의 상태에 따라 다음 상태 결정
            if cell_color == Black:  # 현재 셀이 검은색인 경우
                if cnt == 2 or cnt == 3:
                    next_state[row][col] = True  # 살아남음
                else:
                    next_state[row][col] = False  # 죽음
            else:  # 현재 셀이 흰색인 경우
                if cnt == 3:
                    next_state[row][col] = True  # 살아남음
        # 다음 상태를 현재 상태로 업데이트
        for row in range(len(grid_state)):
            for col in range(len(grid_state[0])):
                grid_state[row][col] = next_state[row][col]
        pygame.time.delay(speed)
        return grid_state

#Text
Title = pygame.freetype.Font("F:\\kimwo\\python\\qrcode\\---\\Arial.ttf", 100)
descript = pygame.freetype.Font("F:\\kimwo\\python\\qrcode\\---\\Arial.ttf", 30)
Run_Quit_text = pygame.freetype.Font("F:\\kimwo\\python\\qrcode\\---\\Arial.ttf", 25)
running_text = pygame.freetype.Font("F:\\kimwo\\python\\qrcode\\---\\Arial.ttf", 200)

#Layers
my_layer = Layer()
my_grid = GridSprite(300,300, White)
my_button_R = ButtonSprite(window, display_width//2-100, display_height//2, 75,50)     #620, 480
my_button_Q = ButtonSprite(window, display_width//2, display_height//2, 75,50)     #720, 480

my_layer.add_grid(my_grid)
my_layer.add_button(my_button_Q, my_button_R)


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                if not Running:
                    erase_bool = True
                    draw_bool = False
                    cells.clear()
            elif event.key == K_RETURN:
                speed_text = user_text
                try:
                    speed = int(speed_text)
                except ValueError:
                    pass
                Running = not Running

            elif event.key == K_BACKSPACE:
                user_text = user_text[:-1]
                    
            else:
                user_text += event.unicode
            
        elif event.type == MOUSEBUTTONUP:
            if event.button ==1:
                is_dragging = False
                draw_bool = True

        elif event.type == MOUSEBUTTONDOWN:
            if event.button ==1:
                is_dragging = True
                mouse_x, mouse_y = event.pos
                row = (mouse_x-my_grid.grid_x)//cell_size
                col = (mouse_y-my_grid.grid_y)//cell_size
                clicked_cell = ((row,col))
                if 0<=row <len(grid_state) and 0<= col < len(grid_state[0]) and my_button_R.visible == False:                
                    grid_state[row][col] = not grid_state[row][col]
                if my_button_R.rect.collidepoint(mouse_x, mouse_y) and my_button_R.visible == True:
                    my_button_R.visible = False
                    my_button_Q.visible = False
                elif my_button_Q.rect.collidepoint(mouse_x, mouse_y) and my_button_Q.visible == True:
                    pygame.quit()
                    sys.exit()
        elif event.type == MOUSEMOTION and my_button_R.visible == False:
   
            if is_dragging and clicked_cell is not None:
                mouse_x, mouse_y = event.pos
                row = (mouse_x - my_grid.grid_x) // cell_size
                col = (mouse_y - my_grid.grid_y) // cell_size
                dx = abs(row-clicked_cell[0])
                dy = abs(col-clicked_cell[1])

                if 0 <= row < len(grid_state) and 0 <= col < len(grid_state[0]):
                    if dx>0 or dy>0:
                        if grid_state[row][col] == White:    
                            grid_state[row][col] = not grid_state[row][col]
                        else:
                            grid_state[row][col] = not grid_state[row][col]
                    clicked_cell = row, col

                            
                    
        elif event.type == MOUSEWHEEL and my_button_R.visible == False:
            if event.y>0:
                if cell_size>=70:
                    cell_size = 70
                else:
                    cell_size+=event.y
            elif event.y<0:
                if cell_size<=10:
                    cell_size = 10
                else:                
                    cell_size+=event.y

    window.fill(White)

    if draw_bool == True:
        for row in range(len(grid_state)):
            for col in range(len(grid_state[0])):
                color = Black if grid_state[row][col] else White
                cells[(row,col)] = color
                draw_cell(window, row, col, color)

    my_button_R.draw((50,50,50), 3)
    my_button_Q.draw((50,50,50), 3)
    Title.render_to(window, (display_width//2-250,display_height//3-70), "Game of life",style=1)
    descript.render_to(window,(display_width//2-260, display_height//3+80), "For play the game, press enter(return) key", style=1)
    Run_Quit_text.render_to(window, (display_width//2-85, display_height//2+15), "Run",fgcolor=White, style=1)
    Run_Quit_text.render_to(window, (display_width//2+13, display_height//2+15), "Quit",fgcolor=White, style=1)

    if Running == True:
        run(grid_state, speed*50)
        running_text.render_to(window, (display_width//3, display_height//3), "Running", fgcolor=(10,10,10,50), style=1)

    if my_button_R.visible == False:
        Title.size =0.1  
        descript.size = 0.1
        Run_Quit_text.size = 0.1
        my_grid.draw_grid(window, cell_size)
    if erase_bool == True:
        erase_cell(cells)
        for row in range(len(grid_state)):
            for col in range(len(grid_state[0])):
                grid_state[row][col] = False
        erase_bool = False
    text_surface = pygame.font.Font(None, 32).render("Please type the speed(only number, default = 1): " + user_text, True, (0,0,0))
    window.blit(text_surface, (0,0))
    pygame.display.update()
    
    clock.tick(FPS)

