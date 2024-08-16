import os

import pygame

MIN_ZOOM = 0.1


def _bezier_curve_point(point_list: list[pygame.Vector2], t: float) -> pygame.Vector2:
    if len(point_list) == 1:
        return point_list[0]
    return round(
        _bezier_curve_point(point_list[:-1], t) * (1 - t)
        + _bezier_curve_point(point_list[1:], t) * t,
        5,
    )


def bezier_curve(def_points: list[pygame.Vector2], speed=0.01) -> list[pygame.Vector2]:
    points = []
    for t in [_ * speed for _ in range(int((1 + speed * 2) // speed))]:
        points.append(_bezier_curve_point(def_points, t))
    return points


class CameraCutscene:
    def __init__(self, path: str):
        self.path = path
        self.name = path.split(os.sep)[-1].split(".")[0]
        self.points = []
        with open(
            self.path, "r"
        ) as data:  # stored as: num1x,num1y/num2x,num2y...;speed
            for p in data.read().split(";")[0].split("/"):
                self.points.append(
                    pygame.Vector2(float(p.split(",")[0]), float(p.split(",")[1]))
                )
            self.speed = float(data.read().split(";")[-1])
            self.curve = bezier_curve(self.points, self.speed)


class Camera:  # TODO: better camera (GMTK-recommended)
    def __init__(self, w: int, h: int, bg_colour=(0, 0, 0)):
        self.display = pygame.display.set_mode((w, h), pygame.RESIZABLE)
        self.screen = pygame.Surface((w, h))
        self.scroll = pygame.Vector2(0, 0)
        self._bgc = bg_colour
        from .game import CAMERA_PATH

        self.cutscene_path = CAMERA_PATH
        self._locked = False
        self.cutscenes = {}
        self._zoom_inv = 1.0
        self.current_points = None

        self._the_dirty_rects = []
        self._to_blit = []

        for file in os.listdir(self.cutscene_path):
            if file[0] != ".":
                cutscene = CameraCutscene(file)
                self.cutscenes[cutscene.name] = cutscene

    def update(self, full_screen=True):
        if full_screen:
            self.screen.fill(self._bgc)

        if self.current_points is not None:
            try:
                self.scroll = pygame.Vector2(next(self.current_points))
                self._the_dirty_rects.append(
                    pygame.Rect(0, 0, *self.display.get_size())
                )
            except StopIteration:
                self.unlock()
                self.current_points = None

        screen = pygame.transform.scale_by(self.screen, self._zoom_inv)
        for i, (img, pos) in enumerate(self._to_blit):
            self._to_blit[i] = (
                img,
                pos + self.scroll,
            )
        screen.blits(self._to_blit, 0)
        self._to_blit *= 0
        pygame.transform.scale(screen, self.display.get_size(), self.display)

        if (
            full_screen
            or self._zoom_inv != 1.0
            or self.screen.get_size() != self.display.get_size()
        ):
            pygame.display.flip()
        else:
            pygame.display.update(self._the_dirty_rects)
        self._the_dirty_rects *= 0

    def play_cutscene(self, name: str) -> list[pygame.Vector2]:
        return_points = []
        last_point = self.scroll

        for point in self.cutscenes[name].curve:
            last_point += point
            return_points.append(last_point)

        self.current_points = iter(return_points)
        self.lock()
        self._the_dirty_rects.append(pygame.Rect(0, 0, *self.display.get_size()))
        return return_points

    def add_update_rects(self, rects: list[pygame.Rect]):
        self._the_dirty_rects.extend(rects)

    def add_update_rect(self, rect: pygame.Rect):
        self._the_dirty_rects.append(rect)

    def render(
        self,
        surf: pygame.Surface,
        pos: tuple[int, int] | list[int, int] | pygame.Vector2,
    ):
        self._to_blit.append((surf, pos))

    def zoom_to(self, flt: float):
        if not self._locked:
            if flt >= MIN_ZOOM:
                self._zoom_inv = 1 / flt

    def get_zoom(self) -> float:
        return self._zoom_inv

    def move_by(self, pos: tuple[int, int] | list[int, int] | pygame.Vector2):
        if not self._locked:
            self._the_dirty_rects.append(pygame.Rect(0, 0, *self.display.get_size()))
            self.scroll[0] += pos[0]
            self.scroll[1] += pos[1]

    def move_to(self, pos: tuple[int, int] | list[int, int] | pygame.Vector2):
        if not self._locked:
            self._the_dirty_rects.append(pygame.Rect(0, 0, *self.display.get_size()))
            self.scroll = pygame.Vector2(pos[:2])

    def center(self, pos: tuple[int, int] | list[int, int] | pygame.Vector2):
        if not self._locked:
            self._the_dirty_rects.append(pygame.Rect(0, 0, *self.display.get_size()))
            self.scroll = pygame.Vector2(
                self.screen.get_width() // 2 - pos[0],
                self.screen.get_height() // 2 - pos[1],
            )

    def get_centre(self) -> tuple[int, int]:
        return (
            self.screen.get_width() // 2 - int(self.scroll[0]),
            self.screen.get_height() // 2 - int(self.scroll[1]),
        )

    def get_background(self) -> tuple[int, int, int]:
        return self._bgc

    def set_background(self, colour):
        self._bgc = colour
        self._the_dirty_rects.append(pygame.Rect(0, 0, *self.display.get_size()))

    def lock(self):
        self._locked = True

    def unlock(self):
        self._locked = False
