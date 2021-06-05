from classes.time import Time


class Message:  # Relating to Crons as Opposed to Discord.py CTX
    def __init__(self, client, channel, text=''):
        self.client = client
        self.channel = channel
        self.text = text

    def delete(self):
        pass

    def edit(self):
        pass

    async def send(self):
        c = self.client.get_channel(self.channel)
        await c.send(f'Channel {c.name} {c.id} Found')
