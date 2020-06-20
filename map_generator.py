import random
import pygame
from maps import maps


class Map:
    TILE_SIZE = 64  # ROZMIAR KAFELKI W PIKSELACH
    OBJECTS = []

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
        self.MAP_PICTURE = [pygame.transform.scale(pygame.image.load("textures/maps_textures/mapa0.png").convert(),
                                                   (self.TILES_W_A * self.TILE_SIZE, self.TILES_H_A * self.TILE_SIZE)),
                            pygame.transform.scale(pygame.image.load("textures/maps_textures/mapa1.png").convert(),
                                                   (self.TILES_W_A * self.TILE_SIZE, self.TILES_H_A * self.TILE_SIZE)),
                            pygame.transform.scale(pygame.image.load("textures/maps_textures/mapa2.png").convert(),
                                                   (self.TILES_W_A * self.TILE_SIZE, self.TILES_H_A * self.TILE_SIZE))]

    def change(self):
        pass

    def draw(self, screen, number_of_map):
        screen.blit(self.MAP_PICTURE[number_of_map], (0, 0))
        for i in range(self.TILES_H_A):
            for n in range(self.TILES_W_A):
                if maps.maps[number_of_map][i][n] != 0:
                    screen.blit(self.OBJECTS[maps.game_map1[i][n] - 1], (n * self.TILE_SIZE, i * self.TILE_SIZE))
