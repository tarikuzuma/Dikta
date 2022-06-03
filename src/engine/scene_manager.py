from engine.timer import Timer
from engine import animator, prefs

import pygame

class SceneManager:
    def __init__(self):
        print("Initialized: Scene Manager")
        self.all_scenes = {}
        self._scene = None
        self._switching = False
        self._overlays = {}
        self.fade_surface = pygame.Surface(prefs.default.get("app.display.layer_size", (0, 0)))
        self.fade_surface.fill(pygame.Color("black"))
        self.fade_surface.set_alpha(255)
        self.fade_duration = prefs.default.get("app.misc.fade_duration", 1000)

    def _toggle_switching(self):
        self._switching = not self._switching

    def get_scene(self):
        return self._scene

    def set_scene(self, scene):
        self._toggle_switching()
        pending_scene = scene

        if isinstance(scene, str):
            if pending_scene in self.all_scenes:
                pending_scene = self.all_scenes[scene]
            else:
                return

        def _fade_in_done():
            self._scene = pending_scene
            animator.fadeout(
                self.fade_surface,
                self.fade_duration,
                self._toggle_switching
            )

        pending_scene.load_content()

        if self._scene:
            self._scene.dispose()
            animator.fadein(
                self.fade_surface,
                self.fade_duration,
                _fade_in_done
            )
        else:
            _fade_in_done()

    def add_overlay(self, id, scene):
        scene.load_content()
        self._overlays[id] = scene

    def remove_overlay(self, id):
        return self._overlays.pop(id, None)

    def get_overlay(self, id):
        return self._overlays.get(id, None)

    def update(self, game, events):
        if self._scene and \
           self._scene.enabled and not \
           self._switching:
            self._scene.update(game, events)

        for overlay in self._overlays.values():
            if not overlay.enabled:
                continue
            overlay.update(game, events)

    def draw(self, layer):
        if self._scene:
            self._scene.draw(layer)

        for overlay in self._overlays.values():
            overlay.draw(layer)

        layer.blit(self.fade_surface, (0, 0))
