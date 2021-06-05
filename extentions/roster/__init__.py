from discord.ext.commands import Bot
from extentions.roster.favorite import Favorite
from extentions.roster.gear import Gear
from extentions.roster.iso import Iso
from extentions.roster.level import Level
from extentions.roster.power import Power
from extentions.roster.redstar import RedStar
from extentions.roster.roster import Roster
from extentions.roster.star import Star
from extentions.roster.t4 import T4
from extentions.roster.trait import Trait


def setup(client: Bot):
    client.add_cog(Favorite(client))
    client.add_cog(Gear(client))
    client.add_cog(Iso(client))
    client.add_cog(Level(client))
    client.add_cog(Power(client))
    client.add_cog(RedStar(client))
    client.add_cog(Roster(client))
    client.add_cog(Star(client))
    client.add_cog(T4(client))
    client.add_cog(Trait(client))
