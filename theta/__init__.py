from os import sep as _sep

from . import camera, game, gfx, input, level, particle, sfx, text, ui, utils
from .entity import Entity, SpriteStackEntity
from .game import Game


def set_default_data_path(path=f".{_sep}data"):
    if not path:
        path = "."
    elif path[-1] == _sep:
        path = path[:-1]
    game.ANIM_PATH = path + _sep + "gfx" + _sep + "anims" + _sep
    game.SS_PATH = path + _sep + "gfx" + _sep + "spritestacks" + _sep
    game.UI_PATH = path + _sep + "ui" + _sep
    game.CAMERA_PATH = path + _sep + "cutscenes" + _sep
    game.FONT_PATH = path + _sep + "fonts" + _sep
    game.WORLD_PATH = path + _sep + "worlds" + _sep
    game.SFX_PATH = path + _sep + "sfx" + _sep


def set_anims_data_path(path=f".{_sep}data{_sep}gfx{_sep}anims"):
    game.ANIM_PATH = path + _sep + "gfx" + _sep + "anims" + _sep


def set_spritestacks_data_path(path=f".{_sep}data{_sep}gfx{_sep}spritestacks"):
    game.SS_PATH = path + _sep + "gfx" + _sep + "spritestacks" + _sep


def set_ui_data_path(path=f".{_sep}data{_sep}ui"):
    game.UI_PATH = path + _sep + "ui" + _sep


def set_camera_data_path(path=f".{_sep}data{_sep}cutscenes"):
    game.UI_PATH = path + _sep + "ui" + _sep


def set_font_data_path(path=f".{_sep}data{_sep}fonts"):
    game.FONT_PATH = path + _sep + "fonts" + _sep


def set_level_data_path(path=f".{_sep}data{_sep}worlds"):
    game.WORLD_PATH = path + _sep + "worlds" + _sep


def set_sfx_data_path(path=f".{_sep}data{_sep}sfx"):
    game.SFX_PATH = path + _sep + "sfx" + _sep
