import discord.ext.commands as commands
from discord.ext.commands import Bot
from settings import Category
from classes.context import Context


class AllTeam(commands.Cog):
    category = Category.team

    def __init__(self, client: Bot):
        self.client = client

    @commands.command(aliases=['alltm', 'ateam'], description='Prebuilt Team Filter')
    async def allteam(self, context: Context, *args):
        """
        """

        await context.pod.get_alliance()
        title = context.pod.alliance.get_all_prebuilt(args)
        return await context.pod.alliance_out(title)
