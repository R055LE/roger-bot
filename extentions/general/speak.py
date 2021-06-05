import discord.ext.commands as commands
from classes.context import Context


class Speak(commands.Cog):
    category = "General"

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['hi', 'hello', 'squawk'], description='Say Hi!')
    async def speak(self, ctx: Context, *args):
        """
        Receive A Friendly Response!
        """
        await ctx.message.delete()
        return await ctx.send('Hello.')
