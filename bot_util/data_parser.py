from __future__ import annotations


from dataclasses import asdict, dataclass, field, InitVar, is_dataclass
import logging
from pathlib import Path
from typing import Callable, TypeVar, Union


import yaml


from . import YAML_DUMP_CONFIG


__all__ = ('DataParser','DataBase')
logger = logging.getLogger(__name__)
class DataBase:pass
D = dict[str, DataBase]
DP = TypeVar('DP', bound='DataParser')


@dataclass
class DataParser:
    path: InitVar[str] = './data'
    __path: Path = field(init=False)
    __dataclass: D = field(default_factory=dict, init=False)
    __names: set[str] = field(default_factory=set, init=False)
    __reload_funcs: list[Callable] = field(default_factory=list, init=False)
    __save_funcs: list[Callable] = field(default_factory=list, init=False)
    __yaml_config: dict[str,dict] = field(default_factory=dict, init=False)

    def __post_init__(self, path):
        self.__path = Path(path)

    def __getattr__(self, name):
        self.load_data()
        if name in self.__names:
            return getattr(self,name)
        else:
            raise AttributeError

    def load_data(self)-> None:
        if not self.__path.exists():
            self.__path.mkdir()
            logger.warning(f'create data dirctory')
        need_load = set(
            p.stem for p in self.__path.iterdir()
                if p.is_file() and p.suffix in ('.yaml','.yml')
                ) | set(self.__dataclass.keys())
        keys = need_load - self.__names
        for key in keys:
            self._setter(key)

    def _setter(self, key: str)-> None:
        is_not_exists = False
        if (not ((p:=self.__path/f'{key}.yaml').exists()
                or (p:=self.__path/f'{key}.yml').exists())
                ):
            p = self.__path/f'{key}.yaml'
            is_not_exists = True
        if key in self.__names:
            return
        if key in self.__dataclass:
            self.__names.add(key)
        yaml_config = YAML_DUMP_CONFIG | self.__yaml_config.get(key, {})
        cls = self.__dataclass.get(key)
        if cls is None:
            if is_not_exists:
                with p.open('w',encoding='utf-8')as f:
                    yaml.dump({}, f, **yaml_config)

            def loader()-> Union[dict, list]:
                with p.open(encoding='utf-8')as f:
                    return yaml.safe_load(f)

            def save_func(self)-> None:
                with p.open('w',encoding='utf-8')as f:
                    yaml.dump(value, f, **yaml_config)

        else:
            if is_not_exists:
                with p.open('w',encoding='utf-8')as f:
                    yaml.dump(asdict(cls()), f, **yaml_config)

            def loader()-> DataBase:
                with p.open(encoding= 'utf-8')as f:
                    data = yaml.safe_load(f)
                    if data is None:
                        return cls()
                    return cls(**data)

            def save_func(self)-> None:
                with p.open('w', encoding= 'utf-8')as f:
                    yaml.dump(asdict(value), f, **yaml_config)

        value: Union[DataBase, dict, list]= loader()

        def getter(self)-> DataBase:
            return value

        def reload_func(self)-> None:
            nonlocal value
            value = loader()

        self.__reload_funcs.append(reload_func)
        self.__save_funcs.append(save_func)

        setattr(self.__class__, key, property(getter))
        setattr(self.__class__, f'save_{key}', save_func)
        setattr(self.__class__, f'reload_{key}', reload_func)

    def add_dataclass(
            self: DP, data: D, *, key: str= None, yaml_config: dict= None
            )-> DP:

        data = data if isinstance(data, type) else type(data)
        if not is_dataclass(data) or not issubclass(data, DataBase):
            raise TypeError('data must be instance or class of dataclass.')

        if key is None:
            key = data.__name__
        if not isinstance(key,str):
            raise KeyError('key must be str.')
        if key.startswith('_') or key in (
                'load_data','add_dataclass','all_reload','all_save'):
            raise KeyError(f'you cannot use this key: {key}.')

        if yaml_config is None:
            yaml_config = {}
        if not isinstance(yaml_config,dict):
            raise ValueError(f'yaml config must be dict. not {yaml_config}.')

        self.__yaml_config[key] = yaml_config
        self.__dataclass[key] = data
        if key not in self.__names:
            self.load_data()
        return self

    def all_reload(self):
        for func in self.__reload_funcs:
            func(self)

    def all_save(self):
        for func in self.__save_funcs:
            func(self)
