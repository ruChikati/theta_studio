from os import sep
from time import time

import pygame

from . import animation, camera, input, level, sfx, ui

CAMERA_PATH = f".{sep}data{sep}cutscenes{sep}"
FONT_PATH = f".{sep}data{sep}fonts{sep}"
LVL_PATH = f".{sep}data{sep}levels{sep}"
SFX_PATH = f".{sep}data{sep}sfx{sep}"
UI_PATH = f".{sep}data{sep}ui{sep}"
ANIM_PATH = f".{sep}data{sep}gfx{sep}anims{sep}"
SS_PATH = f".{sep}data{sep}gfx{sep}spritestacks{sep}"


class Game:
    def __init__(self, width=512, height=512, fps=60, sfx_channels=63):
        self.ui = ui.UIManager(self)
        self.input = input.Input()
        self.camera = camera.Camera(width, height)
        self.anim = animation.AnimationManager()
        self.world = level.LevelManager(self)
        self.sfx = sfx.SFXManager(sfx_channels)

        self.clock = pygame.time.Clock()
        self.fps = fps
        self.dt = 1.0
        self._last_time = time()
        self._t = 0
        self.events = []

        self.entities = []

    def update(self, full_screen=False):
        self.dt = (time() - self._last_time) * self.fps
        self._last_time = time()

        m_clicked = False
        self.events = self.input.get()
        for event in self.events:
            if event.type == input.MOUSEDOWN:
                m_clicked = True

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

    @staticmethod
    def set_icon(path: str):
        surf = pygame.image.load(path)
        pygame.display.set_icon(surf)
