import random
import pygame
from maps import *
import random


class Map:
    TILE_SIZE = 64  # ROZMIAR KAFELKI W PIKSELACH
    OBJECTS = []
    GRASS_LOADED = []

    def __init__(self, WIDTH, HEIGHT):
        self.HEIGHT = HEIGHT
        self.WIDTH = WIDTH

        self.TILES_H_A = self.HEIGHT // self.TILE_SIZE  # ILOŚC KAFELEK 64X64 KTORE SIE ZMIESZCZA NA#
        # EKRANIE O WYKOSOSCI HEIGHT
        self.TILES_W_A = self.WIDTH // self.TILE_SIZE  # ANALOGICZNE TYLKO DO SZEROKOSCI WIDTH
        self.MAP_ARRAY = [[0] * self.TILES_W_A] * self.TILES_H_A
        print(len(self.MAP_ARRAY))
        self.OBJECTS = [pygame.transform.scale(
            pygame.image.load("textures/block_with_collision/big_rock1.png").convert_alpha(),
            (self.TILE_SIZE, self.TILE_SIZE)), pygame.transform.scale(
            pygame.image.load("textures/block_with_collision/cutted_tree.png").convert_alpha(),
            (self.TILE_SIZE, self.TILE_SIZE)), pygame.transform.scale(
            pygame.image.load("textures/block_with_collision/trees.png").convert_alpha(),
            (self.TILE_SIZE, self.TILE_SIZE))]
        self.MAP_PICTURE = pygame.transform.scale(pygame.image.load("textures/mapa.png").convert())
        for i in range(5):
            self.GRASS_LOADED.append(pygame.transform.scale(pygame.image.load(f"textures/grass/grass{i}.png"),
                                                            (self.TILE_SIZE, self.TILE_SIZE)))
        for i in range(4):
            self.GRASS_LOADED.append(pygame.transform.scale(pygame.image.load(f"textures/grass/grass2.png"),
                                                            (self.TILE_SIZE, self.TILE_SIZE)))

    def draw(self, screen):
        screen.blit(self.MAP_PICTURE, (0, 0))
        for i in range(self.TILES_H_A):
            for n in range(self.TILES_W_A):
                screen.blit(random.choice(self.GRASS_LOADED), (n * self.TILE_SIZE, i * self.TILE_SIZE))


6
