from dataclasses import dataclass, field
from typing import Any, Union


from discord import Message
from discord.ext.commands import check, Context


from .data import data, DataBase
from .util import get_unique_list


@dataclass
class BlackList:
    __ids: list[Any]= field(default_factory=list)

    def check(self, msg: Union[Context, Message])-> bool:
        return msg.author.id not in self.__ids

    async def async_check(
            self, name: str, ctx: Union[Context, Message]
            )-> bool:
        flag = self.check(ctx)
        if not flag:
            await ctx.author.send(
                f'あなたは{name!s}の使用が禁止されています。'
                '異議申し立てはサーバーオーナーへ。'
                )
        return flag

    def check_deco(self, name: str= None):
        async def decorator(ctx: Context):
            nonlocal name
            name = (name or (ctx.command and ctx.command.name)) or 'この機能'
            return await self.check(self, name, ctx)
        return check(decorator)

    @property
    def ids(self)-> list:
        return self.__ids.copy()

    def add(self, id_: Any)-> None:
        if id_ not in self.__ids:
            self.__ids.append(id_)

    def delete(self, id_: Any)-> None:
        if id_ in self.__ids:
            self.__ids.remove(id_)


@dataclass
class BlackLists(DataBase):
    blacklists: dict[str: list[Any]]= field(default_factory=dict)

    def __init__(self, blacklists: dict= None)-> None:
        if blacklists is None:
            blacklists = {}
        elif not isinstance(blacklists, dict):
            raise ValueError('blacklists must be dict or None.')
        self.blacklists = blacklists
        for k,v in blacklists.items():
            if not hasattr(self, k):
                setattr(self, k, BlackList(v))
            else:
                raise NameError(f'can not use this key {k}')

    def create_blacklist(self, key: str)-> BlackList:
        if not isinstance(key, str):
            raise ValueError('key must be str.')
        if not hasattr(self, key):
            self.blacklists[key] = ids = []
            setattr(self, key, BlackList(ids))
        return getattr(self, key)

    def combine_blacklist(
            self, *args: Union[str, BlackList], silent_create= False
            )-> BlackList:
        ids_list = []
        for arg in args:
            if isinstance(arg, str):
                if hasattr(self, arg):
                    arg = getattr(self, arg)
                elif silent_create:
                    arg = self.create_blacklist(arg)
                else:
                    raise NameError(f'{arg} is not found.')
            if isinstance(arg, BlackList):
                ids_list.append(arg.ids)
            else:
                raise ValueError(f'{arg} must be BlackList.')
        return BlackList(get_unique_list(ids_list, need_flatten=True))

data.add_dataclass(BlackLists, key='blacklists')
blacklists :BlackLists =data.blacklists
