from dataclasses import dataclass
import logging


from .config import config
from .data import data
from . import dispander
from .help import Help
from . import menus


__all__ = (
    'config',
    'data',
    'dispander',
    'Help',
    'menus',
)


@dataclass
class EmbedColor:
    color: int= 0x54c3f1

config.add_default_config('embed_color',EmbedColor)


logging.getLogger(__name__).addHandler(logging.NullHandler())
