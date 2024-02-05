import pygame

from . import level
from .funcs import distance2


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

    def accelerate(self, acc: pygame.Vector2):
        self.accel += acc

    def teleport(self, pos: pygame.Vector2):
        self.pos = pos
        self.prev_pos = pos


class PhysicsSolver:
    gravity = pygame.Vector2(0, 1)

    def __init__(
        self,
        objects: list[VerletObject] | tuple[VerletObject],
        game,
        lvl: level.Level = None,
        sub_steps=1,
    ):
        self.objects = objects
        self.lvl = lvl if lvl is not None else level.Level([], game)
        self.game = game
        self.steps = sub_steps

    def add_objects(self, objects: list[VerletObject] | tuple[VerletObject]):
        self.objects.extend(objects)

    def remove_objects(self, objects: list[VerletObject] | tuple[VerletObject]):
        for obj in objects:
            for v_obj in self.objects:
                if v_obj == obj:
                    del v_obj

    def reset(self, objects: list[VerletObject] | tuple[VerletObject] = ()):
        self.objects = objects

    def handle_collisions(self):
        for obj in self.objects:
            for obj2 in self.objects:
                if obj is obj2 or not pygame.Rect(obj.pos, (obj.w, obj.h)).colliderect(
                    pygame.Rect(obj2.pos, (obj2.w, obj2.h))
                ):
                    continue
                distv = obj2.pos - obj.pos
                r1 = max(
                    distance2(obj.pos + pygame.Vector2(obj.w / 2, obj.h / 2), obj.pos),
                    distance2(
                        obj.pos + pygame.Vector2(obj.w / 2, obj.h / 2),
                        obj.pos + pygame.Vector2(obj.w, 0),
                    ),
                )
                r2 = max(
                    distance2(
                        obj2.pos + pygame.Vector2(obj2.w / 2, obj2.h / 2), obj2.pos
                    ),
                    distance2(
                        obj2.pos + pygame.Vector2(obj2.w / 2, obj2.h / 2),
                        obj2.pos + pygame.Vector2(obj2.w, 0),
                    ),
                )
                obj.pos -= r1 - distv / 2
                obj2.pos += r2 - distv / 2

    def update(self, dt: float, collisions=True):
        for i in range(self.steps):
            for obj in self.objects:
                obj.accelerate(PhysicsSolver.gravity)
                obj.update(dt / self.steps)
            if collisions:
                self.handle_collisions()
        if collisions:
            self.handle_collisions()
