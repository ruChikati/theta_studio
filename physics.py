
import pygame

from . import level


class VerletObject:

    def __init__(self, curr_pos: pygame.Vector2, prev_pos: pygame.Vector2, accel: pygame.Vector2):
        self.pos = curr_pos
        self.prev_pos = prev_pos
        self.accel = accel

    def __eq__(self, other):
        return (self.pos, self.prev_pos, self.accel) == (other.pos, other.prev_pos, other.accel)

    def update(self, dt: float):
        vel = self.pos - self.prev_pos
        self.prev_pos = self.pos
        self.pos += vel + self.accel * dt * dt
        self.accel = pygame.Vector2(0, 0)

    def accelerate(self, acc: pygame.Vector2):
        self.accel += acc


class PhysicsSolver:

    gravity = pygame.Vector2(0, 10)

    def __init__(self, objects: list[VerletObject] | tuple[VerletObject], game, lvl: level.Level =None, sub_steps=1):
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

    def reset(self, objects: list[VerletObject] | tuple[VerletObject] =()):
        self.objects = objects

    def handle_collisions(self): # TODO
        for obj in self.objects:
            for obj2 in  self.objects:
                if obj is obj2:
                    continue

    def update(self, dt: float):
        for i in range(self.steps):
            for obj in self.objects:
                obj.accelerate(PhysicsSolver.gravity)
                self.handle_collisions()
                obj.update(dt / self.steps)
        self.handle_collisions()
