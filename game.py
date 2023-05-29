
from time import time

import pygame

from . import camera
from . import input
from . import ui
from . import physics


class Game:

    def __init__(self, fps=60):
        self.ui = ui.UIManager(self)
        self.input = input.Input()
        self.camera = camera.Camera(512, 512)
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.dt = 1.
        self._last_time = time()

        self.entities = [] # TODO, contemplate including level/world in Game object
        self.solver = physics.PhysicsSolver(self.entities)

    def update(self):
        self.dt = time() - self._last_time
        self._last_time = time()
        m_clicked = False
        for event in self.input.get():
            if event.type == input.MOUSEDOWN:
                m_clicked = True

        self.solver.update(self.dt)

        self.ui.update(self.camera.screen, self.input.m_pos, m_clicked)
        self.camera.update()

        self.clock.tick(self.fps)

    @staticmethod
    def set_name(name: str):
        pygame.display.set_caption(name)
