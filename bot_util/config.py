from __future__ import annotations


from dataclasses import asdict, dataclass, field, is_dataclass
import logging
from pathlib import Path
from typing import Any, NewType, Union


import yaml


__all__ = ('ConigBase','config')


logger = logging.getLogger(__name__)


class ConfigBase:pass


C = dict[str, ConfigBase]


YAML_DUMP_CONFIG = {
    'encoding': 'utf8',
    'allow_unicode': True,
    'default_flow_style': False
    }


@dataclass
class __Config:
    __default_config: C = field(default_factory=dict)
    __names: set[str] = field(default_factory=set)
    __loaded_config: dict = None

    def __getattr__(self, name):
        self.load_config()
        if name in self.__names:
            return getattr(self, name)
        else:
            raise AttributeError(f'{name} is not found')

    def load_config(self)-> None:
        default, names = self.__default_config, self.__names
        keys = default.keys() - names
        if keys:
            self._loader()
            for key in keys:
                self._setter(key)

    def _loader(self)-> None:
        if Path('./config.yaml').exists():
            with open('./config.yaml')as f:
                self.__loaded_config = yaml.safe_load(f)
        else:
            logger.warning(f'create config.yaml file')
            self.__loaded_config = self.default_config
            self._save()

    def _save(self):
        with open('./config.yaml','w')as f:
            yaml.dump(self.__loaded_config, f, **YAML_DUMP_CONFIG)

    def _setter(self, key: str)-> None:
        value = self.__loaded_config.get(key)
        if value is None:
            try:
                value = self.__default_config[key]()
            except Exception:
                return
            else:
                self.__loaded_config[key] = asdict(value)
        else:
            value = self.__default_config[key](**value)
        self.__names.add(key)
        setattr(self.__class__, key, value)

    def add_default_config(
            self, data: ConfigBase, /, *, key: str= None
            )-> __Config:
        data = data if isinstance(data, type) else type(data)
        if not is_dataclass(data) or not issubclass(data, ConfigBase):
            raise TypeError('data must be instance or class of dataclass.')
        if key is None:
            key = data.__name__
        if not isinstance(key, str):
            raise KeyError('key must be str.')
        if key.startswith('_') or key in (
                'add_default_config', 'load_config', 'default_config'
                ):
            raise KeyError(f'you cannot use this key({key}).')
        self.__default_config[key] = data
        return self

    @property
    def default_config(self)-> dict:
        as_dict = {}
        for k, v in self.__default_config.items():
            as_dict[k] = asdict(v)
        return as_dict


config = __Config()
