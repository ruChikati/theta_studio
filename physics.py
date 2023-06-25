
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

    def __init__(self, objects: list[VerletObject] | tuple[VerletObject], game, lvl: level.Level =None):
        self.objects = objects
        self.lvl = lvl if lvl is not None else level.Level([], game)
        self.game = game

    def add_objects(self, objects: list[VerletObject] | tuple[VerletObject]):
        self.objects.extend(objects)

    def remove_objects(self, objects: list[VerletObject] | tuple[VerletObject]):
        for obj in objects:
            for v_obj in self.objects:
                if v_obj == obj:
                    del v_obj

    def reset(self, objects: list[VerletObject] | tuple[VerletObject] =()):
        self.objects = objects

    def handle_collisions(self):
        pass # TODO: handle collisions, https://www.youtube.com/watch?v=lS_qeBy3aQI

    def update(self, dt: float):
        for obj in self.objects:
            obj.accelerate(PhysicsSolver.gravity)
            obj.update(dt)
            self.handle_collisions()
            obj.update(dt)
