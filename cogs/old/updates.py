# from cogs.cron import Cron
# import discord
# from discord.ext import commands
# import pymongo
# import requests
# import json
# from cogs.mongo import Mongo
# import os

# cwd = os.getcwd()
# with open(f'{cwd}/assets/json/raid_selection.json', 'r') as f:
#     raid_selection = json.load(f)


# class Updates(commands.Cog):

#     def __init__(self, client):
#         self.client = client

#     # Alliance Updates

#     async def update_alli_all(self):
#         alliance_all = Mongo.find_alliance_all()
#         for alliance in alliance_all:
#             alliance_id = alliance.get('alliance_id')
#             api_key_ro = alliance.get('api_key_ro')
#             uri = f'https://msf.pal.gg/rest/v1/alliance/{alliance_id}?api-key={api_key_ro}'
#             response = json.loads(requests.get(
#                 uri).content)
#             alliance_id, alliance_name, alliance_players = response.get(
#                 'id'), response.get('name'), response.get('players')
#             alliance_raids = response.get('raids')
#             # alliance_war = response.get('war')

#             alliance_object = {
#                 'alliance_id': response['id'],
#                 'alliance_name': response['name'],
#                 'alliance_url': response['url']
#             }
#             Mongo.update_alliance(alliance_object)

#             current_players = []

#             for player in alliance_players:
#                 player_object = {
#                     'player_id': player['id'],
#                     'player_name': player['name'],
#                     'player_discord_id': int(player.get('userId', 987654321098765432)),
#                     'player_avatar': player.get('avatar', 'default'),
#                     'player_level': player.get('level') or 0,
#                     'player_characters': player['characters'],
#                     'player_teams': player.get('teams') or [],
#                     'alliance_id': alliance_id,
#                     'alliance_name': alliance_name,
#                 }
#                 current_players.append(player_object.get('player_id'))
#                 Mongo.update_player(player_object)
#             saved_players = Mongo.find_players_all(alliance_id)
#             for sp in saved_players:
#                 if sp.get('player_id') not in current_players:
#                     deleted_player = Mongo.delete_player(sp.get('player_id'))
#                     print(
#                         f'{deleted_player} from {alliance_name}: {sp.get("player_name")}')

#             for raid in alliance_raids:
#                 strike_team_1, strike_team_2, strike_team_3 = [], [], []
#                 selection = next((
#                     filter(lambda rs: rs['raid_name'] == raid['id'] or rs.get('raid_name_alt', None) == raid['id'], raid_selection)), None)
#                 for group in raid['groups']:
#                     group_id, group_lines = group['id'], group['lines']
#                     for idx, line in enumerate(group_lines):
#                         player = next((filter(lambda player: player['id'] == line, alliance_players)), {
#                                       'id': None, 'name': ''})
#                         line_player_name = player.get('name')
#                         if player.get('id') == None:
#                             line = ''

#                         if group_id == 1:
#                             strike_team_1.append(
#                                 {'id': line, 'player': line_player_name, 'lane': idx+1})
#                         elif group_id == 2:
#                             strike_team_2.append(
#                                 {'id': line, 'player': line_player_name, 'lane': idx+1})
#                         elif group_id == 3:
#                             strike_team_3.append(
#                                 {'id': line, 'player': line_player_name, 'lane': idx+1})

#                 raid_object = {
#                     'raid_name': selection['raid_name'],
#                     'strike_team_1': strike_team_1,
#                     'strike_team_2': strike_team_2,
#                     'strike_team_3': strike_team_3,
#                     'raid_url': f'https://msf.pal.gg/{alliance_id}/raids/{selection["raid_url"]}',
#                     'raid_thumbnail': selection['raid_thumbnail'],
#                     'raid_id': selection['raid_id'],
#                     'raid_id_alts': selection['raid_id_alts'],
#                     'alliance_id': alliance_id,
#                     'alliance_name': alliance_name,
#                     'diff_slider': selection['diff_slider']
#                 }
#                 Mongo.update_raid(raid_object)
#         print('All Alliance Info Update Complete')

#     @commands.Cog.listener('on_ready')
#     # alias possibly required or some other initializer
#     async def uai_ready(self):
#         async def job_function():
#             await self.update_alli_all()
#         job_time = {
#             'hour': '*', 'minute': '0', 'second': '0'
#         }
#         await Cron.schedule_cron(self, job_function, job_time)

#     @commands.command(hidden=True)
#     @commands.is_owner()
#     async def upalli(self, ctx):
#         await self.update_alli_all()

#     # Character Updates

#     async def update_char_all(self):
#         response = json.loads(requests.get(
#             'https://msf.pal.gg/rest/v1/characters').content)
#         for character in response:
#             character_object = {
#                 'character_id': character.get('id'),
#                 'character_name': character.get('msf.gg.name'),
#                 'character_game_id': character.get('msf.gg.id'),
#                 'character_traits': character.get('traits'),
#                 'character_speed': character.get('speed'),
#             }
#             Mongo.update_character(character_object)
#         print('All Character Info Update Complete')

#     @commands.Cog.listener('on_ready')
#     async def uci_ready(self):
#         async def job_function():
#             await self.update_char_all()
#         job_time = {
#             'hour': '10', 'minute': '0', 'second': '0'
#         }
#         await Cron.schedule_cron(self, job_function, job_time)

#     @commands.command(hidden=True)
#     @commands.is_owner()
#     async def upchar(self, ctx):
#         await self.update_char_all()


# def setup(client):
#     client.add_cog(Updates(client))
