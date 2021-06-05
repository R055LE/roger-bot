import itertools
import traceback
from datetime import datetime
from pathlib import Path

import discord
import discord.ext.commands as commands
from discord import DiscordException

from classes.context import Context
from settings import BOT_DIR, Client


__all__ = (
    'Bot',
    'bot'
)


class Bot(commands.Bot):

    name = Client.name

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)

    async def on_command_error(self, context: Context, exception: DiscordException) -> None:
        """Logs the Error and Stack Trace into a File and Passes to Super."""
        # Add Work-Around for In content: Must be 2000 or fewer in length.
        traceback_message = f'[DATE] {datetime.now()}\n[COMMAND] {context.command}\n[CHANNEL] #{context.channel}\n[GUILD] {context.guild}\n[CONTEXT] {context.message.content}\n\n'
        traceback_message += ''.join(traceback.format_exception(
            etype=type(exception), value=exception, tb=exception.__traceback__))

        with open(file=Path(BOT_DIR, 'logs', 'traceback.log'), mode='a') as f:
            print(traceback_message, file=f)

        if len(traceback_message) < 1800:
            await self.get_channel(Client.log_channel).send(f'<@{Client.log_owner}>\n```json\n{traceback_message}\n```')

        await super().on_command_error(context, exception)

    async def get_context(self, message, *, cls: Context = Context):
        return await super().get_context(message, cls=cls)


def get_intents():
    intents: discord.Intents = discord.Intents.all()
    intents.presences = False
    intents.dm_typing = False
    intents.dm_reactions = False
    intents.invites = False
    intents.webhooks = False
    intents.integrations = False
    return intents


def custom_when_mentioned_or(prefix: str):
    """Only Works with Single String, Will Duplicate Single Characters. Needs Work, Will Do For Now."""

    def inner_func(bot: Bot, msg: discord.Message):
        pref_string: str = prefix
        rtn = list(map(''.join, itertools.product(
            *zip(pref_string.upper(), pref_string.lower()))))

        r = list(rtn)
        r = commands.when_mentioned(bot, msg) + rtn
        return r

    return inner_func


bot = Bot(
    command_prefix=custom_when_mentioned_or(Client.prefix),
    case_insensitive=True,
    activity=discord.Activity(
        type=discord.ActivityType.watching, name=f'"{Client.prefix}help"'),
    intents=get_intents()
)
