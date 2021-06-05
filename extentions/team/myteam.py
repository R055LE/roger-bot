import discord.ext.commands as commands
from classes.context import Context
from discord.ext.commands import Bot
from settings import Category


class MyTeam(commands.Cog):
    category = Category.team

    def __init__(self, client: Bot):
        self.client = client

    @commands.command(aliases=['mt', 'mytm'], description='MSF.GG Team Filter')
    async def myteam(self, context: Context, *args):
        """
        """

        await context.pod.get_player()
        title = context.pod.player.get_myteam(args)
        return await context.pod.team_out(title)
