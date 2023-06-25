
import os as _os
from . import animation, camera, font, funcs, input, level, particle, physics, sfx, ui
from .entity import Entity
from .game import Game
DATA_DIR = _os.path.abspath('data')

def set_data_path(path=''):
    if path == '':
        path = f'.{_os.sep}'
    elif path[-1] != _os.sep:
        path += _os.sep
    Game.DATA_PATH = path

# TODO: let user set data dir
