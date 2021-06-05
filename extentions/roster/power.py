import discord.ext.commands as commands
from classes.context import Context
from settings import Category, Filters


class Power(commands.Cog):
    category = Category.roster
    func = 'power'

    def __init__(self, client: commands.Bot):
        super().__init__()
        self.client = client

    def alias() -> list:
        output = []
        modifiers = ['pow', 'p', 'pwr']
        for i in range(0, 1000+1):
            for m in modifiers:
                output.append(f'{i}{m}')
                output.append(f'{m}{i}')
        return output

    @ commands.command(aliases=Filters.power, description='Power Filter')
    async def power(self, context: Context, *args):
        """
        Filter Roster by character Power, or within a range. In increments of 1000.

        For Power At or Exceeding a Certain Level
            > rgr power 100
        For Power In a Certain Range
            > rgr power 100 130
        Can be combined with other roster filters.
            > rgr power 100 ys 7
        """

        title = 'Power'
        await context.pod.get_player()

        try:
            rg = (int(args[0]), int(args[1]))
            context.pod.player.get_pow(rg=rg)
            title = f'{rg[0]}K-{rg[1]}K {title}'

        except (IndexError, ValueError):
            try:
                eq = int(args[0])
                context.pod.player.get_pow(eq=eq)
                title = f'{eq}K+ {title}'

            except (IndexError, ValueError):
                await context.send('No Argument Given for POWER')

        return await context.pod.roster_out(title, '+Power')

    @ commands.command(hidden=True, aliases=alias())
    async def _power(self, context: Context, *args, sub=None):
        if sub:
            sub = ''.join(
                filter(str.isdigit, sub))
        else:
            sub = ''.join(
                filter(str.isdigit, context.message.content.split()[1]))
        return await self.client.get_command(self.func)(context, sub, *args)
