import asyncio
import logging


from discord.ext.menus import _cast_emoji
from discord.ext.menus import *


logger = logging.getLogger(__name__)


def button_deco(emoji,**kwargs):
    """ボタンクラスを返すデコレータ

    Args:
        emoji Union[str, discord.PartialEmoji]: The emoji to use for the button.
        kwargs: Button's argument
    """
    def decorator(func):
        return Button(_cast_emoji(emoji),func,**kwargs)
    return decorator


def message(func):
    """messageが送られた場合の処理の実装を書くためのデコレータ

    Args:
        func: 関数はfunc(MsgMenu,message)の形で呼び出される
            return: object
    """
    func.__menu_message__ = True
    return func


def message_check(func):
    """messageが送られた場合のチェック処理の実装を書くためのデコレータ

    Args:
        func: 関数はfunc(MsgMenu,message)の形で呼び出される
            return: boolen
    """
    func.__menu_message_check__ = True
    return func


class MsgMenuBase:
    def __init__(self):
        self._message = None
        self._message_check = None
        for v in self.__class__.__dict__.values():
            try:
                v.__menu_message__
            except AttributeError:
                pass
            else:
                self._message = v
                continue
            try:
                v.__menu_message_check__
            except AttributeError:
                continue
            else:
                self._message_check = v

    def add_message(self, func):
        self._message = func

    def add_message_check(self, func):
        self._message_check = func

    def message_check(self,message):
        """The function that used to check wheter the message should be processed.
        This is passed to discord.ext.commands.Bot.wait_for (method).
        you can set check function: message_check (decorator).

        Thre should be no reason to override this function for most users.

        Args:
            message (discord.message): The message to check.

        Returns:
            bool: Whether the message should be processed.
        """
        if (
               message.channel != self.ctx.channel
               or message.author != self.ctx.author
               ):
            return False
        if self._message_check is None:
            return True
        try:
            return self._message_check(self,message)
        except Exception:
            return False

    async def _internal_loop(self):
        try:
            self.__timed_out = False
            loop = self.bot.loop

            tasks = []
            while self._running:
                tasks = [
                    asyncio.create_task(self.bot.wait_for('raw_reaction_add', check=self.reaction_check),name='reaction'),
                    asyncio.create_task(self.bot.wait_for('raw_reaction_remove', check=self.reaction_check),name='reaction'),
                    asyncio.create_task(self.bot.wait_for('message', check=self.message_check),name='message'),
                ]
                done, pending = await asyncio.wait(tasks, timeout=self.timeout, return_when=asyncio.FIRST_COMPLETED)
                for task in pending:
                    task.cancel()

                if len(done) == 0:
                    raise asyncio.TimeoutError()

                task = done.pop()
                event_name = task.get_name()
                if event_name == 'reaction':
                    payload = task.result()
                    loop.create_task(self.update(payload))
                else:
                    msg = task.result()
                    loop.create_task(self.update_msg(msg))

        except asyncio.TimeoutError:
            self.__timed_out = True
        finally:
            self._event.set()

            for task in tasks:
                task.cancel()

            try:
                await self.finalize(self.__timed_out)
            except Exception:
                pass
            finally:
                self.__timed_out = False

            if self.bot.is_closed():
                return

            try:
                if self.delete_message_after:
                    return await self.message.delete()

                if self.clear_reactions_after:
                    if self._can_remove_reactions:
                        return await self.message.clear_reactions()

                    for button_emoji in self.buttons:
                        try:
                            await self.message.remove_reaction(button_emoji, self.bot.user)
                        except discord.HTTPException:
                            continue
            except Exception:
                pass

    async def update_msg(self,msg):
        """updates the menu after an event has been received.

        Args:
            msg (discord.message): The message event that triggred this update
        """
        if not self._running:
            return
        if self._message is None:
            return
        try:
            await self._message(self,msg)
        except Exception as exc:
            await self.on_menu_msg_error(exc)

    async def on_menu_msg_error(self, exc):
        """Handles reporting of errors hile updateing the menu from events.
        The default behaviour is to log the exception.

        This may be overriden by subclasses.

        Args:
            exc (Exception): The exception which was raised during a menu update.
        """
        logger.exception("Unhandled exception during menu update by msg.", exc_info=exc)

    def should_add_reactions(self):
        """:class:`bool`: Whether to add reactions to this menu session."""
        return len(self.buttons)


class MsgMenu(MsgMenuBase,Menu):
    """An interface that allows handling menus by using reactions as buttons and message.

    Buttons should be marled with the button (decorator). Please note that
    this expects the methods to have a single parameter, the payload. This
    payload is of type discord.RawReactionActionEvent (class).

    Args:
        timeout (float): The timeout to wait between button or message inputs.
        delete_message_after (bool): Whether to delete the message after the menu
            interaction is done.
        clear_reactions_after (bool): Whter to clear reactions after the menu
            interaction is done.
            None that delete_message_after (attr) takes priority over this attribute.
            If the bot does not habe permissions to clear the reactions then it will
            delete the reactions one by one.
        check_embeds (bool): Whter to verify embed permissions as well.
        ctx (optional[discord.ext.commands.Context]): The context that started
            this pagineation session or None if it hasn't been started yet.
        bot (optional[discord.ext.commands.Bot]): The bot that is running
            this pagination session or None if it hasn't been started yet.
        message (optional[discord.Mesasge]): The message that has been sent for
            handling the menu. This is the returned message of
            send_initial_message (method). You can set it in order to avoid calling
            send_initial_message (method), if for example you have a pre-existing
            message you want to attach a menu to.
    """
    def __init__(self,**kwargs):
        super(MsgMenu,self).__init__()
        super(MsgMenuBase,self).__init__(**kwargs)


class MsgMenuPages(MsgMenuBase,MenuPages):
    """A special type of MsgMenu dedicated to pagination.

    Args:
        source (menus.PageSource): I don't have any description this attribute.
        timeout (float): The timeout to wait between button or message inputs.
        delete_message_after (bool): Whether to delete the message after the menu
            interaction is done.
        clear_reactions_after (bool): Whter to clear reactions after the menu
            interaction is done.
            None that delete_message_after (attr) takes priority over this attribute.
            If the bot does not habe permissions to clear the reactions then it will
            delete the reactions one by one.
        check_embeds (bool): Whter to verify embed permissions as well.
        ctx (optional[commands.Context]): The context that started
            this pagineation session or None if it hasn't been started yet.
        bot (optional[commands.Bot]): The bot that is running
            this pagination session or None if it hasn't been started yet.
        message (optional[discord.Mesasge]): The message that has been sent for
            handling the menu. This is the returned message of
            send_initial_message (method). You can set it in order to avoid calling
            send_initial_message (method), if for example you have a pre-existing
            message you want to attach a menu to.
    """
    def __init__(self, source, **kwargs):
        super(MsgMenuPages,self).__init__()
        super(MsgMenuBase,self).__init__(source, **kwargs)
