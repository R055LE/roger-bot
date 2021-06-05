from discord.ext import commands
from classes.context import Context


class Check(commands.Cog):
    category = "Admin"

    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.is_owner()
    @commands.command(hidden=True, description='Administrative Trigger Command')
    async def check(self, context: Context, *args):
        pass
        # await context.pod.check_for_next_step()
