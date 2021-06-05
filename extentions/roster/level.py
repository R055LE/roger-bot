import discord.ext.commands as commands
from classes.context import Context
from settings import Category, Filters


class Level(commands.Cog):
    category = Category.roster
    func = 'lvl'

    def __init__(self, client: commands.Bot):
        super().__init__()
        self.client = client

    def alias() -> list:
        output = []
        modifiers = ['lv', 'lvl', 'l']
        for i in range(0, 100+1):
            for m in modifiers:
                output.append(f'{i}{m}')
                output.append(f'{m}{i}')
        return output

    @ commands.command(aliases=Filters.level, description='Level Filter')
    async def lvl(self, context: Context, *args):
        """
        Filter Roster by character Level, or within a range.

        One argument for a single parameter.
            > rgr lvl 70
        Two arguments for a range.
            > rgr lvl 71 75
        Can be combined with other roster filters.
            > rgr lvl 60 rs 5
        """

        title = 'Level'
        await context.pod.get_player()

        try:
            rg = (int(args[0]), int(args[1]))
            context.pod.player.get_lvl(rg=rg)
            title = f'{title} {rg[0]}-{rg[1]}'

        except (IndexError, ValueError):
            try:
                eq = int(args[0])
                context.pod.player.get_lvl(eq=eq)
                title = f'{title} {eq}'

            except (IndexError, ValueError):
                await context.send('No Argument Given for LVL')

        return await context.pod.roster_out(title, '+Lvl')

    @ commands.command(hidden=True, aliases=alias())
    async def _lvl(self, context: Context, *args, sub=None):
        if sub:
            sub = ''.join(
                filter(str.isdigit, sub))
        else:
            sub = ''.join(
                filter(str.isdigit, context.message.content.split()[1]))
        return await self.client.get_command(self.func)(context, sub, *args)
