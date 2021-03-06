from sprite import Sprite
import pygame
import vision
from properties import *


class PlantSprite(Sprite):
    sprite_image = pygame.image.load(os.path.join(sprites_dir, "plant.png"))

    def __init__(self, world_map, GRID_LOCK, coordinates=None):
        Sprite.__init__(self, world_map, self.sprite_image, GRID_LOCK, coordinates)
        self.type = "plant"
        self.movable_terrain = world_map.get_all_land_tile_types()
        self.is_pollinated = False
        self.pollinate_timer = 0

    def spawn(self):
        Sprite.spawn(self)
        self.tile.ignore_contents = True

    def move(self, target=None):
        """
        :param target: meaningless to plants, just there to suppress warning
        :return: changes plant pollination on a timer right now
        """
        self.pollinate_timer += 1
        if self.pollinate_timer % 25 == 0:
            self.pollinate()
        self.tile.set_sprite(self)
        self.tile.ignore_contents = True
        self.display(self.tile)

    def pollinate(self):
        """
        :return: checks for pollination and either pollinates or de-pollinates accordingly
        """
        if not self.is_pollinated:
            self.image = pygame.image.load(os.path.join(sprites_dir, "plantpollinated.png"))
            self.is_pollinated = True
        elif self.is_pollinated:
            self.image = pygame.image.load(os.path.join(sprites_dir, "plant.png"))
            self.is_pollinated = False
