import discord.ext.commands as commands
from classes.context import Context
from discord.ext.commands import Bot
from settings import Category


class TraitTeam(commands.Cog):
    category = Category.team

    def __init__(self, client: Bot):
        self.client = client

    @commands.command(aliases=['tttm', 'ttm'], description='Traits Team Filter')
    async def tteam(self, context: Context, *args):
        """
        """

        await context.pod.get_player()
        traits = context.pod.player.get_tteam(args)
        description = f'{", ".join(traits)}'
        return await context.pod.team_out('Trait Team', description)
