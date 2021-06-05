from discord.ext.commands import Bot
from extentions.general.help import Help
from extentions.general.speak import Speak


def setup(client: Bot):
    client._old_help = client.get_command('help')
    client.remove_command('help')

    client.add_cog(Help(client))
    client.add_cog(Speak(client))
