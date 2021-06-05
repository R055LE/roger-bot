import importlib
import inspect
import pkgutil
from typing import Iterator, NoReturn

from discord.ext.commands import Context

import extentions


def unqualify(name: str) -> str:
    """Return an unqualified name given a qualified module/package `name`."""
    return name.rsplit(".", maxsplit=1)[-1]


def walk_extensions() -> Iterator[str]:
    """Yield extension names from the bot.exts subpackage."""

    def on_error(name: str) -> NoReturn:
        raise ImportError(name=name)  # pragma: no cover

    for module in pkgutil.walk_packages(extentions.__path__, f"{extentions.__name__}.", onerror=on_error):
        if unqualify(module.name).startswith("_"):
            # Ignore module/package names starting with an underscore.
            continue

        if module.ispkg:
            imported = importlib.import_module(module.name)
            if not inspect.isfunction(getattr(imported, "setup", None)):
                # If it lacks a setup function, it's not an extension.
                continue

        else:
            continue

        yield module.name


async def invoke_help_command(ctx: Context) -> None:
    """Invoke the help command or default help command if help extensions is not loaded."""
    if 'extentions.general' in ctx.bot.extensions:
        help_command = ctx.bot.get_command('help')
        await ctx.invoke(help_command, ctx.command.qualified_name)
        return
    await ctx.send_help(ctx.command)

EXTENSIONS = frozenset(walk_extensions())
