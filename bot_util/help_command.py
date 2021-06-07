from typing import Union
import discord
from discord.ext import commands


from . import _bot_config
from .config import config


__all__ = ('Help')


class Help(commands.HelpCommand):
    def __init__(self):
        super().__init__()
        self.no_category = "カテゴリ未設定"
        self.command_attrs["short_doc"] = "このメッセージを表示します。"
        self.command_attrs["help"] = "このBOTのヘルプコマンドです。"
        self.color = config.embed_setting.color

    async def create_category_tree(
            self,
            category: Union[commands.Cog, commands.Group]
            ):
        content_line: list[str]= []
        lv: list[int]= []
        command_list = category.walk_commands()
        cmds: list[commands.Command]= await self.filter_commands(command_list,sort=False)
        for cmd in cmds:
            if cmd.root_parent is None:
                content_line.append(
                    (f"`{self.get_command_signature(cmd)}`"
                    f" : {cmd.short_doc}")
                    )
                lv.append(0)
            else:
                indent = '-' * cmd.parents.index(cmd.root_parent)
                content_line.append(
                    (f"{indent}`{self.get_command_signature(cmd)}`"
                    f" : {cmd.short_doc}")
                    )
                lv.append(len(indent))
        if lv and min(lv):
            for index, line in enumerate(content_line):
                if line.startswith('-'*min(lv)):
                    content_line[index] = line[min(lv):]
        return '\n'.join(content_line) or 'コマンドは存在しません。'

    async def send_bot_help(self,mapping):
        embed = discord.Embed(title='helpコマンド', color=self.color)
        if self.context:
            embed.description = self.context.bot.description
        for cog in mapping:
            if cog:
                cog_name = cog.qualified_name
            else:
                cog_name = self.no_category
            command_list = await self.filter_commands(
                mapping[cog],sort=True
                )
            content = ''
            for cmd in command_list:
                    content += (
                        f'`{self.context.prefix}{cmd.name}`'
                        f' - {cmd.short_doc}\n'
                        )
            if content == '':
                continue
            embed.add_field(name=cog_name,value=content,inline=False)
        embed.set_footer(text= self.get_ending_note())
        await self.get_destination().send(embed=embed)

    async def send_cog_help(self,cog):
        embed = discord.Embed(
            title=cog.qualified_name,
            description=cog.description,
            color=self.color
            )
        embed.add_field(
            name="コマンドリスト",
            value=await self.create_category_tree(cog)
            )
        embed.set_footer(text= self.get_ending_note())
        await self.get_destination().send(embed=embed)

    async def send_group_help(self,group):
        embed = discord.Embed(
            title=self.get_command_signature(group),
            description=group.description,
            color=self.color
            )
        if group.help:
            embed.add_field(
                name="ヘルプテキスト",
                value=group.help,
                inline=False
                )
        embed.add_field(
            name="サブコマンドリスト",
            value=await self.create_category_tree(group),
            inline=False
            )
        embed.set_footer(text= self.get_ending_note())
        await self.get_destination().send(embed=embed)

    async def send_command_help(self,command):
        embed = discord.Embed(
            title=self.get_command_signature(command),
            description=command.description,
            color=self.color
            )
        if command.help:
            embed.add_field(
                name="ヘルプテキスト",
                value=command.help,
                inline=False
                )
        embed.set_footer(text= self.get_ending_note())
        await self.get_destination().send(embed=embed)

    async def send_error_message(self, error):
        embed = discord.Embed(
            title="ヘルプ表示のエラー",
            description=error,
            color=self.color
            )
        embed.set_footer(text= self.get_ending_note())
        await self.get_destination().send(embed=embed)

    def get_ending_note(self):
        command_name = self.invoked_with
        return (
            f"{self.clean_prefix}{command_name}"
            " <command_name> とすることでコマンドについてのヘルプを閲覧できます。\n"
            f"{self.clean_prefix}{command_name}"
            " <category_name> とすることでカテゴリーの詳細情報を閲覧できます。"
            )

    def command_not_found(self,string):
        return f"{string} というコマンドは存在しません。"

    def subcommand_not_found(self,command,string):
        if (isinstance(command, commands.Group)
                and len(command.all_commands) > 0):
            return (f"{command.qualified_name} に {string}"
                " というサブコマンドは登録されていません。")
        return f"{command.qualified_name} にサブコマンドは登録されていません。"
