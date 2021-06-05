import discord
from discord.ext import commands
import pymongo
import json
import requests
from cogs.mongo import Mongo
from cogs.cron import Cron
from settings import TAGLINES
from pathlib import Path
cwd = Path(__file__).parents[1]


class Test:
    def __init__(self, client):
        self.client = client

    async def testy(self, ctx):
        self.author_name = ctx.message.author.display_name
        self.author_id = ctx.message.author.id
        self.author_avatar = ctx.message.author.avatar_url
        self.author_roles = ctx.message.author.roles[1:]
        self.bot_name = ctx.bot.user.display_name
        self.bot_owner = ''
        self.bot_avatar = ctx.bot.user.avatar_url
        return self

        # print(obj.author_name, obj.author_id, obj.author_avatar,
        #       obj.author_roles, obj.bot_name, obj.bot_owner, obj.bot_avatar)
        # return


with open(f'{cwd}/assets/json/default_messages.json', 'r') as f:
    default_messages = json.load(f)
with open(f'{cwd}/assets/json/war_times.json', 'r') as f:
    war_times = json.load(f)


class Messages(commands.Cog):

    def __init__(self, client):
        self.client = client

    async def message_init(self, force=False):
        changed = False
        alliance_all = Mongo.find_alliance_all()
        for alliance in alliance_all:
            alliance_id, alliance_settings, alliance_name = alliance.get(
                'alliance_id'), alliance.get('alliance_settings'), alliance.get('alliance_name')
            channels, roles = alliance_settings.get(
                'channels'), alliance_settings.get('roles')

            war_announce_channel, war_announce_role = channels.get(
                'war_announce_channel') if channels != None else 0, roles.get('war_announce_role') if roles and roles.get('war_announce_role') != '0' else roles.get('member_role') if roles != None else 0
            alliance_messages = Mongo.find_messages(alliance_id)
            if len(list(alliance_messages)) == 0 or force == True:
                war_zone = war_times.get(alliance_settings.get('war_zone'))
                war_start_1, war_start_2, war_start_3 = war_zone.get(
                    'war_start_1'), war_zone.get('war_start_2'), war_zone.get('war_start_3')
                war_energy_1, war_energy_2, war_energy_3, war_energy_4, war_energy_5, war_energy_6 = war_zone.get('war_energy_1'), war_zone.get(
                    'war_energy_2'), war_zone.get('war_energy_3'), war_zone.get('war_energy_4'), war_zone.get('war_energy_5'), war_zone.get('war_energy_6')

                for msg in default_messages:
                    if force == False:
                        message_object = {
                            'message_description': msg.get('message_description'),
                            'message_channel': msg.get('message_channel'),
                            'message_content': msg.get('message_content'),
                            'message_extra': msg.get('message_extra'),
                            'message_settings': msg.get('message_settings'),
                            'alliance_id': alliance_id,
                            'alliance_name': alliance_name
                        }
                    elif force == True:
                        message_object = {
                            'message_channel': msg.get('message_channel'),
                            'alliance_id': alliance_id,
                            'alliance_name': alliance_name
                        }

                    if msg.get("message_id") == 'war_start':
                        for idx, time in enumerate([war_start_1, war_start_2, war_start_3]):
                            idx = idx + 1
                            message_object['message_id'] = f'{alliance_id}:{idx}'
                            message_object['message_channel'] = war_announce_channel
                            message_object['message_mention'] = f'<@&{war_announce_role}>'
                            message_object['message_title'] = f'{msg.get("message_title")} {idx}: {alliance_name}'
                            message_object['message_time'] = time
                            Mongo.update_message(message_object)
                            changed = True

                    elif msg.get("message_id") == 'war_energy':
                        for idx, time in enumerate([war_energy_1, war_energy_2, war_energy_3, war_energy_4, war_energy_5, war_energy_6]):
                            idx = idx + 1
                            message_object['message_id'] = f'{alliance_id}:{idx+10}'
                            message_object['message_channel'] = war_announce_channel
                            message_object['message_mention'] = f'<@&{war_announce_role}>'
                            message_object['message_title'] = f'{msg.get("message_title")} {idx}: {alliance_name}'
                            message_object['message_time'] = time
                            Mongo.update_message(message_object)
                            changed = True

        prt_str = 'Messages Updated'
        if force == True and changed == True:
            print(f'{prt_str} - Forced')
        elif force == False and changed == True:
            print(prt_str)

    async def message_cycle(self):
        # message load section
        import time
        from random import seed, choice
        seed(time.time())

        messages_all = Mongo.find_messages_all()
        for idx, msg in enumerate(messages_all):
            message_content, message_description, message_mention, message_title, message_extra = msg.get(
                'message_content'), msg.get('message_description'), msg.get('message_mention'), msg.get('message_title'), msg.get('message_extra')
            message_id, message_channel, message_time, message_settings = msg.get(
                'message_id'), msg.get('message_channel'), msg.get('message_time'), msg.get('message_settings')
            alliance_id, alliance_name = msg.get(
                'alliance_id'), msg.get('alliance_name')

            is_enabled = message_settings.get('enabled', False)

            if is_enabled == True:

                embed = discord.Embed(
                    title=message_title, type='rich', description=message_description, color=discord.Color.blurple())
                embed.set_footer(text=discord.Embed.Empty,
                                 icon_url=discord.Embed.Empty)

                if message_extra != '':
                    embed.add_field(
                        name=choice(TAGLINES).title(), value=message_extra, inline=True)

                message_time['minute'] = message_time['minute'] - \
                    message_time['offset']
                if message_time['minute'] < 0:
                    message_time['minute'] = message_time['minute'] + 60
                    message_time['hour'] = message_time['hour'] - 1

                job_time = message_time

                await self.message_cron(message_channel, message_mention, message_content, message_time, embed, message_id)

    async def message_cron(self, message_channel, message_mention, message_content, message_time, embed, message_id):
        async def job_function():
            await self.client.get_channel(int(message_channel)).send(content=f'{message_mention} {message_content}', embed=embed)
        await Cron.schedule_cron(self, job_function, message_time, message_id)

    @commands.Cog.listener()
    async def on_ready(self):
        await self.message_init()
        await self.message_cycle()

    @commands.command(hidden=True)
    @commands.is_owner()
    async def upmess(self, ctx):
        force = True
        await self.message_init(force)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def grab(self, ctx, *args):
        obj = await Test.testy(self, ctx)
        player = Mongo.find_player(obj.author_id)
        alliance_id = player.get('alliance_id')
        messages = list(Mongo.find_messages(alliance_id))

        message_embed = discord.Embed(title='Message Configuration')

        for msg in messages:
            message_content, message_description, message_mention, message_title = msg.get(
                'message_content'), msg.get('message_description'), msg.get('message_mention'), msg.get('message_title')
            message_id, message_channel, message_time, message_settings = msg.get(
                'message_id'), msg.get('message_channel'), msg.get('message_time'), msg.get('message_settings')

            msg_str = f'Title: "{message_title}"\nContent: "{message_content}"\n'
            message_embed.add_field(
                name=f'{message_id}', value=msg_str, inline=False)

        await ctx.send(embed=message_embed)
        user_response = await self.client.wait_for('message', check=lambda m: m.author == ctx.author)
        user_input = int(user_response.content)
        msg = messages[user_input-1]

        message_content, message_description, message_mention, message_title = msg.get(
            'message_content'), msg.get('message_description'), msg.get('message_mention'), msg.get('message_title')
        message_id, message_channel, message_time, message_settings = msg.get(
            'message_id'), msg.get('message_channel'), msg.get('message_time'), msg.get('message_settings')

        msg_str = f'Title: "{message_title}"\nContent: "{message_content}"\n'

        response_embed = discord.Embed(title=f'{message_id} Edit')
        response_embed.add_field(
            name=f'{message_id}', value=msg_str, inline=False)

        await ctx.send(embed=response_embed)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def tmess(self, ctx, *args):
        import time
        from random import seed, choice
        seed(time.time())
        taglines = ['pay attention', 'pay close attention', 'take heed', 'listen to me', 'listen', 'heed', 'listen crefully', 'good listener', 'hear', 'lend an ear', 'hearing', 'watch closely', 'heard', 'great listener', 'look', 'turn your attention', 'pays any attention', 'your attention', 'call your attention', 'hear me out', 'watch', 'give your attendance', 'keep an eye on', 'give heed', 'notice', 'you listen well',
                    'direct your attention', 'just pay attention', 'mark my words', 'attention', 'play', 'obey', 'listening', 'watch out', 'give ear to me', 'be careful', 'draw attention', 'draw your attention', 'bring to your attention', 'get an earful', 'draw to your attention', 'please pay attention', 'note', 'paying attention', 'you need to listen to me', 'excellent listener', 'i need to point out', 'they listened', 'just hear', 'just listen']
        obj = await Test.testy(self, ctx)
        player = Mongo.find_player(obj.author_id)
        alliance_id = player.get('alliance_id')
        msg = next((Mongo.find_messages(alliance_id)), None)
        message_content, message_description, message_mention, message_title, message_extra = msg.get(
            'message_content'), msg.get('message_description'), msg.get('message_mention'), msg.get('message_title'), msg.get('message_extra')
        message_id, message_channel, message_time, message_settings = msg.get(
            'message_id'), msg.get('message_channel'), msg.get('message_time'), msg.get('message_settings')
        alliance_id, alliance_name = msg.get(
            'alliance_id'), msg.get('alliance_name')

        if message_extra == '':
            message_extra = 'empty'

        embed = discord.Embed(
            title=message_title, type='rich', description=message_description, color=discord.Color.blurple())
        embed.add_field(
            name=choice(taglines).title(), value=message_extra, inline=True)
        embed.set_footer(text=discord.Embed.Empty,
                         icon_url=discord.Embed.Empty)
        await ctx.send(content=f'{message_mention} {message_content}', embed=embed)


def setup(client):
    client.add_cog(Messages(client))
