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
        self.refresh_skills()
        self.fate = 9
        self.fortune = 8
        self.db = None

    def refresh_skills(self):
        self.skills.refresh(self.characteristics)

    def read_form(self, form):
        # skills
        for skill in self.skills.basic(0,self.skills.n_basic):
            id = f'{skill.valid_name}_advance'
            skill.set('advance', get_form_value(form, id, skill.get('advance')))
        # fate and fortune
        self.fate = get_form_value(form, 'i_fate', self.fate)
        self.fortune = get_form_value(form, 'i_fortune', self.fortune)

        for key in Char.row_keys[0:2]:
            for char in self.characteristics:
                id = f'{char.name}_{key}'
                char.set(key, get_form_value(form, id, char.get(key)))

        for key, val in self.description.items():
            id = f'd_{key}'
            value = get_form_value(form, id, val)
            self.description[key] = value

        self.refresh_skills()

    def description_dict(self):
        return self.description

