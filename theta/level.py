import csv
import xml.etree.ElementTree as ET
from os import mkdir, sep
from os.path import isdir

import pygame

from .entity import Entity
from .input import custom_event_type
from .utils import FileTypeError, read_json, write_json

SWITCH_LVL = custom_event_type()


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
        name: str,
        size: pygame.Vector2,
        cell_size: pygame.Vector2,
        tiles: list[Tile] = None,
        entities: list[Entity] = None,
    ):
        self.size = size
        self.cell_size = cell_size
        self.name = name

        self.entitites = entities
        self.tiles = tiles

        assert not (
            (size.y % cell_size.y) or (size.x % cell_size.x)
        ), f"Cell size doesn't match level size!\n\t-> Cellsize: {cell_size}\tLevelsize: {size}"

        self.objs = (tiles if tiles is not None else []) + (
            entities if entities is not None else []
        )
        self.cells = [[]] * ((size.x // cell_size.x) * (size.y // cell_size.y))

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

        self.LVL_PATH = LVL_PATH
        mkdir(LVL_PATH + "caches")
        self.current_lvl = None
        self.game = game

    def update(self, dt: float):
        if self.current_lvl is not None:
            self.current_lvl.update(dt)
        for event in self.game.events:
            if event.type == SWITCH_LVL:
                self.switch_lvl(event.name)

    def switch_lvl(self, name: str):
        self.cache(self.current_lvl)
        self.current_lvl = self.load_lvl(name)

    def load_lvl(self, name: str) -> Level:
        if isdir(self.LVL_PATH + sep + "cache" + name):
            entities = read_json(
                self.LVL_PATH + sep + "cache" + name + sep + "entities.json"
            )
        else:
            entities = read_json(self.LVL_PATH + sep + name + sep + "entities.json")

        ts_data = ET.parse(self.LVL_PATH + sep + name + sep + "tileset.tsx")
        map_data = ET.parse(self.LVL_PATH + sep + name + sep + "map.tmx")

        cell_size = pygame.Vector2(
            int(map_data.getroot()[0][0].attrib["width"]),
            int(map_data.getroot()[0][0].attrib["height"]),
        )
        size = cell_size.elementwise() * pygame.Vector2(
            int(map_data.getroot().attrib["tilewidth"]),
            int(map_data.getroot().attrib["tileheight"]),
        )

        if map_data.getroot()[2][0].attrib["encoding"] != "csv":
            raise FileTypeError(
                "Data at"
                + self.LVL_PATH
                + sep
                + name
                + sep
                + "map.tmx"
                + " is not in a csv format"
            )
        tiles = []
        tile_map = {}
        tile_size = pygame.Vector2(
            int(ts_data.getroot().attrib["tilewidth"]),
            int(ts_data.getroot().attrib["tileheight"]),
        )
        for tile in ts_data.getroot():
            if tile.tag == "tile":
                tile_map[tile.attrib["id"]] = tile[0].attrib["source"]

        for chunk in map_data.getroot()[2][0]:
            tile_pos = list(csv.reader(chunk.text.split("\n")[1:-1]))
            chunk_pos = pygame.Vector2(int(chunk.attrib["x"]), int(chunk.attrib["y"]))
            for x, row in enumerate(tile_pos):
                for y, tile_id in enumerate(row):
                    if tile_id:
                        tiles.append(
                            Tile(
                                int((chunk_pos.x + x) * tile_size.x),
                                int((chunk_pos.y + y) * tile_size.y),
                                int(tile_size.x),
                                int(tile_size.y),
                                tile_map[tile_id].split(sep)[-1].split(".")[0],
                                tile_map[tile_id],
                                self.game,
                            )
                        )

        return Level(name, size, cell_size, tiles, entities)

    def cache(self, lvl: Level):
        data = []
        for e in lvl.entitites:
            data.append(e.to_json_object())
        write_json(
            self.LVL_PATH + sep + "cache" + sep + lvl.name + sep + "entities.json", data
        )
