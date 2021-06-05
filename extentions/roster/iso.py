import discord.ext.commands as commands
from classes.context import Context
from settings import Category, Filters


class Iso(commands.Cog):
    category = Category.roster
    func = 'iso'

    def __init__(self, client: commands.Bot):
        super().__init__()
        self.client = client

    def alias() -> list:
        output = []
        modifiers = ['i', 'is', 'iso']
        for i in range(0, 5+1):
            for m in modifiers:
                output.append(f'{i}{m}')
                output.append(f'{m}{i}')
        return output

    @ commands.command(aliases=Filters.iso8, description='ISO-8 Lvl Filter')
    async def iso(self, context: Context, *args):
        """
        Filter Roster by ISO-8 Level, or within a range.

        One argument for a single parameter.
            > rgr iso 5
        Two arguments for a range.
            > rgr iso 1 3
        Can be combined with other roster filters.
            > rgr iso 2 4 lvl 75
        """

        title = 'Iso Lvl'
        await context.pod.get_player()

        try:
            rg = (int(args[0]), int(args[1]))
            context.pod.player.get_iso(rg=rg)
            title = f'{title} {rg[0]}-{rg[1]}'

        except (IndexError, ValueError):
            try:
                eq = int(args[0])
                context.pod.player.get_iso(eq=eq)
                title = f'{title} {eq}'

            except (IndexError, ValueError):
                await context.send('No Argument Given for ISO')

        return await context.pod.roster_out(title, '+Iso')

    @ commands.command(hidden=True, aliases=alias())
    async def _iso(self, context: Context, *args, sub=None):
        if sub:
            sub = ''.join(
                filter(str.isdigit, sub))
        else:
            sub = ''.join(
                filter(str.isdigit, context.message.content.split()[1]))
        return await self.client.get_command(self.func)(context, sub, *args)
