"""
MIT License

Copyright (c) 2019 1ntegrale9

https://github.com/DiscordBotPortalJP/dispander
"""
import re


from discord import Embed


from . import _bot_config
from .config import config


__all__ = ('regex_discord_message_url','dispand')


regex_discord_message_url = (
    'https://(ptb.|canary.)?discord(app)?.com/channels/'
    '(?P<guild>[0-9]{18})/(?P<channel>[0-9]{18})/(?P<message>[0-9]{18})'
)


async def dispand(message):
    messages = await extract_messages(message)
    for m in messages:
        if m.content or m.attachments:
            await message.channel.send(embed=compose_embed(m))
        if len(m.attachments) >= 2:
            # Send the second and subsequent attachments
            # #with embed (named 'embed') respectively:
            for attachment in m.attachments[1:]:
                embed = Embed(color=config.embed_setting.color)
                embed.set_image(
                    url=attachment.proxy_url
                )
                await message.channel.send(embed=embed)
        for embed in m.embeds:
            await message.channel.send(embed=embed)


async def extract_messages(message):
    messages = []
    for ids in re.finditer(regex_discord_message_url, message.content):
        if message.guild.id != int(ids['guild']):
            continue
        fetched_message = await fetch_message_from_id(
            guild=message.guild,
            channel_id=int(ids['channel']),
            message_id=int(ids['message']),
        )
        messages.append(fetched_message)
    return messages


async def fetch_message_from_id(guild, channel_id, message_id):
    channel = guild.get_channel(channel_id)
    message = await channel.fetch_message(message_id)
    return message


def compose_embed(message):
    embed = Embed(
        description=message.content,
        timestamp=message.created_at,
        color=config.embed_setting.color
    )
    embed.set_author(
        name=message.author.display_name,
        icon_url=message.author.avatar_url,
    )
    embed.set_footer(
        text=message.channel.name,
        icon_url=message.guild.icon_url,
    )
    if message.attachments and message.attachments[0].proxy_url:
        embed.set_image(
            url=message.attachments[0].proxy_url
        )
    return embed
