import pygame

from . import physics


class Entity(physics.VerletObject):
    def __init__(self, x: int, y: int, w: int, h: int, name: str, anims: dict, game):
        super().__init__(
            pygame.Vector2(x, y), pygame.Vector2(x, y), pygame.Vector2(0, 0), w, h
        )
        self.rot = 0
        self.anims = anims if anims is not None else {}
        self.rect = pygame.Rect(x, y, w, h)
        self.name = name
        self.game = game
        self.action = "idle" if self.anims else None
        self.img = self.anims[self.action].get_img() if self.anims else None

    def update(self, dt):
        old_rect = self.rect.copy()
        vel = self.pos - self.prev_pos
        self.prev_pos = self.pos.copy()
        self.pos += vel + self.accel * dt * dt
        self.rect.topleft = self.pos
        self.rot %= 360
        self.game.camera.add_update_rect(self.rect.union(old_rect).inflate(3, 3))

        self.accel = pygame.Vector2(0, 0)
        self.img = self.anims[self.action].play(dt)
        self.game.camera.render(self.img, self.pos)

    @property
    def centre(self) -> pygame.Vector2:
        return self.pos + pygame.Vector2(self.w // 2, self.h // 2)


class SpriteStackEntity(physics.VerletObject):
    def __init__(
        self, x: int, y: int, w: int, h: int, name: str, spritestacks: dict, game
    ):
        super().__init__(
            pygame.Vector2(x, y), pygame.Vector2(x, y), pygame.Vector2(0, 0), w, h
        )
        self.rot = 0
        self.spritestacks = spritestacks if spritestacks is not None else {}
        self.rect = pygame.Rect(x, y, w, h)
        self.name = name
        self.game = game
        self.action = "idle" if self.spritestacks else None

    def update(self, dt):
        old_rect = self.rect.copy()
        vel = self.pos - self.prev_pos
        self.prev_pos = self.pos
        self.pos += vel + self.accel * dt * dt
        self.rect.topleft = self.pos
        self.rot %= 360
        self.game.camera.add_update_rect(self.rect.union(old_rect).inflate(3, 3))

        self.accel = pygame.Vector2(0, 0)
        self.spritestacks[self.action].render_to_game(
            self.game, (self.pos.x + self.w // 2, self.pos.y + self.h // 2), self.rot
        )
