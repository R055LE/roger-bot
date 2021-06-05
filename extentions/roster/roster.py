import discord.ext.commands as commands
from classes.context import Context
from settings import Category, Filters


class Roster(commands.Cog):
    category = Category.roster
    func = 'roster'

    def __init__(self, client: commands.Bot):
        super().__init__()
        self.client = client

    @ commands.command(aliases=Filters.roster, description='Whole Roster')
    async def roster(self, context: Context, *args):
        """
        Bring Up The Whole Roster, Top Selection or a Specific Range.

        Whole Roster
            > rgr roster
        Top Section
            > rgr roster 10
        Within Range
            > rgr roster 119 140
        """

        title = 'Roster'
        await context.pod.get_player()

        try:
            rg = (int(args[0]), int(args[1]))
            context.pod.player.get_r(rg=rg)
            title = f'{title} {rg[0]}-{rg[1]}'

        except (IndexError, ValueError):
            try:
                eq = int(args[0])
                context.pod.player.get_r(eq=eq)
                title = f'{title} Top {eq}'

            except (IndexError, ValueError):
                context.pod.player.get_r()
                title = 'All Characters'

        return await context.pod.roster_out(title, '+Roster', single=True)
