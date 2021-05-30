from __future__ import annotations

from dataclasses import dataclass
import datetime
from typing import Union, overload

from discord.colour import Colour
from discord.embeds import Embed as Embed_
from discord.embeds import EmbedProxy, EmptyEmbed, _EmptyEmbed


@dataclass
class _EmbedLimit:
    title: int= 256
    description: int= 2048
    fields: int= 25
    field_name: int= 256
    field_value: int= 1024
    footer_text: int= 2048
    author_name: int=256


EmbedLimit = _EmbedLimit()


class Embed(Embed_):
    """The MIT License (MIT)
    Copyright (c) 2015-present Rapptz
    Copyed By discord.py version 1.7.2-final
    """

    __slots__ = ('title', 'url', 'type', '_timestamp', '_colour', '_footer',
                 '_image', '_thumbnail', '_video', '_provider', '_author',
                 '_fields', 'description')

    @overload
    def __init__(
            self,
            title: str= EmptyEmbed,
            description: str= EmptyEmbed,
            type: str= 'rich',
            url: str= EmptyEmbed,
            color: Colour= EmptyEmbed,
            timestmp: datetime.datetime= EmptyEmbed,
            ):
        ...

    @overload
    def __init__(
            self,
            title: str= EmptyEmbed,
            description: str= EmptyEmbed,
            type: str= 'rich',
            url: str= EmptyEmbed,
            colour: Colour= EmptyEmbed,
            timestmp: datetime.datetime= EmptyEmbed,
            ):
        ...

    def __init__(self, **kwargs):
        if len(kwargs.get('title', '')) >= EmbedLimit.title:
            raise ValueError('title is too long')
        if len(kwargs.get('description', '')) >= EmbedLimit.description:
            raise ValueError('description is too long')
        super().__init__(**kwargs)

    @classmethod
    def from_dict(cls, data: dict)-> Embed:
        if len(data.get('title', '')) >= EmbedLimit.title:
            raise ValueError('title is too long')

        if len(data.get('description', '')) >= EmbedLimit.description:
            raise ValueError('description is too long')

        if len(data.get('fields', {})) >= EmbedLimit.fields:
            raise ValueError('fields is too many')

        for i, f in data.get('fields', {}).items():
            if len(f.get('name', '')) >= EmbedLimit.field_name:
                raise ValueError('fileds [{i}]: name is too long')
            if len(f.get('value', '')) >= EmbedLimit.field_value:
                raise ValueError('fileds [{i}]: value is too long')

        if len(data.get('footer', {}).get('text', '')) >= EmbedLimit.footer_text:
            raise ValueError('footer text is too long')

        if len(data.get('author', {}).get('name', '')) >= EmbedLimit.author_name:
            raise ValueError('author name is too long')

        return super().from_dict(data)

    def copy(self)-> Embed:
        return Embed.from_dict(self.to_dict())

    def __len__(self)-> int:
        return super().__len__()

    @property
    def colour(self)-> Union[Colour, _EmptyEmbed]:
        return super().colour

    @colour.setter
    def colour(self, value: Union[Colour, _EmptyEmbed]):
        super(Embed, self.__class__).colour.fset(self, value)

    color = colour

    @property
    def timestamp(self)-> Union[_EmptyEmbed, datetime.datetime]:
        return super().timestamp

    @timestamp.setter
    def timestamp(self, value: Union[_EmptyEmbed, datetime.datetime]):
        super(Embed, self.__class__).timestamp.fset(self, value)

    @property
    def footer(self)-> EmbedProxy:
        return super().footer

    @overload
    def set_footer(self, *,
            text: str= EmptyEmbed,
            icon_url: str= EmptyEmbed
            )-> Embed:
        ...

    def set_footer(self, **kwargs)-> Embed:
        if len(kwargs.get('text', '')) >= EmbedLimit.footer_text:
            raise ValueError('footer text is too long')

        return super().set_footer(**kwargs)

    @property
    def image(self)-> EmbedProxy:
        return super().image

    def set_image(self, *, url: str)-> Embed:
        return super().set_image(url)

    @property
    def thumbnail(self)-> EmbedProxy:
        return super().thumbnail

    def set_thumbnail(self, *, url: str)-> Embed:
        return super().set_thumbnail(url)

    @property
    def video(self)-> EmbedProxy:
        return super().video

    @property
    def provider(self)-> EmbedProxy:
        return super().provider

    @property
    def author(self)-> EmbedProxy:
        return super().author

    def set_author(
            self, *,
            name: str,
            url: str= EmptyEmbed,
            icon_url: str= EmptyEmbed
            )-> Embed:

        if len(name) >= EmbedLimit.author_name:
            raise ValueError('author name is too long')

        return super().set_author(
            name=name,
            url=url,
            icon_url=icon_url
            )

    def remove_author(self)-> Embed:
        return super().remove_author()

    @property
    def fields(self)-> list[EmbedProxy]:
        return super().fields

    def add_field(self, *, name: str, value: str, inline: bool=True)-> Embed:

        if len(name) >= EmbedLimit.field_name:
            raise ValueError('field name is too long')

        if len(value) >= EmbedLimit.field_value:
            raise ValueError('field value is too long')

        if len(self.fields) == EmbedLimit.fields:
            raise ValueError('cannot add to fields')

        return super().add_field(
            name=name,
            value=value,
            inline=inline
            )

    def insert_field_at(
            self,
            index: int,
            *,
            name: str,
            value: str,
            inline: bool= True
            )-> Embed:

        if len(name) >= EmbedLimit.field_name:
            raise ValueError('field name is too long')

        if len(value) >= EmbedLimit.field_value:
            raise ValueError('field value is too long')

        if len(self.fields) == EmbedLimit.fields:
            raise ValueError('cannot add to fields')

        return super().insert_field_at(
            index,
            name=name,
            value=value,
            inline=inline
            )

    def clear_fields(self)-> None:
        return super().clear_fields()

    def remove_field(self, index: int)-> None:
        return super().remove_field(index)

    def set_field_at(
            self,
            index: int,
            *,
            name: str,
            value: str,
            inline: bool=True
            )-> Embed:

        if len(name) >= EmbedLimit.field_name:
            raise ValueError('field name is too long')

        if len(value) >= EmbedLimit.field_value:
            raise ValueError('field value is too long')

        return super().set_field_at(
            index,
            name=name,
            value=value,
            inline=inline
        )

    def to_dict(self)-> dict:
        return super().to_dict()
