import discord.ext.commands as commands
from classes.context import Context
from settings import Category, Filters


class Favorite(commands.Cog):
    category = Category.roster
    func = 'fav'

    def __init__(self, client: commands.Bot):
        super().__init__()
        self.client = client

    @ commands.command(aliases=Filters.favorite, description='Favorites Filter')
    async def fav(self, context: Context, *args):
        """
        Filter Roster by Favorites Selection.
            > rgr fav

        Can be combined with other roster filters.
        """

        await context.pod.get_player()

        context.pod.player.get_fav()
        title = 'Favorites'

        return await context.pod.roster_out(title, '+Favorite')
