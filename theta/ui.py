import os

import pygame

from .input import Event
from .utils import read_json


# TODO: redo everything here
class UIElement:
    def __init__(self, x: int, y: int, w: int, h: int, colour, event: Event, game):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = colour
        self.surf = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self.surf.fill(colour)
        self.event = event
        self.is_visible = False
        self.game = game

    def update(self, surf: pygame.Surface, m_pos: pygame.Vector2, m_clicked: bool):
        if self.is_visible:
            surf.blit(self.surf, self.rect.topleft)

        if self.rect.collidepoint(m_pos) and m_clicked:
            self.game.input.post(self.event)


class Page:
    def __init__(self, elements: list[UIElement]):
        self.elements = elements
        self.is_active = False

    def update(self, surf: pygame.Surface, m_pos: pygame.Vector2, m_clicked: bool):
        for element in self.elements:
            element.update(surf, m_pos, m_clicked)


class UIManager:
    def __init__(self, game):
        self.pages = {"": Page([])}
        from .game import UI_PATH

        self.path = UI_PATH
        for file in os.listdir(self.path):
            if file[0] != ".":
                self.pages[file.split(".")[0]] = Page(
                    [
                        UIElement(
                            *(f[:-1]),
                            event=Event(game.input.custom_event_type(), *f[-1]),
                            game=game,
                        )
                        for f in read_json(file)
                    ]
                )
                # JSON file contains an array of arrays `f` which specify the arguments of UIElement, the last item of `f` is an array containing all arguments to the Event, except the type
        self.active_page = ""

    def update(self, surf: pygame.Surface, m_pos: pygame.Vector2, m_clicked: bool):
        self.pages[self.active_page].update(surf, m_pos, m_clicked)
