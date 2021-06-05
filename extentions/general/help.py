import discord
import discord.ext.commands as commands
from bot import Bot
from classes.context import Context
from settings import Category, Client


class Help(commands.Cog):
    category = Category.general

    def __init__(self, client: Bot):
        self.client = client

    @commands.command(name='help', aliases=['h', 'halp', 'hlp', 'hp', 'hl'], description='Help Command')
    async def new_help(self, context: Context, page: str = 'Help'):
        """
        Get Help With A Certain Command.
        > rgr help <command>
        """
        PREFIX = Client.prefix
        page = page.capitalize()
        color = discord.Colour.green()
        all_commands = [c.name for c in self.client.commands if not c.hidden]
        all_alliases = [
            c.aliases for c in self.client.commands if not c.hidden]
        page_lo = page.lower()
        if page_lo in all_commands or page_lo in [a for a_list in all_alliases for a in a_list]:
            cmd = self.client.get_command(page_lo)
            embed = discord.Embed(
                title=f'Help with the `{PREFIX}{self.client.get_command(page_lo)}` command', color=color)
            if len(self.client.get_command(page_lo).aliases) > 0:
                embed.add_field(
                    name='Aliases:', value=", ".join(self.client.get_command(page_lo).aliases), inline=False)
            if self.client.get_command(page_lo).help is None:
                message = 'There is no documentation for this command'
            else:
                message = self.client.get_command(page_lo).help
            embed.add_field(name='Documentation:', value=message)

            if self.client.get_command(page_lo).brief is None:
                pass
            elif len(self.client.get_command(page_lo).brief) > 0:
                n, v = self.client.get_command(page_lo).brief
                embed.add_field(
                    name=n, value=v, inline=False)

            if page == 'Help':
                commands = []
                for cog_name in self.client.cogs:
                    cog: commands.Cog = self.client.get_cog(cog_name)

                    cmds: list[commands.Command] = cog.get_commands()

                    if len(cmds) > 0:
                        for cmd in cmds:
                            cmd_available = False
                            if cmd.hidden == False:
                                cmd_available = True

                            if cmd_available == True:
                                commands.append(
                                    {"category": cog.category if hasattr(cog, "category") else "", "command": cmd.name, "description": cmd.description})

                categories = set(
                    sorted(map(lambda c: c.get('category'), commands), key=str.lower))

                embed_categories = ''
                for category in categories:
                    if category != "":

                        cat_cmds = list(
                            filter(lambda c: c.get('category') == category, commands))

                        embed_categories += f'{category}:\n'

                        for cmd in cat_cmds:
                            embed_categories += f'   {cmd.get("command")}{" "*(8-len(cmd.get("command")))}- {cmd.get("description")}\n'

                    else:
                        cat_cmds = list(
                            filter(lambda c: c.get('category') == "", commands))
                        embed_categories += '\nNo Category:\n'
                        for cmd in cat_cmds:
                            embed_categories += f'   {cmd.get("command")}{" "*(8-len(cmd.get("command")))}- {cmd.get("description")}\n'

                embed.add_field(name='Categories',
                                value=f'```{embed_categories}```', inline=False)
        else:
            embed = discord.Embed(title='Error!',
                                  description=f'Help Page for Command **\"{page}\"** not found.\n¯\_(ツ)_/¯',
                                  color=discord.Color.red())

        embed.set_footer(text="Support Provided Within The Beautiful Tahiti.\ndiscord.gg/AEBrZDS",
                         icon_url='https://cdn.discordapp.com/attachments/639546831751348235/767815947145969695/tahiti_discord_logo_still.png?size=1024')
        await context.send(embed=embed)
