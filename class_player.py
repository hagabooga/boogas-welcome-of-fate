from weapons import *

class Player(object):
    def __init__(self):
        self.name = ''
        # Attributes
        self.new_stren = 3
        self.new_intel = 3
        self.new_agi = 3
        self.new_luck = 3
        self.stren = 3
        self.intel = 3
        self.agi = 3
        self.luck = 3
        self.old_stren = 3
        self.old_intel = 3
        self.old_agi = 3
        self.old_luck = 3
        # Stats
        self.HP = 0
        self.maxHP = 0
        self.MP = 0
        self.maxMP = 0
        self.damage = 0
        self.mag_damage = 0
        self.armor = 0
        self.mag_armor = 0
        self.hit = 0
        self.dodge = 0
        self.crit = 0
        self.shield_hp = 0
        # Bonus
        self.bonusStren = 0
        self.bonusIntel = 0
        self.bonusAgi = 0
        self.bonusLuck = 0
        self.bonusMaxHP = 0
        self.bonusMaxMP = 0
        self.bonusPdmg = 0
        self.bonusMdmg = 0
        self.bonusArmor = 0
        self.bonusMag_armor = 0
        self.bonusHit = 0
        self.bonusDodge = 0
        self.bonusCrit = 0
        # Inventory
        self.fists = Axe('Fists','basic/fists.png','Bare hands (cannot unequip)',1,1,\
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        self.fap = L_hand('Left Hand','basic/start_left.png','Fap Fap Fap (cannot unequip)',\
                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        self.china_hat = Head('China Hat','basic/start_head.png','Offers no protection (cannot unequip)',\
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        self.shirt_jeans = Body('Shirt and Jeans','basic/start_body.png','Offers no protection (cannot unequip)',\
                           0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        givebdesc([self.fists,self.fap,self.china_hat,self.shirt_jeans])
        self.weapon = self.fists
        self.lefthand = self.fap
        self.head = self.china_hat
        self.body = self.shirt_jeans
        # General
        self.LV = 1
        self.AP = 5
        self.SP = 1
        self.exp = 0
        self.max_exp = 0
        self.cash = 0
        self.learned_skills = []
        self.fight_actives = []
        self.fight_status = []
        # Game
        self.X = 500
        self.Y = 600
        self.didmiss = None
        self.didcrit = None
        self.fail_run = None
        # Special Skills
        self.rank_up_as_one = False

    def add_stat(self,stat):
        if self.AP > 0:
            if stat == 's':
                self.new_stren += 1
            elif stat == 'i':
                self.new_intel += 1
            elif stat == 'a':
                self.new_agi += 1
            elif stat == 'l':
                self.new_luck += 1
            self.AP -= 1
        self.stren = self.new_stren
        self.intel = self.new_intel
        self.agi = self.new_agi
        self.luck = self.new_luck
        self.statUpdate()

    def rem_stat(self,stat):
        if self.AP >= 0 and not self.AP == 5:
            if stat == 's' and self.new_stren > self.old_stren:
                self.new_stren -= 1
                self.AP += 1
            elif stat == 'i' and self.new_intel > self.old_intel:
                self.new_intel -= 1
                self.AP += 1
            elif stat == 'a' and self.new_agi > self.old_agi:
                self.new_agi -= 1
                self.AP += 1
            elif stat == 'l' and self.new_luck > self.old_luck:
                self.new_luck -= 1
                self.AP += 1
            self.stren = self.new_stren
            self.intel = self.new_intel
            self.agi = self.new_agi
            self.luck = self.new_luck
            self.statUpdate()
            
    def level_up(self):
        self.LV += 1
        self.AP = 5
        self.SP += 1
        self.exp = 0
        self.max_exp = (12+self.LV) * self.LV + 8*self.LV
        
    def healFullHP(self):
        self.HP = self.maxHP
    def healFullMP(self):
        self.MP = self.maxMP
    def restoreHP(self,amount):
        if self.HP + amount > self.maxHP:
            self.HP = self.maxHP
        else:
            self.HP += amount
    def restoreMP(self,amount):
        if self.MP + amount > self.maxMP:
            self.MP = self.maxMP
        else:
            self.MP += amount
    def addItemBonus(self,anItem):
        self.bonusStren += anItem.bonusStren
        self.bonusIntel += anItem.bonusIntel
        self.bonusAgi += anItem.bonusAgi
        self.bonusLuck += anItem.bonusLuck
        self.bonusMaxHP += anItem.bonusMaxHP
        self.bonusMaxMP += anItem.bonusMaxMP
        self.bonusPdmg += anItem.bonusPdmg
        self.bonusMdmg += anItem.bonusMdmg
        self.bonusArmor += anItem.bonusArmor
        self.bonusMag_armor += anItem.bonusMag_armor
        self.bonusHit += anItem.bonusHit
        self.bonusDodge += anItem.bonusDodge
        self.bonusCrit += anItem.bonusCrit
    def loseItemBonus(self,anItem):
        self.bonusStren -= anItem.bonusStren
        self.bonusIntel -= anItem.bonusIntel
        self.bonusAgi -= anItem.bonusAgi
        self.bonusLuck -= anItem.bonusLuck
        self.bonusMaxHP -= anItem.bonusMaxHP
        self.bonusMaxMP -= anItem.bonusMaxMP
        self.bonusPdmg -= anItem.bonusPdmg
        self.bonusMdmg -= anItem.bonusMdmg
        self.bonusArmor -= anItem.bonusArmor
        self.bonusMag_armor -= anItem.bonusMag_armor
        self.bonusHit -= anItem.bonusHit
        self.bonusDodge -= anItem.bonusDodge
        self.bonusCrit -= anItem.bonusCrit
##    def lose(self, what, amount):
##        what -= damage
##    def gain(self, what, amount):
##        what += amount
    def resetStat(self, aBonusStat): # the bonus stat = 0 makes the stat reset
        self.aBonusStat = 0
    def resetStatAll(self):
        self.bonusHP = 0
        self.bonusMP = 0
        self.bonusArmor = 0
        self.bonusMag_armor = 0
        self.bonusPdmg = 0
        self.bonusMdmg = 0
        self.bonusHit = 0
        self.bonusDodge = 0
        self.bonusCrit = 0
    def statUpdate(self):
        self.stren = self.new_stren
        self.intel = self.new_intel
        self.agi = self.new_agi
        self.luck = self.new_luck
        if self.rank_up_as_one:
            self.stren = 1
        # add bonus
        self.stren += self.bonusStren
        self.intel += self.bonusIntel
        self.agi += self.bonusAgi
        self.luck += self.bonusLuck
        # calculate
        self.maxHP = self.maxHPU() + self.bonusMaxHP
        self.maxMP = self.maxMPU() + self.bonusMaxMP
        self.armor = self.armorU() + self.bonusArmor
        self.mag_armor = self.mag_armorU() + self.bonusMag_armor
        self.damage = self.damageU() + self.bonusPdmg
        self.mag_damage = self.mag_damageU() + self.bonusMdmg
        self.hit = self.hitU() + self.bonusHit
        self.dodge = self.dodgeU() + self.bonusDodge
        self.crit = self.critU() + self.bonusCrit
        if self.rank_up_as_one:
            self.HP = 1
            self.maxHP = 1
            self.stren = 1
