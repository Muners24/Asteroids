import pygame
import sys
import math
import numpy
from random import randint

class Vector2:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        
WIDTH, HEIGHT = 1800, 1000
WINDOW_SIZE = (WIDTH, HEIGHT)

NAVE_VEL = 5
NAVE_MAX_VEL = 10
NAVE_RAD = 28
NAVE_ATKV = 4

DISP_RAD = 1
DISP_VEL = 10
DISP_TTL = 100

ASTEROID_V = 5
ASTEROID_RAD0  = 40
ASTEROID_RAD1 = 22
ASTEROID_RAD2 = 10
ASTEROID_MIN_TIMER = 60
ASTEROID_MAX_TIMER = 120
ASTEROID_TTL = 400

RIGHT = 0 
UP = 1
LEFT = 2
DOWN = 3

SPAWNX = WIDTH/2
SPAWNY = HEIGHT/2
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)


