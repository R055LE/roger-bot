import json
from io import BytesIO
from urllib.error import HTTPError
from urllib.request import urlopen

import discord
from classes.character import Character
from classes.player import Player
from PIL import Image, ImageDraw, ImageFont
from settings import API

import requests


def heroids():
    data: list = json.loads(requests.get(
        f'{API.flask_host}/get/heroids/').content)
    return data


class Graphic:
    name_font = ImageFont.truetype(
        urlopen(f'{API.static_host}/fonts/Ultimus-BoldItalic.ttf'), 18)
    level_font = ImageFont.truetype(
        urlopen(f'{API.static_host}/fonts/Ultimus-BoldItalic.ttf'), 22)
    power_font = ImageFont.truetype(
        urlopen(f'{API.static_host}/fonts/Ultimus-BoldItalic.ttf'), 28)
    rs = Image.open(
        urlopen(f'{API.static_host}/icon/RedStar.png')).resize((20, 20))
    ys = Image.open(
        urlopen(f'{API.static_host}/icon/Loyalty.png')).resize((20, 20))
    es = Image.open(
        urlopen(f'{API.static_host}/icon/LoyaltyEmpty.png')).resize((20, 20))
    er = Image.open(
        urlopen(f'{API.static_host}/icon/RedEmpty.png')).resize((20, 20))

    async def portrait(self, character: Character):
        H, W = (200, 200)
        s_h, s_w = (20, 20)
        # s_o = int((s_h*2.5))

        g_h, g_w = (165, 165)
        p_h, p_w = (150, 100)

        new_im = Image.new('RGBA', (H, W))
        if character is None:
            character = Character({})

        traits = character.traits

    # Checks
        grayscale = True if character.unlocked is False else False
        no_level = True if character.level == 0 else False
        no_power = True if character.power == 0 else False
        no_basic = True if character.basic == 0 else False
        no_spec = True if character.special == 0 else False
        no_ult = True if character.ultimate == 0 else False
        no_pass = True if character.passive == 0 else False
        no_class = True if character.iso_class in [
            None, 'undefined', ''] else False

    # Headshot
        try:
            portrait = Image.open(
                urlopen(f'{API.static_host}/character/Portrait_{character.heroid}.png')).resize((p_w, p_h))
        except (FileNotFoundError, HTTPError):
            portrait = Image.open(
                urlopen(f'{API.static_host}/character/Portrait_default.png')).resize((p_w, p_h))
        if grayscale == True:
            portrait = portrait.convert('LA').convert('RGBA')

    # GearLevel
        if character.gear > 0:
            gear = Image.open(
                urlopen(f'{API.static_host}/icon/GearLevel{character.gear}.png')).resize((g_w, g_h))
            new_im.alpha_composite(gear, (int((W-g_w)/2), int((H-g_h)/2)))
        new_im.alpha_composite(
            portrait, (int((W-p_w)/2), int(((H-p_h)/2)-(p_w/5))))

    # ISO8 Class
        if no_class is False:
            class_icon = Image.open(
                urlopen(f'{API.static_host}/icon/Iso8{character.iso_class}.png')).resize((50, 50))
            class_pip = Image.open(
                urlopen(f'{API.static_host}/icon/ClassLevel{character.iso}.png')).resize((50, 15))
            new_im.alpha_composite(class_icon, (10, 30))
            new_im.alpha_composite(class_pip, (10, 20))

    # Abilities
        if no_basic == False:
            basic_icon = Image.open(
                urlopen(f'{API.static_host}/icon/Basic{character.basic}.png')).resize((30, 30))
            new_im.alpha_composite(
                basic_icon, (int((W-30)/2+(-9)*(W/32)), 170))
        if no_spec == False:
            spec_icon = Image.open(
                urlopen(f'{API.static_host}/icon/Special{character.special}.png')).resize((30, 30))
            new_im.alpha_composite(
                spec_icon, (int((W-30)/2+(-3)*(W/32)), 170))
        if 'Minion' in traits and no_pass == False:
            pass_icon = Image.open(
                urlopen(f'{API.static_host}/icon/Passive{character.passive}.png')).resize((30, 30))
            new_im.alpha_composite(
                pass_icon, (int((W-30)/2+(3)*(W/32)), 170))
        elif 'Minion' not in traits:
            if no_ult == False:
                ult_icon = Image.open(
                    urlopen(f'{API.static_host}/icon/Ultimate{character.ultimate}.png')).resize((30, 30))
                new_im.alpha_composite(
                    ult_icon, (int((W-30)/2+(3)*(W/32)), 170))
            if no_pass == False:
                pass_icon = Image.open(
                    urlopen(f'{API.static_host}/icon/Passive{character.passive}.png')).resize((30, 30))
                new_im.alpha_composite(
                    pass_icon, (int((W-30)/2+(9)*(W/32)), 170))

    # Loyalty & RedStar
        portrait_rs = character.redstar
        portrait_ys = character.star
        # portrait_em = 7 - character.star
        portrait_er = character.redstar - \
            character.star
        if portrait_er > 0:
            for i in range(portrait_rs-portrait_er):
                if i >= 7:
                    break
                else:
                    new_im.alpha_composite(self.rs, (30+(s_w*i), 145))
            for i in range(portrait_ys, portrait_rs):
                if i >= 7:
                    break
                else:
                    new_im.alpha_composite(self.er, (30+(s_w*i), 145))
            for i in range(portrait_rs, 7):
                if i >= 7:
                    break
                else:
                    new_im.alpha_composite(self.es, (30+(s_w*i), 145))
        else:
            for i in range(portrait_rs):
                if i >= 7:
                    break
                else:
                    new_im.alpha_composite(self.rs, (30+(s_w*i), 145))
            for i in range(portrait_ys, 7):
                if i >= 7:
                    break
                else:
                    new_im.alpha_composite(self.es, (30+(s_w*i), 145))
        for i in range(portrait_rs, portrait_ys):
            if i >= 7:
                break
            else:
                new_im.alpha_composite(self.ys, (30+(s_w*i), 145))

        d: ImageDraw.ImageDraw = ImageDraw.Draw(new_im)

    # Text
        name_field, power_field, level_field = f'{character.name}', f'{character.power:,}', f'LVL {character.level}'

        p_w, p_h = d.textsize(power_field, font=self.power_font)
        l_w, l_h = d.textsize(level_field, font=self.level_font)
        n_w, n_h = d.textsize(name_field, font=self.name_font)

        p = (no_power, power_field, self.power_font, '#FFF69E',
             '#000000', 2, (int((W-p_w)/2)), int(((H-p_h)/2)+(H/16)))
        l = (no_level, level_field, self.name_font, '#FFFFFF',
             '#000000', 2, int((W-l_w)/2), int(((H-l_h)/2)+(-1)*(H/16)))
        n = (False, name_field, self.name_font, '#FFFFFF',
             '#000000', 2, int((W-n_w)/2), int(((H-n_h)/2)+35))

        for input_tuple in (p, l, n):
            (check, text, font, fill, stroke_fill, stroke_width, W, H) = input_tuple
            if check == False:
                d.text((W, H), text, font=font, fill=fill,
                       stroke_fill=stroke_fill, stroke_width=stroke_width)

    # Output
        return new_im

    async def __assembly_charachter(self, character: Character):
        W, H = 600, 225

        new_im = Image.new('RGBA', (W, H))
        head = await self.portrait(character=character)
        new_im.alpha_composite(head, (int((W-head.width)/2), 0))

        return new_im

    async def __assembly(self, call_list: list):
        total_chars = len(call_list)
        char_rows = 0

        if len(call_list) < 40:
            row_length = 5
            mul = 1
        else:
            row_length = 10
            mul = 2

        for i in range(total_chars):
            while i > (row_length - 1):
                i = i - row_length
            if i == 0:
                char_rows += 1

        H, W = 225*char_rows, 1000*mul

        new_im = Image.new('RGBA', (W, H))

        for char in call_list:
            i = call_list.index(char)
            head = await self.portrait(character=char)
            row = 0
            while i > (row_length - 1):
                row += 1
                i = i - row_length
            new_im.alpha_composite(
                head, (200*i, (225)*row))
        return new_im

    @staticmethod
    async def __assembly_team(roster: list):
        H, W = 225, 1000
        new_im = Image.new('RGBA', (W, H))
        for char in roster:
            i = roster.index(char)
            head = await Graphic.portrait(character=char)
            new_im.alpha_composite(
                head, (200*i, 0))

        return new_im

    @staticmethod
    async def __foreground(*, image: Image.Image, total_power: int = None, player_name: str = None):
        input_W, input_H = image.size
        W, H = input_W, input_H + 50

        new_im = Image.new('RGBA', (W, H))
        new_im.alpha_composite(image, (0, H - input_H))

        player_font = ImageFont.truetype(
            urlopen(f'{API.static_host}/fonts/Ultimus-BoldItalic.ttf'), 45)

        if None not in [total_power, player_name]:
            d: ImageDraw.ImageDraw = ImageDraw.Draw(new_im)
            player_field = f'{total_power} - {player_name}'

            d.text((100, 0), player_field,
                   font=player_font, fill='#FFFFFF', stroke_fill='#000000', stroke_width=4)
        return new_im

    @staticmethod
    async def __background(*, image: Image.Image, title: str = 'None', usr: str = 'None', cmd: str = 'None', alliance_name: str = 'None', descr='None'):
        input_W, input_H = image.size
        W, H = input_W, input_H + 300

        new_im = Image.new('RGBA', (W, H))

        background = Image.open(
            urlopen(f'{API.static_host}/background/background.png'))
        # Transparent Filter
        greybox = Image.open(
            urlopen(f'{API.static_host}/background/titlebox.png')).resize((W, H))

        tahiti_logo = Image.open(
            urlopen(f'{API.static_host}/background/tahiti_logo_cust.png')).resize((140, 90))
        roger_round = Image.open(
            urlopen(f'{API.static_host}/background/roger_round.png')).resize((90, 90))
        new_im.paste(background)
        new_im.alpha_composite(greybox)

        new_im.alpha_composite(tahiti_logo, ((W-140), 20))
        new_im.alpha_composite(roger_round, (20, 20))

        new_im.alpha_composite(image, (0, 225))

        d: ImageDraw.ImageDraw = ImageDraw.Draw(new_im)
        title_font = ImageFont.truetype(
            urlopen(f'{API.static_host}/fonts/Ultimus-BoldItalic.ttf'), 80)
        alliance_font = ImageFont.truetype(
            urlopen(f'{API.static_host}/fonts/Ultimus-BoldItalic.ttf'), 30)
        footer_font = ImageFont.truetype(
            urlopen(f'{API.static_host}/fonts/Ultimus-BoldItalic.ttf'), 30)

        #
        # Dynamic Fields
        #
        title_field = title
        usr_field = f'Usr: {usr}'
        cmd_field = f'Cmd: {cmd if len(cmd) <= 40 else cmd[:40]+"~"}'
        alliance_field = alliance_name

        if descr not in [None, '']:
            descr_font = ImageFont.truetype(
                urlopen(f'{API.static_host}/fonts/Ultimus-BoldItalic.ttf'), 40)
            descr_field = descr
            descr_w, descr_h = d.textsize(descr_field, font=descr_font)
            d.text((int((W-descr_w)/2), 10), descr_field,
                   font=descr_font, fill='#FFFFFF', stroke_fill='#000000', stroke_width=4)

        home_field = f'discord.gg\n/AEBrZDS'
        roger_field = f'Roger\nthe Bot'

        title_w, title_h = d.textsize(title_field, font=title_font)
        d.text((int((W-title_w)/2), 50), title_field,
               font=title_font, fill='#FFFFFF', stroke_fill='#000000', stroke_width=4)

        alli_w, alli_h = d.textsize(alliance_field, font=alliance_font)
        d.text((int((W-alli_w)/2), 130), alliance_field,
               font=alliance_font, fill='#FFFFFF', stroke_fill='#000000', stroke_width=2)

        usr_w, usr_h = d.textsize(usr_field, font=footer_font)
        d.text((W-usr_w-20, H-usr_h-20), usr_field,
               font=footer_font, fill='#FFFFFF', stroke_fill='#000000', stroke_width=2)

        cmd_w, cmd_h = d.textsize(cmd_field, font=footer_font)
        d.text((20, int((H-(cmd_h)-20))), cmd_field,
               font=footer_font, fill='#FFFFFF', stroke_fill='#000000', stroke_width=2)

        rgr_w, rgr_h = d.textsize(roger_field, font=footer_font)
        d.text((20, 100), roger_field,
               font=footer_font, fill='#FFFFFF', stroke_fill='#000000', stroke_width=2, align='center')

        tht_w, tht_h = d.textsize(home_field, font=footer_font)
        d.text((W-tht_w-20, 100), home_field,
               font=footer_font, fill='#FFFFFF', stroke_fill='#000000', stroke_width=2, align='center')

        return new_im

    @staticmethod
    async def __background_teams(*, image_list, title, usr, cmd, alliance_name=None, descr=None):
        rows = int(len(image_list) /
                   2) if len(image_list) >= 12 else len(image_list)
        input_W, input_H = 2000 if len(
            image_list) >= 12 else 1000, rows*275
        W, H = input_W, input_H + 300
        new_im = Image.new('RGBA', (W, H))

        background = Image.open(
            urlopen(f'{API.static_host}/background/background.png'))
        # Transparent Filter
        greybox = Image.open(
            urlopen(f'{API.static_host}/background/titlebox.png')).resize((W, H))
        divider = Image.open(
            urlopen(f'{API.static_host}/background/divider.png')).resize((2, rows*275))

        tahiti_logo = Image.open(
            urlopen(f'{API.static_host}/background/tahiti_logo_cust.png')).resize((140, 90))
        roger_round = Image.open(
            urlopen(f'{API.static_host}/background/roger_round.png')).resize((90, 90))
        new_im.paste(background)
        new_im.alpha_composite(greybox)

        rank_font = ImageFont.truetype(
            urlopen(f'{API.static_host}/fonts/Ultimus-BoldItalic.ttf'), 50)

        new_im.alpha_composite(tahiti_logo, ((W-140), 20))
        new_im.alpha_composite(roger_round, (20, 20))

        d: ImageDraw.ImageDraw = ImageDraw.Draw(new_im)

        for idx, image in enumerate(image_list):
            column = 0
            while idx > (12 - 1):
                column += 1
                idx = idx - 12
            new_im.alpha_composite(image, (1000*column, 225+(275*idx)))
            d.text((25+(1000*column), 225+(275*idx)), f'{idx+1+(0 if column == 0 else 12)}.',
                   font=rank_font, fill='#FFFFFF', stroke_fill='#000000', stroke_width=4)
        if len(image_list) > 1:
            new_im.alpha_composite(divider, (999, 225))

        title_font = ImageFont.truetype(
            urlopen(f'{API.static_host}/fonts/Ultimus-BoldItalic.ttf'), 80)
        alliance_font = ImageFont.truetype(
            urlopen(f'{API.static_host}/fonts/Ultimus-BoldItalic.ttf'), 50)
        footer_font = ImageFont.truetype(
            urlopen(f'{API.static_host}/fonts/Ultimus-BoldItalic.ttf'), 30)

        #
        # Dynamic Fields
        #
        title_field = title
        usr_field = f'Usr: {usr}'
        cmd_field = f'Cmd: {cmd}'
        alliance_field = alliance_name

        if descr not in [None, '']:
            descr_font = ImageFont.truetype(
                urlopen(f'{API.static_host}/fonts/Ultimus-BoldItalic.ttf'), 40)
            descr_field = descr
            descr_w, descr_h = d.textsize(descr_field, font=descr_font)
            d.text((int((W-descr_w)/2), 10), descr_field,
                   font=descr_font, fill='#FFFFFF', stroke_fill='#000000', stroke_width=4)

        home_field = f'discord.gg\n/AEBrZDS'
        roger_field = f'Roger\nthe Bot'

        title_w, title_h = d.textsize(title_field, font=title_font)
        d.text((int((W-title_w)/2), 50), title_field,
               font=title_font, fill='#FFFFFF', stroke_fill='#000000', stroke_width=4)

        alli_w, alli_h = d.textsize(alliance_field, font=alliance_font)
        d.text((int((W-alli_w)/2), 130), alliance_field,
               font=alliance_font, fill='#FFFFFF', stroke_fill='#000000', stroke_width=2)

        usr_w, usr_h = d.textsize(usr_field, font=footer_font)
        d.text((W-usr_w-20, H-usr_h-20), usr_field,
               font=footer_font, fill='#FFFFFF', stroke_fill='#000000', stroke_width=2)

        cmd_w, cmd_h = d.textsize(cmd_field, font=footer_font)
        d.text((20, int((H-(cmd_h)-20))), cmd_field,
               font=footer_font, fill='#FFFFFF', stroke_fill='#000000', stroke_width=2)

        rgr_w, rgr_h = d.textsize(roger_field, font=footer_font)
        d.text((20, 100), roger_field,
               font=footer_font, fill='#FFFFFF', stroke_fill='#000000', stroke_width=2, align='center')

        tht_w, tht_h = d.textsize(home_field, font=footer_font)
        d.text((W-tht_w-20, 100), home_field,
               font=footer_font, fill='#FFFFFF', stroke_fill='#000000', stroke_width=2, align='center')

        return new_im

    @staticmethod
    async def __buffer_out(image: Image.Image, filename: str = 'default'):
        buffer = BytesIO()
        image.save(buffer, format='PNG')
        buffer.seek(0)
        buffer_out = discord.File(buffer, f'{filename}.png')
        return buffer_out

    @staticmethod
    async def __mode(image: Image.Image):
        input_W, input_H = image.size
        W, H = input_W, input_H+80
        new_im = Image.new('RGBA', (W, H), color='#090909')
        new_im.paste(image)
        d = ImageDraw.Draw(new_im)
        logo = Image.open(
            urlopen(f'{API.static_host}/background/msfggbot_logo.png')).resize((300, 80))
        logo_W, logo_H = logo.size
        new_im.alpha_composite(logo, (int((W-logo_W)/2), H-logo_H))
        font = ImageFont.truetype(
            urlopen(f'{API.static_host}/fonts/Ultimus-Bold.ttf'), 20)
        d.text((int((W-logo_W-300)/2), H-40), 'Data Provided By',
               font=font, fill='#FFFFFF', stroke_fill='#000000', stroke_width=4)
        return new_im

    # Use These

    @classmethod
    async def alliance(cls, ctx):
        # Work to be Done
        foreground_teams = []
        for player in ctx.alliance.players:
            faces = await cls.__assembly_team(player.roster)
            foreground = await cls.__foreground(image=faces, total_power=f'{sum(c.power for c in player.roster if c is not None):,}', player_name=player.name)
            foreground_teams.append(foreground)
        background = await cls.__background_teams(image_list=foreground_teams, title='ctx.title', usr=ctx.message.author.display_name, cmd=ctx.message.content, alliance_name='ctx.player.alliance_id', descr=ctx.description)
        mode = await cls.__mode(image=background)
        buffer = await cls.__buffer_out(mode)
        return await ctx.send(file=buffer)

##################################

    async def character(self, pod):
        faces = await self.__assembly_charachter(pod.player.roster[0])
        foreground = await self.__foreground(image=faces, total_power=f'{sum(c.power for c in pod.player.roster if c is not None):,}', player_name=pod.player.name)
        background = await self.__background(image=foreground, title=pod.title, usr=pod.ctx.message.author.display_name, cmd=pod.ctx.message.content, alliance_name=pod.player.alliance_id, descr=pod.description)
        mode = await self.__mode(image=background)
        buffer = await self.__buffer_out(mode)
        return await pod.ctx.send(file=buffer)

##################################

    async def roster(self, pod):
        faces = await self.__assembly(pod.player.roster)
        foreground = await self.__foreground(image=faces, total_power=f'{sum(c.power for c in pod.player.roster if c is not None):,}', player_name=pod.player.name)
        background = await self.__background(image=foreground, title=pod.title, usr=pod.ctx.message.author.display_name, cmd=pod.ctx.message.content, alliance_name=pod.player.alliance_id, descr=pod.description)
        mode = await self.__mode(image=background)
        buffer = await self.__buffer_out(mode)
        return await pod.ctx.send(file=buffer)
###################################

    async def team(self, pod):
        faces = await self.__assembly(pod.player.roster)
        foreground = await self.__foreground(image=faces, total_power=f'{sum(c.power for c in pod.player.roster if c is not None):,}', player_name=pod.player.name)
        background = await self.__background(image=foreground, title=pod.title, usr=pod.ctx.message.author.display_name, cmd=pod.ctx.message.content, alliance_name=pod.player.alliance_id, descr=pod.description)
        mode = await self.__mode(image=background)
        buffer = await self.__buffer_out(mode)
        return await pod.ctx.send(file=buffer)
