from engine import Scene
from engine.entities import *
from app import utils

import pygame

class MouseOverlay(Scene):
    def __init__(self):
        super().__init__("Mouse Overlay")

    def update(self, game, events):
        super().update(game, events)
        if not utils.cursor_current:
            return
        scaled_pos = game.get_mouse_pos()
        cursor_rect = utils.cursor_current.get_rect()
        self.cursor_rect = pygame.Rect(
            scaled_pos[0],
            scaled_pos[1],
            cursor_rect.width,
            cursor_rect.height
        )

    def draw(self, layer):
        super().draw(layer)
        if not utils.cursor_current:
            return
        layer.blit(utils.cursor_current, self.cursor_rect)
