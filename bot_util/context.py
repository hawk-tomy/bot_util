from __future__ import annotations
from typing import Optional


from discord import Colour, Guild, Message
from discord.abc import Messageable
from discord.ext.commands import Context as _Context

from . import menus
from .wraped_embed import Embed

__all__ = ('Context', )


class Confirm(menus.Menu):
    def __init__(self, title: str, description: str= None):
        super().__init__(timeout=None, delete_message_after=True)
        self.result = None
        self.title = title
        self.description = description

    async def send(self, ctx)-> Optional[bool]:
        await self.start(ctx, wait=True)
        return self.result

    async def send_initial_message(self, ctx: Context, channel):
        return await channel.send(embed=ctx._confirm(
            title=self.title,
            description=self.description
        ))

    @menus.button('\u2705')
    async def ok(self, payload):
        self.result = True
        self.stop()

    @menus.button('\u274c')
    async def no(self, payload):
        self.result = False
        self.stop()


class Context(_Context):
    message: Message
    channel: Messageable
    guild: Guild

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

    def _error(self, title: str, description: str= None)-> Embed:
        return Embed(
            title=f'\u26a0 {title!s}',
            description=description if description is not None else '',
            colour=Colour.dark_red()
        )

    def _info(self, title: str, description: str= None)-> Embed:
        return Embed(
            title=f'\u2139\ufe0f {title!s}',
            description=description if description is not None else '',
            colour=Colour.blue()
        )

    def _confirm(self, title: str, description: str= None)-> Embed:
        return Embed(
            title=f'\u2754 {title!s}',
            description=description if description is not None else '',
            color=Colour.gold()
        )

    async def embed(self, embed: Embed, **kwargs)-> Message:
        return await self.send(embed=embed, **kwargs)

    async def re_embed(self, embed: Embed, **kwargs)-> Message:
        return await self.reply(embed=embed, **kwargs)

    async def success(
        self,
        title: str,
        description: str = None,
        **kwargs
    )-> Message:
        return await self.embed(
            self._success(
                title=title,
                description=description
            ),
            **kwargs
        )

    async def re_success(
        self,
        title: str,
        description: str = None,
        **kwargs
    ) -> Message:
        return await self.re_embed(
            self._success(
                title=title,
                description=description,
            ),
            **kwargs
        )

    async def error(
        self,
        title: str,
        description: str = None,
        **kwargs
    )-> Message:
        return await self.embed(
            self._error(
                title=title,
                description=description
            ),
            **kwargs
        )

    async def re_error(
        self,
        title: str,
        description: str = None,
        **kwargs
    )-> Message:
        return await self.re_embed(
            self._error(
                title=title,
                description=description
            ),
            **kwargs
        )

    async def info(
        self,
        title: str,
        description: str = None,
        **kwargs
    )-> Message:
        return await self.embed(
            self._info(
                title=title,
                description=description
            ),
            **kwargs
        )

    async def re_info(
            self,
            title: str,
            description: str = None,
            **kwargs
    )-> Message:
        return await self.re_embed(
            self._info(
                title=title,
                description=description
            ),
            **kwargs
        )

    async def confirm(self, title: str, description: str= None)-> bool:
        return await Confirm(title=title, description=description).send(self)
