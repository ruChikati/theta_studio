import csv
import xml.etree.ElementTree as ET
from os import mkdir, sep
from os.path import exists, isdir

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
        self.pos = pygame.Vector2(x, y)
        self.size = pygame.Vector2(self.rect.x, self.rect.y)

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

        self.entities = entities
        self.tiles = tiles

        assert not (
            (size.y % cell_size.y) or (size.x % cell_size.x)
        ), f"Cell size doesn't match level size!\n\t-> Cellsize: {cell_size}\tLevelsize: {size}"

        self.objs = (tiles if tiles is not None else []) + (
            entities if entities is not None else []
        )
        self.cells = [[]] * int((size.x // cell_size.x) * (size.y // cell_size.y))

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

    def _handle_collisions(self, e: Entity):
        if not e.is_real:
            return
        for i in self.fully_index(e):
            for t in self.cells[i]:
                if isinstance(t, Tile):
                    pass

    def insert(self, obj: Tile | Entity):
        if obj not in self.cells[i := self.index(obj)]:
            self.cells[i].append(obj)

    def remove(self, obj: Tile | Entity):
        self.cells[self.index(obj)].remove(obj)

    def index(self, obj: Tile | Entity) -> int:
        return self.index_at_pos(pygame.Vector2(obj.rect.center))

    def index_at_pos(self, pos: pygame.Vector2) -> int:
        x = min(
            (pos.x - (pos.x % self.cell_size.x)) // self.cell_size.x,
            self.size.x // self.cell_size.x - 1,
        )
        y = min(
            (pos.y - (pos.y % self.cell_size.y)) // self.cell_size.y,
            self.size.y // self.cell_size.y - 1,
        )

        return int(x + (self.size.x // self.cell_size.x - 1) * y)

    def fully_index(
        self, obj: Tile | Entity
    ) -> list[int]:  # TODO: fix, dont assume there is always a cell at i-1, i+1, etc
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
        if not exists(LVL_PATH + "caches"):
            mkdir(LVL_PATH + "caches")
        self.current_lvl = None
        self.game = game

        if not exists(LVL_PATH + "active"):
            with open(LVL_PATH + "active", "w") as f:
                f.write("0")
        with open(LVL_PATH + "active", "r") as f:
            self.switch_lvl(f.read())

    def update(self, dt: float):
        for event in self.game.events:
            if event.type == SWITCH_LVL:
                self.switch_lvl(event.name)
        if self.current_lvl is not None:
            self.current_lvl.update(dt)

    def switch_lvl(self, name: str):
        if self.current_lvl is not None:
            self.cache(self.current_lvl)
        self.current_lvl = self.load_lvl(name)

    def load_lvl(self, name: str) -> Level:
        if isdir(self.LVL_PATH + sep + "cache" + name):
            entities = read_json(
                self.LVL_PATH + sep + "cache" + name + sep + "entities.json"
            )
        else:
            entities = read_json(self.LVL_PATH + name + sep + "entities.json")

        for i, e in enumerate(entities):
            entities[i] = Entity(*e["rect"], e["name"], self.game, real=e["real"])

        if exists(self.LVL_PATH + name + sep + "no_tiles"):
            return Level(
                name,
                pygame.Vector2(2048, 2048),
                pygame.Vector2(1024, 1024),
                [],
                entities,
            )

        ts_data = ET.parse(self.LVL_PATH + name + sep + "tileset.tsx")
        map_data = ET.parse(self.LVL_PATH + name + sep + "map.tmx")
        cell_size = pygame.Vector2(
            int(map_data.getroot().attrib["width"]),
            int(map_data.getroot().attrib["height"]),
        )
        size = cell_size.elementwise() * pygame.Vector2(
            int(map_data.getroot().attrib["tilewidth"]),
            int(map_data.getroot().attrib["tileheight"]),
        )

        if map_data.getroot()[1][0].attrib["encoding"] != "csv":
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
        print(tile_map)
        for chunk in map_data.getroot()[1][0]:
            tile_pos = list(csv.reader(chunk.text.split("\n")[1:-1]))
            chunk_pos = pygame.Vector2(int(chunk.attrib["x"]), int(chunk.attrib["y"]))
            for x, row in enumerate(tile_pos):
                for y, tile_id in enumerate(row):
                    if tile_id != "0" and tile_id:
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
        for e in lvl.entities:
            data.append(e.to_json_object())
        write_json(
            self.LVL_PATH + sep + "cache" + sep + lvl.name + sep + "entities.json", data
        )
