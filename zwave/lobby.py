# -*- conding: utf-8 -*-

import json
import os
import sys

import pygame

import zwave.game
import zwave.helper

class Lobby:

    def __init__(self):

        ## load data ##
        self.load_settings()
        self.load_language()

        ## fonts ##
        pygame.font.init()
        self.font = pygame.font.Font(os.path.join("assets", "fonts", "Renogare.ttf"), 30)

        ## init values ##
        self.running = True
        self.screen = pygame.display.set_mode((1024, 512))
        self.background = zwave.helper.pygame_image(os.path.join("assets", "img", "background.png"), 1024, 512)
        self.page = "main"

        self.cursor = None

        self.bt_exit = {}
        self.bt_settings = {}
        self.bt_start = {}

        self.bt_ptbr = {}
        self.bt_enus = {}
        self.bt_1024x512 = {}
        self.bt_1366x768 = {}
        self.bt_fullscreen = {}
        self.bt_back = {}

        self.set_sounds()
        self.buttons()
        self.set_cursor()
        self.loop()

    def load_settings(self):
        self.settings = json.loads(open("data/settings.json").read())

    def load_language(self):
        if sys.version_info.major > 2:
            self.text = json.loads(open("data/languages/%s.json" % self.settings["language"], encoding="utf-8").read())
        else:
            self.text = json.loads(open("data/languages/%s.json" % self.settings["language"]).read())

    def save_settings(self):
        with open("data/settings.json", "w") as outfile:
            json.dump(self.settings, outfile, indent=4)

    def reload(self):
        self.save_settings()
        self.load_language()
        self.buttons()

    def set_sounds(self):

        self.sound = {}
        self.sound["volume"] = {}
        self.sound["volume"]["geral"] = 1
        self.sound["volume"]["music"] = 0.8
        self.sound["volume"]["effects"] = 0.8

        ## init pygame mixer and configure ##
        pygame.mixer.init(22050, -16, 1, 512)

        ## load, set volume and init music background ##
        pygame.mixer.music.load(os.path.join("assets", "sounds", "music", "1.ogg"))
        pygame.mixer.music.set_volume(self.sound["volume"]["music"] * self.sound["volume"]["geral"])
        pygame.mixer.music.play(-1)

        self.sound["channel"] = pygame.mixer.Channel(1)

    def set_cursor(self):
        pygame.mouse.set_visible(False)
        size = 35
        image = os.path.join("assets", "img", "cursor.png")
        image = zwave.helper.pygame_image(image, size)
        sprite = zwave.helper.pygame_sprite_by_image(image)
        self.cursor = pygame.sprite.GroupSingle(sprite)

    def buttons(self):
        ## start game button ##
        x = 1024 / 2
        y = (512 / 2) - 65
        self.bt_start["normal"] = zwave.helper.pygame_button(self.text["start"].upper(), self.font, x, y, (50, 50, 50), "center")
        self.bt_start["hover"] = zwave.helper.pygame_button(self.text["start"].upper(), self.font, x, y, (0, 140, 90), "center")
        self.bt_start["draw"] =  self.bt_start["normal"]

        ## settings button #
        x = 1024 / 2
        y = (512 / 2)
        self.bt_settings["normal"] = zwave.helper.pygame_button(self.text["settings"].upper(), self.font, x, y, (50, 50, 50), "center")
        self.bt_settings["hover"] = zwave.helper.pygame_button(self.text["settings"].upper(), self.font, x, y, (0, 140, 90), "center")
        self.bt_settings["draw"] =  self.bt_settings["normal"]

        ## exit button #
        x = 1024 / 2
        y = (512 / 2) + 65
        self.bt_exit["normal"] = zwave.helper.pygame_button(self.text["exit"].upper(), self.font, x, y, (50, 50, 50), "center")
        self.bt_exit["hover"] = zwave.helper.pygame_button(self.text["exit"].upper(), self.font, x, y, (0, 140, 90), "center")
        self.bt_exit["draw"] =  self.bt_exit["normal"]

        ## pt-br button #
        x = (1024 / 2) - 5
        y = (512 / 2) - 65
        self.bt_ptbr["normal"] = zwave.helper.pygame_button("PT-BR", self.font, x, y, (50, 50, 50), "left")
        self.bt_ptbr["hover"] = zwave.helper.pygame_button("PT-BR", self.font, x, y, (0, 140, 90), "left")
        self.bt_ptbr["selected"] = zwave.helper.pygame_button("PT-BR", self.font, x, y, (0, 0, 0), "left")
        self.bt_ptbr["draw"] =  self.bt_ptbr["normal"]

        ## en-us button #
        x = (1024 / 2) + 5
        y = (512 / 2) - 65
        self.bt_enus["normal"] = zwave.helper.pygame_button("EN-US", self.font, x, y, (50, 50, 50), "right")
        self.bt_enus["hover"] = zwave.helper.pygame_button("EN-US", self.font, x, y, (0, 140, 90), "right")
        self.bt_enus["selected"] = zwave.helper.pygame_button("EN-US", self.font, x, y, (0, 0, 0), "right")
        self.bt_enus["draw"] =  self.bt_enus["normal"]

        ## 1024x512 button #
        x = (1024 / 2) - 5
        y = 512 / 2
        self.bt_1024x512["normal"] = zwave.helper.pygame_button("1024x512", self.font, x, y, (50, 50, 50), "left")
        self.bt_1024x512["hover"] = zwave.helper.pygame_button("1024x512", self.font, x, y, (0, 140, 90), "left")
        self.bt_1024x512["selected"] = zwave.helper.pygame_button("1024x512", self.font, x, y, (0, 0, 0), "left")
        self.bt_1024x512["draw"] =  self.bt_1024x512["normal"]

        ## 1366x768 button #
        x = (1024 / 2) + 5
        y = 512 / 2
        self.bt_1366x768["normal"] = zwave.helper.pygame_button("1366x768", self.font, x, y, (50, 50, 50), "right")
        self.bt_1366x768["hover"] = zwave.helper.pygame_button("1366x768", self.font, x, y, (0, 140, 90), "right")
        self.bt_1366x768["selected"] = zwave.helper.pygame_button("1366x768", self.font, x, y, (0, 0, 0), "right")
        self.bt_1366x768["draw"] =  self.bt_1366x768["normal"]

        ## fullscreen button #
        x = 1024 / 2
        y = (512 / 2) + 65
        self.bt_fullscreen["normal"] = zwave.helper.pygame_button(self.text["fullscreen"].upper(), self.font, x, y, (50, 50, 50), "center")
        self.bt_fullscreen["hover"] = zwave.helper.pygame_button(self.text["fullscreen"].upper(), self.font, x, y, (0, 140, 90), "center")
        self.bt_fullscreen["selected"] = zwave.helper.pygame_button(self.text["fullscreen"].upper(), self.font, x, y, (0, 0, 0), "center")
        self.bt_fullscreen["draw"] =  self.bt_fullscreen["normal"]

        ## back button #
        x = 1024 / 2
        y = (512 / 2) + 130
        self.bt_back["normal"] = zwave.helper.pygame_button(self.text["back"].upper(), self.font, x, y, (50, 50, 50), "center")
        self.bt_back["hover"] = zwave.helper.pygame_button(self.text["back"].upper(), self.font, x, y, (0, 140, 90), "center")
        self.bt_back["draw"] =  self.bt_back["normal"]

    def draw(self):

        ## draw lobby main page buttons ##
        if self.page == "main":

            ## start game button ##
            self.bt_start["draw"].draw(self.screen)

            ## go to settings page button ##
            self.bt_settings["draw"].draw(self.screen)

            ## exit game button ##
            self.bt_exit["draw"].draw(self.screen)

        ## draw lobby settings page buttons ##
        elif self.page == "settings":

            ## language pt-br ##
            if self.settings["language"] == "pt-br":
                self.bt_ptbr["selected"].draw(self.screen)
            else:
                self.bt_ptbr["draw"].draw(self.screen)

            ## language en-us ##
            if self.settings["language"] == "en-us":
                self.bt_enus["selected"].draw(self.screen)
            else:
                self.bt_enus["draw"].draw(self.screen)

            ## resolution 1024x512 ##
            if (self.settings["width"] == 1024) and (self.settings["height"] == 512) :
                self.bt_1024x512["selected"].draw(self.screen)
            else:
                self.bt_1024x512["draw"].draw(self.screen)

            ## resolution 1366x768 ##
            if (self.settings["width"] == 1366) and (self.settings["height"] == 768):
                self.bt_1366x768["selected"].draw(self.screen)
            else:
                self.bt_1366x768["draw"].draw(self.screen)

            ## fullscreen on or off ##
            if self.settings["fullscreen"]:
                self.bt_fullscreen["selected"].draw(self.screen)
            else:
                self.bt_fullscreen["draw"].draw(self.screen)

            ## back to loby main page ##
            self.bt_back["draw"].draw(self.screen)

    def mouse_hover(self, button):
        if pygame.sprite.groupcollide(self.cursor, button, False, False):
            return True
        else:
            return False

    def start_game(self):
        self.running = False
        settings = self.settings
        zwave.game.Game(self.text, settings["scale"], settings["width"], settings["height"], settings["fullscreen"])

    def loop(self):

        ## set pygame clock ##
        clock = pygame.time.Clock()

        while self.running:

            pygame.display.set_caption("FPS: %.0f" % clock.get_fps())

            ## fill screen ##
            self.screen.blit(self.background, (0, 0))
            
            ## cursor x position ##
            self.cursor.sprites()[0].rect.x = pygame.mouse.get_pos()[0]
            self.cursor.sprites()[0].rect.y = pygame.mouse.get_pos()[1]

            ## draw menu ##
            self.draw()

            ## draw cursor ##
            self.cursor.draw(self.screen)

            ## hover effect for lobby main page buttons #
            if self.page == "main":

                ## game start button ##
                if self.mouse_hover(self.bt_start["draw"]):
                    self.bt_start["draw"] = self.bt_start["hover"]
                else:
                    self.bt_start["draw"] = self.bt_start["normal"]

                ## game settings button ##
                if self.mouse_hover(self.bt_settings["draw"]):
                    self.bt_settings["draw"] = self.bt_settings["hover"]
                else:
                    self.bt_settings["draw"] = self.bt_settings["normal"]

                ## exit game button ##
                if self.mouse_hover(self.bt_exit["draw"]):
                    self.bt_exit["draw"] = self.bt_exit["hover"]
                else:
                    self.bt_exit["draw"] = self.bt_exit["normal"]


            ## hover effect for lobby settings page buttons #
            elif self.page == "settings":

                ## language pt-br ##
                if self.mouse_hover(self.bt_ptbr["draw"]):
                    self.bt_ptbr["draw"] = self.bt_ptbr["hover"]
                else:
                    self.bt_ptbr["draw"] = self.bt_ptbr["normal"]

                ## language en-us ##
                if self.mouse_hover(self.bt_enus["draw"]):
                    self.bt_enus["draw"] = self.bt_enus["hover"]
                else:
                    self.bt_enus["draw"] = self.bt_enus["normal"]

                ## resolution 1024x512 ##
                if self.mouse_hover(self.bt_1024x512["draw"]):
                    self.bt_1024x512["draw"] = self.bt_1024x512["hover"]
                else:
                    self.bt_1024x512["draw"] = self.bt_1024x512["normal"]

                ## resolution 1366x768 ##
                if self.mouse_hover(self.bt_1366x768["draw"]):
                    self.bt_1366x768["draw"] = self.bt_1366x768["hover"]
                else:
                    self.bt_1366x768["draw"] = self.bt_1366x768["normal"]

                ## fullscreen ##
                if self.mouse_hover(self.bt_fullscreen["draw"]):
                    self.bt_fullscreen["draw"] = self.bt_fullscreen["hover"]
                else:
                    self.bt_fullscreen["draw"] = self.bt_fullscreen["normal"]

                ## back to lobby main page ##
                if self.mouse_hover(self.bt_back["draw"]):
                    self.bt_back["draw"] = self.bt_back["hover"]
                else:
                    self.bt_back["draw"] = self.bt_back["normal"]

            ## game events ##
            for event in pygame.event.get():

                ## check button clicks ##
                if event.type == pygame.MOUSEBUTTONUP:

                    ## lobby main page ##
                    if self.page == "main":

                        ## game start ##
                        if self.mouse_hover(self.bt_start["draw"]):
                            self.start_game()

                        ## game settings ##
                        if self.mouse_hover(self.bt_settings["draw"]):
                            self.page = "settings"

                        ## game quit ##
                        if self.mouse_hover(self.bt_exit["draw"]):
                            self.running = False

                    ## lobby settings page ##
                    elif self.page == "settings":

                        ## language pt-br ##
                        if self.mouse_hover(self.bt_ptbr["draw"]):
                            self.settings["language"] = "pt-br"
                            self.reload()

                        ## language en-us ##
                        if self.mouse_hover(self.bt_enus["draw"]):
                            self.settings["language"] = "en-us"
                            self.reload()

                        ## resolution 1024x512 ##
                        if self.mouse_hover(self.bt_1024x512["draw"]):
                            self.settings["width"] = 1024
                            self.settings["height"] = 512
                            self.settings["scale"] = 1
                            self.reload()

                        ## resolution 1366x768 ##
                        if self.mouse_hover(self.bt_1366x768["draw"]):
                            self.settings["width"] = 1366
                            self.settings["height"] = 768
                            self.settings["scale"] = 2
                            self.reload()

                        ## fullscreen ##
                        if self.mouse_hover(self.bt_fullscreen["draw"]):
                            if self.settings["fullscreen"]:
                                self.settings["fullscreen"] = False
                            else:
                                self.settings["fullscreen"] = True
                            self.reload()

                        ## back to lobby main page ##
                        if self.mouse_hover(self.bt_back["draw"]):
                            self.page = "main"

                ## quit ##
                if event.type == pygame.QUIT:
                    self.running = False

            ## pygame clock tick ##
            clock.tick(60)

            ## update pygame screen ##
            pygame.display.update()