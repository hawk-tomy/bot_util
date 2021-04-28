from .config_parser import ConfigParser, ConfigBase


__all__ = ('config', 'ConfigBase')


config = ConfigParser('config.yaml')
