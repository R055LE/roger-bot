class Author:
    def __init__(self, ctx):
        self.author_name = ctx.message.author.display_name
        self.author_id = ctx.message.author.id
        self.author_avatar = ctx.message.author.avatar_url
        self.author_roles = ctx.message.author.roles[1:]
        self.bot_name = ctx.bot.user.display_name
        self.bot_avatar = ctx.bot.user.avatar_url
        return self
