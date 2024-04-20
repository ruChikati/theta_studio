import os

import pygame

from .utils import read_json, sum_list, write_json


class FileTypeError(Exception):
    def __init__(self, type):
        self.type = type

    def __str__(self):
        return f"{self.type} type files cannot be processed"


class LengthError(Exception):
    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self):
        return self.msg


class Animation:
    def __init__(self, path: str):
        self.path = path
        self.frame_paths = os.listdir(self.path)
        self.frame = 0
        self.frame_paths.sort()
        self.rotation = 0
        self.paused = False
        try:
            self.config = read_json(f"{self.path}{os.sep}config.json")
        except FileNotFoundError:
            self.config = {
                "frames": [5] * len(self.frame_paths),
                "speed": 1.0,
                "loop": False,
                "offset": [0, 0],
                "centre": False,
            }
            write_json(f"{self.path}{os.sep}config.json", self.config)
        self.frame_durations = sum_list(self.config["frames"])
        self.frames = []
        for frame in self.frame_paths:
            if frame.split(".")[-1] == "png":
                frame = pygame.image.load(f"{self.path}{os.sep}{frame}").convert_alpha()
                frame.set_colorkey((1, 1, 1))
                self.frames.append(frame)
            elif frame.split(".")[-1] == "json":
                pass
            else:
                raise FileTypeError(frame.split(".")[-1])
        if len(self.frames) > len(self.frame_paths) + 1:
            self.config["frames"] += [5] * (len(self.frames) - len(self.frame_paths))
        elif len(self.frames) < (len(self.frame_paths) - 1):
            raise LengthError("Not enough frames in animation")
        self._calcualate_img()

    def _calcualate_img(self):
        if len(self.frames) != len(self.frame_durations):
            raise LengthError(
                "frame_durations does not have the same length as frames in "
                + self.path
                + "'s animation"
            )
        for frame, t in zip(self.frames, self.frame_durations):
            if t > self.frame:
                self._img = frame
                break
        if self.frame_durations[-1] < self.frame:
            self._img = self.frames[-1]

    def play(self, dt: float, fps=60):
        if not self.paused:
            self.frame += dt * fps * self.config["speed"]
        if self.config["loop"]:
            while self.frame > self.duration:
                self.frame -= self.duration
        self._calcualate_img()
        return self._img

    def get_img(self):
        return self._img

    def rewind(self, index=0):
        self.frame = index

    def pause(self):
        self.paused = True

    def unpause(self):
        self.paused = False

    @property
    def duration(self):
        return sum(self.config["frames"])


class SpriteStack:
    def __init__(self, path: str, caching_step=6):
        self.frames = []
        folder = os.listdir(path)
        folder.sort()
        for f in folder:
            if f[0] != "." and f != "config.json":
                surf = pygame.image.load(path + os.sep + f).convert_alpha()
                self.frames.append(surf)

        self._cache = {}
        self.cache_rotation(0)
        self.cache_rotation(45)
        self.cache_rotation(90)
        self.cache_rotation(135)
        self.cache_rotation(180)
        self.cache_rotation(225)
        self.cache_rotation(270)
        self.cache_rotation(315)
        for i in range(0, 360, caching_step):
            self.cache_rotation(i)

    def cache_rotation(self, rot: float, spread=1):
        rot %= 360
        if rot not in self._cache:
            imgs = []
            for img in self.frames:
                imgs.append(pygame.transform.rotate(img, rot))
            surf = pygame.Surface(
                (
                    max(f.get_width() for f in imgs),
                    max(f.get_height() for f in imgs) + len(imgs) * spread,
                )
            )
            surf.fill((1, 1, 1))
            for i, img in enumerate(imgs):
                surf.blit(
                    img,
                    (
                        (surf.get_width() - img.get_width()) // 2,
                        (surf.get_height() - img.get_height() + len(imgs) * spread) // 2
                        - i * spread,
                    ),
                )
            final_surf = pygame.Surface(
                (surf.get_width(), surf.get_height() - len(imgs))
            )
            final_surf.set_colorkey((1, 1, 1))
            final_surf.fill((1, 1, 1))
            final_surf.blit(surf, (0, -len(imgs) // 2))
            self._cache[rot] = surf

    def render(self, surf: pygame.Surface, pos, rot: float, spread=1):
        rot %= 360
        if rot in self._cache:
            image = self._cache[rot]
            image.set_colorkey((1, 1, 1))
            surf.blit(
                image,
                (pos[0] - image.get_width() // 2, pos[1] - image.get_height() // 2),
            )
        else:
            for i, img in enumerate(self.frames):
                img = pygame.transform.rotate(img, rot)
                img.set_colorkey((1, 1, 1))
                surf.blit(
                    img,
                    (
                        pos[0] - img.get_width() // 2,
                        pos[1] - img.get_height() // 2 - i * spread,
                    ),
                )

    def render_to_game(self, game, pos, rot: float, spread=1):
        rot %= 360
        if rot in self._cache:
            image = self._cache[rot]
            image.set_colorkey((1, 1, 1))
            game.camera.render(
                image,
                (
                    pos[0] - image.get_width() // 2,
                    pos[1] - image.get_height() // 2 - (len(self.frames) // 2) * spread,
                ),
            )
        else:
            for i, img in enumerate(self.frames):
                img = pygame.transform.rotate(img, rot)
                img.set_colorkey((1, 1, 1))
                game.camera.render(
                    img,
                    (
                        pos[0] - img.get_width() // 2,
                        pos[1] - img.get_height() // 2 - i * spread,
                    ),
                )

    def get_img(self, rot: float, spread=1) -> pygame.Surface:
        rot %= 360
        if rot in self._cache:
            return self._cache[rot]
        imgs = []
        for i, img in enumerate(self.frames):
            imgs.append(pygame.transform.rotate(img, rot))
        surf = pygame.Surface(
            (
                max(f.get_width() for f in imgs),
                max(f.get_height() for f in imgs) + len(imgs) * spread,
            )
        )
        surf.set_colorkey((1, 1, 1))
        surf.fill((1, 1, 1))
        for i, img in enumerate(imgs):
            img = pygame.transform.rotate(img, rot)
            surf.blit(
                img,
                (
                    (surf.get_width() - img.get_width()) // 2,
                    (surf.get_height() - img.get_height() + len(imgs) * spread) // 2
                    - i * spread,
                ),
            )
        return surf


class AnimationManager:
    def __init__(self):
        from .game import ANIM_PATH, SS_PATH

        self.path = ANIM_PATH
        self.ss_path = SS_PATH
        self.anims = {}
        self.spritestacks = {}
        for directory in os.listdir(self.path):
            if directory[0] != ".":
                self.anims[directory] = Animation(f"{self.path}{directory}")
                # anims are stored as sortable images, in dirs named obj;anim, along with a config.json file
        for directory in os.listdir(self.path):
            if directory[0] != ".":
                self.spritestacks[directory] = SpriteStack(f"{self.ss_path}{directory}")

    def get_anims(self, name: str) -> dict[str:Animation]:
        dct = {}
        for anim in self.anims:
            if anim.split(";")[0] == name:
                dct[anim.split(";")[1]] = self.anims[anim]
        return dct

    def get_spritestacks(self, name: str) -> dict[str:SpriteStack]:
        dct = {}
        for ss in self.spritestacks:
            if ss.split(";")[0] == name:
                dct[ss.split(";")[1]] = self.spritestacks[ss]
        return dct

    def new(self, path: str):
        self.anims[path.split(os.sep)[-1]] = Animation(path)
