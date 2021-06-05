from discord.ext.commands import Bot
from extentions.team.adhocteam import AdHocTeam
from extentions.team.myteam import MyTeam
from extentions.team.team import Team
from extentions.team.traitteam import TraitTeam


def setup(client: Bot):
    client.add_cog(AdHocTeam(client))
    client.add_cog(MyTeam(client))
    client.add_cog(Team(client))
    client.add_cog(TraitTeam(client))
