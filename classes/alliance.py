from settings import API
from classes.player import Player, PlayerFromAlliance
import json
import requests

from pathlib import Path
cwd = Path(__file__).parents[1]

api_server = API.flask_host


class Alliance:
    def get_player_list(self):
        uri = f'https://api.tyejae.com/services/api/getAlliance&memberId={self.init_id}'
        headers = {"Authorization": f"Bearer {self.token}"}
        r = requests.get(uri, headers=headers)
        Alliance = json.loads(r.content)
        return Alliance

    def __init__(self, init_id):
        self.init_id = init_id
        # Convert to util
        with open(f'{cwd}/config.json', 'r') as f:
            config = json.load(f)
        self.token = config['msf.gg_settings']['api_key']
        self.players = []

    def GetLaneAssignments(self, raid_id):
        uri = f'https://api.tyejae.com/services/api/getLaneAssignments?memberId={self.init_id}&raidId={raid_id}'
        headers = {"Authorization": f"Bearer {self.token}"}
        r = requests.get(uri, headers=headers)
        LaneAssignments = json.loads(r.content)
        return LaneAssignments

    def get_all_roster(self):
        uri = f'https://api.tyejae.com/services/api/getAllianceRoster&memberId={self.init_id}'
        headers = {"Authorization": f"Bearer {self.token}"}
        r = requests.get(uri, headers=headers)
        AllianceRoster = json.loads(r.content).get('Players')
        for name, roster in AllianceRoster.items():
            new_roster = []
            for c in roster:
                new_c = {
                    "aliases": [],
                    "basic": c.get('Basic'),
                    "equip": c.get('Equipped'),
                    "favorite": c.get('Favorite'),
                    "gear": c.get('GearLevel'),
                    "heroid": c.get('HeroId'),

                    "iso": None if c.get('IsoMatrixQuality') == '' else c.get('IsoMatrixQuality'),
                    "iso_class": c.get('IsoSkillId'),
                    "iso_armor": c.get('IsoMatrixQuality_Armor'),
                    "iso_damage": c.get('IsoMatrixQuality_Damage'),
                    "iso_focus": c.get('IsoMatrixQuality_Focus'),
                    "iso_health": c.get('IsoMatrixQuality_Health'),
                    "iso_resist": c.get('IsoMatrixQuality_Resist'),
                    "level": c.get('Level'),
                    # "name": next((n.str for n in self.name), None),
                    "passive": c.get('Passive'),

                    "power": c.get('Power'),
                    "redstar": c.get('RedStar'),

                    "level": c.get('Level'),
                    "special": c.get('Special'),
                    "star": c.get('Loyalty'),
                    "traits": [],
                    "ultimate": c.get('Ultimate'),
                    "unlocked": True if c.get('Level') > 0 else False
                }
                new_roster.append(new_c)
            roster = new_roster
            p = PlayerFromAlliance(name, roster)
            self.players.append(p)

    def get_all_prebuilt(self, args):
        self.get_all_roster()
        for p in self.players:
            p: Player
            title = p.get_prebuilt(args)
        return title

        # class AllianceRoster(Alliance):
        #     def __init__(self, init_id):
        #         super().__init__(init_id)
        #         self.__get_all_players_roster()

        #     def __get_all_players_roster(self):
        #         uri = f'https://api.tyejae.com/services/api/getAllianceRoster&memberId={self.init_id}'
        #         headers = {"Authorization": f"Bearer {self.token}"}
        #         r = requests.get(uri, headers=headers)
        #         AllianceRoster = json.loads(r.content)

        #         self.name = AllianceRoster.get('AllianceName')
        #         self.players = []
        #         Players = AllianceRoster.get('Players')
        #         for p in Players:
        #             P = Player_AllianceRoster(p, Players[p])
        #             self.players.append(P)

        # class AllianceWar(Alliance):
        #     def __init__(self, alliance_id):
        #         super().__init__(init_id=None)
        #         self.__get_registered_alliance(alliance_id)

        #     def __get_registered_alliance(self, alliance_id):
        #         a = SQL.select_alliance(alliance_id)
        #         self.name = a.get('name')
        #         self.zone = a.get('war_zone')

        # a = AllianceWar('170162826051190784')

        # a = AllianceRoster('170162826051190784')
        # print(a.players)


# a = Alliance('170162826051190784')
# a.get_all_roster()
