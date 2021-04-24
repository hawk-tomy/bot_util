from __future__ import annotations


from dataclasses import asdict, dataclass, field, is_dataclass
import logging
from pathlib import Path
from typing import Any, NewType, Union


import yaml


logger = logging.getLogger(__name__)


D = NewType('dataclass',Any)
C = dict[str, D]


YAML_DUMP_CONFIG = {
    'encoding':'utf8',
    'allow_unicode':True,
    'default_flow_style':False
    }


@dataclass
class __Config:
    __default_config: C = field(default_factory=dict)
    __names: set[str] = field(default_factory=set)
    __loaded_config: dict = None

    def __getattr__(self, name):
        self.load_config()
        if name in self.__names:
            return getattr(self,name)
        else:
            raise AttributeError(f'{name} is not found')

    def load_config(self)-> None:
        default, names = self.__default_config, self.__names
        keys = default.keys() - names
        if keys:
            self.__loader()
            for key in keys:
                self._setter(key)

    def _loader(self)-> None:
        if Path('./config.yaml').exists():
            with open('./config.yaml')as f:
                self.__loaded_config = yaml.safe_load(f)
        else:
            logger.warning(f'create config.yaml file')
            with open('./config.yaml','w')as f:
                yaml.dump(self.default_config,f,**YAML_DUMP_CONFIG)
            self.__loaded_config = self.default_config

    def _setter(self, key: str)-> None:
        value = self.__loaded_config
        self.__names.add(key)
        value = self.__default_config[key](**value)
        setattr(self.__class__,key,value)

    def add_default_config(self, data: D, /, *, key: str= None)-> __Config:
        if not is_dataclass(data):
            raise TypeError('data must be instance or class of dataclass.')
        if not isinstance(data, type):
            data = data.__class__
        if key is None:
            key = data.__name__
        if not isinstance(key,str):
            raise KeyError('key must be str.')
        if key.startswith('_') or key in ('add_default_config', 'load_config', 'default_config'):
            raise KeyError(f'you cannot use this key({key}).')
        self.__default_config[key] = data
        return self

    @property
    def default_config(self)-> dict:
        as_dict = {}
        for k,v in self.__default_config.items():
            as_dict[k] = asdict(v)
        return as_dict


config = __Config()
