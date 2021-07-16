from __future__ import annotations
from typing import Optional


from discord import Colour, Message
from discord.ext.commands import Context as _Context

from . import menus
from .wraped_embed import Embed

__all__ = ('Context', )


class Confirm(menus.Menu):
    def __init__(self, msg):
        super().__init__(timeout=None, delete_message_after=True)
        self.result = None
        self.msg = msg

    async def send(self, ctx)-> Optional[bool]:
        await self.start(ctx, wait=True)
        return self.result

    async def send_initial_message(self, ctx: Context, channel):
        return await channel.send(embed=await ctx._confirm(self.msg))

    @menus.button('\u2705')
    async def ok(self, payload):
        self.result = True
        self.stop()

    @menus.button('\u274c')
    async def no(self, payload):
        self.result = False
        self.stop()


class Context(_Context):
    def __init__(self, **attrs):
        self.invoked_error = False
        super().__init__(**attrs)

    @property
    def invoked_error(self)-> bool:
        return self.__invoked_error and self.command_failed

    @invoked_error.setter
    def invoked_error(self, value: bool):
        self.__invoked_error = bool(value)

    def _success(self, title: str, description: str= None)-> Embed:
        return Embed(
            title=f'\u2705 {title!s}',
            description=description if description is not None else '',
            colour=Colour.green()
        )

    async def success(self, title: str, description: str= None)-> Message:
        return await self.embed(self._success(
            title=title,
            description=description
        ))

    async def re_success(self, title: str, description: str= None)-> Message:
        return await self.re_embed(self._success(
            title=title,
            description=description
        ))

    def _error(self, title: str, description: str= None)-> Embed:
        return Embed(
            title=f'\u26a0 {title!s}',
            description=description if description is not None else '',
            colour=Colour.dark_red()
        )

    async def error(self, title: str, description: str= None)-> Message:
        return await self.embed(self._error(
            title=title,
            description=description
        ))

    async def re_error(self, title: str, description: str= None)-> Message:
        return await self.re_embed(self._error(
            title=title,
            description=description
        ))

    async def _confirm(self, msg: str)-> Embed:
        return Embed(title=f'\u26a0\ufe0f {msg!s}', color=Colour.gold())

    async def confirm(self, msg: str)-> bool:
        return await Confirm(msg).send(self)

    async def embed(self, embed: Embed)-> Message:
        return await self.send(embed=embed)

    async def re_embed(self, embed: Embed)-> Message:
        return await self.reply(embed=embed)
