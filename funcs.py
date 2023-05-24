
import json
import math

import pygame


def read_file(path):
    with open(path, 'r') as f:
        data = f.read()
    return data


def write_file(path, data):
    with open(path, 'w') as f:
        f.write(data)


def write_json(path, data, indent=1):
    with open(path, 'x') as f:
        f.write(json.dumps(data, indent=indent))


def read_json(path):
    with open(path, 'r') as f:
        data = f.read()
    data = json.loads(data)
    return data


def sum_list(list_: list, sort=True) -> list:
    """:returns: sub-sums of a given list of numbers"""
    return_list = []
    for i in range(len(list_)):
        return_list.append(sum(list_[:i + 1]))
    if sort:
        return_list.sort()
    return return_list


def string_of_(var):
    """:returns: string of the name of the given variable"""
    return f'{var=}'.split('=')[0]


def get_key(val, dict: dict):
    """:returns: the corresponding key to a given value in O(n) time, else None"""
    for key, value in dict.items():
        if val == value:
            return key
    return


def unique_vals(obj):
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


def prime_generator(end):
    for n in range(2, end):
        for x in range(2, n):
            if n % x == 0:
                break
        else:
            yield n


def is_prime(n):
    if n <= 3:
        return n > 1
    if not (n % 2 and n % 3):
        return False
    i = 5
    while i ** 2 <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def swap_colour(surf, old_colour, new_colour):
    """Swaps one colour for a new one on a pygame.Surface"""
    surf = surf.copy()
    surf.set_colorkey(old_colour)
    swap_surf = pygame.Surface(surf.get_width(), surf.get_height())
    swap_surf.fill(new_colour)
    swap_surf.blit(surf, (0, 0))
    return swap_surf


def colored_text(r, g, b, text):
    return f'\033[38;2;{r};{g};{b}m{text} \033[38;2;255;255;255m'


def centre_blit(source: pygame.Surface, surf: pygame.Surface, dest=(0, 0)):
    """Blits the centre of source onto surf at dest"""
    surf.blit(source, (dest[0] - source.get_width() // 2, dest[1] - source.get_height() // 2))


def centre_of_rect(rect):
    return rect.x + rect.w // 2, rect.y + rect.h // 2


def normalize(num, val):
    if num > val:
        num -= val
    elif num < val:
        num += val
    elif num == val:
        num = 0
    return num


def normalize_list(lst):
    """Normalizes all values in a list to min and max"""
    minimum, maximum = min(lst), max(lst)
    for i, val in enumerate(lst):
        if maximum - minimum:
            lst[i] = (val - minimum) / (maximum - minimum)
        else:
            lst[i] = val - minimum
    return lst


def sum_of_lists(big_list):
    return_list = []
    for small_list in big_list:
        return_list += small_list
    return return_list


def angle2(point1, point2):
    """:returns: angle made between the line passing through point1 and point2 and the x-axis, in radians"""
    if not point2[0] - point1[0]:
        return 0
    return math.atan2((point2[1] - point1[1]), (point2[0] - point1[0]))


def magnitude(point):
    """:returns: the magnitude of an n-dimensional point, works in general, so it's slow"""
    return sum(val ** 2 for val in point) ** 0.5


def magnitude2(point):
    """:returns: the magnitude of a 2-dimensional point"""
    return math.sqrt(point[0] * point[0] + point[1] * point[1])

def magnitude3(point):
    """:returns: the magnitude of a 3-dimensional point"""
    return math.sqrt(point[0] * point[0] + point[1] * point[1] + point[2] * point[2])

def distance2(point1, point2):
    """:returns: the distance between two 2-dimensional points"""
    return math.sqrt((point2[0] - point1[0]) * (point2[0] - point1[0]) + (point2[1] - point1[1]) * (point2[1] - point1[1]))


def distance3(point1, point2):
    """:returns: the distance between two 3-dimensional points"""
    return math.sqrt((point2[0] - point1[0]) * (point2[0] - point1[0]) + (point2[1] - point1[1]) * (point2[1] - point1[1]) + (point2[2] - point1[2]) + (point2[2]  - point1[2]))


def clip(surf, x, y, w, h):
    handle_surf = surf.copy()
    handle_surf.set_clip(pygame.Rect(x, y, w, h))
    image = surf.subsurface(handle_surf.get_clip())
    return image.copy()


def clip_rect(surf, rect):
    handle_surf = surf.copy()
    handle_surf.set_clip(rect)
    image = surf.subsurface(handle_surf.get_clip())
    return image.copy()


def two_point_rect(point1, point2):
    return pygame.Rect(min(point1[0], point2[0]), min(point1[1], point2[1]), max(point1[0], point2[0]) - min(point1[0], point2[0]), max(point1[1], point2[1]) - min(point1[1], point2[1]))
