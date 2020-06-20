import pygame
import sys
import random

class mainMenu:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cursorX = int(self.width / 2)
        self.cursorY = int(self.height / 2)
        self.cursorVX = 0
        self.cursorVY = 0
        pygame.joystick.init()
        self.user = pygame.joystick.Joystick(0)
        self.user.init()
        self.load_images()
        self.fonts_load()
        self.angle_animation = a = [n * 0.25 for n in range(-60, 61, 1)]
        self.rotate = 30
        self.direction = 1
        self.frame = 0
        self.music_status = 1
        self.sound_status = 1
        self.menu_works = 1
        self.response_time = 0
        self.win = 3
        self.options_run = 0
        self.positions_buttons_main_menu()
        self.positions_buttons_sound_n_music()
        self.positions_buttons_options()
        self.maps_random = [1, 1, 1]

    def positions_buttons_main_menu(self):

        self.start_text = self.font_size100.render("START", True, (255, 255, 255))
        self.options_text = self.font_size100.render("OPTIONS", True, (255, 255, 255))
        self.exit_text = self.font_size100.render("EXIT", True, (255, 255, 255))
        # MAIN MENU

        # BUTTONS

        # BIG_BUTTONS
        self.button_X = int(self.width / 2)
        # BUTTON START
        self.button_start_Y = int(self.height * 7 / 12)
        self.button_start_rect = self.buttonbasic_image.get_rect(center=(self.button_X, self.button_start_Y))
        self.text_start_rect = self.start_text.get_rect(center=(self.button_X, self.button_start_Y))
        # BUTTON OPTIONS
        self.button_options_Y = int(self.height * 9 / 12)
        self.button_options_rect = self.buttonbasic_image.get_rect(center=(self.button_X, self.button_options_Y))
        self.text_options_rect = self.options_text.get_rect(center=(self.button_X, self.button_options_Y))
        # BUTTON EXIT
        self.button_exit_Y = int(self.height * 11 / 12)
        self.button_exit_rect = self.buttonbasic_image.get_rect(center=(self.button_X, self.button_exit_Y))
        self.text_exit_rect = self.exit_text.get_rect(center=(self.button_X, self.button_exit_Y))

    def positions_buttons_sound_n_music(self):
        # SOUND AND MUSIC BUTTONS
        self.sound_n_music_buttons_Y = int(self.height * 11 / 12)

        self.sound_button_X = int(self.width * 27 / 32)
        self.sound_button_rect = self.sound_image[self.sound_status].get_rect(
            center=(self.sound_button_X, self.sound_n_music_buttons_Y))

        self.music_button_X = int(self.width * 30 / 32)
        self.music_button_rect = self.music_image[self.music_status].get_rect(
            center=(self.music_button_X, self.sound_n_music_buttons_Y))

    def positions_buttons_options(self):
        self.triangle_button_X = int(self.width / 3)

        self.triangleUP_button_Y = int(self.height * 5 / 9)
        self.triangleSQUARE_button_Y = int(self.height * 6 / 9)
        self.triangleDOWN_button_Y = int(self.height * 7 / 9)

        self.triangleUP_button_rect = self.upbutton_image.get_rect(
            center=(self.triangle_button_X, self.triangleUP_button_Y))

        self.triangleSQUARE_button_rect = self.buttonsquare_image.get_rect(
            center=(self.triangle_button_X, self.triangleSQUARE_button_Y))

        self.triangleDOWN_button_rect = self.downbutton_image.get_rect(
            center=(self.triangle_button_X, self.triangleDOWN_button_Y))

        self.win_text = self.font_size70.render(f"{self.win}", True, (255, 255, 255))
        self.win_text_rect = self.win_text.get_rect(center=(self.triangle_button_X, self.triangleSQUARE_button_Y))

        self.round_to_win_text_Y = int(self.height * 6 / 9)

        self.round_to_win_text_X = int(self.width * 3 / 20)
        self.round_to_win_text = self.font_size70.render("ROUND TO WIN: ", True, (0, 0, 0))
        self.round_to_win_text_rect = self.round_to_win_text.get_rect(
            center=(self.round_to_win_text_X, self.round_to_win_text_Y))

        # BUTTON BACK

        self.button_back_X = int(self.width * 3 / 20)
        self.button_back_Y = int(self.height * 9 / 10)
        self.button_back_rect = self.buttonbasic_image.get_rect(center=(self.button_back_X, self.button_back_Y))

        self.back_text = self.font_size100.render("BACK", True, (255, 255, 255))
        self.back_text_rect = self.back_text.get_rect(center=(self.button_back_X, self.button_back_Y))


        #RIGHT

        self.button_map_X = int(self.width * 17 / 20)
        self.button_map_Y1 = int(self.height * 5 / 9)
        self.button_map_Y2 = int(self.height * 6 / 9)
        self.button_map_Y3 = int(self.height * 7 / 9)

        self.button_map_rect1 = self.buttonsquare_image.get_rect(center=(self.button_map_X, self.button_map_Y1))
        self.button_map_rect2 = self.buttonsquare_image.get_rect(center=(self.button_map_X, self.button_map_Y2))
        self.button_map_rect3 = self.buttonsquare_image.get_rect(center=(self.button_map_X, self.button_map_Y3))

        self.map1_text = self.font_size100.render("MAP 1", True, (127,255,0))
        self.map2_text = self.font_size100.render("MAP 2", True, (34,139,34))
        self.map3_text = self.font_size100.render("MAP 3", True, (128,128,0))

        self.map_textX = int(self.width * 14 / 20)
        self.map_textY1 = self.button_map_Y1
        self.map_textY2 = self.button_map_Y2
        self.map_textY3 = self.button_map_Y3

        self.map_text_rect1 = self.map1_text.get_rect(center=(self.map_textX, self.map_textY1))
        self.map_text_rect2 = self.map2_text.get_rect(center=(self.map_textX, self.map_textY2))
        self.map_text_rect3 = self.map3_text.get_rect(center=(self.map_textX, self.map_textY3))
    def fonts_load(self):
        self.font_size40 = pygame.font.Font('fonts/basic/basic.ttf', 40)
        self.font_size70 = pygame.font.Font('fonts/basic/basic.ttf', 70)
        self.font_size100 = pygame.font.Font('fonts/basic/basic.ttf', 100)
        self.font_size200 = pygame.font.Font('fonts/basic/basic.ttf', 200)
        self.font_size300 = pygame.font.Font('fonts/basic/basic.ttf', 300)

    def load_images(self):
        self.oldlogo = pygame.transform.scale(pygame.image.load('logos/test4.png'),
                                              (int(self.height * 1.6 / 2.5), int(self.height / 2.5)))
        self.logo = self.oldlogo
        self.crosshair_image = pygame.transform.scale(
            pygame.image.load('textures/crosshair/crosshair.png').convert_alpha(),
            (int(64), int(64)))
        self.buttonbasic_image = pygame.transform.scale(pygame.image.load('buttons/buttonbasic.png').convert_alpha(),
                                                        (int(self.width / 4), int(self.height / 8)))
        self.buttonbasicSELECTED_image = pygame.transform.scale(
            pygame.image.load('buttons/buttonbasicSELECTED.png').convert_alpha(),
            (int(self.width / 4), int(self.height / 8)))
        self.buttonsquare_image = pygame.transform.scale(pygame.image.load('buttons/buttonsquare.png').convert_alpha(),
                                                         (int(self.height / 10), int(self.height / 10)))
        self.buttonsquareON_image = pygame.transform.scale(pygame.image.load('buttons/buttonsquareON.png').convert_alpha(),
                                                         (int(self.height / 10), int(self.height / 10)))
        self.buttonsquareSELECTED_image = pygame.transform.scale(pygame.image.load('buttons/buttonsquareSELECTED.png').convert_alpha(),
                                                         (int(self.height / 10), int(self.height / 10)))
        self.circlebutton_image = pygame.image.load('buttons/circlebutton.png').convert_alpha()
        self.circlebuttonSELECTED_image = pygame.transform.scale(
            pygame.image.load('buttons/circlebuttonSELECTED.png').convert_alpha(),
            (int(self.height / 10), int(self.height / 10)))
        self.upbutton_image = pygame.transform.scale(pygame.image.load('buttons/upbutton.png').convert_alpha(),
                                                     (int(self.height / 10), int(self.height / 10)))
        self.upbuttonSELECTED_image = pygame.transform.scale(
            pygame.image.load('buttons/upbuttonSELECTED.png').convert_alpha(),
            (int(self.height / 10), int(self.height / 10)))
        self.downbutton_image = pygame.transform.scale(pygame.image.load('buttons/downbutton.png').convert_alpha(),
                                                       (int(self.height / 10), int(self.height / 10)))
        self.downbuttonSELECTED_image = pygame.transform.scale(
            pygame.image.load('buttons/downbuttonSELECTED.png').convert_alpha(),
            (int(self.height / 10), int(self.height / 10)))
        self.music_image = [pygame.transform.scale(pygame.image.load('buttons/musicOFF.png').convert_alpha(),
                                                   (int(self.height / 10), int(self.height / 10))),
                            pygame.transform.scale(pygame.image.load('buttons/musicON.png').convert_alpha(),
                                                   (int(self.height / 10), int(self.height / 10)))]
        self.sound_image = [pygame.transform.scale(pygame.image.load('buttons/soundOFF.png').convert_alpha(),
                                                   (int(self.height / 10), int(self.height / 10))),
                            pygame.transform.scale(pygame.image.load('buttons/soundON.png').convert_alpha(),
                                                   (int(self.height / 10), int(self.height / 10)))]

    def draw(self, screen, music_in_game):
        self.where_collision = 0
        screen.fill((255, 255, 255))
        # LOGO
        screen.blit(self.logo, self.logo.get_rect(center=(int(self.width / 2), int(self.height / 4))))

        # BUTTONS
        if self.options_run == 0:
            screen.blit(self.buttonbasic_image,
                        self.button_start_rect)
            screen.blit(self.start_text, self.text_start_rect)

            screen.blit(self.buttonbasic_image,
                        self.button_options_rect)
            screen.blit(self.options_text, self.text_options_rect)

            screen.blit(self.buttonbasic_image,
                        self.button_exit_rect)
            screen.blit(self.exit_text, self.text_exit_rect)
        else:
            #LEFT

            screen.blit(self.upbutton_image, self.triangleUP_button_rect)

            screen.blit(self.buttonsquare_image, self.triangleSQUARE_button_rect)

            screen.blit(self.round_to_win_text, self.round_to_win_text_rect)

            screen.blit(self.win_text, self.win_text_rect)

            screen.blit(self.downbutton_image, self.triangleDOWN_button_rect)

            screen.blit(self.buttonbasic_image, self.button_back_rect)

            screen.blit(self.back_text, self.back_text_rect)

            #RIGHT

            screen.blit(self.map1_text, self.map_text_rect1)
            screen.blit(self.map2_text, self.map_text_rect2)
            screen.blit(self.map3_text, self.map_text_rect3)

            if self.maps_random[0] == 1:
                screen.blit(self.buttonsquareON_image,self.button_map_rect1)
            else:
                screen.blit(self.buttonsquare_image, self.button_map_rect1)

            if self.maps_random[1] == 1:
                screen.blit(self.buttonsquareON_image,self.button_map_rect2)
            else:
                screen.blit(self.buttonsquare_image, self.button_map_rect2)

            if self.maps_random[2] == 1:
                screen.blit(self.buttonsquareON_image,self.button_map_rect3)
            else:
                screen.blit(self.buttonsquare_image, self.button_map_rect3)

        screen.blit(self.sound_image[self.sound_status], self.sound_button_rect)

        screen.blit(self.music_image[self.music_status], self.music_button_rect)
        self.collision(screen, music_in_game)
        # CELOWNIK
        screen.blit(self.crosshair_image, self.crosshair_image.get_rect(center=(self.cursorX, self.cursorY)))

    def movement(self):
        self.cursorVX = 5 * self.user.get_axis(0)
        self.cursorVY = 5 * self.user.get_axis(1)
        self.cursorX += self.cursorVX
        self.cursorY += self.cursorVY

    def logo_rotating(self):
        if self.frame == 4:
            self.logo = pygame.transform.rotate(self.oldlogo, self.angle_animation[self.rotate])
            if self.rotate in (0, len(self.angle_animation) - 1):
                self.direction *= -1
            if self.direction == 1:
                self.rotate += 1
            if self.direction == -1:
                self.rotate -= 1
            self.frame = 0
        self.frame += 1

    def collision(self, screen, music_in_game):
        self.response_time = self.response_time - 1 if self.response_time > 0 else 0

        # MAIN MENU
        if self.options_run == 0:
            if self.button_X - int(self.width / 8) <= self.cursorX <= self.button_X + int(self.width / 8):
                if self.button_start_Y - int(self.height / 16) <= self.cursorY <= self.button_start_Y + int(
                        self.height / 16):
                    screen.blit(self.buttonbasicSELECTED_image, self.button_start_rect)
                    if self.press():
                        self.menu_works = 0
                elif self.button_options_Y - int(self.height / 16) <= self.cursorY <= self.button_options_Y + int(
                        self.height / 16):
                    screen.blit(self.buttonbasicSELECTED_image, self.button_options_rect)
                    if self.press():
                        self.options_run = 1
                elif self.button_exit_Y - int(self.height / 16) <= self.cursorY <= self.button_exit_Y + int(
                        self.height / 16):
                    screen.blit(self.buttonbasicSELECTED_image, self.button_exit_rect)
                    if self.press():
                        sys.exit(0)

        # OPTIONS
        else:
            # LEFT

            if self.button_back_X - int(self.width / 8) <= self.cursorX <= self.button_back_X + int(self.width / 8) and \
                    self.button_back_Y - int(self.height / 16) <= self.cursorY <= self.button_back_Y + int(
                self.height / 16):
                screen.blit(self.buttonbasicSELECTED_image, self.button_back_rect)
                if self.press():
                    self.options_run = 0
            if self.triangle_button_X - int(self.height / 20) <= self.cursorX <= self.triangle_button_X + int(
                    self.height / 20):
                if self.triangleUP_button_Y - int(self.height / 20) <= self.cursorY <= self.triangleUP_button_Y + int(
                        self.height / 20):
                    screen.blit(self.upbuttonSELECTED_image, self.triangleUP_button_rect)
                    if self.press() and self.response_time == 0:
                        self.response_time = 10
                        self.win = self.win + 1 if self.win < 99 else 1
                        self.win_text = self.font_size70.render(f"{self.win}", True, (255, 255, 255))
                        self.win_text_rect = self.win_text.get_rect(
                            center=(self.triangle_button_X, self.triangleSQUARE_button_Y))
                if self.triangleDOWN_button_Y - int(
                        self.height / 20) <= self.cursorY <= self.triangleDOWN_button_Y + int(
                    self.height / 20):
                    screen.blit(self.downbuttonSELECTED_image, self.triangleDOWN_button_rect)
                    if self.press() and self.response_time == 0:
                        self.response_time = 10
                        self.win = self.win - 1 if self.win > 1 else 99
                        self.win_text = self.font_size70.render(f"{self.win}", True, (255, 255, 255))
                        self.win_text_rect = self.win_text.get_rect(
                            center=(self.triangle_button_X, self.triangleSQUARE_button_Y))
            # RIGHT
            if self.button_map_X - int(self.height/20) <= self.cursorX <= self.button_map_X + int(self.height/20):
                if self.button_map_Y1 - int(self.height / 20) <= self.cursorY <= self.button_map_Y1 + int(
                    self.height / 20):
                    screen.blit(self.buttonsquareSELECTED_image,self.button_map_rect1)
                    if self.press() and self.response_time == 0:
                        self.response_time = 30
                        self.maps_random[0] = abs(self.maps_random[0] - 1)
                        if 1 not in self.maps_random:
                                    self.maps_random[2] = 1
                if self.button_map_Y2 - int(self.height / 20) <= self.cursorY <= self.button_map_Y2 + int(
                        self.height / 20):
                    screen.blit(self.buttonsquareSELECTED_image, self.button_map_rect2)
                    if self.press() and self.response_time == 0:
                        self.response_time = 30
                        self.maps_random[1] = abs(self.maps_random[1] - 1)
                        if 1 not in self.maps_random:
                            self.maps_random[random.choice([0,2])] = 1
                if self.button_map_Y3 - int(self.height / 20) <= self.cursorY <= self.button_map_Y3 + int(
                        self.height / 20):
                    screen.blit(self.buttonsquareSELECTED_image, self.button_map_rect3)
                    if self.press() and self.response_time == 0:
                        self.response_time = 30
                        self.maps_random[2] = abs(self.maps_random[2] - 1)
                        if 1 not in self.maps_random:
                            self.maps_random[0] = 1

        # CIRCLE MUSIC AND SOUND
        if abs(self.cursorY - self.sound_n_music_buttons_Y) <= int(self.height / 20):

            if abs(self.cursorX - self.sound_button_X) <= int(self.height / 20):

                screen.blit(self.circlebuttonSELECTED_image, self.sound_button_rect)

                if self.press() and self.response_time == 0:
                    self.response_time = 60
                    self.sound_status = abs(self.sound_status - 1)
                    if self.music_status == 0:
                        pygame.mixer.pause()
                    else:
                        pygame.mixer.unpause()

            elif abs(self.cursorX - self.music_button_X) <= int(self.height / 20):

                screen.blit(self.circlebuttonSELECTED_image, self.music_button_rect)

                if self.press() and self.response_time == 0:
                    self.response_time = 60
                    self.music_status = abs(self.music_status - 1)
                    if self.music_status == 0:
                        music_in_game.stop()
                    else:
                        music_in_game.play(-1)
        # IF CURSOR OUT OF SCREEN
        if self.cursorX > self.width or self.cursorX < 0 or self.cursorY > self.height or self.cursorY < 0:
            self.cursorX = self.width / 2
            self.cursorY = self.height / 2

    def press(self):
        if self.user.get_button(0) or self.user.get_button(2):
            return True
        else:
            return False
