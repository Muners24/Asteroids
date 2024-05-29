import pygame
import sys
import math
import numpy
from random import randint

class Vector2:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        
WIDTH, HEIGHT = 1600, 900
WINDOW_SIZE = (WIDTH, HEIGHT)

NAVE_VEL = 5
NAVE_MAX_VEL = 10
NAVE_RAD = 28
NAVE_ATKV = 4
NAVE_INV_TIMER = 90

DISP_RAD = 2
DISP_VEL = 10
DISP_TTL = 120

ASTEROID_V = 6
ASTEROID_RAD0  = 40
ASTEROID_RAD1 = 27
ASTEROID_RAD2 = 14
ASTEROID_MIN_TIMER = 40
ASTEROID_MAX_TIMER = 60
ASTEROID_TTL = 300

RIGHT = 0 
UP = 1
LEFT = 2
DOWN = 3

SPAWNX = WIDTH/2
SPAWNY = HEIGHT/2+HEIGHT/4
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREY = (219,220,233)
BLACK = (0,0,0)

