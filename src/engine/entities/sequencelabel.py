from engine.entities import Entity, Label
from engine.timer import Timer

import pygame

PIXEL_INCREMENT = 5

class SequenceLabel(Label):
    def __init__(self, text, font, color, position_or_rect = (0, 0), size = None):
        super().__init__(text, font, color, position_or_rect, size)

    def skip(self):
        if self.completed:
            return

        self._timer.close()
        self.completed = True
        self._surface = self._text_surface

    def _add_char_to_surface(self, sender):
        if self._rect_offset.x >= self._rect.width:
            sender.close()
            self.completed = True
            return

        self.get_surface().blit(self._text_surface, self._rect_offset, self._rect_offset)
        self._rect_offset.x += PIXEL_INCREMENT

    def _on_entity_dirty(self, resize = True):
        rendered_text = self.get_font().render(self.get_text(), self.get_color())
        self._surface = pygame.Surface(rendered_text[1].size, pygame.SRCALPHA, 32)
        self._text_surface = rendered_text[0]
        self._rect_offset = pygame.Rect(0, 0, PIXEL_INCREMENT, rendered_text[1].height)
        self._timer = Timer(1, False, True)
        self._timer.elapsed += self._add_char_to_surface
        self.completed = False

        if resize:
            self._mask = None
            self._rect.size = rendered_text[1].size

        self.entity_dirty(self, resize)

    def set_text(self, text):
        self._text = text
        self._on_entity_dirty()

    def set_font(self, font):
        self._font = font
        self._on_entity_dirty()

    def set_color(self, color):
        self._color = color
        self._on_entity_dirty(False)

    def draw(self, layer):
        if not self.get_surface():
            return

        layer.blit(self.get_surface(), self._rect)

    def update(self, game, events):
        if not self.completed and not self._timer.enabled:
            self._timer.start()