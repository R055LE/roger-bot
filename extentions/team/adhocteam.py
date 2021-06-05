import discord.ext.commands as commands
from classes.context import Context
from discord.ext.commands import Bot
from settings import Category


class AdHocTeam(commands.Cog):
    category = Category.team

    def __init__(self, client: Bot):
        self.client = client

    @commands.command(aliases=['at', 'atm', 'adtm'], description='Ad Hoc Team Filter')
    async def adteam(self, context: Context, *args):
        """
        """

        title = 'Ad Hoc Team'
        stop_args = ('#', '!', ',', '.', '$', '@', '*')

        for arg in args:
            arg: str
            stop = next(
                filter(lambda s:  s in args or arg.startswith(s), stop_args), None)
            stop_arg = arg
            stop_index = args.index(stop_arg)
            if stop:
                title = " ".join(args[stop_index:]).upper()
                if title[0] in stop_args:
                    title = title[1:]
                args = args[:stop_index]
                break

        await context.pod.get_player()
        context.pod.player.get_adteam(args)
        return await context.pod.team_out(title)
