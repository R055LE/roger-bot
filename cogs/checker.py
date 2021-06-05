from classes.character import Character
from classes.player import Player
from classes.alliance import Alliance
from json.decoder import JSONDecodeError
# from utils.dataload import SQL
import discord
from discord.ext import commands
import json
import re
from pathlib import Path
cwd = Path(__file__).parents[1]


async def error_handle(ctx, e, blurb):
    import traceback
    tb_str = traceback.format_exception(
        etype=type(e), value=e, tb=e.__traceback__)
    traceback_str = ''.join(tb_str)  # To Log
    print(traceback_str)
    return await ctx.send(blurb)


class Checker(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(hidden=True, aliases=['p'])
    @commands.is_owner()
    async def pull(self, ctx, *args):
        try:
            ME = Player('170162826051190784')  # R055LE

        except JSONDecodeError as e:
            return await error_handle(ctx, e, 'JSON Decode Error, Response Not Recieved From Data Source')

    @commands.command(hidden=True)
    @commands.is_owner()
    async def check(self, ctx, *args):
        # Send to Specific Channel of Specific Guild, from Any Guild
        try:
            guild_id = 583423823123316739
            channel_id = 628102784771686427

            g = self.client.get_guild(guild_id)
            c = g.get_channel(channel_id)
            return await c.send('This is a Test.')
        except discord.errors.Forbidden as e:
            return await error_handle(ctx, e, 'Forbidden Request, Permissions for This Action Are Not Enabled.')

    @commands.command(hidden=True)
    @commands.is_owner()
    async def check_roles(self, ctx, *args):
        guild = self.client.get_guild(ctx.message.guild.id)
        members = guild.members
        find_roles = []
        check_role = int(args[0][3:-1])
        for a in args[1:]:
            find_role = int(a[3:-1])
            find_roles.append(find_role)

        for m in members:
            if check_role in list(r.id for r in m.roles):
                for role in find_roles:
                    if ctx.message.guild.get_role(role) in m.roles:
                        print(m.display_name,
                              ctx.message.guild.get_role(role).name)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def remove_roles(self, ctx, *args):
        guild = self.client.get_guild(ctx.message.guild.id)
        members = guild.members
        manage_roles = []
        check_role = int(args[0][3:-1])
        for a in args[1:]:
            manage_role = int(a[3:-1])
            manage_roles.append(manage_role)

        for m in members:
            if check_role in list(r.id for r in m.roles):
                for role in manage_roles:
                    await m.remove_roles(ctx.message.guild.get_role(role))


def setup(client):
    client.add_cog(Checker(client))
