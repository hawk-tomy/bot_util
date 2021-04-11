from __future__ import annotations


from dataclasses import asdict, is_dataclass
from pathlib import Path
import logging
from typing import Any, NewType


import yaml


logger = logging.getLogger(__name__)


Dc = NewType('dataclass',Any)
D = dict[str, Dc]


YAML_DUMP_CONFIG = {
    'encoding':'utf8',
    'allow_unicode':True,
    'default_flow_style':False
    }


class __Data:
    def __init__(self)-> None:
        self.__dataclass = {}
        self.__names = set()
        p = Path('./data')
        if not p.exists():
            p.mkdir()
            logger.warning(f'create data dirctory')

    def __getattr__(self, name):
        self.load_data()
        if name in self.__names:
            return getattr(self,name)
        else:
            raise AttributeError

    def load_data(self)-> None:
        for p in Path('./data').iterdir():
            if not p.is_file() or p.suffix not in ('.yaml','.yml'):
                continue
            self._setter(p)

    def _setter(self,p: Path)-> None:
        name = p.stem
        if name.startswith('_') or name in self.__names:
            return
        self.__names.add(name)
        cls = self.__dataclass.get(name,None)

        def loader()-> Dc:
            with p.open()as f:
                value = yaml.safe_load(f)
            if cls is not None:
                value = cls(**value)
            return value

        value: Dc = loader()

        def getter(self)-> Dc:
            return value

        def save_func(self)-> None:
            with p.open('w')as f:
                yaml.dump(asdict(value),f,**YAML_DUMP_CONFIG)

        def reload_func(self)-> None:
            nonlocal value
            value = loader()

        setattr(self.__class__,name,property(getter))
        setattr(self.__class__,f'save_{name}',save_func)
        setattr(self.__class__,f'reload_{name}',reload_func)

    def add_dataclass(self, key: str, data: D)-> __Data:
        if not is_dataclass(data):
            raise TypeError('data must be instance or class of dataclass.')
        if not isinstance(key,str):
            raise KeyError('key must be str.')
        if not isinstance(data, type):
            data = data.__class__
        self.__dataclass[key] = data
        return self


data = __Data()
