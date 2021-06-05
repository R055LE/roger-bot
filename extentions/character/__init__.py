from discord.ext.commands import Bot
from extentions.character.char import Character


def setup(client: Bot):
    client.add_cog(Character(client))
