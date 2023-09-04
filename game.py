from time import time
from os import sep

import pygame

from . import camera, input, physics, ui


class Game:
    def __init__(self, fps=60):
        self.ui = ui.UIManager(self)
        self.input = input.Input()
        self.camera = camera.Camera(512, 512)
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.dt = 1.0
        self._last_time = time()

        self.entities = []
        self.solver = physics.PhysicsSolver(self.entities, self)

    def update(self, full_screen=False):
        self.dt = (time() - self._last_time) * self.fps
        self._last_time = time()

        m_clicked = False
        for event in self.input.get():
            if event.type == input.MOUSEDOWN:
                m_clicked = True

        self.solver.update(self.dt)

        self.ui.update(self.camera.screen, self.input.m_pos, m_clicked)
        self.camera.update(full_screen)

        self.clock.tick(self.fps)

    @staticmethod
    def set_name(name: str):
        pygame.display.set_caption(name)
