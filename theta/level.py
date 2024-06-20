from os import listdir, sep

import pygame

from .utils import read_json

CHUNK_SIZE = 16


class Tile:
    def __init__(
        self,
        x: int,
        y: int,
        w: int,
        h: int,
        name: str,
        img_path: str,
        is_invisible: bool,
        is_solid: bool,
        game,
    ):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.name = name
        self.img_path = img_path
        self.img = pygame.image.load(f"data{sep}{img_path}").convert()
        self.is_invisible = is_invisible
        self.is_solid = is_solid
        self.game = game

    def __eq__(self, other):
        return (
            self.x,
            self.y,
            self.w,
            self.h,
            self.name,
            self.is_invisible,
            self.is_solid,
        ) == (
            other.x,
            other.y,
            other.w,
            other.h,
            other.name,
            other.is_invisible,
            other.is_solid,
        )

    def update(self, surf: pygame.Surface = None):
        if surf is not None:
            surf.blit(self.img, (self.x, self.y))
        else:
            self.game.camera.add_update_rects(
                [pygame.Rect(self.x, self.y, self.w, self.h)]
            )
            self.game.camera.render(self.img, (self.x, self.y))

    def collides(self, rect) -> bool:
        try:
            return self.rect.colliderect(rect)
        except AttributeError:
            return self.rect.colliderect(rect.rect)

    @property
    def pos(self) -> pygame.Vector2:
        return pygame.Vector2(self.x, self.y)

    @pos.setter
    def pos(self, pos: tuple[int, int] | list[int, int] | pygame.Vector2):
        self.x = pos[0]
        self.y = pos[1]

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.w, self.h)

    @rect.setter
    def rect(self, rect: pygame.Rect):
        self.x = rect.x
        self.y = rect.y
        self.w = rect.w
        self.h = rect.h


class Chunk:
    def __init__(
        self, tile_list: list | tuple, game
    ):  # pass in list from json file as tile in tile_list
        self.tiles = []
        self.solid_tiles = []
        self.unsolid_tiles = []
        for tile in tile_list:
            self.tiles.append(Tile(*tile, game))
            if tile[7]:
                self.solid_tiles.append(Tile(*tile, game))
            else:
                self.unsolid_tiles.append(Tile(*tile, game))
        self.pos = self.x, self.y = min(tile.x for tile in self.tiles), min(
            tile.y for tile in self.tiles
        )
        self.size = CHUNK_SIZE
        self.chunk_pos = self.chunk_x, self.chunk_y = (
            self.x // self.size,
            self.y // self.size,
        )
        self.collision_mesh = self.get_collision_mesh()
        self.game = game

    def __contains__(
        self,
        rect: Tile | pygame.Rect | tuple[int, int] | list[int, int] | pygame.Vector2,
    ):
        if isinstance(rect, Tile):
            return rect in self.tiles
        elif isinstance(rect, pygame.Rect):
            return bool(self.rect.contains(rect))
        elif isinstance(rect, list) or isinstance(rect, tuple):
            return bool(self.rect.collidepoint(rect))
        elif isinstance(rect, pygame.Vector2):
            return bool(self.rect.collidepoint(rect))
        else:
            return False

    def __eq__(self, other):
        try:
            return self.tiles == other.tiles
        except AttributeError:
            return False

    def is_equal(self, other) -> bool:
        try:
            return (
                self.chunk_pos,
                len(self.tiles),
                len(self.solid_tiles),
                len(self.unsolid_tiles),
            ) == (
                other.chunk_pos,
                len(other.tiles),
                len(other.solid_tiles),
                len(other.unsolid_tiles),
            )
        except AttributeError:
            return False

    def update(self, surf: pygame.Surface = None, tile_type: str = ""):
        """:type: '' for all tiles, 's' for solid tiles, 'u' for unsolid tiles, 'x' for invisible tiles, 'v' for visible tiles"""
        if tile_type == "":
            for tile in self.tiles:
                tile.update(surf)
        if "s" in tile_type:
            for tile in self.solid_tiles:
                if (tile.is_invisible and "x" in tile_type) or (
                    not tile.is_invisible and "v" in tile_type
                ):
                    tile.update(surf)
        if "u" in tile_type:
            for tile in self.unsolid_tiles:
                if (tile.is_invisible and "x" in tile_type) or (
                    not tile.is_invisible and "v" in tile_type
                ):
                    tile.update(surf)

    def get_collision_mesh(self) -> list[pygame.Rect]:
        tiles = [tile.rect for tile in self.tiles if tile.is_solid]
        for i in range(
            len(tiles) // 20
        ):  # to reduce runtime divide by a number, since most of the passes will likely be completed by then; 20 seems to fit, recursion is slower since it is O(n^2)
            for tile1 in tiles:
                for tile2 in tiles:
                    if tile1 == tile2:
                        continue
                    if (
                        (tile2.topleft == tile1.topright and tile2.h == tile1.h)
                        or (tile2.bottomleft == tile1.topleft and tile2.w == tile1.w)
                        or (
                            tile2.bottomright == tile1.bottomleft and tile2.h == tile1.h
                        )
                        or (tile2.topright == tile1.bottomright and tile2.w == tile1.w)
                        or (tile1.topleft == tile2.topright and tile1.h == tile2.h)
                        or (tile1.bottomleft == tile2.topleft and tile1.w == tile2.w)
                        or (
                            tile1.bottomright == tile2.bottomleft and tile1.h == tile2.h
                        )
                        or (tile1.topright == tile2.bottomright and tile1.w == tile2.w)
                    ):
                        tiles.append(tile1.union(tile2))
                        if tile1 in tiles:
                            tiles.remove(tile1)
                        if tile2 in tiles:
                            tiles.remove(tile2)
        return tiles

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect((self.x, self.y), (self.size, self.size))


class Level:
    def __init__(self, chunk_list: list[Chunk], game):
        self.chunks = chunk_list
        self.chunks_dict = {chunk.chunk_pos: chunk for chunk in self.chunks}
        self.chunk_size = CHUNK_SIZE
        self.collision_mesh = self.get_collision_mesh()
        self.game = game

    def get_chunks_at_points(self, points: list | tuple) -> list[Chunk]:
        return_list = []
        for point in points:
            try:
                return_list.append(
                    self.chunks_dict[point[0] * CHUNK_SIZE, point[1] * CHUNK_SIZE]
                )
            except KeyError:
                pass
        return return_list

    def get_all_tiles(self) -> list[Tile]:
        return_list = []
        for chunk in self.chunks:
            for tile in chunk.tiles:
                return_list.append(tile)
        return return_list

    def get_collision_mesh(self, points: tuple | list = ()) -> list[pygame.Rect]:
        return_list = []
        if not points:
            for chunk in self.chunks:
                for tile in chunk.collision_mesh:
                    return_list.append(tile)
        else:
            for chunk in self.get_chunks_at_points(points):
                for tile in chunk.collision_mesh:
                    return_list.append(tile)
        return return_list

    def update(self, surf: pygame.Surface = None, tile_type: str = ""):
        for chunk in self.chunks:
            chunk.update(surf, tile_type)


class World:  # TODO: maybe move entities to the chunk level? easier to compute with only chunks
    def __init__(self, name: str, chunk_list: list[Chunk], game, entities=()):
        self.name = name
        self.level = Level(chunk_list, game)
        self.entities = list(entities)
        self.game = game

    def update(self, dt: float, surf: pygame.Surface = None, tile_type: str = ""):
        self.level.update(surf, tile_type)
        for entity in self.entities:
            if entity.is_active:
                entity.update(surf, dt)

    def get_chunks_at_points(self, points) -> list[Chunk]:
        return self.level.get_chunks_at_points(points)


class WorldManager:
    def __init__(self, game):
        from .game import WORLD_PATH

        self.path = WORLD_PATH
        self.worlds = {}
        for world in listdir(self.path):
            if not world.startswith("."):
                data = read_json(f"{self.path}{world}")
                self.worlds[world.split(".")[0]] = World(
                    world.split(".")[0],
                    [Chunk(d, game) for d in data["level"]["chunks"]],
                    game,
                    data["entities"],
                )
        self.active_world = "0"
        self.game = game
        self.game.solver.reset()
        self.game.solver.add_objects(self.worlds[self.active_world].entities)

    def update(self, dt: float, surf: pygame.Surface = None, tile_type: str = ""):
        self.worlds[self.active_world].update(dt, surf, tile_type)

    def get_active_world(self) -> World:
        return self.worlds[self.active_world]

    def change_world(self, name: str) -> World:
        self.active_world = name
        self.game.solver.reset()
        self.game.solver.add_objects(self.worlds[self.active_world].entities)
        return self.get_active_world()
