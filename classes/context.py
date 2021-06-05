import discord
import discord.ext.commands as commands
from discord.ext.commands import Cog, Command
from classes.alliance import Alliance
from classes.player import Player
from settings import Category
from utils.graphic import Graphic


class Context(commands.Context):
    def __init__(self: commands.Context, **attrs):
        super().__init__(**attrs)
        self.client: commands.Bot = self.bot
        self.message: discord.Message
        self.pod: Pod = Pod(self)
        self.graphic = Graphic()


class Pod:
    def __init__(self, ctx: Context):
        self.ctx: Context = ctx
        self.alliance: Alliance = None
        self.player: Player = None
        self.description: list = []
        self.title: str = None
        self.iteration_count: int = 0

    async def get_player(self):
        """Returns Invoking User by Default"""
        if self.player is None:
            self.player = Player(self.ctx.message.author.id)

    async def get_alliance(self):
        """Returns Invoking User's Alliance"""
        self.alliance = Alliance(self.ctx.message.author.id)

    async def roster_out(self, title: str, description: str, *, pad=False, single=False):
        """Sends Roster Data to Graphic Builder"""
        if self.title is None:
            self.title = title

        if self.iteration_count <= 3 and not single:
            self.iteration_count = self.iteration_count + 1

            if self.iteration_count > 1 or pad:
                self.description.append(description)

            if self.iteration_count == 1:
                self.ctx.args = self.ctx.args[2:]

            for cog_name in self.ctx.client.cogs:
                cog: Cog = self.ctx.client.get_cog(cog_name)

                if cog.category == Category.roster:
                    for cmd in cog.get_commands():
                        cmd: Command
                        name: str = cmd.name
                        aliases: list = [alias.casefold()
                                         for alias in cmd.aliases]

                        for i, a in enumerate(self.ctx.args):
                            a: str
                            i: int
                            if a.casefold() == name.casefold() or a.casefold() in aliases:
                                self.ctx.args = self.ctx.args[i+1:]
                                return await self.ctx.client.get_command(name)(self.ctx, *self.ctx.args, sub=a)

        if len(self.player.roster) == 0:
            return await self.ctx.send(f'No Results Found.')

        self.title += f' ({len(self.player.roster)})'
        self.description = ', '.join(self.description)

        return await self.ctx.graphic.roster(self)

    async def team_out(self, title: str, description: str = None):
        """Sends Team Data to Graphic Builder"""
        if self.title is None:
            self.title = title

        if description:
            self.description.append(description)

        self.description = ', '.join(self.description)

        if len(self.player.roster) == 0:
            return await self.ctx.send(f'No Results Found.')

        return await self.ctx.graphic.team(self)

    async def alliance_out(self, title: str, description: str = None):
        """Sends Alliance Data to Graphic Builder"""
        print(self.alliance)

    async def character_out(self):
        """Sends Character Data to Graphic Builder"""
        self.title = self.player.roster[0].name
        self.description = ', '.join(self.description)
        return await self.ctx.graphic.character(self)
