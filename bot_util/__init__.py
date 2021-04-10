import logging


from .config import config


__all__ = (
    'config',
)


logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())
