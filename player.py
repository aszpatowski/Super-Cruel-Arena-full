import math

import pygame
import random


class Player(object):
    playerX = 0.0
    playerY = 0.0
    playerVX = 0.0
    playerVY = 0.0
    playerAngle = 0.0
    joystickID = None
    rect = 0
    cooldown = 0
    alive = 1
    stun_time = None
    MIN_V = 0.25
    points = None

    def __init__(self, joystickID, X, Y):
        self.joystickID = joystickID
        self.playernormal = pygame.image.load(
            "textures/players/player{}/sprite_0.png".format(self.joystickID))
        self.playerstun = pygame.image.load(
            "textures/players/player{}/stunplayer.png".format(self.joystickID))
        self.playerdead = pygame.image.load(
            "textures/players/player{}/deadplayer.png".format(self.joystickID))
        self.playerak47 = pygame.image.load(
            "textures/players/player{}/ak47player.png".format(self.joystickID))
        self.playerpistol = pygame.image.load(
            "textures/players/player{}/pistolplayer.png".format(self.joystickID))
        self.playerknife = pygame.image.load(
            "textures/players/player{}/knifeplayer.png".format(self.joystickID))
        self.playerbaseball = pygame.image.load(
            "textures/players/player{}/baseballplayer.png".format(self.joystickID))
        self.playerimage = self.playernormal
        self.playerold = self.playerimage
        pygame.joystick.init()
        self.player = pygame.joystick.Joystick(self.joystickID)
        self.playerX = X
        self.playerY = Y
        self.sound_shot = pygame.mixer.Sound('sounds/colt.wav')
        self.sound_throw = pygame.mixer.Sound('sounds/throw.wav')
        self.sound_no_ammo = pygame.mixer.Sound('sounds/no_ammo.wav')
        self.font_type = pygame.font.Font('fonts/basic1/basic.ttf', 20)
        self.player.init()
        self.weapon = []
        self.stun_time = 0
        self.walk = Walk()
        self.points = 0
        self.sprint = 120
        self.does_sprint = 1
    def movement(self):
        self.does_sprint = self.does_sprint - 1 if self.does_sprint != 1 else 1
        if self.player.get_button(3) == 1 and self.sprint >= 60 and self.does_sprint == 1:
            self.does_sprint = 6
            self.sprint -= 60
        else:
            self.sprint = self.sprint + 1 if self.sprint < 120 else self.sprint
        self.playerVX = 3.5 * self.does_sprint * self.player.get_axis(0) if abs(self.player.get_axis(0)) > self.MIN_V else 0
        self.playerVY = 3.5 * self.does_sprint * self.player.get_axis(1) if abs(self.player.get_axis(1)) > self.MIN_V else 0
        self.cooldown = self.cooldown - 1 if self.cooldown > 0 else 0  # cooldown broni
        self.playerX += self.playerVX
        self.playerY += self.playerVY
        # print(self.player.get_button(0))

        if 'XBOX' in self.player.get_name():
            if round(self.player.get_axis(3), 2) != 0 or round(self.player.get_axis(4), 2) != 0:
                self.playerAngle = math.atan2(round(self.player.get_axis(4), 2), \
                                              round(self.player.get_axis(3), 2))

        elif self.player.get_name() == 'PC/PS3/Android':
            if round(self.player.get_axis(2), 2) != 0 or round(self.player.get_axis(3), 2) != 0:
                self.playerAngle = math.atan2(round(self.player.get_axis(2), 2), \
                                              round(self.player.get_axis(3), 2))
        else:
            if round(self.player.get_axis(2), 2) != 0 or round(self.player.get_axis(3), 2) != 0:
                self.playerAngle = math.atan2(round(self.player.get_axis(3), 2), \
                                              round(self.player.get_axis(2), 2))

        if abs(self.playerVX) + abs(self.playerVY) > 1.5:
            self.walk.walking()
        else:
            self.walk.not_walking()

    def interreaction(self, bullets_in_game, bullet):
        if len(self.weapon) != 0:
            if self.player.get_button(4) == 1:
                self.sound_throw.play()
                self.pop_weapon(0)
            elif self.weapon[0].TYPE in (1, 2) and self.player.get_button(5) == 1 \
                    and self.cooldown == 0:
                if self.weapon[0].bullets > 0:
                    self.sound_shot.play()
                    self.fire(bullets_in_game, bullet)
                else:
                    self.sound_no_ammo.play()
                    self.cooldown = self.weapon[0].cooldown

    def draw(self, screen,tps):
        self.rect = self.playerimage.get_rect(center=(self.playerX, self.playerY))
        # print(type(self.rect))
        self.playerimage = pygame.transform.rotate(self.playerold, math.degrees(self.playerAngle))
        if len(self.weapon) != 0 and self.weapon[0].TYPE in (1, 2) and self.alive == 1:
            self.ammo_text = self.font_type.render(
                f"{self.joystickID + 1} {self.weapon[0].bullets}/{self.weapon[0].MAX_BULLETS}", True,
                (0, 0, 0))
        else:
            self.ammo_text = self.font_type.render(
                f"{self.joystickID + 1}", True,
                (0, 0, 0))
        screen.blit(self.ammo_text, (self.playerX - 32, self.playerY - 50))
        screen.blit(self.playerimage, self.rect)
        if self.stun_time > 0 and self.alive == 1:
            screen.blit(self.font_type.render(
                f"{round(self.stun_time / tps, 2)} sec", True,
                (255, 255, 255)), (self.playerX, self.playerY))
            self.stun_time -= 1
            self.playerVX = self.playerVY = 0
            if self.stun_time == 0:
                self.change_outfit()

    def pop_weapon(self, type):
        if type:
            self.weapon[0].x = self.playerX - 32
            self.weapon[0].y = self.playerY - 32
            self.weapon[0].vx = 1 * self.playerVX + 5 * math.sin(self.playerAngle)
            self.weapon[0].vy = 1 * self.playerVY + 5 * math.cos(self.playerAngle)
            print(self.weapon[0].vx)
            print(self.weapon[0].vy)
            self.weapon[0].place = True
            self.weapon[0].throw_player_id = self.joystickID
            self.weapon.pop()
        else:
            self.weapon[0].x = self.playerX - 32 + 4 * math.sin(self.playerAngle)
            self.weapon[0].y = self.playerY - 32 + 4 * math.cos(self.playerAngle)
            self.weapon[0].vx = 2 * self.playerVX + 14 * math.sin(self.playerAngle)
            self.weapon[0].vy = 2 * self.playerVY + 14 * math.cos(self.playerAngle)
            self.weapon[0].place = True
            self.weapon[0].throw_player_id = self.joystickID
            self.weapon.pop()
            self.change_outfit()

    def fire(self, bullets_in_game, Bullet):
        self.cooldown = self.weapon[0].cooldown
        vx = 1 * self.playerVX * random.choice(self.weapon[0].recoil) + 15 * math.sin(
            self.playerAngle) + random.choice(self.weapon[0].recoil)
        vy = 1 * self.playerVY * random.choice(self.weapon[0].recoil) + 15 * (math.cos(
            self.playerAngle) + random.choice(self.weapon[0].recoil))
        bullets_in_game.append(Bullet(self.playerX,
                                      self.playerY,
                                      vx,
                                      vy,
                                      self.joystickID))
        self.weapon[0].bullets -= 1

    def change_outfit(self):
        if (len(self.weapon) == 0) and self.stun_time <= 0:
            self.playerimage = self.playerold = self.playernormal
        else:
            if (self.weapon[0].TYPE == 1):
                self.playerimage = self.playerak47
                self.playerold = self.playerimage
            elif (self.weapon[0].TYPE == 2):
                self.playerimage = self.playerpistol
                self.playerold = self.playerimage
            elif (self.weapon[0].TYPE == 3):
                self.playerimage = self.playerknife
                self.playerold = self.playerimage
            elif (self.weapon[0].TYPE == 4):
                self.playerimage = self.playerbaseball
                self.playerold = self.playerimage

    def agony(self, vx_bullet, vy_bullet):
        if (len(self.weapon)) != 0:
            self.pop_weapon(1)
        self.alive = 0
        self.playerVX += vx_bullet
        self.playerVY += vy_bullet
        self.playerAngle = math.degrees(math.atan2(vx_bullet, vy_bullet))
        self.playerimage = self.playerold = self.playerdead

    def stun(self, vx_bullet, vy_bullet, stun_time):
        if (len(self.weapon)) != 0:
            self.pop_weapon(1)
        self.stun_time = stun_time
        self.playerVX += vx_bullet
        self.playerVY += vy_bullet
        self.playerAngle = math.degrees(math.atan2(vx_bullet, vy_bullet))
        self.playerimage = self.playerold = self.playerstun

    def revive(self, x, y):
        self.alive = 1
        self.playerX = x
        self.playerY = y
        self.weapon.clear()
        self.playerimage = self.playerold = self.playernormal

class Walk():
    sound = None
    i = True  # Czy gierce wolno odtworzyć dźwięk?

    def __init__(self):
        self.sound = pygame.mixer.Sound('sounds/walking/walking2.wav')

    def walking(self):
        self.sound.set_volume(0.05)
        if self.i:
            self.sound.play(-1)
            self.i = False

    def not_walking(self):
        self.sound.stop()
        self.i = True
