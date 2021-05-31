#!/usr/bin/env python3

from dices import DiceRoll
from utils import *

class RPC:
    default_descriptors = { 'name':'Enter Name',
                            'specie':'specie',
                            'class':'class',
                            'career':'carreer',
                            'level':'0',
                            'path':'path',
                            'status':'status',
                            'age':'42 years',
                            'height':'100 cm',
                            'hair':'hair',
                            'eyes':'yes' }

    def __init__(self, player, desc=default_descriptors):
        self.player = player
        self.description = desc
        self.characteristics = CharList()
        self.skills = SkillList()
        self.talents = TalentList()
        self.refresh()
        self.fate = 9
        self.fortune = 8
        self.db = None

    def refresh(self):
        # May happen, perhaps, if loaded from old version
        if not hasattr(self, 'skills'):
            self.skills = SkillList()
        if not hasattr(self, 'talents'):
            self.skills = TallentList()
        # Necessary to update skill values from rpc chars
        self.skills.refresh(self.characteristics)

    def read_form(self, form):
        # skills
        for skill in self.skills.basic(0,self.skills.n_basic):
            id = f'{skill.valid_name}_advance'
            skill.set('advance', get_form_value(form, id, skill.get('advance')))

        for i in range(SkillList.n_advanced):
            pfx = f'added_skill_{i}'
            skill_name = get_form_value(form, f'name_{pfx}', '')
            char_name = get_form_value(form, f'char_{pfx}', 'ws')
            adv = get_form_value(form, f'{pfx}_advance', 0)

            a_skill =  Skill(skill_name, Char(char_name), adv)

            self.skills[SkillList.n_basic + i] = a_skill

        # fate and fortune
        self.fate = get_form_value(form, 'i_fate', self.fate)
        self.fortune = get_form_value(form, 'i_fortune', self.fortune)

        for item in search_form(form,".*name_.*"):
            Info(item)

        for key in Char.row_keys[0:2]:
            for char in self.characteristics:
                id = f'{char.name}_{key}'
                char.set(key, get_form_value(form, id, char.get(key)))

        for key, val in self.description.items():
            id = f'd_{key}'
            value = get_form_value(form, id, val)
            self.description[key] = value

        self.skills.refresh(self.characteristics)

    def description_dict(self):
        return self.description

