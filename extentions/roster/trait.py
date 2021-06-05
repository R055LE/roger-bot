import discord.ext.commands as commands
from classes.context import Context
from settings import API, Category, Filters
import json
import requests


class Trait(commands.Cog):
    category = Category.roster
    func = 'trait'

    def __init__(self, client: commands.Bot):
        super().__init__()
        self.client = client

    def alias() -> list:
        return json.loads(requests.get(f'{API.flask_host}/get/traits/').content)

    @ commands.command(aliases=Filters.trait, description='Traits Filter')
    async def trait(self, context: Context, *args):
        """
        Filter Roster by character Traits, up to 3 at a time.
        Result set will include characters with at least one of the traits provided.
        Matching is applied to arguments to find closest value.

        Single Trait
            > rgr trait sym
        List of Characters with Any of the Following
            > rgr trait bio mystic
        List of Characters with ALL of the Following
            > rgr trait mys vil cont &
        """

        title = 'Traits'
        await context.pod.get_player()

        traits = context.pod.player.get_tt(tts=args)
        description = f'{", ".join(traits)}'
        return await context.pod.roster_out(title, description, pad=True)

    @ commands.command(hidden=True, aliases=alias())
    async def _trait(self, context: Context, *args):
        # Potential Bug if not 1st Positional Filter
        command = context.message.content.split()[1]
        return await self.client.get_command(self.func)(context, command, *args)
