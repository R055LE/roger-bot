import discord.ext.commands as commands
from classes.context import Context
from settings import Category, Filters


class Star(commands.Cog):
    category = Category.roster
    func = 'ys'

    def __init__(self, client: commands.Bot):
        super().__init__()
        self.client = client

    def alias() -> list:
        output = []
        modifiers = ['y', 'ys']
        for i in range(0, 7+1):
            for m in modifiers:
                output.append(f'{i}{m}')
                output.append(f'{m}{i}')
        return output

    @ commands.command(aliases=Filters.yellowstar, description='Star Filter')
    async def ys(self, context: Context, *args):
        """
        Filter Roster by a number of Stars, or within a range.

        One argument for a single parameter.
            > rgr ys 5
        Two arguments for a range.
            > rgr ys 4 6
        Can be combined with other roster filters.
            > rgr ys 5 gr 12 14
        """

        title = 'Star'
        await context.pod.get_player()

        try:
            rg = (int(args[0]), int(args[1]))
            context.pod.player.get_ys(rg=rg)
            title = f'{rg[0]}-{rg[1]} {title}'

        except (IndexError, ValueError):
            try:
                eq = int(args[0])
                context.pod.player.get_ys(eq=eq)
                title = f'{eq} {title}'

            except (IndexError, ValueError):
                await context.send('No Argument Given for YS')

        return await context.pod.roster_out(title, '+Star')

    @ commands.command(hidden=True, aliases=alias())
    async def _ys(self, context: Context, *args, sub=None):
        if sub:
            sub = ''.join(
                filter(str.isdigit, sub))
        else:
            sub = ''.join(
                filter(str.isdigit, context.message.content.split()[1]))
        return await self.client.get_command(self.func)(context, sub, *args)
