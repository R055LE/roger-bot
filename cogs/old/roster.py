# # import discord
# # from discord.ext import commands
# # from utils.portrait import Portrait
# # from utils.fromroster import FromRoster
# # from utils.bufferout import BufferOut
# # from utils.rosterout import RosterOut
# # from utils.builder import Builder
# # import json
# # import math
# # from cogs.mongo import Mongo
# # from pathlib import Path
# # cwd = str(Path(__file__).parents[1])

# # red_star_filter = ['rs', 'red', 'rds', 'reds']
# # yellow_star_filter = ['ys', 'yel', 'star', 'yellow']
# # gear_filter = ['gr', 'gear', 'gt', 'tier', 'gl']
# # level_filter = ['lvl', 'lv', 'level', 'lev']
# # t4_filter = ['t4', 'tier4', 'or', 'ora', 'orange']
# # fav_filter = ['fav', 'favor', 'favorite', 'fa']
# # power_filter = ['pow', 'po', 'pwr', 'power']
# # trait_filter = ['trait', 'tra', 'trt', 'tt']
# # roster_filter = ['roster', 'r', 'ros', 'rost', 'ro']
# # team_filter = ['team', 'tm', 'teams']
# # char_filter = ['char', 'ch', 'cr', 'cha', 'character']
# # limit_filter = ['limit', 'top', 'lmt']
# # iso8_filter = ['i8', 'iso8', 'iso', 'is', 'iso-8']

# with open(f'{cwd}/assets/json/teams.json', 'r') as f:
#     teams = json.load(f)
# with open(f'{cwd}/assets/json/characters.json', 'r') as f:
#     characters = json.load(f).get('Data')

# traits = []
# for c in characters:
#     new_traits = characters.get(c).get('traits', [])
#     for t in new_traits:
#         if t not in traits and t not in ['Civilian', 'Loki', 'Martial Artist', 'Operator', 'Summon', 'Trait', 'Ultron']:
#             traits.append(t)
# traits.sort()

# team_help = """
#             Display A Team of 5 Characters from a Prebuilt List, Trait Assortment or Your MSF.PAL/MSF.GG Page.
#             Prebuilt and Trait Teams Sort By Power, Page Teams Show as Added.

#             Standard for Prebuilt Teams
#             > rgr team as

#             Matching Can Be Used Against Team Names You Have Saved If A Prebuilt Was Not Found.
#             > rgr team u7
#             > rgr team "super bros"

#             With Trait Modifier, Characters Only Have to Match 1 Trait Provided
#             > rgr team trait city
#             > rgr tm tt bio mys

#             """

# tl = '```'
# for t in teams:
#     tl += f'{t.get("TeamId")[0].upper()}{" "*(8-len(t.get("TeamId")[0]))}- {t.get("TeamName")}\n'
# tl += '```'
# team_list = ["Teams Available:", tl]

# trl = f'```{", ".join(traits)}```'
# trait_list = ["Traits Available:", trl]

# cls_list = ['Striker', 'Fortifier', 'Healer', 'Skirmisher', 'Raider', 'None']
# iso_list = ["Classes Available:", f"```{', '.join(cls_list)}```"]


# class Roster(commands.Cog):

#     def __init__(self, client):
#         self.client = client
#         self.fromroster = FromRoster(self)
#         self.portrait = Portrait(self)
#         self.bufferout = BufferOut(self)
#         self.rosterout = RosterOut(self)
#         self.builder = Builder(self)

#     @ commands.group(invoke_without_command=True, aliases=['a', 'al', 'ali', 'alli', 'alliance'], description='Alliance Filter')
#     async def all(self, ctx, *args):
#         """
#         Command Group With The Following Options:

#         **All Char**
#         Returns A Sheet With A Single Character From Each Member of Your Alliance.
#         > rgr all char thor
#            Additional Help Within `rgr help char`

#         **All Team**
#         Returns A Sheet With A Team of 5 Characters From Each Member of Your Alliance.
#         > rgr all team as
#         > rgr a tm tt legend
#            Additional Help Within `rgr help team`
#         """
#         pass

#     @ all.command(name='char', aliases=[f for f in char_filter if f != 'char'])
#     async def _char(self, ctx, *args):
#         import csv
#         async with ctx.message.channel.typing():
#             resp = await ctx.send('Building Report')
#             discord_id = ctx.message.author.id
#             if len(args) > 0:
#                 image_list = []

#                 all_aliases = {}
#                 with open(f'{cwd}/assets/csv/characterAlias.csv', 'r') as f:
#                     reader = csv.DictReader(f)
#                     for row in reader:
#                         try:
#                             id = row['CharacterKey']
#                             row['Aliases'] = [row['Alias'], *row[None]]
#                         except KeyError:
#                             id = row['CharacterKey']
#                             row['Aliases'] = [row['Alias']]
#                         all_aliases[id] = list(
#                             map(lambda a: a.strip(), row['Aliases']))

#                 select = next((c for item in [all_aliases[a]
#                                               for a in all_aliases] for c in item if args[0].casefold() == c.casefold()), None)
#                 if select is None:
#                     select = next((c for item in [all_aliases[a]
#                                                   for a in all_aliases] for c in item if c.casefold().startswith(args[0].casefold())), None)
#                     if select is None:
#                         select = next((c for item in [all_aliases[a]
#                                                       for a in all_aliases] for c in item if args[0].casefold() in c.casefold()), None)
#                         if select is None:
#                             select = next(
#                                 (a for a in all_aliases if args[0].casefold() in a.casefold()), None)
#                             if select is None:
#                                 return await resp.edit(content='This Character Could Not Be Found.')
#                 char_selected = next(
#                     (character for character in all_aliases if select in all_aliases[character]), None)

#                 Alliance_Team = await self.fromroster.get_all(discord_id, team_comp=[char_selected])
#                 await resp.edit(content='Info Obtained')
#                 alliance_name = Alliance_Team.get('AllianceName')
#                 Roster_list = Alliance_Team.get('Roster_List')
#                 for r in Roster_list:
#                     Name = r.get('Name')
#                     Character = r.get('Roster')[0]
#                     output = await self.rosterout.char_out(character=Character)
#                     foreground = await self.builder.foreground_char(image=output, player_name=Name)
#                     image_list.append(foreground)

#                 if len(image_list) > 24:
#                     image_list = image_list[:24]

#                 newim = await self.builder.background_chars(
#                     image_list=image_list, title=f'Alliance Chars', usr=ctx.message.author.display_name, cmd=ctx.message.content, alliance_name=f'{alliance_name} ({"1"}-{len(image_list)})')
#                 newim = await self.builder.add_mode(image=newim)
#                 final_picture = await self.bufferout.build(image=newim, filename=f'{alliance_name} ALL CHAR {char_selected} {"1"}-{len(image_list)}')
#                 await resp.delete()
#                 return await ctx.send(file=final_picture)

#             else:
#                 return await ctx.send('No Character Selected.')

#     @ all.command(name='team', aliases=[f for f in team_filter if f != 'team'])
#     async def _team(self, ctx, *args):
#         if len(args) > 0:
#             async with ctx.message.channel.typing():
#                 resp = await ctx.send('Building Report')
#                 with open(f'{cwd}/assets/json/teams.json', 'r') as f:
#                     teams = json.load(f)

#                 discord_id = ctx.message.author.id

#                 if args[0].casefold() in ['trait', 'trt', 'tt']:
#                     args = list(args[1:])
#                     Alliance = await self.fromroster.get_alliance(discord_id)
#                     Name, Players = Alliance.get(
#                         'Name'), Alliance.get('Players')
#                     image_list, sort_list = [], []
#                     for player in Players:
#                         Player = Players.get(player)
#                         PlayerName = Player.get('Name')
#                         Roster = Player.get('Roster')

#                         call_list, trait_list = await self.trait_or(args, call_list=Roster)

#                         call_list = sorted(call_list, key=lambda c: c.get(
#                             'Power'), reverse=True)

#                         list_size = 5 if len(
#                             call_list) >= 5 else len(call_list)
#                         team_out = call_list[:list_size]
#                         TeamOut = {}
#                         TeamOut['team_out'] = team_out
#                         TeamOut['PlayerName'] = PlayerName
#                         sort_list.append(TeamOut)
#                     sort_list = sorted(sort_list, key=lambda s: sum(
#                         c.get('Power') for c in s.get('team_out')), reverse=True)
#                     for to in sort_list:
#                         team_out, PlayerName = to.get(
#                             'team_out'), to.get('PlayerName')
#                         output = await self.rosterout._roster_out(call_list=team_out)
#                         foreground = await self.builder.foreground(image=output, total_power=f'{sum(c.get("Power") for c in team_out):,}', player_name=PlayerName)
#                         image_list.append(foreground)

#                     if len(image_list) > 24:
#                         image_list = image_list[:24]

#                     newim = await self.builder.background_teams(
#                         image_list=image_list, title=f'TRAIT TEAM', usr=ctx.message.author.display_name, cmd=ctx.message.content, alliance_name=f'{Name} ({"1"}-{len(image_list)})', descr=trait_list)
#                     newim = await self.builder.add_mode(image=newim)
#                     final_picture = await self.bufferout.build(image=newim, filename=f'{Name} ALL TEAM "team_name" {"1"}-{len(image_list)}')
#                     await resp.delete()
#                     return await ctx.send(file=final_picture)
#                 else:
#                     Player = await self.fromroster.get(discord_id=discord_id)
#                     Teams = Player.get('Teams')
#                     team_id = next(
#                         (TeamId for team in teams for TeamId in team.get('TeamId') if TeamId.casefold().startswith(args[0].casefold())), None)
#                     if team_id is None:
#                         team_id = next(
#                             (TeamId for team in teams for TeamId in team.get('TeamId') if args[0].casefold() in TeamId.casefold()), None)
#                         if team_id is None:
#                             team_id = next(
#                                 (team.get('TeamName') for team in Teams if team.get('TeamName').casefold().startswith(args[0].casefold())), None)
#                             if team_id is None:
#                                 return await ctx.send('Team not Found.')
#                     t = next(
#                         (team for team in teams if team_id in team.get('TeamId')), None)
#                     if t is None:
#                         t = next(
#                             (team for team in Teams if team_id.casefold() in team.get('TeamName').casefold()), None)
#                         team_comp = t.get('Team')
#                         Alliance_Team = await self.fromroster.get_all(discord_id, team_comp=team_comp, ordered=True)
#                         if t is None:
#                             return await ctx.send('Internal Team Error.')
#                     else:
#                         team_comp = t.get('Team')
#                         Alliance_Team = await self.fromroster.get_all(discord_id, team_comp=team_comp)

#                     image_list = []
#                     await resp.edit(content='Info Obtained')
#                     alliance_name = Alliance_Team.get('AllianceName')
#                     Roster_list = Alliance_Team.get('Roster_List')
#                     for r in Roster_list:
#                         Name = r.get('Name')
#                         Roster = r.get('Roster')
#                         output = await self.rosterout._roster_out(call_list=Roster)
#                         foreground = await self.builder.foreground(image=output, total_power=f'{sum(c.get("Power") for c in Roster):,}', player_name=Name)
#                         image_list.append(foreground)

#                     if len(image_list) > 24:
#                         image_list = image_list[:24]

#                     newim = await self.builder.background_teams(
#                         image_list=image_list, title=f'{t.get("TeamName").upper()}', usr=ctx.message.author.display_name, cmd=ctx.message.content, alliance_name=f'{alliance_name} ({"1"}-{len(image_list)})')
#                     newim = await self.builder.add_mode(image=newim)
#                     final_picture = await self.bufferout.build(image=newim, filename=f'{alliance_name} ALL TEAM {t.get("TeamName")} {"1"}-{len(image_list)}')
#                     await resp.delete()
#                     return await ctx.send(file=final_picture)

#         else:
#             return await ctx.send('No Team Selected.')

#     @ commands.command(aliases=[f for f in char_filter if f != 'char'], description='Character Filter')
#     async def char(self, ctx, *args):
#         """
#         Returns a Single Character Based on Name.
#         If Multiple Characters Qualify The First Match Is Returned.

#         Matching Against Name, ID and Common Aliases
#         > rgr char thor
#         > rgr char mbaku
#         > rgr char ssm
#         """
#         if len(args) > 0:
#             discord_id = ctx.message.author.id
#             discord_id, arg = await self.change_id(ctx, args, discord_id)
#             async with ctx.message.channel.typing():
#                 Player = await self.fromroster.get(discord_id=discord_id)
#                 player_roster, Name, Alliance = Player.get(
#                     'Roster'), Player.get('Name'), Player.get('Alliance')
#                 call_list = player_roster

#                 # This Needs Reworked, Based on All Char. No Reason To Attach Aliases to Roster
#                 als = next((c for character in call_list for c in character.get(
#                     'Aliases') if args[0].casefold() == c.casefold()), None)
#                 if als is None:
#                     als = next((c for character in call_list for c in character.get(
#                         'Aliases') if c.casefold().startswith(args[0].casefold())), None)
#                     if als is None:
#                         als = next((c for character in call_list for c in character.get(
#                             'Aliases') if args[0].casefold() in c.casefold()), None)
#                         if als is None:
#                             als = next((c for character in call_list for c in character.get(
#                                 'Name') if args[0].casefold() in c.casefold()), None)
#                             if als is None:
#                                 # await resp.edit(content='This Character Could Not Be Found.')
#                                 return
#                 char_called = next(
#                     (character for character in call_list if als in character.get('Aliases')), None)
#                 if char_called is None:
#                     char_called = next(
#                         (character for character in call_list if args[0].casefold() in character.get('Name')), None)
#                     if char_called is None:
#                         char_called = next(
#                             (character for character in call_list if args[0] in character.get('HeroId')), None)

#                 output = await self.rosterout.char_out(character=char_called)
#                 foreground = await self.builder.foreground_char(image=output, player_name=Name)
#                 newim = await self.builder.background_char_single(
#                     image=foreground, title='Char', usr=ctx.message.author.display_name, cmd=ctx.message.content, alliance_name=Alliance)
#                 newim = await self.builder.add_mode(image=newim)
#                 final_picture = await self.bufferout.build(image=newim, filename='filename')
#                 await ctx.send(file=final_picture)

#         else:
#             return await ctx.send('No Character Selected.')

#     @ commands.command(aliases=[f for f in team_filter if f != 'team'], help=team_help, description='Team Filter', brief=[team_list, trait_list])
#     async def team(self, ctx, *args):
#         if len(args) > 0:
#             async with ctx.message.channel.typing():
#                 with open(f'{cwd}/assets/json/teams.json', 'r') as f:
#                     teams = json.load(f)

#                 prefix, *_ = await self.client.get_prefix(ctx)
#                 discord_id = ctx.message.author.id
#                 discord_id, arg = await self.change_id(ctx, args, discord_id)

#                 Player = await self.fromroster.get(discord_id=discord_id)
#                 Name, Teams = Player.get('Name'), Player.get('Teams')
#                 player_roster = Player.get('Roster')
#                 call_list = player_roster

#                 if args[0].casefold() in ['trait', 'trt', 'tt']:
#                     args = list(args[1:])
#                     if arg is not None:
#                         args.remove(arg)

#                     call_list, trait_list = await self.trait_or(args, call_list=call_list)

#                     call_list = sorted(call_list, key=lambda c: c.get(
#                         'Power'), reverse=True)

#                     list_size = 5 if len(
#                         call_list) >= 5 else len(call_list)
#                     team_out = call_list[:list_size]
#                     return await self.output(ctx, team_out=team_out, title='TRAIT TEAM', descr=f'{trait_list}', Player=Player)
#                 else:
#                     team_id = next(
#                         (TeamId for team in teams for TeamId in team.get('TeamId') if TeamId.casefold().startswith(args[0].casefold())), None)
#                     if team_id is None:
#                         team_id = next(
#                             (TeamId for team in teams for TeamId in team.get('TeamId') if args[0].casefold() in TeamId.casefold()), None)
#                         if team_id is None:
#                             team_id = next(
#                                 (team.get('TeamName') for team in Teams if team.get('TeamName').casefold().startswith(args[0].casefold())), None)
#                             if team_id is None:
#                                 return await ctx.send('Team not Found.')

#                     t = next(
#                         (team for team in teams if team_id.casefold() in team.get('TeamId')), None)
#                     if t is None:
#                         t = next(
#                             (team for team in Teams if team_id.casefold() in team.get('TeamName').casefold()), None)
#                         team_out = []
#                         for c in t.get('Team'):
#                             team_out.append(next(
#                                 (character for character in call_list if character.get('HeroId') == c), None))
#                         if t is None:
#                             return await ctx.send('Internal Team Error.')
#                     else:
#                         team_out = list(
#                             character for character in call_list if character.get('HeroId') in t.get('Team'))

#                     return await self.output(ctx, team_out=team_out, title=f'{t.get("TeamName").upper()}', Player=Player, filename=f'{Name} TEAM {t.get("TeamName")}')
#         else:
#             return await ctx.send('No Team Selected.')

#     # @ commands.command(aliases=[f for f in roster_filter if f != 'roster'], description='Whole Roster')
#     # async def roster(self, ctx, *args):
#     #     """
#     #     Bring Up The Whole Roster, Top Selection or a Specific Range.

#     #     Whole Roster
#     #         > rgr roster
#     #     Top Section
#     #         > rgr roster 10
#     #     Within Range
#     #         > rgr roster 119 140
#     #     """
#     #     args = list(args)
#     #     args.insert(0, 'roster')
#     #     async with ctx.message.channel.typing():
#     #         return await self.roster_parse(ctx, args)

#     # @ commands.command(aliases=[f for f in red_star_filter if f != 'rs'], description='Red Star Filter')
#     # async def rs(self, ctx, *args):
#     #     """
#     #     Filter Roster by a number of Red Stars, or within a range.

#     #     One argument for a single parameter.
#     #         > rgr rs 7
#     #     Two arguments for a range.
#     #         > rgr rs 1 3
#     #     Can be combined with other roster filters.
#     #         > rgr rs 5 lvl 71 75
#     #     """
#     #     if len(args) > 0:
#     #         args = list(args)
#     #         args.insert(0, 'rs')
#     #         async with ctx.message.channel.typing():
#     #             return await self.roster_parse(ctx, args)
#     #     else:
#     #         return await ctx.send('No Arguments Given.')

#     # @ commands.command(aliases=[f for f in yellow_star_filter if f != 'ys'], description='Star Filter')
#     # async def ys(self, ctx, *args):
#     #     """
#     #     Filter Roster by a number of Stars, or within a range.

#     #     One argument for a single parameter.
#     #         > rgr ys 5
#     #     Two arguments for a range.
#     #         > rgr ys 4 6
#     #     Can be combined with other roster filters.
#     #         > rgr ys 5 gr 12 14
#     #     """
#     #     if len(args) > 0:
#     #         args = list(args)
#     #         args.insert(0, 'ys')
#     #         async with ctx.message.channel.typing():
#     #             return await self.roster_parse(ctx, args)
#     #     else:
#     #         return await ctx.send('No Arguments Given.')

#     # @ commands.command(aliases=[f for f in gear_filter if f != 'gr'], description='Gear Filter')
#     # async def gr(self, ctx, *args):
#     #     """
#     #     Filter Roster by Gear Tier, or within a range.

#     #     One argument for a single parameter.
#     #         > rgr gr 14
#     #     Two arguments for a range.
#     #         > rgr gr 12 14
#     #     Can be combined with other roster filters.
#     #         > rgr gr 11 13 power 100
#     #     """
#     #     if len(args) > 0:
#     #         args = list(args)
#     #         args.insert(0, 'gr')
#     #         async with ctx.message.channel.typing():
#     #             return await self.roster_parse(ctx, args)
#     #     else:
#     #         return await ctx.send('No Arguments Given.')

#     # @ commands.command(aliases=[f for f in level_filter if f != 'lvl'], description='Level Filter')
#     # async def lvl(self, ctx, *args):
#     #     """
#     #     Filter Roster by character Level, or within a range.

#     #     One argument for a single parameter.
#     #         > rgr lvl 70
#     #     Two arguments for a range.
#     #         > rgr lvl 71 75
#     #     Can be combined with other roster filters.
#     #         > rgr lvl 60 rs 5
#     #     """
#     #     if len(args) > 0:
#     #         args = list(args)
#     #         args.insert(0, 'lvl')
#     #         async with ctx.message.channel.typing():
#     #             return await self.roster_parse(ctx, args)
#     #     else:
#     #         return await ctx.send('No Arguments Given.')

#     # @ commands.command(aliases=[f for f in t4_filter if f != 't4'], description='T4 Equipped')
#     # async def t4(self, ctx, *args):
#     #     """
#     #     Filter Roster by T4 Abilities, T4 Maxed or T4 None.

#     #     Any T4
#     #         > rgr t4
#     #     All T4
#     #         > rgr t4 all
#     #     T4 None
#     #         > rgr t4 none
#     #     Can be combined with other roster filters.
#     #         > rgr t4 all gr 14
#     #     """
#     #     args = list(args)
#     #     args.insert(0, 't4')
#     #     async with ctx.message.channel.typing():
#     #         return await self.roster_parse(ctx, args)

#     # @ commands.command(aliases=[f for f in fav_filter if f != 'fav'], description='Favorites Filter')
#     # async def fav(self, ctx, *args):
#     #     args = list(args)
#     #     args.insert(0, 'fav')
#     #     async with ctx.message.channel.typing():
#     #         return await self.roster_parse(ctx, args)

#     # @ commands.command(aliases=[f for f in power_filter if f != 'power'], description='Power Filter')
#     # async def power(self, ctx, *args):
#     #     """
#     #     Filter Roster by character Power, or within a range. In increments of 1000.

#     #     For Power At or Exceeding a Certain Level
#     #         > rgr power 100
#     #     For Power In a Certain Range
#     #         > rgr power 100 130
#     #     Can be combined with other roster filters.
#     #         > rgr power 100 ys 7
#     #     """
#     #     if len(args) > 0:
#     #         args = list(args)
#     #         args.insert(0, 'power')
#     #         async with ctx.message.channel.typing():
#     #             return await self.roster_parse(ctx, args)
#     #     else:
#     #         return await ctx.send('No Arguments Given.')

#     # @ commands.command(aliases=[f for f in trait_filter if f != 'trait'], description='Traits Filter', brief=[trait_list])
#     # async def trait(self, ctx, *args):
#     #     """
#     #     Filter Roster by character Traits, up to 3 at a time.
#     #     Result set will include characters with at least one of the traits provided.
#     #     Matching is applied to arguments to find closest value.

#     #     Single Trait
#     #         > rgr trait sym
#     #     List of Characters with Any of the Following
#     #         > rgr trait bio mystic
#     #     List of Characters with ALL of the Following
#     #         > rgr trait mys vil cont &
#     #     """
#     #     if len(args) > 0:
#     #         args = list(args)
#     #         args.insert(0, 'trait')
#     #         async with ctx.message.channel.typing():
#     #             return await self.roster_parse(ctx, args)
#     #     else:
#     #         return await ctx.send('No Arguments Given.')

#     # @ commands.command(aliases=[f for f in iso8_filter if f != 'iso8'], description='ISO-8 Class Filter', brief=[iso_list])
#     # async def iso8(self, ctx, *args):
#     #     """
#     #     Filter Roster by ISO-8 Class, up to 3 at a time.
#     #     Result set will include characters with at least one of the classes provided.
#     #     Matching is applied to arguments to find closest value.

#     #     Single Class
#     #         > rgr iso strike
#     #     List of Characters with Any of the Following
#     #         > rgr iso fort skirm
#     #     """
#     #     if len(args) > 0:
#     #         args = list(args)
#     #         args.insert(0, 'iso8')
#     #         async with ctx.message.channel.typing():
#     #             return await self.roster_parse(ctx, args)
#     #     else:
#     #         return await ctx.send('No Arguments Given.')

#     # async def roster_parse(self, ctx, args):
#     #     prefix, *_ = await self.client.get_prefix(ctx)
#     #     discord_id = ctx.message.author.id
#     #     discord_id, arg = await self.change_id(ctx, args, discord_id)
#     #     if arg is not None:
#     #         args.remove(arg)
#     #     Player = await self.fromroster.get(discord_id=discord_id)

#     #     player_roster = Player.get('Roster')
#     #     Name = Player.get('Name')
#     #     number_filters = [red_star_filter, yellow_star_filter,
#     #                       gear_filter, level_filter]
#     #     filters = [roster_filter, t4_filter, trait_filter, fav_filter, power_filter,
#     #                trait_filter, *number_filters, limit_filter, iso8_filter]
#     #     all_filter_gen = list(item for f in filters for item in f)
#     #     num_filter_gen = list(item for f in number_filters for item in f)
#     #     list_of_args = []
#     #     title, descr, filename = '', '', ''

#     #     for i, arg in enumerate(args):
#     #         if arg.casefold() in all_filter_gen:
#     #             sublist = [arg]
#     #             while i+1 < len(args):
#     #                 if args[i+1].casefold() not in all_filter_gen:
#     #                     sublist.append(args[i+1])
#     #                 else:
#     #                     break
#     #                 i = i+1
#     #             list_of_args.append(sublist)
#     #     call_list = player_roster
#     #     compare = args[0].casefold()

#     #     for lst in list_of_args:
#     #         if lst[0].casefold() in roster_filter:
#     #             if len(lst) == 2:
#     #                 roster1 = lst[1]
#     #             elif len(lst) == 3:
#     #                 roster1, roster2 = lst[1], lst[2]
#     #         cmd = lst.pop(0)
#     #         cmd = cmd.casefold()
#         # # Numbered Filters - Red Stars, Yellow Stars, Gear Tier, Levels
#         #     if cmd in num_filter_gen:
#         #         try:
#         #             searcher = ('RedStar' if cmd in red_star_filter
#         #                         else 'GearLevel' if cmd in gear_filter
#         #                         else 'Level' if cmd in level_filter
#         #                         else 'Loyalty' if cmd in yellow_star_filter
#         #                         else None)

#         #             if searcher == None:
#         #                 return await ctx.send('Filter not found.')
#         #             if len(lst) == 1:
#         #                 call_list = list(
#         #                     character for character in call_list if character.get(searcher) == int(lst[0]))
#         #                 if compare in red_star_filter:
#         #                     filename = f'{Name} Red Stars {args[1]}'
#         #                     title = f'{args[1]} Red Stars ({len(call_list)})'
#         #                 elif compare in yellow_star_filter:
#         #                     filename = f'{Name} Stars {args[1]}'
#         #                     title = f'{args[1]} Stars ({len(call_list)})'
#         #                 elif compare in gear_filter:
#         #                     filename = f'{Name} Gear Tier {args[1]}'
#         #                     title = f'Gear Tier {args[1]} ({len(call_list)})'
#         #                 elif compare in level_filter:
#         #                     filename = f'{Name} Level {args[1]}'
#         #                     title = f'Level {args[1]} ({len(call_list)})'

#         #             elif len(lst) == 2:
#         #                 call_list = list(character for character in call_list if character.get(
#         #                     searcher) in range(int(lst[0]), int(lst[1])+1))
#         #                 if compare in red_star_filter:
#         #                     filename = f'{Name} Red Stars {args[1]}-{args[2]}'
#         #                     title = f'{args[1]}-{args[2]} Red Stars ({len(call_list)})'
#         #                 elif compare in yellow_star_filter:
#         #                     filename = f'{Name} Stars {args[1]}-{args[2]}'
#         #                     title = f'{args[1]}-{args[2]} Stars ({len(call_list)})'
#         #                 elif compare in gear_filter:
#         #                     filename = f'{Name} Gear Tier {args[1]}-{args[2]}'
#         #                     title = f'Gear Tier {args[1]}-{args[2]} ({len(call_list)})'
#         #                 elif compare in level_filter:
#         #                     filename = f'{Name} Level {args[1]}-{args[2]}'
#         #                     title = f'Level {args[1]}-{args[2]} ({len(call_list)})'
#         #             call_list = sorted(call_list, key=lambda c: c.get(
#         #                 searcher), reverse=True)
#         #         except ValueError:
#         #             return await ctx.send(f'`{lst}` is an invalid argument set for `{cmd}`.')
#         # # Whole Roster
#         #     # Bug - Roster must be first sub-command or it won't affect the call_list
#         #     elif cmd in roster_filter:
#         #         if len(lst) == 1:
#         #             call_list = list(
#         #                 character for character in call_list[:int(lst[0])])
#         #             if compare:
#         #                 filename = f'{Name} Roster {roster1}'
#         #                 title = f'Roster Top {roster1}'
#         #         elif len(lst) == 2:
#         #             call_list = list(
#         #                 character for character in call_list[int(lst[0])-1:int(lst[1])])
#         #             if compare:
#         #                 filename = f'{Name} Roster {roster1}-{roster2}'
#         #                 title = f'Roster {roster1}-{roster2}'
#         #         elif len(lst) == 0:
#         #             call_list = list(character for character in call_list)
#         #             if compare:
#         #                 filename = f'{Name} All Characters'
#         #                 title = f'All Characters ({len(call_list)})'
#         # # Favorites
#             # elif cmd in fav_filter:
#             #     call_list = list(
#             #         character for character in call_list if character.get('Favorite') == 0)
#             #     if compare in fav_filter:
#             #         filename = f'{Name} Favorites'
#             #         title = f'Favorites ({len(call_list)})'
#         # # Power
#         #     elif cmd in power_filter:
#         #         if len(lst) == 1:
#         #             call_list = list(
#         #                 character for character in call_list if character.get('Power') >= int(lst[0])*1000)
#         #             if compare in power_filter:
#         #                 descr = 'Power'
#         #                 filename = f'{Name} Power {lst[0]}K'
#         #                 title = f'{lst[0]}K+ ({len(call_list)})'
#         #         elif len(lst) == 2:
#         #             call_list = list(character for character in call_list if character.get(
#         #                 'Power') in range(int(lst[0])*1000, int(lst[1]*1000)+1))
#         #             if compare in power_filter:
#         #                 descr = 'Power'
#         #                 filename = f'{Name} Power {lst[0]}K-{lst[1]}K'
#         #                 title = f'{lst[0]}K-{lst[1]}K ({len(call_list)})'
#         # Traits - Default is OR
#             # elif cmd in trait_filter:
#             # lst = sorted(lst)
#             # # Characters Must Have ALL Traits Listed
#             # if any(l.casefold() in ['and', '&'] for l in lst):
#             #     lst = [f for f in lst if f.casefold() not in ['and', '&']]
#             #     for l in lst:
#             #         call_list = list(
#             #             character for character in call_list if any(c for c in character.get('Traits') if c.casefold().startswith(l.casefold()) or l.casefold() in c.casefold()))
#             #     if compare in trait_filter:
#             #         descr = 'w/ All Traits'
#             #         filename = f'{Name} Traits(ALL) {"_".join(lst)}'
#             #         title = f'Traits ({len(call_list)})'
#             # else:
#             #     # Characters Can Have ANY of the Traits Listed
#             #     call_list, descr = await self.trait_or(lst, call_list=call_list)
#             #     call_list = sorted(call_list, key=lambda c: c.get(
#             #         'Power'), reverse=True)
#             #     if compare in trait_filter:
#             #         filename = f'{Name} Traits {descr}'
#             #         title = f'Traits ({len(call_list)})'
#         # # ISO-8
#         #     elif cmd in iso8_filter:
#         #         call_list, descr = await self.iso8_or(lst, call_list=call_list)
#         #         if compare in iso8_filter:
#         #             filename = f'{Name} ISO-8 {descr}'
#         #             title = f'ISO-8 ({len(call_list)})'
#         # # T4
#         #     elif cmd in t4_filter:
#         #         if any(l.casefold() in ['max', 'all', '*'] for l in lst):
#         #             call_list = list(
#         #                 character for character in call_list if (character.get('Basic') >= 7 and character.get('Special') >= 7 and character.get('Ultimate') >= 7 and character.get('Passive') >= 5)
#         #                 or (character.get('Basic') >= 7 and character.get('Special') >= 7 and character.get('Passive') >= 5 and 'Minion' in character.get('Traits')))
#         #             if compare in t4_filter:
#         #                 filename = f'{Name} T4 All'
#         #                 title = f'T4 All ({len(call_list)})'
#         #         elif any(l.casefold() in ['none', 'no', '-', 'n'] for l in lst):
#         #             call_list = list(
#         #                 character for character in call_list if (character.get('Basic') < 7 and character.get('Special') < 7 and character.get('Ultimate') < 7 and character.get('Passive') < 5))
#         #             if compare in t4_filter:
#         #                 filename = f'{Name} T4 None'
#         #                 title = f'T4 None ({len(call_list)})'
#         #         else:
#         #             call_list = list(
#         #                 character for character in call_list if character.get('Basic') >= 7 or character.get('Special') >= 7 or character.get('Ultimate') >= 7 or character.get('Passive') >= 5)
#         #             if compare in t4_filter:
#         #                 filename = f'{Name} T4'
#         #                 title = f'T4 Abilities ({len(call_list)})'
#         # Limit Results
#             # elif cmd in limit_filter:
#             #     call_list = call_list[:int(lst[0])]

#         # if len(call_list) == 0:
#         #     return await ctx.send(f'No Results Found.')

#         team_out = call_list
#         await self.output(ctx, team_out=team_out, title=f'{title.upper()}', filename=f'{filename}', descr=descr, Player=Player)

#     async def change_id(self, ctx, args, discord_id):
#         AllianceCheck = await self.fromroster.get_alliance_check(discord_id=discord_id)
#         not_me = next((a for a in args if any(U.get('DisplayName').casefold().startswith(
#             a.casefold()) for U in AllianceCheck) and a is not args[0]), None)
#         if not_me is None:
#             return discord_id, None
#         else:
#             arg_rtn = not_me
#             not_me = not_me.casefold()
#             discord_id = next((User.get('MemberId') for User in AllianceCheck if User.get(
#                 'DisplayName').casefold().startswith(not_me)), None)
#             if discord_id is None:
#                 return await ctx.send('Internal Discord ID Error.')
#             return discord_id, arg_rtn

#     # async def trait_or(self, args, *, call_list):
#     #     filter_list = ''
#     #     super_list = []
#     #     hard_limit = 1
#     #     for arg in args:
#     #         if hard_limit > 3:
#     #             break
#     #         fltr = next((
#     #             c for character in call_list for c in character.get('Traits') if c.casefold().startswith(arg.casefold()) or arg.casefold() in c.casefold()), None)
#     #         filter_list = fltr if filter_list == '' else f'{filter_list}, {fltr}'
#     #         sub_list = list(
#     #             character for character in call_list if
#     #             fltr in character.get(
#     #                 'Traits')
#     #             and character not in super_list)
#     #         super_list.extend(sub_list)
#     #         hard_limit += 1
#     #     call_list = super_list
#     #     return call_list, filter_list

#     # async def iso8_or(self, args, *, call_list):
#     #     filter_list = ''
#     #     super_list = []
#     #     hard_limit = 1
#     #     for arg in args:
#     #         if hard_limit > 3:
#     #             break
#     #         fltr = next((
#     #             clss for clss in cls_list if clss.casefold() == arg.casefold()), None)
#     #         if fltr is None:
#     #             fltr = next((
#     #                 clss for clss in cls_list if clss.casefold().startswith(arg.casefold())), None)
#     #             if fltr is None:
#     #                 fltr = next((
#     #                     clss for clss in cls_list if arg.casefold() in clss.casefold()), None)
#     #         filter_list = fltr if filter_list == '' else f'{filter_list}, {fltr}'
#     #         sub_list = list(
#     #             character for character in call_list if
#     #             fltr == character.get(
#     #                 'IsoSkillId')
#     #             and character not in super_list)
#     #         super_list.extend(sub_list)
#     #         hard_limit += 1
#     #     call_list = super_list
#     #     return call_list, filter_list

#     # async def output(self, ctx, *, team_out, title, descr=None, Player, filename='default'):
#     #     Name, Alliance, Level, PID = Player.get('Name'), Player.get(
#     #         'Alliance'), Player.get('Level'), Player.get('PID')
#     #     output = await self.rosterout._roster_out(call_list=team_out)
#     #     foreground = await self.builder.foreground(image=output, total_power=f'{sum(c.get("Power") for c in team_out):,}', player_name=Name)
#     #     newim = await self.builder.background_team_single(
#     #         image=foreground, title=title, usr=ctx.message.author.display_name, cmd=ctx.message.content, alliance_name=Alliance, descr=descr)
#     #     newim = await self.builder.add_mode(image=newim)
#     #     final_picture = await self.bufferout.build(image=newim, filename=filename)
#     #     await ctx.send(file=final_picture)


# def setup(client):
#     client.add_cog(Roster(client))
