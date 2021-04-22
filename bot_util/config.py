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

    def __getattr__(self, name):
        self.load_config()
        if name in self.__names:
            return getattr(self,name)
        else:
            raise AttributeError(f'{name} is not found')

    def load_config(self)-> None:
        if Path('./config.yaml').exists():
            with open('./config.yaml')as f:
                self._setter(yaml.safe_load(f))
        else:
            logger.warning(f'create config.yaml file')
            default_config = {}
            for k,v in self.__default_config.items():
                default_config[k] = asdict(v)
            with open('./config.yaml','w')as f:
                yaml.dump(default_config,f,**YAML_DUMP_CONFIG)
            self._setter(default_config)

    def _setter(self, config: dict[str,Union[dict,list]])-> None:
        for k,v in config.items():
            if k not in self.__default_config or k in self.__names:
                continue
            self.__names.add(k)
            v = self.__default_config[k].__class__(**v)
            setattr(self.__class__,k,v)

    def add_default_config(self, data: D, /, *, key: str= None)-> __Config:
        if not is_dataclass(data):
            raise TypeError('data must be instance or class of dataclass.')
        if isinstance(data, type):
            data = data()
        if key is None:
            key = data.__class__.__name__
        if not isinstance(key,str):
            raise KeyError('key must be str.')
        if key.startswith('_') or key in ('add_default_config', 'load_config', 'default_config'):
            raise KeyError(f'you cannot use this key({key}).')
        self.__default_config[key] = data
        return self

    @property
    def default_config(self):
        return self.__default_config


config = __Config()
