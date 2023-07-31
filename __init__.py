
from os import sep as _sep
from . import animation, camera, font, funcs, input, level, particle, physics, sfx, ui
from .entity import Entity, SpriteStackEntity
from .game import Game

def set_default_data_path(path=f'.{_sep}data'):
    if not path:
        path = '.'
    elif path[-1] == _sep:
        path = path[:-1]
    animation.AnimationManager.DATA_PATH = path + _sep + 'gfx' + _sep + 'anims' + _sep
    animation.AnimationManager.SS_PATH = path + _sep + 'gfx' +  _sep + 'spritestacks' + _sep
    ui.UIManager.DATA_PATH = path + _sep + 'ui' + _sep
    camera.Camera.DATA_PATH = path + _sep + 'cutscenes' + _sep
    font.FontManager.DATA_PATH = path + _sep + 'fonts' + _sep
    level.WorldManager.DATA_PATH = path + _sep + 'worlds' + _sep
    sfx.SFXManager.DATA_PATH = path + _sep + 'sfx' + _sep

def set_anims_data_path(path=f'.{_sep}data{_sep}gfx{_sep}anims'):
    animation.AnimationManager.DATA_PATH = path + _sep

def set_spritestacks_data_path(path=f'.{_sep}data{_sep}gfx{_sep}spritestacks'):
    animation.AnimationManager.SS_PATH = path + _sep

def set_ui_data_path(path=f'.{_sep}data{_sep}ui'):
    ui.UIManager.DATA_PATH = path + _sep

def set_camera_data_path(path=f'.{_sep}data{_sep}cutscenes'):
    camera.Camera.DATA_PATH = path + _sep

def set_font_data_path(path=f'.{_sep}data{_sep}fonts'):
    font.FontManager.DATA_PATH = path + _sep

def set_level_data_path(path=f'.{_sep}data{_sep}worlds'):
    level.WorldManager.DATA_PATH = path + _sep

def set_sfx_data_path(path=f'.{_sep}data{_sep}sfx'):
    sfx.SFXManager.DATA_PATH = path + _sep
