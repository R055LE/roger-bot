from discord.ext import commands
import pymongo
from pymongo import ReturnDocument
import json
from pathlib import Path
cwd = Path(__file__).parents[1]
with open(f'{cwd}/config.json', 'r') as f:
    config = json.load(f)

mongo_settings = config.get('mongo_settings')
db_user, db_passwd, db_host, db_name, header_str, mode = mongo_settings.get('db_user'), mongo_settings.get(
    'db_passwd'), mongo_settings.get('db_host'), mongo_settings.get('db_name'), mongo_settings.get('header_str'), mongo_settings.get('mode')

myclient = pymongo.MongoClient(
    f'{mode}://{db_user}:{db_passwd}@{db_host}/{db_name}?{header_str}')

roger_db = myclient[db_name]

alliance_model = roger_db["alliances"]
player_model = roger_db["players"]
raid_model = roger_db["raids"]
character_model = roger_db["characters"]
message_model = roger_db["messages"]


class Mongo(commands.Cog):

    @staticmethod
    def find_alliance(alliance_id, return_fields=None):
        query = {"alliance_id": alliance_id}
        alliance = alliance_model.find_one(
            query) if return_fields == None else alliance_model.find_one(query, return_fields)
        return alliance

    # @staticmethod
    # def find_in(discord_id):
    #     query = {"player_discord_id": discord_id}
    #     player = player_model.find_one(query)

    #     def find_a(player):
    #         query2 = {"alliance_id": player.get('alliance_id')}
    #         return_fields = {"_id": 0, "alliance_id": 1, "api_key_ro": 1}
    #         print(query2)
    #         alliance = alliance_model.find_one(query2, return_fields)
    #         return alliance
    #     alliance = find_a(player)
    #     return alliance

    @staticmethod
    def find_player(player_discord_id, return_fields=None):
        query = {"player_discord_id": player_discord_id}
        player = player_model.find_one(
            query) if return_fields == None else player_model.find_one(query, return_fields)
        return player

    @staticmethod
    def find_players_all(alliance_id):
        query = {"alliance_id": alliance_id}
        players_all = player_model.find(query)
        return players_all

    @staticmethod
    def find_messages_all():
        messages_all = message_model.find()
        return messages_all

    @staticmethod
    def find_characters_all():
        characters_all = character_model.find()
        return characters_all

    @staticmethod
    def find_messages(alliance_id):
        query = {"alliance_id": alliance_id}
        messages = message_model.find(query)
        return messages

    @staticmethod
    def find_raids(alliance_id, raid_id):
        query = {"alliance_id": alliance_id, "raid_id": raid_id}
        raids = raid_model.find_one(query)
        return raids

    @staticmethod
    def find_alliance_all():
        alliance_all = alliance_model.find()
        return list(alliance_all)

    @staticmethod
    def update_alliance(alliance_object):
        query = {"alliance_id": alliance_object['alliance_id']}
        values = {"$set": alliance_object}
        alliance_model.find_one_and_update(
            query, values, upsert=True, return_document=ReturnDocument.AFTER)

    @staticmethod
    def update_message(message_object):
        query = {"message_id": message_object['message_id'],
                 "alliance_id": message_object['alliance_id']}
        values = {"$set": message_object}
        message_model.find_one_and_update(
            query, values, upsert=True, return_document=ReturnDocument.AFTER)

    @staticmethod
    def update_player(player_object):
        query = {"player_id": player_object['player_id']}
        values = {"$set": player_object}
        player_model.find_one_and_update(
            query, values, upsert=True, return_document=ReturnDocument.AFTER)

    @staticmethod
    def update_raid(raid_object):
        query = {"raid_id": raid_object['raid_id'],
                 "alliance_id": raid_object['alliance_id']}
        values = {"$set": raid_object}
        raid_model.find_one_and_update(
            query, values, upsert=True, return_document=ReturnDocument.AFTER)

    @staticmethod
    def update_character(character_object):
        query = {"character_id": character_object['character_id']}
        values = {"$set": character_object}
        character_model.find_one_and_update(
            query, values, upsert=True, return_document=ReturnDocument.AFTER)

    @staticmethod
    def delete_player(player_id):
        query = {"player_id": player_id}
        deleted_player = player_model.delete_one(query)
        return f'{deleted_player.deleted_count} Player Deleted'


def setup(client):
    client.add_cog(Mongo(client))
