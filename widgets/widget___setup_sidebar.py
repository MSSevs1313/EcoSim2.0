import pygame
import os
from properties import *
from pygame.locals import *
from threading import Thread
from screens.screen___pause import *
from widgets.widget___button import *
from widgets.widget___button_group import *
from widgets.widget___setup_button import *


class SetupSideBar:
    def __init__(self, height, sprite_group, GRID_LOCK, placement_method, game_method):
        self.width = 154
        self.height = height
        self.sidebar_rect = Rect((0, 0), (154, height))
        self.screen = screen
        self.setup_buttons = ButtonGroup()
        self.buttons = ButtonGroup()
        self.sprite_group = sprite_group
        self.GRID_LOCK = GRID_LOCK
        self.thread = Thread(target=self.run)
        self.thread.daemon = True
        self.is_alive = True

        # passing these in because at this point i don't have better ideas.
        self.placement_method = placement_method
        self.game_method = game_method

    def run(self):
        while True:
            self.monitor_buttons()

    def draw(self):
        # draw a rectangle for the background
        pygame.draw.rect(self.screen, (55, 55, 55, 100), self.sidebar_rect)

        # We'll need to pass in a universal list of available species instead of just writing it here.
        species = ["wolf", "deer", "bees", "plant", "bear"]
        self.make_setup_buttons()

        start_y = self.height - 52
        start = Button((13, start_y), "startnormal", "startselected", self.start_game)
        self.buttons.append(start)

        start.draw()

        self.draw_text()

        pygame.display.update()

    def draw_text(self):
        text_block = pygame.image.load(os.path.join(sidebar_dir, "placement_text" + png_ext))
        text_rect = Rect((0, 6), (154, 88))
        screen.blit(text_block, text_rect)

    def make_setup_buttons(self):
        iterator = 0
        start = (12, 102)
        for species in self.sprite_group.get_subgroups():
            setup_btn = SetupButton(iterator, start, species.type, species, self.set_placement_mode)
            setup_btn.draw()
            setup_btn.update_population()
            self.setup_buttons.append(setup_btn)
            iterator += 1

    def monitor_buttons(self):
        self.setup_buttons.monitor()
        self.buttons.monitor()

    def set_placement_mode(self, button, species):
        self.setup_buttons.deactivate_buttons()
        button.select_on()
        return self.placement_method(species)

    # Placeholder until we have a real way of pausing the game.
    def start_game(self):
        # self.sprite_group.pause()
        return self.game_method()
