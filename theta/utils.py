import json
import math

import pygame


def read_file(path: str, binary: bool = False) -> str | bytes:
    """Reads the given file and returns the data"""
    with open(path, "rb" if binary else "r") as f:
        data = f.read()
    return data


def write_file(path: str, data: str | bytes, binary: bool = False):
    """Writes the given data to the file"""
    with open(path, "wb" if binary else "w") as f:
        f.write(data)


def write_json(path: str, data, indent: int = 1):
    """Writes python objects (lists, tuples, dicts) into a JSON format at a given path"""
    with open(path, "x") as f:
        f.write(json.dumps(data, indent=indent))


def read_json(path: str):
    """Reads a JSON file into python data"""
    with open(path, "r") as f:
        data = f.read()
    data = json.loads(data)
    return data


def sum_list(list_: list, sort: bool = True) -> list:
    """:returns: sub-sums of a given list of numbers"""
    return_list = []
    for i in range(len(list_)):
        return_list.append(sum(list_[: i + 1]))
    if sort:
        return_list.sort()
    return return_list


def string_of_(var) -> str:
    """:returns: string of the name of the given variable"""
    return f"{var=}".split("=")[0]


def get_key(val, dict: dict):
    """:returns: the corresponding key to a given value in O(n) time, else None"""
    for key, value in dict.items():
        if val == value:
            return key
    return


def unique_vals(obj: list | tuple):
    """Removes duplicates of any type from a list in O(n^2)"""
    for val in obj:
        if obj.count(val) > 1:
            first_i = obj.index(val)
            while True:
                try:
                    del obj[obj.index(val)]
                except ValueError:
                    obj.insert(first_i, val)
                    break
    return obj


def single_true(iterable):
    """Checks if an iterable has exactly one True element in it"""
    iterator = iter(iterable)
    has_true = any(iterator)
    has_another_true = any(iterator)
    return has_true and not has_another_true


def prime_generator(end: int):
    """Generates all primes until a given number"""
    for n in range(2, end):
        for x in range(2, n):
            if n % x == 0:
                break
        else:
            yield n


def is_prime(n: int) -> bool:
    """Checks if a number is prime"""
    if n <= 3:
        return n > 1
    if not (n % 2 and n % 3):
        return False
    i = 5
    while i**2 <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def swap_colour(
    surf: pygame.Surface,
    old_colour: tuple[int, int, int],
    new_colour: tuple[int, int, int],
) -> pygame.Surface:
    """Swaps one colour for a new one on a pygame.Surface"""
    surf = surf.copy()
    surf.set_colorkey(old_colour)
    swap_surf = pygame.Surface((surf.get_width(), surf.get_height()))
    swap_surf.fill(new_colour)
    swap_surf.blit(surf, (0, 0))
    return swap_surf


def colored_text(text: str, r: int, g: int, b: int) -> str:
    """:returns: a string which when printed, is printed in a colour"""
    return f"\033[38;2;{r};{g};{b}m{text} \033[38;2;255;255;255m"


def centre_blit(
    source: pygame.Surface, surf: pygame.Surface, dest: tuple[int, int] = (0, 0)
):
    """Blits the centre of source onto surf at dest"""
    surf.blit(
        source, (dest[0] - source.get_width() // 2, dest[1] - source.get_height() // 2)
    )


def centre_of_rect(rect: pygame.Rect) -> tuple[int, int]:
    """:returns: the centre of a given rect"""
    return rect.x + rect.w // 2, rect.y + rect.h // 2


def normalize_list(lst: list) -> list:
    """Normalizes all values in a list to min and max"""
    minimum, maximum = min(lst), max(lst)
    for i, val in enumerate(lst):
        if maximum - minimum:
            lst[i] = (val - minimum) / (maximum - minimum)
        else:
            lst[i] = val - minimum
    return lst


def sum_of_lists(big_list: list[list]) -> list:
    """compiles a list of lists into one single list"""
    return_list = []
    for small_list in big_list:
        return_list += small_list
    return return_list


def angle2(
    point1: pygame.Vector2 | tuple[int, int], point2: pygame.Vector2 | tuple[int, int]
) -> float:
    """:returns: angle made between the line passing through point1 and point2 and the x-axis, in radians"""
    if not point2[0] - point1[0]:
        return 0
    return math.atan2((point2[1] - point1[1]), (point2[0] - point1[0]))


def magnitude(point: tuple[int | float]) -> float:
    """:returns: the magnitude of an n-dimensional point, works in general, so it's slow"""
    return sum(val**2 for val in point) ** 0.5


def clip(surf: pygame.Surface, x: int, y: int, w: int, h: int) -> pygame.Surface:
    """:returns: a subsurface of `surf` based on x, y, w, h"""
    handle_surf = surf.copy()
    handle_surf.set_clip(pygame.Rect(x, y, w, h))
    image = surf.subsurface(handle_surf.get_clip())
    return image.copy()


def clip_rect(surf: pygame.Surface, rect: pygame.Rect) -> pygame.Surface:
    """:returns: a subsurface of `surf` based on a rect"""
    handle_surf = surf.copy()
    handle_surf.set_clip(rect)
    image = surf.subsurface(handle_surf.get_clip())
    return image.copy()


def two_point_rect(
    point1: pygame.Vector2 | tuple[int, int], point2: pygame.Vector2 | tuple[int, int]
) -> pygame.Rect:
    """:returns: a rect with the two input points diagonal from each other"""
    return pygame.Rect(
        min(point1[0], point2[0]),
        min(point1[1], point2[1]),
        max(point1[0], point2[0]) - min(point1[0], point2[0]),
        max(point1[1], point2[1]) - min(point1[1], point2[1]),
    )


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


class ForbiddenCharacterError(Exception):
    def __init__(self, char: str):
        self.char = char
        self.error_str = ", ".join(self.char)

    def __str__(self):
        return "Forbidden character(s): " + self.error_str
