from .logger import logger
from . import init_data
from . import launcher
from . import scripts
from . import default
from . import json_db
from . import proxy


import os

if not os.path.exists(path='sessions'):
    os.mkdir(path='sessions')
