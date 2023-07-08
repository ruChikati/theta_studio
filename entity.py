
import pygame

from . import physics


class Entity(physics.VerletObject):

    def __init__(self, x: int, y: int, w: int, h: int, name: str, anims: dict, game):
        super().__init__(pygame.Vector2(x, y), pygame.Vector2(x, y), pygame.Vector2(0, 0))
        self.w = w
        self.h = h
        self.anims = anims if anims is not None else {}
        self.rect = pygame.Rect(x, y, w, h)
        self.name = name
        self.game = game
        self.action = 'idle' if self.anims else None
        self.img = self.anims[self.action].get_img() if self.anims else None

    def update(self, dt):
        vel = self.pos - self.prev_pos
        self.prev_pos = self.pos
        self.game.camera.add_update_rects([self.rect])
        self.pos += vel + self.accel * dt * dt
        self.rect.topleft = self.pos
        self.game.camera.add_update_rects([self.rect])

        self.accel = pygame.Vector2(0, 0)
        self.img = self.anims[self.action].play(dt)
        self.game.camera.render(self.img, self.pos)
