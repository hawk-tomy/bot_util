from __future__ import annotations


from dataclasses import asdict, dataclass, field, is_dataclass
import logging
from pathlib import Path
from typing import Callable, Union


import yaml


from . import YAML_DUMP_CONFIG


__all__ = ('DataParser','DataBase')
logger = logging.getLogger(__name__)
class DataBase:pass
D = dict[str, DataBase]


@dataclass
class DataParser:
    _path: Path = './data'
    __dataclass: D = field(default_factory=dict)
    __names: set[str] = field(default_factory=set)
    __reload_funcs: list[Callable] = field(default_factory=list)
    __save_funcs: list[Callable] = field(default_factory=list)

    def __post_init__(self):
        self._path = Path(self._path)

    def __getattr__(self, name):
        self.load_data()
        if name in self.__names:
            return getattr(self,name)
        else:
            raise AttributeError

    def load_data(self)-> None:
        if not self._path.exists():
            self._path.mkdir()
            logger.warning(f'create data dirctory')
        paths = set(
            p.stem for p in self._path.iterdir()
                if p.is_file() and p.suffix in ('.yaml','.yml')
                )
        keys = paths - self.__names
        for key in keys:
            self._setter(key)

    def _setter(self, key: str)-> None:
        if (not ((p:=self._path/f'{key}.yaml').exists()
                or (p:=self._path/f'{key}.yml').exists())
                or key in self.__names):
            return
        self.__names.add(key)
        cls = self.__dataclass.get(key)
        if cls is not None:

            def loader()-> DataBase:
                with p.open(encoding='utf-8')as f:
                    return cls(**yaml.safe_load(f))

            def save_func(self)-> None:
                with p.open('w',encoding='utf-8')as f:
                    yaml.dump(asdict(value),f,**YAML_DUMP_CONFIG)

        else:

            def loader()-> Union[dict, list]:
                with p.open(encoding='utf-8')as f:
                    return yaml.safe_load(f)

            def save_func(self)-> None:
                with p.open('w',encoding='utf-8')as f:
                    yaml.dump(value,f,**YAML_DUMP_CONFIG)

        value: DataBase = loader()

        def getter(self)-> DataBase:
            return value

        def reload_func(self)-> None:
            nonlocal value
            value = loader()

        self.__reload_funcs.append(reload_func)
        self.__save_funcs.append(save_func)

        setattr(self.__class__,key,property(getter))
        setattr(self.__class__,f'save_{key}',save_func)
        setattr(self.__class__,f'reload_{key}',reload_func)

    def add_dataclass(self, data: D, *, key: str=None)-> DataParser:
        data = data if isinstance(data, type) else type(data)
        if not is_dataclass(data) or not issubclass(data, DataBase):
            raise TypeError('data must be instance or class of dataclass.')
        if key is None:
            key = data.__name__
        if not isinstance(key,str):
            raise KeyError('key must be str.')
        if key.startswith('_') or key in (
                    'load_data','add_dataclass','all_reload','all_save'
                    ):
            raise KeyError(f'you cannot use this key({key}).')
        self.__dataclass[key] = data
        return self

    def all_reload(self):
        for func in self.__reload_funcs:
            func(self)

    def all_save(self):
        for func in self.__save_funcs:
            func(self)
