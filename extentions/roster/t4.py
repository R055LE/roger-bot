import discord.ext.commands as commands
from classes.context import Context
from settings import Category, Filters


class T4(commands.Cog):
    category = Category.roster
    func = 't4'

    def __init__(self, client: commands.Bot):
        super().__init__()
        self.client = client

    @ commands.command(aliases=Filters.t4, description='T4 Filter')
    async def t4(self, context: Context, *args):
        """
        Filter Roster by T4 Abilities, T4 Maxed or T4 None.

        Any T4
            > rgr t4
        All T4
            > rgr t4 all
        T4 None
            > rgr t4 none
        Can be combined with other roster filters.
            > rgr t4 all gr 14
        """

        await context.pod.get_player()

        try:
            if any(l for l in ['max', 'all', '*'] if l == args[0].casefold()):
                context.pod.player.get_t4(t4_all=True)
                title = 'T4 ALL'

            if any(l for l in ['none', 'no', '-', 'n'] if l == args[0].casefold()):
                context.pod.player.get_t4(t4_none=True)
                title = 'T4 NONE'

        except (IndexError, ValueError):
            context.pod.player.get_t4()
            title = 'T4 Abilities'

        return await context.pod.roster_out(title, '+T4')
