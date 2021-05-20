#!/usr/bin/env python3

import random

class DiceRoll:
    def __init__(self):
        self.history = []
        self.roll()

    def roll_one(self):
        self.d1 = random.randint(0,9)
        return self.d1

    def roll(self):
        self.d1,self.d2 = (self.roll_one(),self.roll_one())
        self.history.append((self.d1,self.d2))

    def sum(self):
        d1 = 10 if self.d1 == 0 else self.d1
        d2 = 10 if self.d2 == 0 else self.d2
        return d1+d2

    def hectohedron(self):
        if self.d1+self.d2 == 0:
            return 100
        else:
            return 10*self.d1+self.d2

    def check(self, n):
        v = 0
        for i in range(n):
            v += self.hectohedron()
        return v/n

    def roll_chars(self, additions=[0]*9):
        for add in additions:
            self.roll()
            yield self.sum()+add

    def attribute(self, name, add = 0):
        self.roll()
        print(f'{name}  = {self.sum()+add}')

if __name__ == '__main__':
    dice = DiceRoll()
    for r in dice.roll_chars():
        print(r)
