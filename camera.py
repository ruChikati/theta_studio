
import os

import pygame

from .funcs import normalize


def _bezier_curve_point(point_list, t: float, x_or_y: 0 | 1):
    if len(point_list) == 1:
        return point_list[0][x_or_y]
    return round(_bezier_curve_point(point_list[:-1], t, x_or_y) * (1 - t) + _bezier_curve_point(point_list[1:], t, x_or_y) * t, 5)


def bezier_curve(def_points, speed=0.01):
    points = []
    for t in [_ * speed for _ in range(int((1 + speed * 2) // speed))]:
        points.append([_bezier_curve_point(def_points, t, 0), _bezier_curve_point(def_points, t, 1)])
    return points


class CameraCutscene:

    def __init__(self, path: str):
        self.path = path
        self.name = path.split(os.sep)[-1].split('.')[0]
        with open(self.path, 'r') as data:
            self.points = [float(num) for num in data.read().split(';')[0].split(',')]
            self.curve = bezier_curve(self.points, float(data.read().split(';')[-1]))


class Camera:

    def __init__(self, w: int, h: int, cutscene_path=f'data{os.sep}cutscenes', bg_colour=(0, 0, 0)):
        self.display = pygame.display.set_mode((w, h), pygame.RESIZABLE)
        self.screen = pygame.Surface((w, h))
        self.scroll = [0, 0]
        self.bgc = bg_colour
        self.cutscene_path = cutscene_path
        self._locked = False
        self.cutscenes = {}
        self.zoom = 1.0
        self.current_points = None

        self._the_dirty_rects = []

        for file in os.listdir(self.cutscene_path):
            if file[0] != '.':
                cutscene = CameraCutscene(file)
                self.cutscenes[cutscene.name] = cutscene

    def update(self, full_screen=False):
        if self.current_points is not None:
            try:
                self.scroll = next(self.current_points)
            except StopIteration:
                self.unlock()
                self.current_points = None
        self.display.fill(self.bgc)
        self.screen.fill(self.bgc)
        self.display.blit(self.screen, (0, 0))
        if full_screen:
            pygame.display.update()
        else:
            pygame.display.update(self._the_dirty_rects)

    def play_cutscene(self, name: str) -> list[list[int, int]]:
        points = self.cutscenes[name].curve
        for i, point in enumerate(points):
            points[i] = [normalize(points[0][0], point[0]), normalize(points[0][1], point[1])]

        return_points = []
        last_point = self.scroll
        for point in points:
            last_point[0] += point[0]
            last_point[1] += point[1]
            return_points.append(last_point)

        self.current_points = iter(return_points)
        self.lock()
        return return_points

    def add_update_rects(self, rects: list[pygame.Rect] | tuple[pygame.Rect]):
        self._the_dirty_rects.extend(rects)

    def render(self, surf: pygame.Surface, pos: tuple[int, int] | list[int, int] | pygame.Vector2):
        self.screen.blit(surf, pos)

    def zoom(self, flt: float):
        if not self._locked:
            if not (flt < 0 and self.zoom <= .1):
                self.zoom += flt

    def move_by(self, pos: tuple[int, int] | list[int, int] | pygame.Vector2):
        if not self._locked:
            self.scroll[0] += pos[0]
            self.scroll[1] += pos[1]

    def move_to(self, pos: tuple[int, int] | list[int, int] | pygame.Vector2):
        if not self._locked:
            self.scroll = pos[:2]

    def center(self, pos: tuple[int, int] | list[int, int] | pygame.Vector2):
        if not self._locked:
            self.scroll = [self.screen.get_width() // 2 - pos[0], self.screen.get_height() // 2 - pos[1]]

    def lock(self):
        self._locked = True

    def unlock(self):
        self._locked = False
