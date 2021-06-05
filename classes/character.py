import os
cwd = os.getcwd()


class Character:
    def __init__(self, character):
        self.aliases = character.get('aliases', [])
        self.basic = character.get('basic', 0)
        self.equip = character.get('equip', '000000')
        self.favorite = character.get('favorite', False)
        self.gear = character.get('gear', 0)
        self.heroid = character.get('heroid', 'default')
        self.id = character.get('id', '')
        self.iso = character.get('iso', 0)
        self.iso_class = character.get('iso_class', None)
        self.iso_armor = character.get('iso_armor', 0)
        self.iso_damage = character.get('iso_damage', 0)
        self.iso_focus = character.get('iso_focus', 0)
        self.iso_health = character.get('iso_health', 0)
        self.iso_resist = character.get('iso_resist', 0)
        self.level = character.get('level', 0)
        self.name = character.get('name', '')
        self.passive = character.get('passive', 0)
        self.player_id = character.get('player_id', '')
        self.power = character.get('power', 0)
        self.redstar = int(character.get('redstar', 0))
        self.id = character.get('id', '')
        self.level = character.get('level', 0)
        self.shards = character.get('shards', 0)
        self.special = character.get('special', 0)
        self.star = character.get('star', 0)
        self.traits = character.get('traits', [])
        self.ultimate = character.get('ultimate', 0)
        self.unlocked = character.get('unlocked', False)

    def __str__(self):
        return f"({self.name} LV{self.level} G{self.gear} {self.star}/{self.redstar} {self.basic}{self.special}{self.ultimate}{self.passive})"

    def __repr__(self):
        return f"({self.name} LV{self.level} G{self.gear} {self.star}/{self.redstar} {self.basic}{self.special}{self.ultimate}{self.passive})"

    # def GetSpeed(self):
    #     try:
    #         self.speed = self.stats.get(
    #             self.key).get('speed_Override').get('1')
    #         return self.speed
    #     except AttributeError:
    #         self.speed = '100'
    #         return self.speed
