
from os import listdir, sep

import pygame

from .funcs import read_json

CHUNK_SIZE = 16


class Tile:

    def __init__(self, x, y, w, h, name, img_path, is_invisible, is_solid):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.name = name
        self.img_path = img_path
        self.img = pygame.image.load(f'data{sep}{img_path}').convert()
        self.is_invisible = is_invisible
        self.is_solid = is_solid

    def __eq__(self, other):
        return (self.x, self.y, self.w, self.h, self.name, self.is_invisible, self.is_solid) == (other.x, other.y, other.w, other.h, other.name, other.is_invisible, other.is_solid)

    def update(self, surf=None):
        pass

    def collides(self, rect):
        try:
            return self.rect.colliderect(rect)
        except AttributeError:
            return self.rect.colliderect(rect.rect)

    @property
    def pos(self):
        return [self.x, self.y]

    @pos.setter
    def pos(self, pos):
        self.x = pos[0]
        self.y = pos[1]

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)

    @rect.setter
    def rect(self, rect):
        self.x = rect.x
        self.y = rect.y
        self.w = rect.w
        self.h = rect.h


class Chunk:

    def __init__(self, tile_list):    # pass in list from json file as tile in tile_list
        self.tiles = []
        self.solid_tiles = []
        self.unsolid_tiles = []
        for tile in tile_list:
            self.tiles.append(Tile(*tile))
            if tile[7]:
                self.solid_tiles.append(Tile(*tile))
            else:
                self.unsolid_tiles.append(Tile(*tile))
        self.pos = self.x, self.y = min(tile.x for tile in self.tiles), min(tile.y for tile in self.tiles)
        self.size = CHUNK_SIZE
        self.chunk_pos = self.chunk_x, self.chunk_y = self.x // self.size, self.y // self.size
        self.collision_mesh = self.get_collision_mesh()

    def __contains__(self, rect):
        if isinstance(rect, Tile):
            return rect in self.tiles
        elif isinstance(rect, pygame.Rect):
            return bool(self.rect.contains(rect))
        elif isinstance(rect, list) or isinstance(rect, tuple):
            return bool(self.rect.collidepoint(rect))
        else:
            return False

    def __eq__(self, other):
        try:
            return self.tiles == other.tiles
        except AttributeError:
            return False

    def is_equal(self, other):
        try:
            return (self.chunk_pos, len(self.tiles), len(self.solid_tiles), len(self.unsolid_tiles)) == (other.chunk_pos, len(other.tiles), len(other.solid_tiles), len(other.unsolid_tiles))
        except AttributeError:
            return False

    def update(self, surf=None, tile_type=''):
        """:type: anything for all tiles, 's' for solid tiles, 'u' for unsolid tiles"""
        match tile_type:
            case 's':
                for tile in self.solid_tiles:
                    tile.update(surf)
            case 'u':
                for tile in self.unsolid_tiles:
                    tile.update(surf)
            case _:
                for tile in self.tiles:
                    tile.update(surf)


    def get_collision_mesh(self):
        tiles = [tile.rect for tile in self.tiles if tile.is_solid]
        for i in range(len(tiles) // 20):   # to reduce runtime divide by a number, since most of the passes will likely be completed by then; 20 seems to fit, recursion is slower since it is O(n^2)
            for tile1 in tiles:
                for tile2 in tiles:
                    if tile1 == tile2:
                        continue
                    if (tile2.topleft == tile1.topright and tile2.h == tile1.h) or (tile2.bottomleft == tile1.topleft and tile2.w == tile1.w) or (tile2.bottomright == tile1.bottomleft and tile2.h == tile1.h) or (tile2.topright == tile1.bottomright and tile2.w == tile1.w) or (tile1.topleft == tile2.topright and tile1.h == tile2.h) or (tile1.bottomleft == tile2.topleft and tile1.w == tile2.w) or (tile1.bottomright == tile2.bottomleft and tile1.h == tile2.h) or (tile1.topright == tile2.bottomright and tile1.w == tile2.w):
                        tiles.append(tile1.union(tile2))
                        if tile1 in tiles:
                            tiles.remove(tile1)
                        if tile2 in tiles:
                            tiles.remove(tile2)
        return tiles

    @property
    def rect(self):
        return pygame.Rect((self.x, self.y), (self.size, self.size))


class Level:

    def __init__(self, chunk_list):
        self.chunks = chunk_list
        for i, chunk in enumerate(self.chunks):
            self.chunks[i] = Chunk(chunk)
        self.chunks_dict = {chunk.chunk_pos: chunk for chunk in self.chunks}
        print(self.chunks_dict)
        self.chunk_size = CHUNK_SIZE
        self.collision_mesh = self.get_collision_mesh()

    def get_chunks_at_points(self, points):
        return_list = []
        for point in points:
            try:
                return_list.append(self.chunks_dict[point[0] * CHUNK_SIZE, point[1] * CHUNK_SIZE])
            except KeyError:
                pass
        return return_list

    def get_all_tiles(self):
        return_list = []
        for chunk in self.chunks:
            for tile in chunk.tiles:
                return_list.append(tile)
        return return_list

    def get_collision_mesh(self, points=()):
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

    def update(self, surf=None, tile_type=0):
        for chunk in self.chunks:
            chunk.update(surf, tile_type)


class World:    # TODO: maybe move entities to the chunk level? easier to compute with only chunks

    def __init__(self, name, chunk_list, entities=()):
        self.name = name
        self.level = Level(chunk_list)
        self.entities = entities

    def update(self, dt, surf=None, tile_type=0):
        self.level.update(surf, tile_type)
        for entity in self.entities:
            if entity.is_active:
                entity.update(surf, dt)

    def get_chunks_at_points(self, points):
        return self.level.get_chunks_at_points(points)


class WorldManager:

    def __init__(self, path=f'data{sep}worlds'):
        self.path = path
        self.worlds = {}
        for world in listdir(path):
            if not world.startswith('.'):
                data = read_json(f'{path}{sep}{world}')
                self.worlds[world.split('.')[0]] = World(world.split('.')[0], data['level']['chunks'], data['entities'])
        self.active_world = '0'

    def update(self, dt, surf=None, tile_type=0):
        self.worlds[self.active_world].update(dt, surf, tile_type)

    def get_active_world(self):
        return self.worlds[self.active_world]
