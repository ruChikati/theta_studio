from time import time

import pygame
from os import sep

from . import camera, input, physics, ui


CAMERA_PATH = f".{sep}data{sep}cutscenes{sep}"
FONT_PATH = f".{sep}data{sep}fonts{sep}"
WORLD_PATH = f".{sep}data{sep}worlds{sep}"
SFX_PATH = f".{sep}data{sep}sfx{sep}"
UI_PATH = f".{sep}data{sep}ui{sep}"
ANIM_PATH = f".{sep}data{sep}gfx{sep}anims{sep}"
SS_PATH = f".{sep}data{sep}gfx{sep}spritestacks{sep}"


class Game:
    def __init__(self, fps=60):
        self.ui = ui.UIManager(self)
        self.input = input.Input()
        self.camera = camera.Camera(512, 512)
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.dt = 1.0
        self._last_time = time()
        self._t = 0

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
        self._t += 1

    def get_frames(self) -> int:
        """Returns the number of frames that have elapsed since update() has started being called."""
        return self._t

    @staticmethod
    def set_name(name: str):
        pygame.display.set_caption(name)
