import logging
import discord
from discord.ext import commands
import pymongo
import json
from cogs.mongo import Mongo
import re
import os
cwd = os.getcwd()
with open(f'{cwd}/assets/json/raid_selection.json', 'r') as f:
    raid_selection = json.load(f)


module_logger = logging.getLogger('Roger.raid')


class Raid(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.logger = logging.getLogger('Roger.raid.Raid')

    @commands.command(aliases=['l'], description='Raid Launch')
    async def launch(self, ctx, *args):
        invoke_message = await ctx.message.channel.fetch_message(int(ctx.message.id))
        await invoke_message.delete()

        class Test:
            def __init__(self, client):
                self.client = client

            async def testy(self, ctx):
                self.author_name = ctx.message.author.display_name
                self.author_id = ctx.message.author.id
                self.author_avatar = ctx.message.author.avatar_url
                self.author_roles = ctx.message.author.roles[1:]
                self.bot_name = ctx.bot.user.display_name
                self.bot_owner = 'R055LE#9503'
                self.bot_avatar = ctx.bot.user.avatar_url
                return self

        obj = await Test.testy(self, ctx)

        # print(obj.author_name, obj.author_id, obj.author_avatar,
        #       obj.author_roles, obj.bot_name, obj.bot_owner, obj.bot_avatar)
        # return

        app_info = await ctx.bot.application_info()

        player = Mongo.find_player(obj.author_id)
        alliance_id = player.get('alliance_id')
        return_fields = {"_id": 0, "alliance_settings": 1}
        alliance = Mongo.find_alliance(alliance_id, return_fields)
        alliance_settings, guild_id = alliance.get(
            'alliance_settings'), alliance.get('guild_id')
        alliance_channels, alliance_roles = alliance_settings.get(
            'channels'), alliance_settings.get('roles')
        raid_announce_channel, member_channel = alliance_channels.get(
            'raid_announce_channel'), alliance_channels.get('member_channel')
        if raid_announce_channel == "0":
            raid_announce_channel = member_channel
        raid_announce_role, member_role, leader_role = alliance_roles.get(
            'raid_announce_role'), alliance_roles.get('member_role'), alliance_roles.get('leader_role')
        if raid_announce_role == "0":
            raid_announce_role = member_role

        if ctx.message.guild.get_role(int(leader_role)) not in obj.author_roles:
            if obj.author_id != app_info.owner.id:
                return await ctx.send('Sorry, it looks like you\'re not a Captain in your Alliance.')
            else:
                raid_announce_channel = ctx.message.channel.id

        raid_array = set()
        for r in raid_selection:
            raid_id, raid_id_alts = r.get('raid_id'), r.get('raid_id_alts')
            raid_array.add(raid_id)
        user_selection = next(
            (r for r in raid_array if args[0].lower().startswith(r)), None)
        raid_id = user_selection

        # Assign Raid Id and Split off Difficulty if present.
        try:
            user_selection_split = re.split('[.,;:\-_d#]', args[0])
            raid_id = user_selection_split[0].lower()
        except TypeError:
            await ctx.send('No Raid Selected or Invalid Option Chosen.')
            return

        # Assign Push Value as Arg after Raid Selection
        try:
            push = int(args[1]) if int(
                args[1]) in range(0, 101) else None
        except IndexError:
            push = None
        except ValueError:
            push = None

        raid = Mongo.find_raids(alliance_id, raid_id)
        raid_name, raid_id, raid_id_alts, raid_thumbnail, raid_url, strike_team_1, strike_team_2, strike_team_3, diff_slider = raid.get(
            'raid_name'), raid.get('raid_id'), raid.get('raid_id_alts'), raid.get('raid_thumbnail'), raid.get('raid_url'), raid.get('strike_team_1'), raid.get('strike_team_2'), raid.get('strike_team_3'), raid.get('diff_slider')

        if diff_slider == True:
            try:
                difficulty = int(user_selection_split[1]) if int(
                    user_selection_split[1]) in range(0, 6) else None
                # difficulty = 'Normal' if difficulty == 0 else difficulty
            except IndexError:
                difficulty = None
            except ValueError:
                difficulty = None
        else:
            difficulty = None

        strike_team_1_str, strike_team_2_str, strike_team_3_str = '', '', ''
        for p in strike_team_1:
            strike_team_1_str += f'{p.get("lane")}. {p.get("player")}\n'
        for p in strike_team_2:
            strike_team_2_str += f'{p.get("lane")}. {p.get("player")}\n'
        for p in strike_team_3:
            strike_team_3_str += f'{p.get("lane")}. {p.get("player")}\n'

        image_name = raid_thumbnail
        image_used = f'{cwd}/roger/assets/images/raid/{image_name}'
        with open(f'{image_used}', 'rb') as f:
            picture = discord.File(f, filename=f'{image_name}')

        content_sub_diff = '' if difficulty == None else f' *[Difficulty {difficulty}]*'
        content_sub_push = '' if push == None else f' with a Target of {push}%'
        content = f'<@&{raid_announce_role}>, {raid_name}{content_sub_diff} Launched{content_sub_push}'

        prefix = await self.client.get_prefix(ctx)
        prefix = prefix[0]

        embed = discord.Embed(
            title=raid_name, url=raid_url, color=discord.Color.dark_blue())
        embed.add_field(name='Strike Team 1',
                        value=strike_team_1_str, inline=False)
        embed.add_field(name='Strike Team 2',
                        value=strike_team_2_str, inline=False)
        embed.add_field(name='Strike Team 3',
                        value=strike_team_3_str, inline=False)
        embed.set_author(name=obj.author_name, url=discord.Embed.Empty,
                         icon_url=obj.author_avatar)
        embed.set_thumbnail(url=f'attachment://{image_name}')
        embed.set_footer(
            text=f'{prefix}launch {args[0]}{f" {args[1]}" if len(args) > 1 else ""}{f" {args[2]}" if len(args) > 2 else ""}', icon_url=obj.bot_avatar)
        test = ctx.guild.get_channel(int(raid_announce_channel))

        # int(raid_announce_channel))
        def predicate(message):
            return message.author.bot and message.content.startswith(f'<@&{raid_announce_role}>, {raid_name}')

        async for msg in self.client.get_channel(int(raid_announce_channel)).history().filter(predicate):
            await msg.delete()

        await self.client.get_channel(int(raid_announce_channel)).send(content=content, embed=embed, file=picture)

        self.logger.info(
            f'{ctx.message.author.display_name} used Launch in {ctx.message.channel}')


def setup(client):
    client.add_cog(Raid(client))
