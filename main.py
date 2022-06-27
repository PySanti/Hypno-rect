import pygame
from pygame.locals import *
from random import randint
pygame.init()


class MovingRect:
    def __init__(self,position,color,size, speed, first_rect, size_increase, size_decrease_limit):
        self.rect           = pygame.Rect(position[0], position[1], size[0], size[1])
        self.color          = color
        self.x_speed        = speed
        self.y_speed        =   speed
        self.x_momentum     = 0
        self.y_momentum     = 0
        self.size           = size.copy()
        self.original_size  = size.copy()
        self.size_diff      = 0
        self.first_rect    =   first_rect
        self.size_increase = size_increase
        self.size_decrease_limit = size_decrease_limit

    def update(self, window_size):

        self.y_momentum += self.y_speed
        self.rect.y += self.y_momentum
        if self.y_speed > 0 and self.rect.centery >= window_size[1]/2:
            self.y_speed = -self.y_speed
        elif self.y_speed < 0  and self.rect.centery < window_size[1]/2:
            self.y_speed = -self.y_speed
        self.x_momentum += self.x_speed
        self.rect.x += self.x_momentum
        if self.x_speed > 0 and self.rect.centerx >= window_size[0]/2:
            self.x_speed = -self.x_speed
        elif self.x_speed < 0  and self.rect.centerx < window_size[0]/2:
            self.x_speed = -self.x_speed

        if self.first_rect == False:
            if (self.size[0] == self.original_size[0]):
                self.size_diff = -1
            elif (self.size[0] == self.original_size[0]/self.size_decrease_limit):
                self.size_diff = 1
        else:
            if (self.size[0] == self.original_size[0]) and (self.first_rect != False and self.first_rect.size_diff > 0):
                self.size_diff = -1
            elif (self.size[0] == self.original_size[0]/self.size_decrease_limit) and (self.first_rect != False and self.first_rect.size_diff < 0):
                self.size_diff = 1

        self.size[0] += self.size_diff
        self.size[1] += self.size_diff
        self.rect.size = self.size





    def render(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)



WINDOW_SIZE         = (700,700)
WINDOW              = pygame.display.set_mode(WINDOW_SIZE)
EXIT                = False
CLOCK               =   pygame.time.Clock()
WINDOW_COLOR        = (255,255,255)


RECT_SPEED          =   1
RECT_COLOR          =   [0,0,0]
RECT_SIZE           =   [100,100]
RECT_INITIAL_POSITION = [100,WINDOW_SIZE[1]/2]
RECT_SIZE_INCREASE  = 0.3
RECT_SIZE_DEACREASE_LIMIT = 10
MAIN_RECT           = MovingRect(RECT_INITIAL_POSITION, RECT_COLOR, RECT_SIZE, RECT_SPEED, False, RECT_SIZE_INCREASE, RECT_SIZE_DEACREASE_LIMIT)
BACK_RECT           = MovingRect([RECT_INITIAL_POSITION[0]/2, RECT_INITIAL_POSITION[1]/2], RECT_COLOR, RECT_SIZE, RECT_SPEED, MAIN_RECT, RECT_SIZE_INCREASE, RECT_SIZE_DEACREASE_LIMIT)
RECTS = [MAIN_RECT, BACK_RECT]
BORDERS_SIZE        =   3
CORNER_SIZE         =   5

def updateRects(RECTS,WINDOW_SIZE, WINDOW):
    for rect in RECTS:
        rect.render(WINDOW)
        rect.update(WINDOW_SIZE)

def draw3DRectBorder(RECTS, WINDOW, border_color, border_size):
    if len(RECTS) != 2:
        print("Error en la funcion 'draw3DRectBorder'")
    else:
        rect_1 = RECTS[0]
        rect_2 = RECTS[1] 
        lines_list = [
                        [rect_1.rect.topleft, rect_2.rect.topleft],
                        [rect_1.rect.topright, rect_2.rect.topright],
                        [rect_1.rect.bottomleft, rect_2.rect.bottomleft],
                        [rect_1.rect.bottomright, rect_2.rect.bottomright],
                        ]
        for current_line in lines_list:
            pygame.draw.line(WINDOW, border_color,current_line[0],current_line[1], border_size)

def drawCornerCircelsRects(RECTS, WINDOW, corner_color, corner_size):
    for rect in RECTS:
        points = [
                        rect.rect.topleft,
                        rect.rect.topright,
                        rect.rect.bottomleft,
                        rect.rect.bottomright,
                        ]
        for point in points:
            pygame.draw.circle(WINDOW, corner_color,point,corner_size)




while not EXIT:
    WINDOW.fill(WINDOW_COLOR)
    draw3DRectBorder(RECTS, WINDOW, RECT_COLOR, BORDERS_SIZE)
    drawCornerCircelsRects(RECTS, WINDOW, RECT_COLOR, CORNER_SIZE)
    updateRects(RECTS,WINDOW_SIZE, WINDOW)

    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            EXIT = True

    pygame.display.update()
    CLOCK.tick(60)
