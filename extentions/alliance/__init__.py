from discord.ext.commands import Bot
from extentions.alliance.allteam import AllTeam


def setup(client: Bot):
    client.add_cog(AllTeam(client))
