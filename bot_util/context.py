from discord import Colour, Message
from discord.ext.commands import Context as _Context

from .wraped_embed import Embed

__all__ = ('Context', )

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
            title= f'\u2705 {title}',
            description= description if description is not None else '',
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
            title= f'\u26a0 {title}',
            description= description if description is not None else '',
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

    async def embed(self, embed)-> Message:
        return await self.send(embed=embed)

    async def re_embed(self, embed)-> Message:
        return await self.reply(embed=embed)
