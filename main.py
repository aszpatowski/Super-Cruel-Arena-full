import sys

import math
import random
import pygame
import operator
from map_generator import Map
from mainmenu import mainMenu
from player import Player
from maps import maps
from weapon import *
from bullet import Bullet


class Game(object):
    TPS_MAX = 80.0
    width = 1920
    height = 1080
    WEAPONS_AVAILABLE = [AK47, Pistol, Knife, Baseball]
    weapons_in_game = []
    bullets_in_game = []
    frames = 0
    PLAYERS_COORDINATE = [(100, 100), (100, 100), (100, 100), (100, 100)]  # default

    def __init__(self):
        # Config
        # Config
        # Intitialization
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.init()
        pygame.mixer.init(22100, -16, 2, 64)
        pygame.font.init()
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)  # , pygame.FULLSCREEN
        pygame.display.set_caption("Super Cruel Arena")
        pygame.display.set_icon(pygame.image.load("logos/icon.png"))
        self.tps_clock = pygame.time.Clock()
        self.Map = Map(self.width, self.height)
        self.Menu = mainMenu(self.width, self.height)
        self.title = pygame.image.load("title.png")
        self.sound_collision_weapon = pygame.mixer.Sound('sounds/collision_weapon.wav')
        self.sound_ricochet = pygame.mixer.Sound('sounds/ricochet.wav')
        self.sound_punch_weapon = pygame.mixer.Sound('sounds/punch_weapon.wav')
        self.sound_shot_body = pygame.mixer.Sound('sounds/shot_body.wav')
        self.music_in_game = pygame.mixer.music
        self.music_in_game.load('music/music1.wav')
        self.music_in_game.set_volume(0.01)
        self.font_size40 = pygame.font.Font('fonts/basic/basic.ttf', 40)
        self.font_size200 = pygame.font.Font('fonts/basic/basic.ttf', 200)
        self.font_size300 = pygame.font.Font('fonts/basic/basic.ttf', 300)
        # colors 0 - red 1 - blue 2 - green 3 - yellow 4 - white 5- black
        self.colors = [(255, 0, 0), (0, 0, 255), (0, 255, 0), (255, 223, 0), (255, 255, 255), (0, 0, 0)]
        self.music_in_game.play(-1)
        self.game_works = True
        # self.start(self.screen)
        self.maps_random = [1, 1, 1]
        self.choosed_map = 2
        while True:
            while self.Menu.menu_works:
                self.basic_handleEvents()
                self.Menu.draw(self.screen, self.music_in_game)
                self.Menu.movement()
                self.Menu.logo_rotating()
                self.maps_random = self.Menu.maps_random
                pygame.display.flip()
            self.random_map()
            self.game_works = True
            self.Spawnplayers(pygame.joystick.get_count())  # spawnowanie graczy zaleznie od ilosc padow
            while self.game_works:
                self.basic_handleEvents()
                self.game_continues()

    def basic_handleEvents(self):
        self.tps_clock.tick(self.TPS_MAX)
        pygame.display.set_caption("Super Cruel Arena FPS:{}".format(self.tps_clock.get_fps()))
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                if self.Menu.menu_works == True:
                    sys.exit(0)
                self.game_works = False
                self.Menu.menu_works = True
    def random_map(self):
        while True:
            self.choosed_map = random.randint(0, 2)
            if self.maps_random[self.choosed_map] == 0:
                pass
            else:
                return
    def game_continues(self):
        self.frames += 1
        if self.frames == self.TPS_MAX:
            self.frames = 0
            self.Spawnweapons()
        self.check_collision_between_players(pygame.joystick.get_count())
        self.check_collision_environment(pygame.joystick.get_count())
        self.weapon_interreaction()
        self.bullets_interreaction()
        self.check()
        self.draw(self.tps_clock.get_fps())
        pygame.display.flip()

    def Spawnplayers(self, number_of_players):
        self.random_coordinates_players(number_of_players)
        self.players = [Player(n, self.PLAYERS_COORDINATE[n][0], self.PLAYERS_COORDINATE[n][1]) for n in
                        range(0, number_of_players)]

    def Spawnweapons(self):
        if random.randint(0, 1) == 1 and len(self.weapons_in_game) <= 8:
            while True:
                randomX = random.randint(0, len(
                    maps.maps[self.choosed_map][0]) - 1)  # random.randint ma przedział zamknięty
                randomY = random.randint(0, len(maps.maps[self.choosed_map]) - 1)
                # Sprawdza czy nie ma przeszkody
                if maps.maps[self.choosed_map][randomY][randomX] == 0:
                    x = Map.TILE_SIZE * randomX
                    y = Map.TILE_SIZE * randomY
                    # Sprawdza czy nie ma innej broni
                    if (x, y) not in [weapon.back_xy() for weapon in self.weapons_in_game]:
                        self.weapons_in_game.append(random.choice(self.WEAPONS_AVAILABLE)(x, y, Map.TILE_SIZE))
                        break

    def random_coordinates_players(self, number_of_players):
        for i in range(number_of_players):
            while True:
                randomX = random.randint(0, len(maps.maps[self.choosed_map][0]) - 1)
                randomY = random.randint(0, len(maps.maps[self.choosed_map]) - 1)
                # Sprawdza czy nie ma przeszkody
                if maps.maps[self.choosed_map][randomY][randomX] == 0:
                    x = Map.TILE_SIZE * randomX + 32
                    y = Map.TILE_SIZE * randomY + 32
                    if (x, y) not in self.PLAYERS_COORDINATE:
                        self.PLAYERS_COORDINATE[i] = (x, y)
                        break

    def draw(self, tps):
        self.Map.draw(self.screen, self.choosed_map)
        for weapon in self.weapons_in_game:
            weapon.draw_and_check(self.screen)
        for player in self.players:
            if player.alive == 1 and player.stun_time == 0:
                player.movement()
                player.interreaction(self.bullets_in_game, Bullet)
            player.draw(self.screen, tps)
        for bullet in self.bullets_in_game:
            bullet.movement()
            bullet.draw(self.screen)
        self.menu_board(self.screen)

    def check_collision_between_players(self, number_of_players):
        for player1 in self.players:
            for player2 in self.players:
                if id(player1) != id(player2) and (player1.alive == 1 and player2.alive == 1):
                    if math.sqrt((player1.playerX - player2.playerX) ** 2 + \
                                 (player1.playerY - player2.playerY) ** 2) <= 64:

                        player1.playerX -= player1.playerVX
                        player1.playerY -= player1.playerVY
                        player2.playerX -= player2.playerVX
                        player2.playerY -= player2.playerVY

                        player1.playerVX *= -1
                        player2.playerVX *= -1
                        player1.playerVY *= -1
                        player2.playerVY *= -1
                    else:
                        continue
                else:
                    continue

    def check_collision_environment(self, number_of_players):
        for player in self.players:
            if player.alive != 0:
                for i in range(len(maps.maps[self.choosed_map])):
                    for n in range(len(maps.maps[self.choosed_map][0])):
                        if maps.maps[self.choosed_map][i][n] != 0:
                            deltaX = player.playerX - Map.TILE_SIZE * n - 32
                            deltaY = player.playerY - Map.TILE_SIZE * i - 32
                            if math.sqrt((deltaX) ** 2 + \
                                         (deltaY) ** 2) < 48:
                                player.playerX -= player.playerVX
                                player.playerY -= player.playerVY
                                player.playerVX *= -abs(math.sin(math.atan2(deltaX, deltaY)))
                                player.playerVY *= -abs(math.cos(math.atan2(deltaX, deltaY)))

                            else:
                                continue
                        else:
                            if 32 <= player.playerX <= self.width - 32 and \
                                    32 <= player.playerY <= self.height - 88:  # -32 - 56
                                continue
                            else:
                                player.playerX -= player.playerVX
                                player.playerY -= player.playerVY
                                player.playerVX = player.playerVY = 0

    def weapon_interreaction(self):
        weapons_to_delete = []
        for weapon in self.weapons_in_game:
            for player in self.players:
                # nastepny if sprawdza kolejno:
                # czy gracz nie ma broni,
                # czy bron nie jest podniesiona,
                # czy gracz ma wcisniety klawisz od podnieszenia,
                # czy styka się z bronią
                if weapon.place == True and \
                        math.sqrt((player.playerX - weapon.x - 32) ** 2 + \
                                  (player.playerY - weapon.y - 32) ** 2) < 64:
                    if (abs(weapon.vx) + abs(weapon.vy)) > 4 and player.joystickID != weapon.throw_player_id \
                            and player.alive == 1 and player.stun_time == 0:
                        if weapon.TYPE == 3:
                            self.sound_shot_body.play()
                            player.agony(10 * weapon.vx, 10 * weapon.vy)
                            weapon.vx = weapon.vy = 0.0
                            self.players = sorted(self.players, key=operator.attrgetter('alive'))
                        else:
                            self.sound_punch_weapon.play()
                            player.stun(10 * weapon.vx, 10 * weapon.vy, weapon.STUN)
                            weapon.vx = weapon.vy = 0.0
                    if len(player.weapon) == 0 and \
                            player.player.get_button(1):
                        weapon.place = False
                        weapon.vx = weapon.vy = 0.0  # zerowanie predkosci
                        player.weapon.append(weapon)
                        player.change_outfit()

            for i in range(len(maps.maps[self.choosed_map])):
                for n in range(len(maps.maps[self.choosed_map][0])):
                    if maps.maps[self.choosed_map][i][n] != 0:
                        deltaX = weapon.x - Map.TILE_SIZE * n
                        deltaY = weapon.y - Map.TILE_SIZE * i
                        if math.sqrt((deltaX) ** 2 + \
                                     (deltaY) ** 2) < 50:
                            # głośność jest zależna od predkosci przedmiotu
                            volume = (abs(weapon.vx) + abs(weapon.vy)) / 14 if ((abs(weapon.vx) + abs(
                                weapon.vy)) / 14) <= 1 else 1
                            self.sound_collision_weapon.set_volume(volume)
                            self.sound_collision_weapon.play()
                            weapon.vx *= -abs(math.sin(math.atan2(deltaX, deltaY)))
                            weapon.vy *= -abs(math.cos(math.atan2(deltaX, deltaY)))
                            weapon.x += weapon.vx
                            weapon.y += weapon.vy
                        else:
                            pass
                        # Usuwanie broni z mapy, po jej wyleceniu poza mape.
            if 0 <= weapon.x <= self.width - 32 and 0 <= weapon.y <= self.height - 88 or \
                    self.weapons_in_game.index(weapon) in weapons_to_delete:
                continue
            else:
                weapons_to_delete.append(self.weapons_in_game.index(weapon))
        weapons_to_delete.sort(reverse=True)
        for i in range(0, len(weapons_to_delete)):
            self.weapons_in_game.pop(weapons_to_delete[i])

    # Funkcja bullets_interreaction jest dosyć skompilkowana
    # Prawdopodobnie ulegnie przebudowie
    # Zeby nie raziłą w oczy swoją potęgą
    def bullets_interreaction(self):
        bullets_to_delete = []

        # Najpierw sprawdam czy nabój trafił gracza
        for bullet in self.bullets_in_game:
            for player in self.players:
                if math.sqrt((player.playerX - bullet.x) ** 2 + \
                             (player.playerY - bullet.y) ** 2) < 36 and \
                        bullet.playerID != player.joystickID:
                    self.sound_shot_body.play()
                    player.agony(bullet.vx, bullet.vy)
                    self.players = sorted(self.players, key=operator.attrgetter('alive'))
                    bullets_to_delete.append(self.bullets_in_game.index(bullet))

            # Potem sprawdzam czy naboj trafil w sciane, jesli tak to go niszcze
            for i in range(len(maps.maps[self.choosed_map])):
                for n in range(len(maps.maps[self.choosed_map][0])):
                    if maps.maps[self.choosed_map][i][n] != 0:
                        if math.sqrt((bullet.x - Map.TILE_SIZE * n - 32) ** 2 + \
                                     (bullet.y - Map.TILE_SIZE * i - 32) ** 2) < 32:
                            if self.bullets_in_game.index(bullet) not in bullets_to_delete:
                                self.sound_ricochet.play()
                                bullets_to_delete.append(self.bullets_in_game.index(bullet))
                            else:
                                pass
            # Sprawdzanie czy naboj nie wyleciał poza mape
            if 0 <= bullet.x <= self.width - 32 and 0 <= bullet.y <= self.height - 32:
                pass
            else:
                if self.bullets_in_game.index(bullet) not in bullets_to_delete:
                    bullets_to_delete.append(self.bullets_in_game.index(bullet))
                else:
                    pass
        bullets_to_delete.sort(reverse=True)
        for i in range(0, len(bullets_to_delete)):
            self.bullets_in_game.pop(bullets_to_delete[i])

    def menu_board(self, screen):  # pisana na szybko przy piwie wiec do poprawy
        players_menu = sorted(self.players, key=operator.attrgetter('joystickID'))
        menu = pygame.Rect(0, 1024, 1920, 1080)
        pygame.draw.rect(screen, [0, 0, 0], menu)
        win = self.font_size40.render(f"Win: {self.Menu.win}", True, self.colors[4])
        players_points = []
        for i in range(len(self.players)):
            players_points.append(
                self.font_size40.render(f"Player {i + 1} : {players_menu[i].points}", True, self.colors[i]))
        screen.blit(win, (32, 1036))
        for i in range(len(players_points)):
            screen.blit(players_points[i], (400 + 450 * i, 1036))

    def start(self, screen):
        self.music_in_game.play(-1)
        A = True
        while A:
            pygame.joystick.init()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    A = False
                    self.music_in_game.stop()
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    sys.exit(0)
            self.tps_clock.tick(self.TPS_MAX)
            screen.blit(self.title, (0, 0))
            text = self.font_size40.render("PRESS SPACE TO START", True, (0, 0, 0))
            screen.blit(text, (755, 755))
            pads = self.font_size40.render(f"CONNECTED JOYSTICKS: {pygame.joystick.get_count()}", True, (0, 0, 0))
            screen.blit(pads, (797, 281))
            pygame.display.flip()
            pygame.display.set_caption("Super Cruel Arena FPS:{}".format(self.tps_clock.get_fps()))

    def check(self):
        a = 0
        for player in self.players:
            if player.alive == 1:
                a += 1
        if a in (0, 1):
            self.reset()

    def reset(self):
        self.players = sorted(self.players, key=operator.attrgetter('joystickID'))
        for player in self.players:
            if player.alive == 1:
                player.points += 1
                self.end_round(self.screen, player)
                if player.points == self.Menu.win:
                    self.end_battle(self.screen)
        self.random_map()
        self.random_coordinates_players(pygame.joystick.get_count())
        self.weapons_in_game.clear()
        i = 0
        for player in self.players:
            player.walk.not_walking()
            player.revive(self.PLAYERS_COORDINATE[i][0], self.PLAYERS_COORDINATE[i][1])
            i += 1

    def end_battle(self, screen):
        self.players = sorted(self.players, key=operator.attrgetter('points'), reverse=True)
        A = True
        while A:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.game_works = False
                    self.Menu.menu_works = True
                    A = False
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.game_works = False
                    self.Menu.menu_works = True
                    A = False
            screen.fill((255, 255, 255))
            ROUND_WIN = self.font_size200.render("FINAL BOARD:", True, self.colors[5])
            screen.blit(ROUND_WIN, (350, 50))
            i = 50
            place = 0
            for player in self.players:
                player.walk.not_walking()
                i += 210
                place += 1
                screen.blit(
                    self.font_size200.render(f"{place}. PLAYER {player.joystickID + 1}: {player.points}", True,
                                             self.colors[player.joystickID]),
                    (350, i))
            pygame.display.flip()

    def end_round(self, screen, player):
        ROUND_WIN = self.font_size200.render("THE WINNER OF THE ROUND: ", True, self.colors[4])
        player_win = self.font_size300.render(f"Player {player.joystickID + 1}", True, self.colors[player.joystickID])
        screen.blit(ROUND_WIN, (200, 270))
        screen.blit(player_win, (500, 540))
        pygame.display.flip()
        pygame.time.wait(3000)


if __name__ == "__main__":
    Game()
