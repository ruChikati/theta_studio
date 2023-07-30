
from os import sep as _sep
from . import animation, camera, font, funcs, input, level, particle, physics, sfx, ui
from .entity import Entity, SpriteStackEntity
from .game import Game

def set_data_path(path=''):
    if not path:
        path = '.'
    elif path[-1] == _sep:
        path = path[:-1]
    Game.DATA_PATH = path + _sep
    animation.AnimationManager.DATA_PATH = path + _sep + 'gfx' + _sep + 'anims' + _sep
    animation.AnimationManager.SS_PATH = path + _sep + 'gfx' +  _sep + 'spritestacks' + _sep
    ui.UIManager.DATA_PATH = path + _sep + 'ui' + _sep
    camera.Camera.DATA_PATH = path + _sep + 'cutscenes' + _sep
    font.FontManager.DATA_PATH = path + _sep + 'fonts' + _sep
    level.WorldManager.DATA_PATH = path + _sep + 'worlds' + _sep
    sfx.SFXManager.DATA_PATH = path + _sep + 'sfx' + _sep

# TODO: let data dir be changed individually
