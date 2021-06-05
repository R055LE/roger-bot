from bot import bot
from utils.loader import unqualify, walk_extensions
from settings import Client


@ bot.event
async def on_ready():
    print(f'--- Logged in as {bot.user.name} #{str(bot.user.id)} ---')


for ext in walk_extensions():
    bot.load_extension(ext)
    print(f'-   {unqualify(ext).upper()} Extention Loaded   -')


bot.run(Client.token)
