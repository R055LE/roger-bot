import discord.ext.commands as commands
from classes.context import Context
from settings import Category, Filters


class RedStar(commands.Cog):
    category = Category.roster
    func = 'rs'

    def __init__(self, client: commands.Bot):
        super().__init__()
        self.client = client

    def alias() -> list:
        output = []
        modifiers = ['r', 'rs']
        for i in range(0, 7+1):
            for m in modifiers:
                output.append(f'{i}{m}')
                output.append(f'{m}{i}')
        return output

    @ commands.command(aliases=Filters.redstar, description='Red Star Filter')
    async def rs(self, context: Context, *args):
        """
        Filter Roster by a number of Red Stars, or within a range.

        One argument for a single parameter.
            > rgr rs 7
        Two arguments for a range.
            > rgr rs 1 3
        Can be combined with other roster filters.
            > rgr rs 5 lvl 71 75

        Aliases available: 0r, 7rs, r6, etc.
        """

        title = 'Red Star'
        await context.pod.get_player()

        try:
            rg = (int(args[0]), int(args[1]))
            context.pod.player.get_rs(rg=rg)
            title = f'{rg[0]}-{rg[1]} {title}'

        except (IndexError, ValueError):
            try:
                eq = int(args[0])
                context.pod.player.get_rs(eq=eq)
                title = f'{eq} {title}'

            except (IndexError, ValueError):
                await context.send('No Argument Given for RS')

        return await context.pod.roster_out(title, '+Reds')

    @ commands.command(hidden=True, aliases=alias())
    async def _rs(self, context: Context, *args, sub=None):
        if sub:
            sub = ''.join(
                filter(str.isdigit, sub))
        else:
            sub = ''.join(
                filter(str.isdigit, context.message.content.split()[1]))
        return await self.client.get_command(self.func)(context, sub, *args)
