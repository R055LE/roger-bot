import discord.ext.commands as commands
from classes.context import Context
from bot import Bot
from settings import Category


class Character(commands.Cog):
    category = Category.character

    def __init__(self, client: Bot):
        self.client = client

    @commands.command(aliases=['c', 'ch', 'character'], description='Character Filter')
    async def char(self, context: Context, *args):
        """
        """

        await context.pod.get_player()
        context.pod.player.get_character(args)
        if len(context.pod.player.roster) > 1:
            title = f'Characters ({len(context.pod.player.roster)})'
            return await context.pod.team_out(title)

        elif len(context.pod.player.roster) == 1:
            return await context.pod.character_out()

        else:
            return await context.send(f'No Results Found.')
