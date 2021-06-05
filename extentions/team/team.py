import discord.ext.commands as commands
from classes.context import Context
from discord.ext.commands import Bot
from settings import Category


class Team(commands.Cog):
    category = Category.team

    def __init__(self, client: Bot):
        self.client = client

    @commands.command(aliases=['t', 'tm'], description='Prebuilt Team Command')
    async def team(self, context: Context, *args: tuple):
        """
        Display a Team Selected from a List of Prebuilt Meta Options
            > rgr tm s6
        """

        await context.pod.get_player()
        title = context.pod.player.get_prebuilt(*args)
        return await context.pod.team_out(title)
