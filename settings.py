import pygame, sys
from pygame.math import Vector2 as vector
from os import listdir
from os.path import join
from pytmx.util_pygame import load_pygame

WIDTH, HEIGHT = 1280, 720
TILE_SIZE = 64

diffculty_modifier = 0.15 
difficulty = 1
upgrade_value = 1.1
rooms_cleared = 0

playing = True