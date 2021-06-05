import discord.ext.commands as commands
from classes.context import Context
from settings import Category, Filters


class Gear(commands.Cog):
    category = Category.roster
    func = 'gr'

    def __init__(self, client):
        super().__init__()
        self.client = client

    def alias() -> list:
        output = []
        modifiers = ['g', 'gr', 'gt']
        for i in range(0, 16+1):
            for m in modifiers:
                output.append(f'{i}{m}')
                output.append(f'{m}{i}')
        return output

    @ commands.command(aliases=Filters.gear, description='Gear Filter')
    async def gr(self, context: Context, *args):
        """
        Filter Roster by Gear Tier, or within a range.

        One argument for a single parameter.
            > rgr gr 14
        Two arguments for a range.
            > rgr gr 12 14
        Can be combined with other roster filters.
            > rgr gr 11 13 power 100
        """

        title = 'Gear Tier'
        await context.pod.get_player()

        try:
            rg = (int(args[0]), int(args[1]))
            context.pod.player.get_gr(rg=rg)
            title = f'{title} {rg[0]}-{rg[1]}'

        except (IndexError, ValueError):
            try:
                eq = int(args[0])
                context.pod.player.get_gr(eq=eq)
                title = f'{title} {eq}'

            except (IndexError, ValueError):
                await context.send('No Argument Given for GR')

        return await context.pod.roster_out(title, '+Gear')

    @ commands.command(hidden=True, aliases=alias())
    async def _gr(self, context: Context, *args, sub=None):
        if sub:
            sub = ''.join(
                filter(str.isdigit, sub))
        else:
            sub = ''.join(
                filter(str.isdigit, context.message.content.split()[1]))
        return await self.client.get_command(self.func)(context, sub, *args)
