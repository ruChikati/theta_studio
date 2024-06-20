import pygame

from . import level


class VerletObject:
    def __init__(
        self,
        curr_pos: pygame.Vector2,
        prev_pos: pygame.Vector2,
        accel: pygame.Vector2,
        w=None,
        h=None,
    ):
        self.pos = curr_pos
        self.prev_pos = prev_pos
        self.accel = accel
        self.w = w if w is not None else 1
        self.h = h if h is not None else 1

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
        if (self.pos - self.prev_pos).magnitude() <= max_vel:
            self.accel += acc

    def teleport(self, pos: pygame.Vector2, keep_vel: bool = False):
        self.prev_pos = self.prev_pos + (pos - self.pos) if keep_vel else pos
        self.pos = pos


class PhysicsSolver:

    def __init__(
        self,
        objects: list[VerletObject] | tuple[VerletObject],
        game,
        lvl: level.Level = None,
        sub_steps=1,
    ):
        self.objects = list(objects)
        self.lvl = lvl if lvl is not None else level.Level([], game)
        self.game = game
        self.steps = sub_steps
        self.gravity = pygame.Vector2(0, 0)

    def add_objects(self, objects: list[VerletObject] | tuple[VerletObject]):
        self.objects.extend(objects)

    def remove_objects(self, objects: list[VerletObject] | tuple[VerletObject]):
        for obj in objects:
            for v_obj in self.objects:
                if v_obj == obj:
                    del v_obj

    def reset(self, objects: list[VerletObject] | tuple[VerletObject] = ()):
        self.objects = list(objects)

    def handle_collisions(self):  # TODO: make this better, use chunks
        for obj in self.objects:
            for obj2 in self.objects:
                if obj is obj2 or not pygame.Rect(obj.pos, (obj.w, obj.h)).colliderect(
                    pygame.Rect(obj2.pos, (obj2.w, obj2.h))
                ):
                    continue
                distv = obj2.pos - obj.pos
                r1 = max(
                    obj.pos.distance_to(obj.pos + pygame.Vector2(obj.w / 2, obj.h / 2)),
                    (obj.pos + pygame.Vector2(obj.w, 0)).distance_to(
                        obj.pos + pygame.Vector2(obj.w / 2, obj.h / 2),
                    ),
                )
                r2 = max(
                    obj2.pos.distance_to(
                        obj2.pos + pygame.Vector2(obj2.w / 2, obj2.h / 2), obj2.pos
                    ),
                    (obj2.pos + pygame.Vector2(obj2.w, 0)).distance_to(
                        obj2.pos + pygame.Vector2(obj2.w / 2, obj2.h / 2),
                    ),
                )
                obj.pos -= r1 - distv / 2
                obj2.pos += r2 - distv / 2

    def update(self, dt: float, collisions=True):
        for i in range(self.steps):
            for obj in self.objects:
                obj.accelerate(self.gravity)
                obj.update(dt / self.steps)
            if collisions:
                self.handle_collisions()
        if collisions:
            self.handle_collisions()
