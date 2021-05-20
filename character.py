#!/usr/bin/env python3

from dices import DiceRoll


class Characteristics:
    names = 'ws bs s t i ag dex int wp fel'.split()
    specie_char_adds = {'human':10*[20],
                        'dwarf':    [30,20,20,30,20,10,30,20,40,10,0],
                        'halfling': [10,30,10,20,20,20,30,20,30,30,0]}

    def __init__(self):
        self.initial = [45,34,22,22,35,33,22,11,2,8]
        self.advances = [0,0,0,0,0,0,0,0,0,0]
        self.ok()

    def ok(self):
        try:
            assert len(self.initial) == len(self.names) == len(self.advances), \
                    'characteristics array sizes differ'
        except AssertionError as e:
            print(e)
            return False
        return True

    def roll_dices(self, specie='human'):
        dices = DiceRoll()
        specie = specie.lower()
        if specie in self.specie_char_adds:
            adds = self.specie_char_adds[specie]
        else:
            adds = self.specie_char_adds['human']
        self.initial = list(dices.roll_chars(adds))

    def current(self):
        return [a+b for a,b in zip(self.initial,self.advances)]

    def as_dict(self,line):
        if line == 1:
            return dict(zip(self.names, self.initial))
        elif line == 2:
            return dict(zip(self.names, self.advances))
        elif line == 3:
            return dict(zip(self.names, self.current()))

    def all(self):
        return [self.as_dict(c) for c in range(1,4)]

    def get(self,name,line=1):
        return self.as_dict(line)[name]

    def set(self, name, value, line=1):
        index = self.names.index(name)
        if line == 1:
            self.initial[index] = value
        elif line == 2:
            self.advances[index] = value


class Skill:
    def __init__(self, name, char, adv=0, basic=True):
        self.basic = basic
        self.name = name
        self.valid_name = ''.join(e for e in self.name if e.isalnum())
        self.char = char
        self.adv = adv
        self.skill_value = 0

    def advance(self,amount):
        self.adv = amount

    def __str__(self):
        t = 'basic' if self.basic else 'extended'
        return f'{t}: {self.name} [{self.char}] {self.adv} {self.skill_value}'

class Skills:
    basic       = [ 'art', 'athletics', 'bribery', 'charm',
                    'charm animal', 'climb', 'cool', 'consume alcohol',
                    'dodge', 'drive', 'endurance', 'entertain',
                    'gamble', 'gossip', 'haggle', 'intimidate',
                    'intuition', 'leadership', 'melee basic', 'melee',
                    'navigation', 'outdoor survival', 'perception', 'ride',
                    'row', 'stealth' ]
    basic_chars = [ 'dex', 'ag', 'fel', 'fel',
                    'wp', 's', 'wp', 't',
                    'ag', 'ag', 't', 'fel',
                    'int', 'fel', 'fel', 's',
                    'i', 'fel', 'ws', 'ws',
                    'i', 'int', 'i', 'ag',
                    's', 'ag']

    @staticmethod
    def is_basic(name):
        return name.lower() in basic

    def __init__(self):
        self.basic_skills = [Skill(n,c) for n,c in \
                             zip(self.basic, self.basic_chars)]
        self.added_skills = []

    def all(self):
        return self.basic_skills+self.added_skills

    def get(self, name, basic=True):
        skill_set = self.basic_skills if basic else self.added_skills
        for s in skillset:
            if name.lower() == s.name.lower():
                return s
        return None

    def add(self, skill):
        '''Assuming all added skills are non-basic'''
        skill.basic = False
        self.added_skills.append(skill)

def get_form_value(form, id, default=-1):
    try:
        value = form.get(id)
        value = default.__class__(value)
        return value
    except:
        print(f'FORM READ ERROR: {id}')
        return default

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
        self.characteristics = Characteristics()
        self.skills = Skills()
        self.update_skills()
        self.fate = 9
        self.fortune = 8
        self.db = None

    def update_skills(self):
        for skill in self.skills.all():
            char = self.characteristics.get(skill.char, line=3)
            skill.skill_value = char + skill.adv

    def read_form(self, form):
        # skills
        for skill in self.skills.basic_skills:
            id = f'adv_{skill.valid_name}'
            skill.adv = get_form_value(form, id, skill.adv)
        # fate and fortune
        self.fate = get_form_value(form, 'i_fate', self.fate)
        self.fortune = get_form_value(form, 'i_fortune', self.fortune)

        for i in range(1,3):
            for char,val in self.characteristics.as_dict(i).items():
                id = f'{char}_{i}'
                value = get_form_value(form, id, val)
                self.characteristics.set(char, value, i)

        for key, val in self.description.items():
            id = f'd_{key}'
            value = get_form_value(form, id, val)
            self.description[key] = value

        self.update_skills()


    def description_dict(self):
        return self.description
        #d = {}
        #for item in self.default_descriptors:
        #    d[item] = getattr(self, item)
        #return d


