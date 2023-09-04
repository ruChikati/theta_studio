import os

import pygame

from .funcs import clip, read_file, write_file


class ForbiddenCharacterError(Exception):
    def __init__(self, char: str):
        self.char = char
        self.error_str = ", ".join(self.char)

    def __str__(self):
        return "Forbidden character(s): " + self.error_str


class Font:
    def __init__(
        self, file_path, order_path, bar_colour=(128, 128, 128), colourkey=(0, 0, 0)
    ):
        self.fnt_img = pygame.image.load(file_path).convert()
        self.fnt_img.set_colorkey(colourkey)
        self.bar_colour = bar_colour
        self.imgs = []
        self.distances = [0]
        self.order = list(read_file(order_path))

        if (
            len(
                set(self.order).difference(
                    "!-.0123456789:;?ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopqrstuvwxyz"
                )
            )
            > 0
        ):
            raise ForbiddenCharacterError(
                "".join(
                    set(self.order).difference(
                        "!-.0123456789:;?ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopqrstuvwxyz"
                    )
                )
            )

        for i in range(self.fnt_img.get_width()):
            if self.fnt_img.get_at((i, 0)) == self.bar_colour:
                self.distances.append(i)

        for i in range(1, len(self.distances)):
            img = clip(
                self.fnt_img,
                self.distances[i - 1],
                0,
                self.distances[i] - self.distances[i - 1],
                self.fnt_img.get_height(),
            )
            img.set_colorkey(colourkey)
            self.imgs.append(img)

        self.chars = {char: img for char, img in zip(self.order, self.imgs)}
        self.chars[" "] = pygame.Surface((5, self.fnt_img.get_height()))

    def __getitem__(self, text: str) -> pygame.Surface:
        num_lines = 1
        if not isinstance(text, str):
            text = str(text)
        imgs = []
        for char in text:
            if char not in (self.order + ["\n"]):
                raise TypeError("text contains invalid character: " + char)
            if char == "\n":
                num_lines += 1
            else:
                imgs.append([self.chars[char], num_lines])

        return_img = pygame.Surface(
            (
                sum(img[0].get_width() for img in imgs),
                max(img[0].get_height() for img in imgs) * num_lines,
            )
        )
        x = 0
        for img in imgs:
            return_img.blit(img[0], (x, img[0].get_height() * (img[1] - 1)))
            x += img[0].get_width()
        return return_img

    def __call__(self, text: str):
        return self[text]

    def __getattr__(self, text):
        return self[text]

    def render(self, text: str):
        return self[text]


SysFont = pygame.font.SysFont


class FontManager:
    DATA_PATH = f".{os.sep}data{os.sep}fonts{os.sep}"

    def __init__(self, path=DATA_PATH, bar_colour=(128, 128, 128), colourkey=(0, 0, 0)):
        self.path = path
        self.fonts = {}
        order = None
        for file in os.listdir(path):
            if file.split(".")[0] == "order":
                order = path + file

        if order is None:
            write_file(
                path + "order",
                "!-.0123456789:;?ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopqrstuvwxyz",
            )
            order = path + "order"

        for file in os.listdir(path):
            if file[0] != "." and file != "order":
                self.fonts[file.split(".")[0]] = Font(
                    f"{path}{file}", order, bar_colour, colourkey
                )
                # fonts are stored in a directory alongs with the order `order` in which the chars appear

    def __getitem__(self, item) -> Font:
        return self.fonts[item]
