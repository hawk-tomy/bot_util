from dataclasses import InitVar, dataclass, field
from logging import getLogger
from typing import Any, Union


from discord import Message
from discord.ext.commands import check, Context


from .data import data, DataBase
from .util import get_unique_list


logger = getLogger(__name__)


@dataclass
class BlackList:
    name: InitVar[str]
    _ids: list[Any]= field(default_factory=list)

    def check(self, msg: Union[Context, Message])-> bool:
        return msg.author.id not in self._ids

    async def async_check(
            self, ctx: Union[Context, Message], name: str= None
            )-> bool:
        name = name or self.name
        flag = self.check(ctx)
        if not flag:
            await ctx.author.send(
                f'あなたは{name!s}の使用が禁止されています。'
                '異議申し立てはサーバーオーナーへ。'
                )
        return flag

    def check_deco(self, name: str= None):
        async def decorator(ctx: Context):
            _name = name or ctx.message.content.split()[0]
            return await self.async_check(ctx=ctx, name=_name)
        return check(decorator)

    @property
    def ids(self)-> list:
        return self._ids.copy()

    def add(self, id_: Any)-> None:
        if id_ not in self._ids:
            self._ids.append(id_)

    def delete(self, id_: Any)-> None:
        if id_ in self._ids:
            self._ids.remove(id_)


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
            instance = BlackList(k, v['_ids'])
            self.blacklists[k] = instance
            if not hasattr(self, k):
                setattr(self, k, instance)
            else:
                logger.warning(f'can not use {k} on attribute.')

    def __getitem__(self, item: str)-> BlackList:
        return self.blacklists[item]

    def create_blacklist(self, key: str)-> BlackList:
        if not isinstance(key, str):
            raise ValueError('key must be str.')
        if key not in self.blacklists:
            v = BlackList(key, [])
            self.blacklists[key] = v
            if not hasattr(self, key):
                setattr(self, key, v)
        return self[key]

    def combine_blacklist(
            self,
            *args: Union[str, BlackList],
            silent_create: bool= False,
            name: str= None
            )-> BlackList:
        ids_list = []
        for arg in args:
            if isinstance(arg, str):
                if arg in self.blacklists:
                    arg = self[arg]
                elif silent_create:
                    arg = self.create_blacklist(arg)
                else:
                    raise NameError(f'{arg} is not found.')
            if isinstance(arg, BlackList):
                ids_list.append(arg.ids)
            else:
                raise ValueError(f'{arg} must be BlackList.')
        return BlackList(
            name or ', '.join(args),
            get_unique_list(ids_list, need_flatten=True)
            )

data.add_dataclass(BlackLists, key='blacklists')
blacklists :BlackLists =data.blacklists
