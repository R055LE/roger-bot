import requests
import json
from classes.character import Character
from utils.requests import get_aliases
from settings import API

from pathlib import Path
cwd = Path(__file__).parents[1]

api_server = API.flask_host


# def GetAlliance(self, discord_id):
#     uri = f'https://api.tyejae.com/services/api/getAlliance&memberId={discord_id}'
#     headers = {"Authorization": f"Bearer {self.msfgg_api}"}
#     r = requests.get(uri, headers=headers)
#     Alliance = json.loads(r.content)
#     return Alliance

# async def GetAllianceRoster(self, discord_id):
#     uri = f'https://api.tyejae.com/services/api/getAllianceRoster&memberId={discord_id}'
#     headers = {"Authorization": f"Bearer {self.msfgg_api}"}
#     r = requests.get(uri, headers=headers)
#     AllianceRoster = json.loads(r.content)
#     return AllianceRoster

# async def GetAllianceTeam(self, discord_id, team_comp):
#     uri = f'https://api.tyejae.com/services/api/getAllianceTeam&memberId={discord_id}'
#     for idx, each in enumerate(team_comp):
#         uri += f'&c{idx+1}={each}'
#     headers = {"Authorization": f"Bearer {self.msfgg_api}"}
#     r = requests.get(uri, headers=headers)
#     AllianceTeam = json.loads(r.content)
#     return AllianceTeam
def heroids():
    data = json.loads(requests.get(
        f'{api_server}/get/heroids/').content)
    return data


def teams():
    teams = json.loads(requests.get(
        f'{api_server}/get/teams/').content)
    return teams


def traits():
    traits = json.loads(requests.get(
        f'{api_server}/get/traits/').content)
    return traits


def trait_sort(tts, *, roster, ampersand=False):
    _list = []
    f_list = []
    all_traits = traits()
    limit = 1
    for a in tts:
        if limit > 3:
            break
        f = next((
            filter(lambda t: t.casefold().startswith(a.casefold()), all_traits)), None)
        if f is not None:
            f_list.append(f)
            if ampersand:
                roster = list(
                    filter(lambda c: f in c.traits, roster))
            else:
                __list = list(
                    filter(lambda c: f in c.traits and c not in _list, roster))
                _list.extend(__list)
                limit += 1
    roster = roster if ampersand else _list
    return roster, f_list


class Player:
    def __init__(self, discord_id):
        uri = f'{api_server}/get/player/msfgg/{discord_id}'
        r = requests.get(uri)
        P = json.loads(r.content)
        self.alliance_id = P.get('alliance_id')
        self.discord_id = P.get('discord_id')
        self.icon = P.get('icon')
        self.id = P.get('id')
        self.level = P.get('level')
        self.name = P.get('name')
        self.pid = P.get('pid')
        self.roster = []
        self.teams = P.get('teams')

        for c in P.get('roster'):
            C = Character(c)
            self.roster.append(C)
        self.roster = sorted(self.roster, key=lambda c: c.power, reverse=True)

    def __str__(self):
        return f"Player({self.name})"

    def __repr__(self):
        return f"{self.name}"

    def get_character(self, args: tuple):
        aliases: list = get_aliases()

        char_match = []

        for arg in args:
            match: dict

            match = next(
                (filter(lambda r: r.get('alias').casefold() == arg.casefold(), aliases)), None)
            if match is None:
                match = next(
                    (filter(lambda r: r.get('alias').casefold().startswith(arg.casefold()), aliases)), None)
                if match is None:
                    match = next(
                        (filter(lambda r: r.get('heroid').casefold() == arg.casefold(), aliases)), None)
                    if match is None:
                        match = next(
                            (filter(lambda r: r.get('heroid').casefold().startswith(arg.casefold()), aliases)), None)
            if match:
                char_match.append(match.get('heroid'))

        self.roster = list(
            filter(lambda c: c.heroid in char_match, self.roster))

    def get_fav(self):
        self.roster = list(filter(lambda c: c.favorite == True, self.roster))

    def get_gr(self, *, eq=None, rg=None):
        if eq in range(0, 15+1):
            self.roster = list(filter(lambda c: c.gear == eq, self.roster))
        elif rg:
            self.roster = list(
                filter(lambda c: c.gear in range(rg[0], rg[1]+1), self.roster))

    def get_iso(self, *, eq=None, rg=None):
        if eq:
            self.roster = list(
                filter(lambda c: c.iso == eq, self.roster))
        elif rg:
            self.roster = list(
                filter(lambda c: c.iso in range(rg[0], rg[1]+1), self.roster))

    def get_lvl(self, *, eq=None, rg=None):
        if eq:
            self.roster = list(filter(lambda c: c.level == eq, self.roster))
        elif rg:
            self.roster = list(
                filter(lambda c: c.level in range(rg[0], rg[1]+1), self.roster))

    def get_pow(self, *, eq=None, rg=None):
        if eq:
            self.roster = list(
                filter(lambda c: int(c.power/1000) >= eq, self.roster))
        elif rg:
            self.roster = list(
                filter(lambda c: int(c.level/1000) in range(rg[0], rg[1]+1), self.roster))

    def get_prebuilt(self, args):
        tm = teams()
        team = next((filter(lambda t: any(c for c in t.get('call')
                                          if c.casefold().startswith(args[0].casefold())), tm)), None)
        #   Build Error
        comp, name = team.get('comp'), team.get('name')
        roster = []
        for heroid in comp:
            roster.append(
                next(filter(lambda c: c.heroid == heroid, self.roster), None))
        self.roster = roster
        return name

    def get_r(self, *, eq=None, rg=None):
        """
        Accepts eq (int) or rq (collection of 2 int's), or no Arguments.
        All Args must be >= 1.
        """
        if eq is not None:
            self.roster = self.roster[:eq]
        elif rg is not None:
            self.roster = self.roster[rg[0]-1:rg[1]]

    def get_rs(self, *, eq=None, rg=None):
        if eq in range(0, 7+1):
            self.roster = list(filter(lambda c: c.redstar == eq, self.roster))
        elif rg:
            self.roster = list(
                filter(lambda c: c.redstar in range(rg[0], rg[1]+1), self.roster))

    def get_t4(self, *, t4_all=False, t4_none=False):
        if t4_all:
            self.roster = list(filter(lambda c: (c.basic >= 7 and c.special >= 7 and c.passive >= 5) and (
                (c.ultimate >= 7 and 'Minion' not in c.traits) or ('Minion' in c.traits)), self.roster))
        elif t4_none:
            self.roster = list(filter(lambda c: (c.basic < 7 and c.special < 7 and c.passive < 5) and (
                (c.ultimate < 7 and 'Minion' not in c.traits) or ('Minion' in c.traits)), self.roster))
        else:
            self.roster = list(filter(lambda c: (
                c.basic >= 7 or c.special >= 7 or c.ultimate >= 7 or c.passive >= 5), self.roster))

    def get_tt(self, *, tts):
        # Characters Must Have ALL Traits Listed
        if any(a.casefold() in ['and', '&'] for a in tts):
            tts = [a for a in tts if a.casefold() not in ['and', '&']]
            self.roster, f_list = trait_sort(
                tts, roster=self.roster, ampersand=True)
        # Characters Can Have ANY of the Traits Listed
        else:
            self.roster, f_list = trait_sort(tts, roster=self.roster)
        self.roster = sorted(
            self.roster, key=lambda c: c.power, reverse=True)
        return f_list

    def get_tteam(self, args):
        f_list = self.get_tt(tts=args)
        if len(self.roster) >= 5:
            self.roster = self.roster[:5]
        return f_list

    def get_myteam(self, args):
        myteam = next((t for t in self.teams if any(a for a in args if t.get(
            'TeamName').casefold().startswith(a.casefold()))), None)
        self.roster = list(
            filter(lambda c: c.heroid in myteam.get('Team'), self.roster))
        return myteam.get('TeamName')

    def get_adteam(self, args):
        request = json.loads(requests.get(
            f'{api_server}/get/aliases/').content)

        new_args = []

        for arg in args:
            match = next(
                (filter(lambda r: r.get('alias').casefold() == arg.casefold(), request)), None)
            if match is None:
                match = next(
                    (filter(lambda r: r.get('alias').casefold().startswith(arg.casefold()), request)), None)
                if match is None:
                    match = next(
                        (filter(lambda r: r.get('heroid').casefold() == arg.casefold(), request)), None)
                    if match is None:
                        match = next(
                            (filter(lambda r: r.get('heroid').casefold().startswith(arg.casefold()), request)), None)

            if match:
                new_args.append(match.get('heroid'))

        self.roster = list(
            filter(lambda c: any(a for a in new_args if c.heroid.casefold() == a.casefold()), self.roster))

    def get_ys(self, *, eq=None, rg=None):
        if eq in range(0, 7+1):
            self.roster = list(filter(lambda c: c.star == eq, self.roster))
        elif rg:
            self.roster = list(
                filter(lambda c: c.star in range(rg[0], rg[1]+1), self.roster))


class PlayerFromAlliance(Player):
    def __name_fix(self):
        self.name = self.name.replace('%20', ' ')

    def __init__(self, name, roster):
        self.from_alliance(name, roster)
        self.__name_fix()

    def from_alliance(self, name, roster, team=True):
        self.name = name
        self.roster = []
        for key in heroids():
            char = next((c for c in roster if c.get('heroid') == key), None)
            if char:
                c = Character(char)
                self.roster.append(c)
