import pygame
import sys
import math
import numpy


WIDTH, HEIGHT = 800, 600
WINDOW_SIZE = (WIDTH, HEIGHT)
NAVE_VEL = 5
SPAWN = (400,300)

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

class Vector2:
    def __init__(self,x,y):
        self.x = x
        self.y = y
