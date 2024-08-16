import pygame


class VerletObject:
    def __init__(
        self,
        curr_pos: pygame.Vector2,
        prev_pos: pygame.Vector2,
        accel: pygame.Vector2,
        w=1,
        h=1,
    ):
        self.pos = curr_pos
        self.prev_pos = prev_pos
        self.accel = accel
        self.w = w
        self.h = h

    def __eq__(self, other):
        return (self.pos, self.prev_pos, self.accel) == (
            other.pos,
            other.prev_pos,
            other.accel,
        )

    def update(self, dt: float):
        vel = self.pos - self.prev_pos
        self.prev_pos = self.pos.copy()
        self.pos += vel + self.accel * dt * dt
        self.accel = pygame.Vector2(0, 0)

    def accelerate(self, acc: pygame.Vector2, max_vel: float = float("inf")):
        if (
            self.get_vel().magnitude_squared() <= max_vel**2
            or self.get_vel().normalize().dot(acc.normalize()) <= 0.0
        ):
            self.accel += acc

    def teleport(self, pos: pygame.Vector2, keep_vel: bool = False):
        self.prev_pos = self.prev_pos + (pos - self.pos) if keep_vel else pos
        self.pos = pos

    def get_vel(self) -> pygame.Vector2:
        return self.pos - self.prev_pos


class Entity(VerletObject):
    def __init__(
        self,
        x: int,
        y: int,
        w: int,
        h: int,
        name: str,
        game,
        unattached=False,
        real=True,
    ):
        super().__init__(
            pygame.Vector2(x, y), pygame.Vector2(x, y), pygame.Vector2(0, 0), w, h
        )
        self.game = game
        self.anims = game.anim.get_anims(name)
        self.rect = pygame.Rect(x, y, w, h)
        self.name = name
        self.action = "idle" if self.anims else None
        self.img = self.anims[self.action].get_img() if self.anims else None
        self.is_real = real
        if unattached:
            self.game.ua_entities.append(self)

    def update(self, dt, decel: float = 0.1):
        old_rect = self.rect.copy()
        vel = self.pos - self.prev_pos

        # if self.accel == pygame.Vector2(0, 0):
        self.accel += vel * -decel
        self.prev_pos = self.pos.copy()
        self.pos += vel + self.accel * dt * dt
        self.rect.topleft = self.pos
        self.game.camera.add_update_rect(self.rect.union(old_rect).inflate(1, 1))

        self.accel = pygame.Vector2(0, 0)
        if self.action is not None and self.img is not None:
            self.anims[self.action].play(dt)
            self.img = self.anims[self.action].get_img()
            self.game.camera.render(self.img, self.pos)

    def to_json_object(self) -> dict:
        return {
            "name": self.name,
            "action": self.action,
            "frame": self.anims[self.action].frame,
            "rect": [self.rect.x, self.rect.y, self.rect.w, self.rect.h],
            "real": True,
        }

    @property
    def centre(self) -> pygame.Vector2:
        return self.pos + pygame.Vector2(self.w // 2, self.h // 2)

    @property
    def size(self) -> pygame.Vector2:
        return pygame.Vector2(self.rect.w, self.rect.h)


class SpriteStackEntity(VerletObject):
    def __init__(self, x: int, y: int, w: int, h: int, name: str, game):
        super().__init__(
            pygame.Vector2(x, y), pygame.Vector2(x, y), pygame.Vector2(0, 0), w, h
        )
        self.rot = 0
        self.game = game
        self.spritestacks = game.anim.get_spritestacks(name)
        self.rect = pygame.Rect(x, y, w, h)
        self.name = name
        self.action = "idle" if self.spritestacks else None

    def update(self, dt, decel: float = 0.1):
        old_rect = self.rect.copy()
        vel = self.pos - self.prev_pos

        self.accelerate(vel * -decel)

        self.prev_pos = self.pos
        self.pos += vel + self.accel * dt * dt
        self.rect.topleft = self.pos
        self.rot %= 360
        self.game.camera.add_update_rect(self.rect.union(old_rect).inflate(3, 3))

        self.accel = pygame.Vector2(0, 0)
        if self.action is not None:
            self.spritestacks[self.action].render_to_game(
                self.game,
                (self.pos.x + self.w // 2, self.pos.y + self.h // 2),
                self.rot,
            )

    def rotate(self, angle: float):
        self.rot += angle

    def to_json_object(self) -> dict:
        return {
            "name": self.name,
            "action": self.action,
            "rot": self.rot,
            "rect": [self.rect.x, self.rect.y, self.rect.w, self.rect.h],
        }
