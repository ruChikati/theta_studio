from os import listdir, sep

import pygame

from .entity import Entity
from .utils import read_json


class Tile:
    def __init__(
        self,
        x: int,
        y: int,
        w: int,
        h: int,
        name: str,
        img_path: str,
        game,
    ):
        self.rect = pygame.Rect(x, y, w, h)
        self.name = name
        self.img_path = img_path
        self.img = pygame.image.load(f"data{sep}{img_path}").convert()
        self.game = game

    def __eq__(self, other):
        return (self.rect.topleft, (self.rect.x, self.rect.y), self.name) == (
            other.pos,
            other.size,
            other.name,
        )

    def update(self, surf: pygame.Surface = None):
        if surf is not None:
            surf.blit(self.img, self.rect.topleft)
        else:
            self.game.camera.add_update_rects([self.rect])
            self.game.camera.render(self.img, self.rect.topleft)

    def collides(self, rect: pygame.Rect) -> bool:
        return self.rect.colliderect(rect)


class Level:

    def __init__(
        self,
        size: pygame.Vector2,
        cell_size: pygame.Vector2,
        tiles: list[Tile] = None,
        entities: list[Entity] = None,
    ):
        self.size = size
        self.cell_size = cell_size

        if not (size.y % cell_size.y) or not (size.x % cell_size.x):
            raise ArithmeticError("Cell size doesn't match level size!")

        self.objs = (tiles if tiles is not None else []) + (
            entities if entities is not None else []
        )
        self.cells = [[]] * (size.x // cell_size.x) * (size.y // cell_size.y)

        for obj in self.objs:
            self.insert(obj)

    def update(self, dt: float):
        for cell in self.cells:
            for obj in cell:
                if isinstance(obj, Entity):
                    prev_i = self.index(obj)
                    obj.update(dt)
                    if prev_i != self.index(obj):
                        self.remove(obj)
                        self.insert(obj)
                else:
                    obj.update()

    def insert(self, obj: Tile | Entity):
        if obj not in self.cells[i := self.index(obj)]:
            self.cells[i].append(obj)

    def remove(self, obj: Tile | Entity):
        self.cells[self.index(obj)].remove(obj)

    def index(self, obj: Tile | Entity) -> int:
        return self.index_at_pos(pygame.Vector2(obj.rect.center))

    def index_at_pos(self, pos: pygame.Vector2) -> int:
        x = (pos.x - (pos.x % self.cell_size.x)) // self.cell_size.x
        y = (pos.y - (pos.y % self.cell_size.y)) // self.cell_size.y
        return x + (self.size.x // self.cell_size.x) * y

    def fully_index(self, obj: Tile | Entity) -> list[int]:
        indices = [i := self.index(obj)]
        left = (
            obj.rect.centerx - (obj.rect.centerx % self.cell_size.x) + obj.rect.w // 2
        )
        right = left + self.size.x - obj.rect.w
        top = obj.rect.centery - (obj.rect.centery % self.cell_size.y) + obj.rect.h // 2
        bottom = top + self.size.y - obj.rect.h

        if obj.rect.centerx < left:
            indices.append(i - 1)
            if obj.rect.centery < top:
                indices.append(i - self.size.x // self.cell_size.x)
                indices.append(i - self.size.x // self.cell_size.x - 1)
            elif obj.rect.centery > bottom:
                indices.append(i + self.size.x // self.cell_size.x)
                indices.append(i + self.size.x // self.cell_size.x - 1)

        elif obj.rect.centerx > right:
            indices.append(i + 1)
            if obj.rect.centery < top:
                indices.append(i - self.size.x // self.cell_size.x)
                indices.append(i - self.size.x // self.cell_size.x + 1)
            elif obj.rect.centery > bottom:
                indices.append(i + self.size.x // self.cell_size.x)
                indices.append(i + self.size.x // self.cell_size.x + 1)

        elif obj.rect.centery < top:
            indices.append(i - self.size.x // self.cell_size.x)
        elif obj.rect.centery > bottom:
            indices.append(i + self.size.x // self.cell_size.x)

        return indices


class LevelManager:
    def __init__(self, game):
        from .game import LVL_PATH

        self.lvls = {}
        self.current_lvl = None
        for file in listdir(LVL_PATH):
            raw_data = read_json(f"{LVL_PATH}{sep}{file}")
            for i, t in enumerate(raw_data["tiles"]):
                raw_data["tiles"][i] = Tile(*t, game)
            for i, e in enumerate(raw_data["entities"]):
                raw_data["entities"][i] = game.anim.create_entity(*e, game)

            self.lvls[file.split(".")[0]] = Level(
                pygame.Vector2(raw_data["size"]),
                pygame.Vector2(raw_data["cell_size"]),
                raw_data["tiles"],
                raw_data["enitities"],
            )

    def update(self, dt: float):
        self.lvls[self.current_lvl].update(dt)

    def switch_lvl(self, name: str):
        self.current_lvl = name
