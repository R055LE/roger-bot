from extentions.admin.check import Check


def setup(client):
    client.add_cog(Check(client))
