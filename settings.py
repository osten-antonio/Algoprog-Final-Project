import pygame, sys
from pygame.math import Vector2 as vector
from os import listdir
from os.path import join
from pytmx.util_pygame import load_pygame

WIDTH, HEIGHT = 1280, 720
TILE_SIZE = 64
class playerDifficulty():
    def __init__(self):
        self.diffculty_modifier = 0.15 
        self.difficulty = 1
        self.upgrade_value = 1.1
        self.rooms_cleared = 0
        self.player_level = 1
        self.playing = False


player_difficulty = playerDifficulty()