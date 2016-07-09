from class_player import *

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
        stat = round(self.weapon.damage*(1+self.stren/50))
        return stat
    def mag_damageU(self):
        stat = round(self.weapon.mag_damage*(1+self.intel/60))
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
        stat = round(325 + self.stren*11.47 + self.LV*38)
        return stat
    def maxMPU(self):
        stat = round(400 + self.intel*24.483 + self.LV*150)
        return stat
    def damageU(self):
        stat = round(25 + 3*self.LV + self.stren/4.2 + self.weapon.damage + self.weapon.damage*(1+self.stren/50))
        return stat
    def mag_damageU(self):
        stat = round(11 + 8*self.LV + self.intel/2 + self.weapon.mag_damage + self.weapon.mag_damage*(1+self.intel/50))
        return stat
    def armorU(self):
        stat = 10 + round(self.stren/2 + self.intel/5 + self.agi/3)
        return stat
    def mag_armorU(self):
        stat = 15 + round(self.intel/2 + self.agi/3)
        return stat
    def hitU(self):
        stat = 95 + round(self.agi/6 + self.luck/5)
        return stat
    def dodgeU(self):
        stat = 1 + round(self.agi/5 + self.luck/4)
        return stat
    def critU(self):
        stat = 3 + round(self.agi/5 + self.luck/4)
        return stat

class Rogue(Player):
    def __init__(self):
        super(Rouge,self).__init__()
        self.job = 'Rogue'
    def maxHPU(self):
        stat = 25 + round(self.stren*0.25 + self.LV*5)
        return stat
    def maxMPU(self):
        stat = 25 + round(self.intel*0.4 + self.LV*5)
        return stat
    def damageU(self):
        stat = round(self.weapon.damage*(1+self.stren/55))
        return stat
    def mag_damageU(self):
        stat = round(self.weapon.mag_damage*(1+self.intel/55))
        return stat
    def armorU(self):
        stat = 1 + round(self.stren/40 + self.agi/35)
        return stat
    def mag_armorU(self):
        stat = 2 + round(self.intel/20 + self.agi/35)
        return stat
    def hitU(self):
        stat = 105 + round(self.agi/5 + self.luck/6)
        return stat
    def dodgeU(self):
        stat = 5 + round(self.agi/12 + self.luck/12)
        return stat
    def critU(self):
        stat = 5 + round(self.agi/10 + self.luck/10)
