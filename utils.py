import sys
from collections import UserDict, UserList

def Error(*args):
    s = 'Error: '
    for a in args:
        s += f'{a} '
    print(s, file=sys.stdout, flush=True)

def Info(*args):
    s = '>>>>> '
    for a in args:
        s += f'{a} '
    print(s)

def Log(*args, log_file_name='log'):
    s = '>>>>> '
    for a in args:
        s += f'{a} '
    s+='\n'
    with open(log_file_name,'a') as fp:
        fp.write(s)
    
def valid_name(name):
    return ''.join(e for e in self.name if e.isalnum()).lower()

def get_form_value(form, id, default=-1):
    try:
        value = form.get(id)
        value = default.__class__(value)
        return value
    except:
        Log(f'FORM READ ERROR: {id}')
        return default

def search_form(form, expression):
    Info('SEARCHING FORM')
    import re
    pat = re.compile(expression)
    matches = []
    for key in form.keys():
        if pat.match(key):
            matches.append(key)
    return matches

def tryCast(d,typ):
    try:
        return typ(d)
    except:
        Error('in NameMap.cast',e)
        return typ()

class NamedMap(UserDict): 
    def __init__(self, name, **kw): 
        self.name = name
        super().__init__(**kw)
        self.valid_name = ''.join(e for e in self.name if e.isalnum()).lower()

    def sum(self, typ=int):
        return sum(self.cast(typ).values())

    def get(self,key):
        if key == 'sum': return self.sum()
        return super().get(key)

    def set(self,key,value):
        '''Prevents setting a key that is not already there'''
        if key in self.keys():
            self[key] = tryCast(value,int)
        else:
            Error('NamedMap.set', 'wrong key', key)

    def cast(self,typ):
        data = [tryCast(d,typ) for d in self.values()]
        return NamedMap(self.name,**dict(zip(self.keys(),data)))

    def __repr__(self):
        return f'{self.name}: {super().__repr__()}'

    def __str__(self):
        return f'{self.name}: {super().__str__()}'

class Char(NamedMap):
    dummy_name = '--'
    row_keys = ['initial','advance','sum']
    def __init__(self, name, initial=0, advance=0):
        if name not in CharList.names:
            Error('Char.__init__', 'Wrong characteristic name', name)
        super().__init__(name, initial=initial, advance=advance)
        self.rows = list(self.keys())+['sum']

    def __eq__(self,other):
        return self.name == other.name

    def __hash__(self):
        return hash((self.name, self.get('initial')))

class CharList(UserList):
    names = 'ws bs s t i ag dex int wp fel'.split()
    specie_char_adds = {'human':    len(names)*[20],
                        'dwarf':    [30,20,20,30,20,10,30,20,40,10],
                        'halfling': [10,30,10,20,20,20,30,20,30,30]}
    def __init__(self, *args):
        super().__init__(*args)
        if len(self) == 0:
            for item in self.names:
                self.append(Char(item,initial=0,advance=0))
        elif len(self) != len(self.names):
            Error('CharList.__init__', 'incomplete chars')
        else:
            if not all([isinstance(a, Char) for a in self]):
                Error('CharList.__init__', 'wrong types')
    def append(self, item):
        if not isinstance(item, Char):
            Error('CharList.append','can only append Char')
        super().append(item)

    def get(self, name):
        if not name.lower() in self.names:
            Error('CharList.get', 'wrong char name', name)
        else:
            for item in self:
                if item.name.lower() == name.lower():
                    return item
        return None

    def initial(self):
        return [c.get('initial') for c in self]
    def advance(self):
        return [c.get('advance') for c in self]
    def sum(self):
        return [c.sum() for c in self]

    def as_dict(self):
        d = {}
        for item in self:
            d[item.name] = item
        return d

class Skill(NamedMap):
    def __init__(self, name, char, advance=0):
        self.char = char
        super().__init__(name, initial=char.sum(), advance=advance)
        self.basic = name in SkillList.basic_names

    def refresh(self):
        self.valid_name = ''.join(e for e in self.name if e.isalnum()).lower()
        self.set('initial', self.char.sum())

    def __eq__(self, other):
        return self.valid_name == other.valid_name # and self.char == other.char

    def __hash__(self):
        return hash((self.valid_name,  self.char))

class Talent(NamedMap):
    def __init__(self, name):
        self.times_taken = 0
        self.description = ''

    def __eq__(self, other):
        return self.name == other.name and self.description == others.description

    def __hash__(self):
        return hash((self.name, self.description))

class SkillList(UserList):
    basic_names = [ 'art', 'athletics', 'bribery', 'charm',
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
    n_basic = len(basic_names)
    n_advanced = 13

    @staticmethod
    def is_basic(name):
        return name.lower() in basic_names

    def __init__(self, content = None):
        if content:
            super().__init__(content)
        else:
            super().__init__([Skill(n,Char(c)) for n,c in \
                          zip(self.basic_names, self.basic_chars)])
            self += [Skill(str(i), Char('ws')) for i in range(self.n_advanced)]

    def basic(self, first=0, last=n_basic):
        return (self[i] for i in range(first,last))

    def added(self):
        return (self[i] for i in range(self.n_basic, len(self)))

    def get(self, name):
        for item in self:
            if item.name.lower() == name.lower():
                return item
        return None

    def remove_by_name(self, name):
        for i, item in enumerate(self):
            if item.name.lower() == name.lower() or item.valid_name == name:
                return self.remove(item)
        return None

    def refresh(self,chars):
        for item in self:
            item.char = chars.get(item.char.name)
            if item.char:
                item.refresh()
        #self.remove_duplicates()

    def remove_duplicates(self):
        tmp_skills = []
        for skill in self:
            if skill in tmp_skills or not skill.valid_name:
                self.remove(skill)
            else:
                tmp_skills.append(skill)

class TalentList(UserList):
    n_talents = 12

    def __init__(self):
        super().__init__([Talent('') for i in range(self.n_talents)])


if __name__ == '__main__':
    cl = CharList()

    cl.get('ws').update(initial=33)
    cl.get('i').update(initial=48)

    for item in cl:
        print(item, 'sum =', item.sum(), item.get('initial'))
    print(cl.sum())
    print(cl.initial())
    print(cl.as_dict())

    print('=====================================================')

    slist = SkillList()
    skill = Skill('Wrestle', Char('s',initial=34,advance=5), advance=3)

    slist.append(skill)
    slist.append(skill)

    gotSkill = slist.get('stealth')
    gotSkill.set('advance', 6)
    gotChar = cl.get(gotSkill.char.name)
    gotChar.set('initial', 43)
    gotChar.set('advance', 1)
    slist.refresh(cl)
    schars = []
    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    for skill in slist:
        print(skill.char, skill.sum())
    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')

    for i in slist.added():
        print(i)
    print('=====================================================')
    for i in slist.basic():
        print(i.name, i.get('initial'), i.get('advance'), i.get('sum'))
    gotSkill = slist.get('stealth')
    print(gotSkill.name, gotSkill.char, gotSkill.get('sum'))
