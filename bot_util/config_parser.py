from __future__ import annotations


from dataclasses import InitVar, asdict, dataclass, field, is_dataclass
import logging
from pathlib import Path
from typing import Any, TypeVar


import yaml


from . import YAML_DUMP_CONFIG


__all__ = ('ConfigParser','ConfigBase')
logger = logging.getLogger(__name__)
class ConfigBase:pass
C = dict[str, ConfigBase]
CP = TypeVar('CP', bound='ConfigParser')


@dataclass
class ConfigParser:
    path: InitVar[str] = './config.yaml'
    __path: Path = field(init=False)
    __default_config: C = field(default_factory=dict, init=False)
    __names: set[str] = field(default_factory=set, init=False)
    __loaded_config: dict[str,Any] = field(default=None, init=False)

    def __post_init__(self, path):
        self.__path = Path(path)

    def __getattr__(self, name):
        self.load_config()
        if name in self.__names:
            return getattr(self, name)
        else:
            raise AttributeError(f'{name} is not found')

    def load_config(self)-> None:
        if self.__loaded_config is None:
            self._loader()
        keys = (
            self.__loaded_config.keys()
            | self.__default_config.keys()
            )
        for key in keys:
            self._setter(key)

    def _loader(self)-> None:
        if self.__path.exists():
            with self.__path.open(encoding='utf-8')as f:
                self.__loaded_config = yaml.safe_load(f)
        else:
            logger.warning(f'create config.yaml file')
            self.__loaded_config = self.default_config
            self._save()

    def _save(self):
        with self.__path.open('w',encoding='Utf-8')as f:
            yaml.dump(self.__loaded_config, f, **YAML_DUMP_CONFIG)

    def _setter(self, key: str)-> None:
        loaded_value = self.__loaded_config.get(key)
        default_class = self.__default_config.get(key)
        if loaded_value is None:
            try:
                value = default_class()
            except Exception:
                return
            else:
                self.__loaded_config[key] = asdict(value)
        elif default_class is None:
            value = loaded_value
        else:
            value = default_class(**loaded_value)
        self.__names.add(key)
        setattr(self.__class__, key, value)

    def add_default_config(
            self: CP, data: ConfigBase, /, *, key: str= None
            )-> CP:
        data = data if isinstance(data, type) else type(data)
        if not is_dataclass(data) or not issubclass(data, ConfigBase):
            raise TypeError('data must be instance or class of dataclass.')
        if key is None:
            key = data.__name__
        if not isinstance(key, str):
            raise KeyError('key must be str.')
        if key.startswith('_') or key in (
                'add_default_config', 'load_config', 'default_config',
                ):
            raise KeyError(f'you cannot use this key ({key}).')
        self.__default_config[key] = data
        if self.__loaded_config is None:
            self._loader()
        self._setter(key)
        return self

    @property
    def default_config(self)-> dict[str,dict]:
        as_dict = {}
        for k, v in self.__default_config.items():
            try:
                as_dict[k] = asdict(v())
            except Exception:
                continue
        return as_dict
