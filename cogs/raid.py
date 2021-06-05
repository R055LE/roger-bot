from pathlib import Path
import json
import os
import re

import discord
import requests
from classes.alliance import Alliance
from discord.ext import commands

api_server = 'http://10.0.0.40:5000'

cwd = Path(__file__).parents[1]


def alliance():
    alliances = json.loads(requests.get(
        f'{api_server}/get/alliances/').content)
    return alliances


def members(discord_id):
    members = json.loads(requests.get(
        f'{api_server}/get/members/msfgg/{discord_id}').content)
    return members


def raids():
    raids = json.loads(requests.get(
        f'{api_server}/get/raids/').content)
    return raids


async def error_handle(ctx, e, blurb):
    import traceback
    tb_str = traceback.format_exception(
        etype=type(e), value=e, tb=e.__traceback__)
    traceback_str = ''.join(tb_str)  # To Log
    print(traceback_str)
    return await ctx.send(blurb)


class Raid(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['l'])
    async def launch(self, ctx, *args):
        all_members = members(ctx.message.author.id)
        all_alliances = alliance()
        all_raids = raids()

        alli = next(filter(lambda a: ctx.message.author.id in a.get(
            'player_list'), all_alliances), None)
        if alli is None:
            return await ctx.send('Your Alliance is Not Registered.')

        try:
            selection, difficulty = re.split('[.,;:\-#]', args[0])
            difficulty = int(difficulty)
        except (IndexError, ValueError) as e:
            try:
                selection = args[0]
                difficulty = None
            except (IndexError, ValueError) as e:
                return await error_handle(ctx, e, 'Required Argument Missing, See `rgr help launch` for the Correct Context.')

        raid = next(
            filter(lambda r: selection.casefold() in r.get('aliases'), all_raids), None)

        if raid is None:
            return await ctx.send(f'Raid for Argument {selection} Not Found.')

        try:
            push = round(float(args[1]))
        except IndexError:
            push = None
        except (IndexError, ValueError) as e:
            return await error_handle(ctx, e, 'Push Ammount is Invalid, See `rgr help launch` for the Correct Context.')

        a = Alliance(ctx.message.author.id)
        # Must be Captain in MSF.GG for Now
        is_captain = next(filter(lambda m: m.get('MemberId') == ctx.message.author.id and m.get('Role') in [
            'Captain', 'Leader'], all_members), None)

        if is_captain is False:
            return await ctx.send('You Are not a Captain nor the Leader of your Alliance in MSF.GG')

        strike_teams = a.GetLaneAssignments(raid.get('designation'))

        st = [[], [], []]
        for i in range(3):
            for ii in range(8):
                player = next((p for p in strike_teams if (
                    p.get('Team') == i+1) and p.get('Lane') == ii+1), None)
                st[i].append(
                    f"{ii+1}: {'' if player is None else player.get('DisplayName')}")

        with open(f'{cwd}/assets/images/raid/{raid.get("thumbnail")}', 'rb') as f:
            thumbnail = discord.File(f, filename=raid.get('thumbnail'))

        uri = f'https://msf.gg/alliance/id/{alli.get("msfgg_id")}/maps?raidId={raid.get("designation")}'

        if raid.get('slider') and push in range(1, 100+1) and difficulty in range(1, raid.get('max_difficulty')+1):
            title = f'{alli.get("raid_role")}, {raid.get("name")} *[Difficulty {difficulty}]* Launched with a Target of {push}%'
        elif raid.get('slider') and push in range(1, 100+1):
            title = f'{alli.get("raid_role")}, {raid.get("name")} Launched with a Target of {push}%'
        else:
            title = f'{alli.get("raid_role")}, {raid.get("name")} Launched'
        embed = discord.Embed(
            title=raid.get('name'), url=uri, color=discord.Color.dark_blue())
        for i in range(3):
            embed.add_field(name=f'Strike Team {i+1}',
                            value='\n'.join(st[i]))
        embed.set_author(name=ctx.message.author.display_name, url=discord.Embed.Empty,
                         icon_url=f'https://cdn.discordapp.com/avatars/{ctx.message.author.id}/{ctx.message.author.avatar}')
        embed.set_thumbnail(url=f'attachment://{raid.get("thumbnail")}')
        embed.set_footer(
            text=ctx.message.content, icon_url=f'https://cdn.discordapp.com/avatars/{self.client.user.id}/{self.client.user.avatar}')

        # self.client.get_channel(int(raid_announce_channel)).send(content=content, embed=embed, file=picture)
        return await ctx.message.channel.send(content=title, embed=embed, file=thumbnail)


def setup(client):
    client.add_cog(Raid(client))
