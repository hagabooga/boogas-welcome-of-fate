from player import *


class Warrior(Player):
    def __init__(self):
        super(Warrior,self).__init__()
        self.job = 'Warrior'
    def maxHPU(self):
        stat = 35 + round(self.stren*0.35 + self.LV*7)
        return stat
    def maxMPU(self):
        stat = 15 + round(self.intel*0.3 + self.LV*3)
        return stat
    def damageU(self):
        stat = round(self.weapon.damage*(1+self.stren/15))
        return stat
    def mag_damageU(self):
        stat = round(self.weapon.mag_damage*(1+self.intel/35))
        return stat
    def armorU(self):
        stat = 2 + round(self.stren/33)
        return stat
    def mag_armorU(self):
        stat = 1 + round(self.intel/25)
        return stat
    def hitU(self):
        stat = 95 + round(self.agi/5 + self.luck/6)
        return stat
    def dodgeU(self):
        stat = 1 + round(self.agi/15 + self.luck/13)
        return stat
    def critU(self):
        stat = 1 + round(self.agi/12 + self.luck/12)
        return stat

class Mage(Player):
    def __init__(self):
        super(Mage,self).__init__()
        self.job = 'Mage'
        self.img = pygame.image.load('game/player/play_mage.png')
    def maxHPU(self):
        stat = round(325 + self.stren*11.47 + self.LV*51)
        return stat
    def maxMPU(self):
        stat = round(425 + self.intel*24.483 + self.LV*180)
        return stat
    def damageU(self):
        stat = round(25 + 3*self.LV + self.stren/3.2 + self.weapon.damage + self.weapon.damage*(1+self.stren/20))
        return stat
    def mag_damageU(self):
        stat = round(16 + 8*self.LV + self.intel/2 + self.weapon.mag_damage + self.weapon.mag_damage*(1+self.intel/15))
        return stat
    def armorU(self):
        stat = 10 + round(self.stren/2 + self.intel/5 + self.agi/3)
        return stat
    def mag_armorU(self):
        stat = 15 + round(self.intel/2 + self.agi/3)
        return stat
    def hitU(self):
        stat = 90 + round(self.agi/6 + self.luck/5)
        return stat
    def dodgeU(self):
        stat = 1 + round(self.agi/5 + self.luck/4)
        return stat
    def critU(self):
        stat = 3 + round(self.agi/5 + self.luck/4)
        return stat

class Rogue(Player):
    def __init__(self):
        super(Rogue,self).__init__()
        self.job = 'Rogue'
        self.img = pygame.image.load('game/player/play_rogue.png')
    def maxHPU(self):
        stat = round(475 + self.stren*17.856 + self.LV*125)
        return stat
    def maxMPU(self):
        stat = round(275 + self.intel*17.744 + self.LV*100)
        return stat
    def damageU(self):
        stat = round(45 + 7*self.LV + self.stren/1.8 + self.weapon.damage + self.weapon.damage*(1+self.stren/20))
        return stat
    def mag_damageU(self):
        stat = round(18 + 5*self.LV + self.intel/3 + self.weapon.mag_damage + self.weapon.mag_damage*(1+self.intel/20))
        return stat
    def armorU(self):
        stat = 13 + round(self.stren/2 + self.intel/5 + self.agi/3)
        return stat
    def mag_armorU(self):
        stat = 13 + round(self.intel/2 + self.agi/3)
        return stat
    def hitU(self):
        stat = 95 + round(self.agi/5 + self.luck/5)
        return stat
    def dodgeU(self):
        stat = 4 + round(self.agi/3 + self.luck/4)
        return stat
    def critU(self):
        stat = 4 + round(self.agi/3 + self.luck/4)
        return stat
