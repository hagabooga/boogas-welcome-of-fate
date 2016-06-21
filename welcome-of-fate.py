import pygame
import random
import math
import time

pygame.init()
pygame.display.set_caption('''Booga's Welcome of Fate''')
screenW = 1024
screenH = 768
screen = pygame.display.set_mode((screenW,screenH))
clock = pygame.time.Clock()

#colors
black = (0,0,0)
white = (255,255,255)
yellow = (250,250,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
cyan = (71,223,198)
grey = (215,215,215)
orange = (255,128,0)
brown = (200,120,90)
lime = (136,255,0)
lightYellow = (225,225,0)
lighterYellow = (210,210,0)
lightCyan = (77,242,209)
lightRed = (200,0,0)
lighterRed = (180,0,0)
lightGreen = (0,210,0)
lighterGreen = (0,190,0)
lightBlue = (0,0,215)
lighterBlue = (0,0,190)
lightOrange = (255,153,51)

randColor = (random.choice(range(50,175)),random.choice(range(50,175)),random.choice(range(50,175)))
randColor2 = (random.choice(range(50,175)),random.choice(range(50,175)),random.choice(range(50,175)))

# Music/sounds
def weapon_atk_sound():
    atk_sound = pygame.mixer.Sound(random.choice(['atk1.wav','atk2.wav','atk3.wav','atk4.wav','atk5.wav','atk6.wav','atk7.wav']))
    return atk_sound
pygame.mixer.music.load('bgm_intro.mp3')
heal = pygame.mixer.Sound('heal.wav')
wear = pygame.mixer.Sound('wear.wav')
buySound = pygame.mixer.Sound('buy.wav')
potSound = pygame.mixer.Sound('pheal.wav')
rank_up = pygame.mixer.Sound('rank_up.wav')
pg_flip = pygame.mixer.Sound('page_flip.wav')
crit = pygame.mixer.Sound('crit.wav')
select = pygame.mixer.Sound('select.wav')
#congrats = pygame.mixer.Sound('

# Pictures
small_arrow_left = pygame.image.load('small_arrow_left.png')
small_arrow_right = pygame.image.load('small_arrow_right.png')
st_burn = pygame.image.load('st_burn.png')
st_para = pygame.image.load('st_para.png')
st_bleed = pygame.image.load('st_bleed.png')
st_curse = pygame.image.load('st_curse.png')

# Global Variables
inSome = False
inFight = False
inStore = False
inInv = False
inHosp = False
inSkill = False
inLearnSkill = False

# For fight
fight_detail_text_list = [[['',black],['',black],['',black],['',black],['',black],['',black]],\
                          [['',black],['',black],['',black],['',black],['',black],['',black]],\
                          [['',black],['',black],['',black],['',black],['',black],['',black]]]    # (text,color)
text_detail_pg_num = 1
fight_shown_text = []
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
        self.weapon = fists
        self.lefthand = fap
        self.head = china_hat
        self.body = shirt_jeans
        # General
        self.LV = 1
        self.AP = 5
        self.SP = 1
        self.exp = 0
        self.max_exp = 12
        self.cash = 0
        self.learned_skills = []
        self.fight_actives = []
        self.fight_status = []
        # Game
        self.img = pygame.image.load('play_nor.png')
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
        player.statUpdate()

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
            player.statUpdate()
            
    def level_up(self):
        self.LV += 1
        self.AP = 5
        self.SP += 1
        self.exp = 0
        self.max_exp = (12+self.LV) * self.LV + 8*self.LV
        stats()
        self.healFullHP()
        self.healFullMP()

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
    def lose(self, what, amount):
        what -= damage
    def gain(self, what, amount):
        what += amount

    
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
        if player.rank_up_as_one:
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
        if player.rank_up_as_one:
            self.HP = 1
            self.maxHP = 1
            self.stren = 1


class Action:
    def skillAttack(user,victim,used_skill):
        user.MP -= used_skill.mana
        if isinstance(used_skill,Physical):
            damage = used_skill.damage - victim.armor
        else: # magical attack
            damage = used_skill.damage - victim.mag_armor
        if meditate in user.fight_actives and isinstance(used_skill,Magical): # MEDITATE SKILL (all damage multipliers should go here)
                damage *= meditate.scale/100 # a percentage
                user.fight_actives.remove(meditate)
        #####
        crit_chance = user.crit
        hit_chance = user.hit - victim.dodge
        if hasattr(used_skill,'hit_chance'): # hit increaser
                hit_chance += used_skill.hit_chance
        print(hit_chance)
        if hit_chance >= random.choice(range(100)): # Check if hit
            if hasattr(used_skill,'crit_chance'): # Crit increaser
                crit_chance += used_skill.crit_chance
            print(crit_chance)
            if crit_chance >= random.choice(range(100)): # Check if crit
                damage = round(damage*2.25) # crit multiplier
                user.didCrit = True
            else:
                user.didCrit = False
            if user == player:
                damage += random.choice(range(0+user.luck,15+user.luck)) # bonus damage
            else:
                damage += random.choice(range(0,round(15+user.damage/90)))
            if damage < 0: # if damage less than 0, damage = 0 so no heal
                damage = 0
            if victim.shield_hp > 0: # SHIELD DAMAGE GOES FIRST ALWAYS
                if victim.shield_hp - damage < 0:
                    victim.shield_hp = 0
                    victim.HP -= damage - victim.shield_hp 
                else:
                    victim.shield_hp -= damage
            elif mana_gaurd in player.fight_actives and user == enemy: # MANA GAURD SKILL
                    if victim.MP - damage < 0: # if deal more than current MP
                        victim.HP -= damage - victim.MP
                        victim.MP = 0
                    else: # else regular
                        victim.MP -= damage
            else: # no active skills
                victim.HP -= damage # final calculation
            if hasattr(used_skill,'sound'):
                used_skill.sound.play() # sound play if hit
            else: #generic hit sound
                weapon_atk_sound().play()
            return damage
        else: # player miss
            wear.play()
    def skillActive(user,victim,used_skill): # all skill actives
        user.MP -= used_skill.mana
        used_skill.sound.play()
        Active.effect(used_skill)

##        ###############################
##        ### Lunge Crit/Dodge factor ###
##        if self == player.skill_lunge:
##            dodge_rate = victim.dodge + 15
##            crit_rate = round(user.crit*2 + 13)

##            total = self.damage
##        ################################
##        ### Sonic Hit Chance factor ####
##        elif self == player.skill_sonic:
##            dodge_rate = round(dodge_rate*0.43 - 1)
##            total = self.damage
##        ###############################
##        ### Sweep Damage Bonus ########
##        elif self == player.skill_sweep:
##            bonus = 0
##            time = 0
##            for x in range(10,110,10):
##                if victim.HP < x:
##                    for n in range(time+1):
##                        bonus += round(2*n*(0.5 + victim.HP/125))
##                    total = self.damage + bonus
##                    break
##                time += 1
##        ################################
##        ### Basic Attack ##############
class Skill(Action):
    def __init__(self,name,img,sound,desc,effdesc,requiredesc,maxRank):
        self.name = name
        if img != None:
            self.img = pygame.image.load(img)
        if sound != None:
            self.sound = pygame.mixer.Sound(sound)
        self.desc = desc
        self.effdesc = effdesc
        self.requiredesc = requiredesc
        self.rank = 0
        self.maxRank = maxRank
        self.damage = 0
        self.mana = 0
        
    def skill_requirement(self): ##### ALL SKILL REQUIREMENTS
        if isinstance(self,Magical):
            if self == fireball:
                return player.LV >= 4 and ember.rank >= 3
            elif self == river:
                return player.LV >= 4 and shower.rank >= 3
            elif self == gust:
                return player.LV >= 4 and breeze.rank >= 3
            elif self == thunderbolt:
                return player.LV >= 4 and shock.rank >= 3
            elif self == blaze:
                return player.LV >= 10 and fireball.rank >= 3
            elif self == waterfall:
                return player.LV >= 10 and river.rank >= 3
            elif self == whirlwind:
                return player.LV >= 10 and gust.rank >= 3
            elif self == lightning:
                return player.LV >= 10 and thunderbolt.rank >= 3
            elif self == inferno:
                return player.LV >= 18 and blaze.rank >= 3
            elif self == tsunami:
                return player.LV >= 18 and waterfall.rank >= 3
            elif self == tornado:
                return player.LV >= 18 and whirlwind.rank >= 3
            elif self == thunderstorm:
                return player.LV >= 18 and lightning.rank >= 3
            else:
                return True
        elif isinstance(self,Active):
            if self == mana_gaurd:
                return player.LV >= 2
            elif self == restore:
                return player.LV >= 4
            elif self == barrier:
                return player.LV >= 6
            elif self == meditate:
                return player.LV >= 9
            else:
                return True
        elif isinstance(self,Passive):
            if self == magic_mast:
                return player.LV >= 5
            elif self == mana_armor:
                return player.LV >= 8
            elif self == as_one:
                return player.LV >=5
            else:
                return True
        else:
            return True
    def status_effect(self,victim):
        if hasattr(self,'burn_chance'):
            if self.burn_chance >= random.choice(range(101)):
                if st_burn not in victim.fight_status:
                    victim.fight_status.append(st_burn)
                return st_burn
        elif hasattr(self,'para_chance'):
            if self.para_chance >= random.choice(range(101)):
                if st_burn not in victim.fight_status:
                    victim.fight_status.append(st_para)
                return st_para
        elif hasattr(self,'bleed_chance'):
            if self.bleed_chance >= random.choice(range(101)):
                if st_burn not in victim.fight_status:
                    victim.fight_status.append(st_bleed)
                return st_bleed
        elif hasattr(self,'curse_chance'):
            if self.curse_chance >= random.choice(range(101)):
                if st_curse not in victim.fight_status:
                    victim.fight_status.append(st_curse)
                return st_curse
        else:
            return None
    

class Physical(Skill):
    def __init__(self,name,img,sound,desc,effdesc,requiredesc,maxRank):
        super(Physical,self).__init__(name,img,sound,desc,effdesc,requiredesc,maxRank)
        self.type = 'Spell'

class Magical(Skill):
    def __init__(self,name,img,sound,desc,effdesc,requiredesc,maxRank):
        super(Magical,self).__init__(name,img,sound,desc,effdesc,requiredesc,maxRank)
        self.type = 'Spell'
# actives and passives have unique detail
class Active(Skill):
    def __init__(self,name,img,sound,desc,effdesc,requiredesc,maxRank):
        super(Active,self).__init__(name,img,sound,desc,effdesc,requiredesc,maxRank)
        self.type = 'Active' 
        del self.damage
    def effect(used_skill):
        player.fight_actives.append(used_skill)
        if used_skill == mana_gaurd:
            mana_gaurd.setTurnEnd(fight_turn,5)
            mana_gaurd.setCooldownEnd(fight_turn,mana_gaurd.cooldown)
        elif used_skill == restore:
            player.restoreHP(restore.hp)
            player.bonusLuck += restore.bonus_stat
            player.bonusHit += restore.bonus_stat
            player.bonusCrit += restore.bonus_stat
            restore.setTurnEnd(fight_turn,3)
            restore.setCooldownEnd(fight_turn,restore.cooldown)
        elif used_skill == barrier:
            player.shield_hp = barrier.shield
            barrier.setTurnEnd(fight_turn,3)
            barrier.setCooldownEnd(fight_turn,barrier.cooldown)
        elif used_skill == meditate:
            meditate.setCooldownEnd(fight_turn,meditate.cooldown)

    def loseEffect(self):
        if self == restore:
            player.bonusLuck -= restore.bonus_stat
            player.bonusHit -= restore.bonus_stat
            player.bonusCrit -= restore.bonus_stat
        elif self == barrier:
            player.shield_hp -= barrier.shield
            
    def setTurnEnd(self,turn,duration):
        self.turnEnd = turn + duration
    def setCooldownEnd(self,turn,duration):
        self.cooldownEnd = turn + duration
    def delCooldownEnd(self):
        if hasattr(self,'cooldownEnd'):
            del self.cooldownEnd
                
class Passive(Skill):
    def __init__(self,name,img,sound,desc,effdesc,requiredesc,maxRank):
        super(Passive,self).__init__(name,img,sound,desc,effdesc,requiredesc,maxRank)
        self.type = 'Passive'
        del self.damage
    def giveBonus(self):
        if self == max_mp_inc:
            player.bonusMaxMP += self.bonus
        elif self == magic_mast:
            player.bonusLuck += self.bonus
            player.bonusCrit += self.bonus
            player.bonusHit += self.bonus
        elif self == mana_armor:
            player.bonusArmor += self.bonus
            player.bonusMag_armor += self.bonus
        elif self == as_one:
            player.rank_up_as_one = True
            player.bonusMaxMP += as_one.bonus
            as_one.given_bonus = as_one.bonus
            
            

basic_attack = Physical('Basic Attack','fists.png',None,'Attack with your weapon','Deals physical damage','',0)
# Mage Skills #1
# attack skills
ember = Magical('Ember','ember.png','fire.wav','Burn the enemy','Small chance to burn','',3)
shower = Magical('Shower','shower.png','water.wav','Call the rain to fall','Increased hit rate','',3)
breeze = Magical('Breeze','breeze.png','wind.wav','Blow the enemy away','Increased crit rate, decreased hit chance','',3)
shock = Magical('Shock','shock.png','thunder.wav','Shock with electricity','Small chance to paralyze, small increased crit rate','',3)
fireball = Magical('Fireball','fireball.png','fire.wav','Lob a ball of fire','Medium rate to burn','LV: 4, Ember: Rank 3',3)
river = Magical('River','river.png','water.wav','Call a river','More increased hit rate','LV: 4, Shower: Rank: 3',3)
gust = Magical('Gust','gust.png','wind.wav','Make the enemy fly','More increased crit rate, decreased hit chance','LV: 4, Breeze: Rank: 3',3)
thunderbolt = Magical('Thunderbolt','thunderbolt.png','thunder.wav','Pikachu','Medium chance to paralyze, increased crit rate','LV: 4, Shock: Rank: 3',3)
blaze = Magical('Blaze','blaze.png','fire.wav','Set enemy ablaze','High chance to burn','LV: 10, Fireball: Rank: 3',3)
waterfall = Magical('Waterfall','waterfall.png','water.wav','A fall of water','Greatly increased hit rate', 'LV: 10, River: Rank: 3',3)
whirlwind = Magical('Whirlwind','whirlwind.png','wind.wav','A strong wind','Greatly increased crit rate, decreased hit chance','LV: 10, Gust: Rank: 3',3)
lightning = Magical('Lightning','lightning.png','thunder.wav','Electrify the enemy','High chance to paralyze, more increased crit rate',\
                    'LV: 10, Thunderbolt: Rank: 3',3)
inferno = Magical('Inferno','inferno.png','fire.wav','The strongest flames in the game','Higher chance to burn','LV: 18, Blaze: Rank: 3',3)
tsunami = Magical('Tsunami','tsunami.png','water.wav','Wash away the enemy','Greater increased hit rate','LV: 18, Waterfall: Rank: 3',3)
tornado = Magical('Tornado','tornado.png','wind.wav','Blow away the enemy','Greater increased crit rate, decreased hit chance','LV: 18, Whirlwind: Rank: 3',3)
thunderstorm = Magical('Thunderstorm','thunderstorm.png','thunder.wav','A storm of lightning','Higher chance to paralyze, Greatly increased crit rate',\
                       'LV: 18, Lightning: Rank: 3',3)
## Actives
mana_gaurd = Active('Mana Gaurd','mana_gaurd.png','pheal.wav','Mana gaurds your health','For 5 turns, take damage from mana instead of health','LV: 2',3)
restore = Active('Restore','restore.png','heal.wav','Restore health','Restore health and gain temp. bonuses for 3 turns','LV: 4',5)
barrier = Active('Barrier','barrier.png','charge.wav','Create a barrier','For 3 turns, create a shield','LV: 6',5)
meditate = Active('Meditate','meditate.png','charge.wav','Focus your mind','Next spell deals massive damage','LV: 9',4)

## Passivesonus
max_mp_inc = Passive('Max MP +','max_mp_inc.png',None,'Expand your mind','Increases Maximum MP','',7)
magic_mast = Passive('Spell Mastery','magic_mast.png',None,'Train your skills','Increases Luck/Hit/Crit Chance','LV: 5',5)
mana_armor = Passive('Mana Armor','mana_armor.png',None,'Mana is Armor','Gain bonus Armor/Resist based on Current Max MP','LV: 8',3)
as_one = Passive('As One','as_one.png',None,'You are one','Set Str/HP = 1, gain bonus MP based on difference','LV: 5',1)


# lists in list
mage_skills_pg = [[ember,shower,breeze,shock,\
                   fireball,river,gust,thunderbolt,\
                   blaze,waterfall,whirlwind,lightning,\
                   inferno,tsunami,tornado,thunderstorm],\
                  [mana_gaurd,restore,barrier,meditate,None,None,None,None,\
                   max_mp_inc,magic_mast,mana_armor,as_one,None,None,None,None]]

def skillUpdate():
    if player.job == 'Mage': # MAGE SKILLS
        # attack skills
        basic_attack.damage = player.damage
        basic_attack.mana = 0
        ### Damage Skills
        # Fire
        ember.damage = round(75 + (player.mag_damage/1.8)*(1.8 * (1 + ember.rank)))
        ember.mana = round(50 + ember.damage/(17-ember.rank) + ember.rank * 35)
        ember.burn_chance = round(15 + 3*ember.rank + player.mag_damage/(25 + player.mag_damage/4))
        fireball.damage = round(ember.damage + (player.mag_damage/1.75)*(1.8 * (1 + fireball.rank)))
        fireball.mana = round(ember.mana + fireball.damage/(15-fireball.rank) + fireball.rank * 60)
        fireball.burn_chance = round(ember.burn_chance + 3*fireball.rank + player.mag_damage/(25 + player.mag_damage/4))
        blaze.damage = round(fireball.damage + (player.mag_damage/1.7)*(1.8 * (1 + blaze.rank)))
        blaze.mana = round(fireball.mana + blaze.damage/(15-blaze.rank) + blaze.rank * 125)
        blaze.burn_chance = round(fireball.burn_chance + 4*blaze.rank + player.mag_damage/(25 + player.mag_damage/4))
        inferno.damage = round(blaze.damage + (player.mag_damage/1.65)*(1.8 * (1 + inferno.rank)))
        inferno.mana = round(blaze.mana + inferno.damage/(15-inferno.rank) + inferno.rank * 210)
        inferno.burn_chance = round(blaze.burn_chance + 5*inferno.rank + player.mag_damage/(25 + player.mag_damage/4))
        # Water
        shower.damage = round(88 + (player.mag_damage/1.7)*(1.85 * (1 + shower.rank)))
        shower.mana = round(45 + shower.damage/(20-shower.rank) + shower.rank * 25)
        shower.hit_chance = round(20 + 3.5*shower.rank)
        river.damage = round(shower.damage + (player.mag_damage/1.65)*(1.85 * (1 + river.rank)))
        river.mana = round(shower.mana + river.damage/(20-river.rank) + river.rank * 60)
        river.hit_chance = round(shower.hit_chance + 3.5*river.rank)
        waterfall.damage = round(river.damage + (player.mag_damage/1.6)*(1.85 * (1 + waterfall.rank)))
        waterfall.mana = round(river.mana + waterfall.damage/(20-waterfall.rank) + waterfall.rank * 100)
        waterfall.hit_chance = round(river.hit_chance + 3.5*waterfall.rank)
        tsunami.damage = round(waterfall.damage + (player.mag_damage/1.5)*(1.85 * (1 + tsunami.rank)))
        tsunami.mana = round(waterfall.mana + tsunami.damage/(20-tsunami.rank) + tsunami.rank * 225)
        tsunami.hit_chance = round(waterfall.hit_chance + 3.5*tsunami.rank)
        # Wind
        breeze.damage = round(70 + (player.mag_damage/2.1)*(1.6 * (1 + breeze.rank)))
        breeze.mana = round(30 + breeze.damage/(23-breeze.rank) + breeze.rank * 20)
        breeze.crit_chance = round(26 + 3*breeze.rank)
        breeze.hit_chance = round(-20 + 2*breeze.rank)
        gust.damage = round(breeze.damage + (player.mag_damage/2.0)*(1.65 * (1 + gust.rank)))
        gust.mana = round(breeze.mana + gust.damage/(23-gust.rank) + gust.rank * 40)
        gust.crit_chance = round(breeze.crit_chance + 3*gust.rank)
        gust.hit_chance = round(breeze.hit_chance + 2*gust.rank)
        whirlwind.damage = round(gust.damage + (player.mag_damage/1.9)*(1.7 * (1 + whirlwind.rank)))
        whirlwind.mana = round(gust.mana + whirlwind.damage/(23-whirlwind.rank) + whirlwind.rank * 80)
        whirlwind.crit_chance = round(gust.crit_chance + 3*whirlwind.rank)
        whirlwind.hit_chance = round(gust.hit_chance + 1*whirlwind.rank)
        tornado.damage = round(whirlwind.damage + (player.mag_damage/1.8)*(1.8 * (1 + tornado.rank)))
        tornado.mana = round(whirlwind.mana + tornado.damage/(23-tornado.rank) + tornado.rank * 200)
        tornado.crit_chance = round(whirlwind.crit_chance + 3*tornado.rank)
        tornado.hit_chance = round(whirlwind.hit_chance + 1*tornado.rank)
        # Electric
        shock.damage = round(100 + (player.mag_damage/1.7)*(1.9 * (1 + shock.rank)))
        shock.mana = round(80 + shock.damage/(14-shock.rank) + shock.rank * 55)
        shock.para_chance = round(20 + 3*shock.rank + player.mag_damage/(25 + player.mag_damage/4))
        shock.crit_chance = round(16 + 3*shock.rank)
        thunderbolt.damage = round(shock.damage + (player.mag_damage/1.6)*(2 * (1 + thunderbolt.rank)))
        thunderbolt.mana = round(shock.mana + thunderbolt.damage/(14-thunderbolt.rank) + thunderbolt.rank * 60)
        thunderbolt.para_chance = round(shock.para_chance + 3*thunderbolt.rank + player.mag_damage/(25 + player.mag_damage/3.8))
        thunderbolt.crit_chance = round(25 + 3*thunderbolt.rank)
        lightning.damage = round(thunderbolt.damage + (player.mag_damage/1.5)*(2.1 * (1 + lightning.rank)))
        lightning.mana = round(thunderbolt.mana + lightning.damage/(14-lightning.rank) + lightning.rank * 100)
        lightning.para_chance = round(thunderbolt.para_chance + 3*lightning.rank + player.mag_damage/(25 + player.mag_damage/3.6))
        lightning.crit_chance = round(35 + 2*lightning.rank)
        thunderstorm.damage = round(lightning.damage + (player.mag_damage/1.4)*(2.2 * (1 + thunderstorm.rank)))
        thunderstorm.mana = round(lightning.mana + thunderstorm.damage/(14-thunderstorm.rank) + thunderstorm.rank * 200)
        thunderstorm.para_chance = round(lightning.para_chance + 4*thunderstorm.rank + player.mag_damage/(25 + player.mag_damage/3.4))
        thunderstorm.crit_chance = round(42 + 2*thunderstorm.rank)
        ### Actives (has unique detail)
        mana_gaurd.mana = round(75*mana_gaurd.rank + (player.MP*0.25)/(mana_gaurd.rank+1))
        mana_gaurd.cooldown = 5
        mana_gaurd.detail = 'CD: %i, Mana Cost: %i'%(mana_gaurd.cooldown,mana_gaurd.mana)
        restore.hp = round(100+restore.rank*5 + player.maxHP/(10 - restore.rank/3) + player.mag_damage*0.5/player.maxHP)
        restore.bonus_stat = round(player.mag_damage/99 + restore.rank*6.5)
        restore.cooldown = 3
        restore.mana = round(50 + player.mag_damage*0.6*(1 - restore.rank/20))
        restore.detail = 'HP: +%i, Luck/Hit/Crit: +%i, CD: %i, Mana Cost: %i'%(restore.hp,restore.bonus_stat,restore.cooldown,restore.mana)
        barrier.shield = round(75 + barrier.rank*6 + player.mag_damage*(1.5+0.8*barrier.rank)*(1+barrier.rank/5))
        barrier.cooldown = 5
        barrier.mana = round(60 + barrier.rank*50 + player.mag_damage*0.25)
        barrier.detail = 'Shield Amount: %i, CD: %i, Mana Cost: %i'%(barrier.shield,barrier.cooldown,barrier.mana)
        meditate.scale = round(215 + (meditate.rank-1)*15)
        meditate.cooldown = 7 - meditate.rank
        meditate.mana = round(200 + player.maxMP/(15 + meditate.rank))
        meditate.detail = 'Multiplier: %i%%, CD: %i, Mana Cost: %i'%(meditate.scale,meditate.cooldown,meditate.mana)
        ### Passives (has unique detail)
        max_mp_inc.bonus = round((320 + 245*max_mp_inc.rank)*(1 + max_mp_inc.rank/65)) # each level gains amount
        max_mp_inc.detail = 'Max MP: +%i'%(max_mp_inc.bonus)
        magic_mast.bonus = 4
        magic_mast.detail = 'Luck/Hit/Crit: +%i, Next rank: +%i'%(magic_mast.bonus*magic_mast.rank,magic_mast.bonus*(magic_mast.rank+1))
        mana_armor.bonus = round(player.maxMP/40)
        mana_armor.detail = 'When ranked up, Armor/Resist: +%i instantly'%mana_armor.bonus
        as_one.bonus = (player.stren*2 + player.maxHP)*3
        if not player.rank_up_as_one:
            as_one.detail = 'When ranked up, Max MP:  +%i'%as_one.bonus
        else:
            as_one.detail = 'You have gained, Max MP: +%i'%as_one.given_bonus

### Rouge Skills #1
##bleed = Skill()
##cripple = Skill()
##cutthroat = Passive()
##stealth = Skill()


 ### Warrior Skills #1
##lunge = Skill('Lunge','lunge.png','Deal medium damage with increased crit chance but low hit chance')
##sonic = Skill()
##blaze = Skill()
##sweep = Skill()

    
class Item(object):
    def __init__(self,name,img,desc,\
                 bstr,bint,bagi,bluk,bhp,bmp,bpdmg,bmdmg,barm,bmarm,bhit,bdge,bcrt,cost):
        self.name = name
        self.cost = cost
        self.img = pygame.image.load(img)
        self.desc = desc
        self.bonusStren = bstr
        self.bonusIntel = bint
        self.bonusAgi = bagi
        self.bonusLuck = bluk
        self.bonusPdmg = bpdmg
        self.bonusMdmg = bmdmg
        self.bonusMaxHP = bhp
        self.bonusMaxMP = bmp
        self.bonusArmor = barm
        self.bonusMag_armor = bmarm
        self.bonusHit = bhit
        self.bonusDodge = bdge
        self.bonusCrit = bcrt
    def addBonus(self):
        player.bonusStren += self.bonusStren
        player.bonusIntel += self.bonusIntel
        player.bonusAgi += self.bonusAgi
        player.bonusLuck += self.bonusLuck
        player.bonusMaxHP += self.bonusMaxHP
        player.bonusMaxMP += self.bonusMaxMP
        player.bonusPdmg += self.bonusPdmg
        player.bonusMdmg += self.bonusMdmg
        player.bonusArmor += self.bonusArmor
        player.bonusMag_armor += self.bonusMag_armor
        player.bonusHit += self.bonusHit
        player.bonusDodge += self.bonusDodge
        player.bonusCrit += self.bonusCrit
    def noBonus(self):
        player.bonusStren -= self.bonusStren
        player.bonusIntel -= self.bonusIntel
        player.bonusAgi -= self.bonusAgi
        player.bonusLuck -= self.bonusLuck
        player.bonusMaxHP -= self.bonusMaxHP
        player.bonusMaxMP -= self.bonusMaxMP
        player.bonusPdmg -= self.bonusPdmg
        player.bonusMdmg -= self.bonusMdmg
        player.bonusArmor -= self.bonusArmor
        player.bonusMag_armor -= self.bonusMag_armor
        player.bonusHit -= self.bonusHit
        player.bonusDodge -= self.bonusDodge
        player.bonusCrit -= self.bonusCrit

    def giveBonusDesc(self):
        check = self.bonusStren
        if  check == self.bonusStren and check == self.bonusIntel and check == self.bonusAgi and check == self.bonusLuck :
            new = bdescMake('All Stats: ',self.bonusStren)
            e = bdescMake('HP: ',self.bonusMaxHP)
            f = bdescMake('MP: ',self.bonusMaxMP)
            g = bdescMake('PHYS: ',self.bonusPdmg)
            h = bdescMake('MAGIC: ',self.bonusMdmg)
            i = bdescMake('Armor: ',self.bonusArmor)
            j = bdescMake('Resist: ',self.bonusMag_armor)
            k = bdescMake('Hit: ',self.bonusHit)
            l = bdescMake('Dodge: ',self.bonusDodge)
            m = bdescMake('Crit: ',self.bonusCrit)
            stat_list = [new]
            hp_list = [e,f,g,h]
            armor_list = [i,j]
            hit_list = [k,l,m]
        else:
            a = bdescMake('Str: ',self.bonusStren)
            b = bdescMake('Int: ',self.bonusIntel)
            c = bdescMake('Agi: ',self.bonusAgi)
            d = bdescMake('Luk: ',self.bonusLuck)
            e = bdescMake('HP: ',self.bonusMaxHP)
            f = bdescMake('MP: ',self.bonusMaxMP)
            g = bdescMake('PHYS: ',self.bonusPdmg)
            h = bdescMake('MAGIC: ',self.bonusMdmg)
            i = bdescMake('Armor: ',self.bonusArmor)
            j = bdescMake('Resist: ',self.bonusMag_armor)
            k = bdescMake('Hit: ',self.bonusHit)
            l = bdescMake('Dodge: ',self.bonusDodge)
            m = bdescMake('Crit: ',self.bonusCrit)
            stat_list = [a,b,c,d]
            hp_list = [e,f,g,h]
            armor_list = [i,j]
            hit_list = [k,l,m]
        test_list = [bdescJoin(stat_list),bdescJoin(hp_list),bdescJoin(armor_list),bdescJoin(hit_list)]
        toDelete = [False,False,False,False]
        self.bdesc_list = []
        for index in range(4):
            if len(test_list[index]) == 0:
                toDelete[index] = True
        for index in range(4):
            if not toDelete[index]:
                   self.bdesc_list.append(test_list[index])


def bdescMake(aStat,anInteger):
    if anInteger > 0:
        amount = aStat + '+' + str(anInteger)
        return amount
    elif anInteger < 0:
        amount = aStat + str(anInteger)
        return amount
    else:
      if anInteger < 0:
        return None

def bdescJoin(aList):
    aStr = ''
    for desc in aList:
        if desc != None:
            aStr += desc + ', '
    aStr = aStr[0:(len(aStr)-2)]
##    if len(aStr) == 0:
##        aStr = 'No Bonus'def givebdesc(aList):
    return aStr

### ARMORS ###
class Armor(Item):
    def __init__(self,name,img,desc,\
                 bstr,bint,bagi,bluk,bhp,bmp,bpdmg,bmdmg,barm,bmarm,bhit,bdge,bcrt,cost):
        super(Armor,self).__init__(name,img,desc,\
                                   bstr,bint,bagi,bluk,bhp,bmp,bpdmg,bmdmg,barm,bmarm,bhit,bdge,bcrt,cost)

class Body(Armor):
    def __init__(self,name,img,desc,\
                 bstr,bint,bagi,bluk,bhp,bmp,bpdmg,bmdmg,barm,bmarm,bhit,bdge,bcrt,cost):
        super(Body,self).__init__(name,img,desc,\
                                   bstr,bint,bagi,bluk,bhp,bmp,bpdmg,bmdmg,barm,bmarm,bhit,bdge,bcrt,cost)
        self.type = 'Body'

class Head(Armor):
    def __init__(self,name,img,desc,\
                 bstr,bint,bagi,bluk,bhp,bmp,bpdmg,bmdmg,barm,bmarm,bhit,bdge,bcrt,cost):
        super(Head,self).__init__(name,img,desc,\
                                   bstr,bint,bagi,bluk,bhp,bmp,bpdmg,bmdmg,barm,bmarm,bhit,bdge,bcrt,cost)
        self.type = 'Head'

class L_hand(Armor):
    def __init__(self,name,img,desc,\
                 bstr,bint,bagi,bluk,bhp,bmp,bpdmg,bmdmg,barm,bmarm,bhit,bdge,bcrt,cost):
        super(L_hand,self).__init__(name,img,desc,\
                                   bstr,bint,bagi,bluk,bhp,bmp,bpdmg,bmdmg,barm,bmarm,bhit,bdge,bcrt,cost)
        self.type = 'Left Hand'

        
######################### WEAPONS #########################
        
class Weapon(Item):
    def __init__(self, name, img,desc,watk,wmatk,\
                 bstr,bint,bagi,bluk,bhp,bmp,bpdmg,bmdmg,barm,bmarm,bhit,bdge,bcrt,cost):
        super(Weapon,self).__init__(name, img,desc,\
                 bstr,bint,bagi,bluk,bhp,bmp,bpdmg,bmdmg,barm,bmarm,bhit,bdge,bcrt,cost)
        self.damage = watk
        self.mag_damage = wmatk
    def weapon_requirement(self):
        if self == inner:
            return player.requirement(player.LV,5)
        else:
            return True

class Sword(Weapon):
    def __init__(self, name, img,desc,watk,wmatk,\
                 bstr,bint,bagi,bluk,bhp,bmp,bpdmg,bmdmg,barm,bmarm,bhit,bdge,bcrt,cost):
        super(Sword,self).__init__(name, img,desc,watk,wmatk,\
                 bstr,bint,bagi,bluk,bhp,bmp,bpdmg,bmdmg,barm,bmarm,bhit,bdge,bcrt,cost)
        self.type = 'Sword'

class Axe(Weapon):
    def __init__(self, name, img,desc,watk,wmatk,\
                 bstr,bint,bagi,bluk,bhp,bmp,bpdmg,bmdmg,barm,bmarm,bhit,bdge,bcrt,cost):
        super(Axe,self).__init__(name, img,desc,watk,wmatk,\
                 bstr,bint,bagi,bluk,bhp,bmp,bpdmg,bmdmg,barm,bmarm,bhit,bdge,bcrt,cost)
        self.type = 'Axe'

class Wand(Weapon):
    def __init__(self, name, img,desc,watk,wmatk,\
                 bstr,bint,bagi,bluk,bhp,bmp,bpdmg,bmdmg,barm,bmarm,bhit,bdge,bcrt,cost):
        super(Wand,self).__init__(name, img,desc,watk,wmatk,\
                 bstr,bint,bagi,bluk,bhp,bmp,bpdmg,bmdmg,barm,bmarm,bhit,bdge,bcrt,cost)
        self.type = 'Wand'

class Staff(Weapon):
    def __init__(self, name, img,desc,watk,wmatk,\
                 bstr,bint,bagi,bluk,bhp,bmp,bpdmg,bmdmg,barm,bmarm,bhit,bdge,bcrt,cost):
        super(Staff,self).__init__(name, img,desc,watk,wmatk,\
                 bstr,bint,bagi,bluk,bhp,bmp,bpdmg,bmdmg,barm,bmarm,bhit,bdge,bcrt,cost)
        self.type = 'Staff'

class Dagger(Weapon):
    def __init__(self, name, img,desc,watk,wmatk,\
                 bstr,bint,bagi,bluk,bhp,bmp,bpdmg,bmdmg,barm,bmarm,bhit,bdge,bcrt,cost):
        super(Dagger,self).__init__(name, img,desc,watk,wmatk,\
                 bstr,bint,bagi,bluk,bhp,bmp,bpdmg,bmdmg,barm,bmarm,bhit,bdge,bcrt,cost)
        self.type = 'Dagger'

class Shuriken(Weapon):
    def __init__(self, name, img,desc,watk,wmatk,\
                 bstr,bint,bagi,bluk,bhp,bmp,bpdmg,bmdmg,barm,bmarm,bhit,bdge,bcrt,cost):
        super(Shuriken,self).__init__(name, img,desc,watk,wmatk,\
                 bstr,bint,bagi,bluk,bhp,bmp,bpdmg,bmdmg,barm,bmarm,bhit,bdge,bcrt,cost)
        self.type = 'Shuriken'
            
def givebdesc(aList):
    for item in aList:
        item.giveBonusDesc()
### Shop
## pg1 Weapons 
# Sword
inner = Sword('Inner','inner.png','Strong base, weak tip',16,1,\
               4, 0, 0, 0, 0, 0, 0, 0, 0, 0, -15, 0, 0, 200)
battleaxe = Axe('Battleaxe','battleaxe.png','Can chop a tree with one swing',30,2,\
                   6, 0, 0, 0, 0, 0, 0, 0, 0, 0, -20, 0, 0, 460)
katana = Sword('Katana','katana.png','A sharp sword that easily cuts',25,15,\
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 20, 450)
scimitar = Sword('Scimitar','scimitar.png','A curved and very sharp blade',29,9,
                  12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1000)
# Axe
# Wand
wand = Wand('Wand','wand.png','A wooden wand',3,7,\
            0, 5, 0, 0, 0, 10, 0, 0, 0, 0, 0, 0, 0, 225)

mag_wand = Wand('Magic Wand','mag_wand.png','A magic wand',7,17,\
            0, 14, 0, 0, 0, 20, 0, 0, 0, 0, 0, 0, 0, 450)

star_wand = Wand('Star Wand','star_wand.png','A Star wand',9,27,\
            0, 25, 0, 0, 0, 60, 0, 0, 0, 0, 0, 0, 0, 800)

element_wand = Wand('Element Wand','element_wand.png','An Elemental wand',14,50,\
            0, 42, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 1500)
# Staff
staff = Staff('Staff','staff.png','A wooden staff used by novice mages',5,9,\
               0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 250)
mag_staff = Staff('Magic Staff','mag_staff.png','A staff powered up by magic',9,21,\
                     0, 17, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 500)
star_staff = Staff('Star Staff','star_staff.png','A staff blessed by the power of the stars',10,32,\
                    0, 31, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 900)
element_staff = Staff('Elemental Staff','element_staff.png','A staff imbued with fire, wind and water',16,55,\
                       0, 47, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1600)
# Dagger
long_dag = Dagger('Long Dagger','long_dag.png','A long blade dagger',12,12,\
                  0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 25, 250)
edge_dag = Dagger('Edged Dagger','edge_dag.png','A sharper dagger',18,18,\
                  0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 28, 550)
poison_dag = Dagger('Poisoned Dagger','poison_dag.png','A dagger dipped in poison',23,23,\
                    0, 0, 12, 12, 0, 0, 0, 0, 0, 0, 0, 0, 32, 650)
balance_dag = Dagger('Balanced Dagger','balance_dag.png','Sharp and fast',32,32,\
                     15, 15, 15, 15, 0, 0, 0, 0, 0, 0, 0, 0, 38, 875)
# Shuriken

# Balanced
shortsword = Dagger('Shortsword','shortsword.png','A cheap, simple and easy to use sword',7,7,\
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 125)
longsword = Sword('Longsword','longsword.png','A standard sword used by many swordsmen',19,5,\
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 225)
tipper = Sword('Tipper','tipper.png','Strong at the tip but weak at the base',15,10,\
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 200)
def_sword = Sword('Defensive Sword','def_sword.png','Big and heavy sword',14,14,\
                   0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 325)
# Fun
fire_sword = Sword('Fire Sword','fire_sword.png','Blaze Strike: +5 ranks, -15 mana cost',35,25,\
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1250)
big_axe = Axe('Big Axe','big_axe.png','A huge axe that can cause an earthquake',70,0,\
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4500)
fruit = Axe('The Fruits of Booga','fruit.png','Fruits saved when Booga dropped them from the sky',70,70,\
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6000)
allin = Axe('All In','allin.png','HP set to 8',120,120,\
               50, 50, 50, 50, 0, 0, 0, 0, 0, 0, 0, 0, 0, 12000)
shop_weapons_1 = [inner,battleaxe,katana,scimitar,shortsword,longsword,tipper,def_sword,staff,mag_staff,star_staff,element_staff,\
       long_dag,edge_dag,poison_dag,balance_dag,fire_sword,big_axe,fruit,allin]
givebdesc(shop_weapons_1)
## pg2 Armors Body
# Warrior
bronze_body = Body('Bronze Armour','bronze_body.png','Armour made from bronze',\
                   3, 0, 0, 0, 10, 0, 0, 0, 10, 2, 0, 0, 0, 100)
iron_body = Body('Iron Armour','iron_body.png','Armour made from iron. Stronger than bronze',\
                 5, 0, 0, 0, 20, 0, 0, 0, 16, 4, 0, 0, 0, 250)
steel_body = Body('Steel Armour','steel_body.png','Armour made from Steel. Stronger than iron',\
                  9, 0, 0, 0, 30, 0, 0, 0, 30, 6, 0, 0, 0, 650)
dia_body = Body('Diamond Armour','dia_body.png','Armour made from Diamond. The strongest armour',\
                15, 0, 0, 0, 50, 0, 0, 0, 49, 9, 0, 0, 0, 1200)
# Rouge
cloak = Body('Cloak','cloak.png','A cloak made to blend in with the shadows',\
             0, 0, 5, 0, 0, 0, 0, 0, 7, 7, 0, 10, 0, 150)
black_cloak = Body('Black Cloak','black_cloak.png','A cloak darker than the night',\
                   0, 0, 8, 0, 0, 0, 0, 0, 12, 12, 5, 20, 0, 400)
stealth_cloak = Body('Stealth Cloak','stealth_cloak.png','A cloak that blends in with its surroundings',\
                     0, 0, 12, 0, 0, 0, 0, 0, 20, 20, 10, 30, 0, 1000)
ass_cloak = Body('''Assasin's Cloak''','ass_cloak.png','think ur good?',\
                 0, 0, 20, 0, 0, 0, 0, 0, 31, 31, 15, 40, 0, 1500)
# Mage
robe = Body('Robe','robe.png','A simple robe made from cloth',\
            0, 5, 0, 0, 0, 15, 0, 0, 5, 9, 0, 0, 0, 125)
mag_robe = Body("Magician's Robe",'mag_robe.png','A robe used by experienced mages',\
                0, 10, 0, 0, 0, 30, 0, 0, 8, 16, 0, 0, 0, 300)
star_robe = Body('Star Robe','star_robe.png','A robe blessed by the stars above',\
                 0, 15, 0, 0, 0, 45, 0, 0, 13, 31, 0, 0, 0, 800)
element_robe = Body('Elemental Robe','element_robe.png','A robe that gaurds the 3 elements',\
                    0, 30, 0, 0, 0, 70, 0, 0, 21, 43, 0, 0, 0, 1350)
# Balanced
leather = Body('Leather Armour','leather.png','Cheap and durable armour',\
               1, 1, 1, 1, 0, 0, 0, 0, 5, 5, 0, 0, 0, 60)
chain = Body('Chainmail','chain.png','Chains made from steel',\
             0, 0, 0, 0, 0, 0, 0, 0, 42, 6, 0, 0, 0, 900)
machine = Body('Machine','machine.png','dunno GG',\
               0, 0, 0, 0, 0, 0, 0, 0, 45, 25, 0, 0, 0, 1100)
reflect = Body('Reflector','reflect.png','Deal half of any magic dmg taken',\
               0, 0, 0, 0, 0, 0, 0, 0, 30, 100, 0, 0, 0, 3000)
# Fun
blanket = Body('Blanket','blanket.png','A blanket to sleep with',\
               1, 2, 3, 4, 8, 8, 1, 1, 2, 2, 5, 5, 5, 75)
toast = Body('Toast','toast.png','All toasters toast toast',\
             0, 0, 0, 0, 0, 0, 0, 0, 100, 0, 0, 0, 0, 4500)
smile = Body('Smile','smile.png','A smile can make you happy',\
             0, 0, 0, 0, 0, 0, 0, 0, 50, 200, 0, 0, 0, 5000)
god = Body('God of Elements','god.png','Control the elements as you will',\
           0, 0, 0, 0, 0, 0, 0, 0, 500, 800, 0, 0, 0, 10000)

shop_body_1 = [bronze_body,iron_body,steel_body,dia_body,cloak,black_cloak,stealth_cloak,ass_cloak,robe,mag_robe,star_robe,element_robe,\
       leather,chain,machine,reflect,blanket,toast,smile,god]
givebdesc(shop_body_1)

##pg3 Left hand
#mage
shld_wood = L_hand('Wooden Shield','shld_wood.png','A shield made from wood',\
                    0, 0, 0, 0, 15, 75, 0, 0, 17, 37, 0, 0, 0, 400)
shld_mana = L_hand('Mana Shield','shld_mana.png','Shield imbued with mana',\
                   0, 0, 0, 0, 30, 150, 0, 0, 48, 75, 0, 0, 0, 900)
shld_star = L_hand('Star Shield','shld_star.png','Stars is your shield',\
                   0, 0, 0, 0, 45, 450, 0, 0, 72, 134, 0, 0, 0, 1900)
shld_element = L_hand('Elemental Shield','shld_element.png','The elements gaurds you',\
                      0, 0, 0, 0, 75, 600, 0, 0, 100, 215, 0, 0, 0, 4200)
##pg4 Head(helmets)
#mage
app_hat = Head("Apprentice's Hat",'app_hat.png','A hat used by apprentices',\
              0, 5, 0, 0, 0, 0, 0, 0, 12, 40, 0, 0, 0, 500)
mage_hat = Head('Mage Hat','mage_hat.png','Experienced mages wears this',\
               0, 10, 0, 0, 0, 0, 0, 0, 32, 75, 0, 0, 0, 1100)
star_hat = Head('Star Hat','star_hat.png','This hat glows a bit',\
               0, 18, 0, 0, 0, 0, 0, 0, 60, 152, 0, 0, 0, 2500)
element_hat = Head('Element Hat','element_hat.png','Focus the elements',\
                  0, 40, 0, 0, 0, 0, 0, 0, 100, 210, 0, 0, 0, 5000)


shop_L_hand_1 = [shld_wood,shld_mana,shld_star,shld_element,\
                 app_hat,mage_hat,star_hat,element_hat,\
                 None,None,None,None,\
                 None,None,None,None,\
                 None,None,None,None]

givebdesc(shop_L_hand_1[0:8])

### FOR ALPHA USE
shop_alpha_mage1 = [wand,staff,robe,app_hat,shld_wood,\
                    mag_wand,mag_staff,mag_robe,mage_hat,shld_mana,\
                    star_wand,star_staff,star_robe,star_hat,shld_star,\
                    element_wand,element_staff,element_robe,element_hat,shld_element]
givebdesc(shop_alpha_mage1[0:20:5])

shop_pg = [shop_alpha_mage1]

#shop_pg = [shop_weapons_1,shop_body_1,shop_L_hand_1] # list in list


# Starting Weapons
fists = Axe('Fists','fists.png','Bare hands (cannot unequip)',1,1,\
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
basic_wand = Wand('Basic Wand','bas_wand.png','A basic wand',2,6,\
                    0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
basic_dag = Dagger('Basic Dagger','bas_dag.png','A basic dagger',4,4,\
                   0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
basic_sword = Sword('Basic Sword','normal.png','A basic sword',6,2,\
                     2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
# Strating armors
fap = L_hand('Left Hand','start_left.png','Fap Fap Fap (cannot unequip)',\
                  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
china_hat = Head('China Hat','start_head.png','Offers no protection (cannot unequip)',\
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
shirt_jeans = Body('Shirt and Jeans','start_body.png','Offers no protection (cannot unequip)',\
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

no_left = L_hand('Cannot Equip','no.png','Two-handed weapon equipped',\
                  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

start_items = [fap,china_hat,shirt_jeans,fists,basic_wand,basic_dag,basic_sword,no_left]
givebdesc(start_items)


        
class Potion(Item):
    def __init__(self,name,img,desc,bdesc,\
                 bstr,bint,bagi,bluk,bhp,bmp,bpdmg,bmdmg,barm,bmarm,bhit,bdge,bcrt,cost):
        super(Potion,self).__init__(name,img,desc,\
                                    bstr,bint,bagi,bluk,bhp,bmp,bpdmg,bmdmg,barm,bmarm,bhit,bdge,bcrt,cost)
        self.type = 'Potion'
        self.bdesc = bdesc
        self.num_held = 0
    def activate_eff(aPot):
        if aPot == pot_hp:
            player.restoreHP(500)
        elif aPot == pot_mp:
            player.restoreMP(400)
        elif aPot == pot_purple:
            player.restoreHP(350)
            player.restoreMP(350)
        potSound.play()
        if aPot.num_held > 1:
            aPot.num_held -= 1
        else:
            aPot.num_held -= 1
            player.numItemInv -= 1
            player.inv.remove(aPot)
            player.inv.append(None)

# Potions
pot_hp = Potion('Health Potion','pot_hp.png','A simple potion that restores health','Restore: +500 HP',\
           0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 75)
pot_mp = Potion('Mana Potion','pot_mp.png','A simple potion that restores mana','Restore: +400 MP',\
           0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 100)
pot_purple = Potion('Purple Potion','pot_purple.png','A potion that restores both health and mana','Restore: +350 HP, +350 MP',\
           0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 125)
hospital_pots = [pot_hp,pot_mp,pot_purple]
for i in range(15):
    hospital_pots.append(None)


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
        stat = round(11 + 7.5*self.LV + self.intel/3.3 + self.weapon.mag_damage + self.weapon.mag_damage*(1+self.intel/50))
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

class Rouge(Player):
    def __init__(self):
        super(Rouge,self).__init__()
        self.job = 'Rouge'
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
        return stat

class Enemy:
    def __init__(self, name, img, HP, MP, damage, mag_damage, armor, mag_armor, hit, dodge, crit, loot, exp):
        self.name = name
        self.img = pygame.image.load(img)
        self.maxHP = HP
        self.maxMP = MP
        self.HP = HP
        self.MP = MP
        self.damage = damage
        self.mag_damage = mag_damage
        self.armor = armor
        self.mag_armor = mag_armor
        self.hit = hit
        self.dodge = dodge
        self.crit = crit
        self.loot = loot
        self.exp = exp
        self.shield_hp = 0
        ## SKILLS
        self.basic = Physical('Basic Attack',None,None,'','','',0)
        self.curse = Magical('Curse',None,'curse.wav','','','',0)
        ## GENERAL
        self.fight_actives = []
        self.fight_status = []
    def randSkill(self): # All enemy attacks are in here
        skill = random.choice([self.basic,self.curse])
        return skill
    def updateSkill(self):
        self.basic.damage = self.damage
        self.basic.mana = 0
        self.curse.damage = round(10 + self.mag_damage*1.25)
        self.curse.mana = round(self.mag_damage*1.43)
        self.curse.curse_chance = 33

player = 'some Mage/Rouge/Warrior()'
enemy = 'some Enemy()'
name = ''

# place center img
def centerIMG(imgX, imgY, x, y):
    center = ((x - imgX / 2), (y - imgY / 2))
    return center

# Make a textbox
def textObj(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def textbox(msg, size, color, x, y):  # font for game is 'comicsansms'
    fontSize = pygame.font.SysFont('segoeui', size)
    textSurf, textRect = textObj(msg, fontSize, color)
    textRect.center = ((x, y))
    screen.blit(textSurf, textRect)

# Rotate an image
def rotate_img(now_direct, want_direct, img):
    rotate_time = want_direct - now_direct
    rotate_time = rotate_time * 45
    newIMG = pygame.transform.rotate(img, rotate_time)
    return newIMG

# rectangle buttons
def button(msg, msgSize, x, y, w, h, color, onColor, action, parameter):
    # print(mouse)
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    # print(click) (left click,scroll click, right click)
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, color, (x, y, w, h))
        if click[0] == 1 and parameter != None:
            action(parameter)
        elif click[0] == 1 and parameter == None:
            action()
    else:
        pygame.draw.rect(screen, onColor, (x, y, w, h))
    textbox(msg, msgSize, black, x + w / 2, y + h / 2)

def quitGame():
    pygame.quit()
    quit()

def leaveSome():
    global inSome
    inSome = False

def gameover():
    global inSome
    inSome = True
    while inSome:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
        screen.fill(white)
        textbox('You Died! Try Again?',50,black,screenW/2,325)
        textbox('(you will lose all money)',30,black,screenW/2,380)
        button('Yes',80,200,450,200,200,green,lightGreen,leaveSome,None)
        button('No',80,650,450,200,200,red,lightRed,quitGame,None)
        pygame.display.update()
    player.healFullHP()
    player.cash = 0
    time.sleep(0.5)

def status_bar():
    if player.shield_hp > 0 and inFight and not inInv and not inSome:
        textbox('Shield: %i'%player.shield_hp,50,orange,500,650)
    textbox(player.name,30,black,80,725)
    textbox(('LV %i     HP  %i / %i   MP  %i / %i' %(player.LV,player.HP,player.maxHP,player.MP,player.maxMP)),40,black,600,725)

def intro():
    global inSome
    global name
    # music
    pygame.mixer.music.play(-1)
    inSome = True
    while inSome:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                ### user input for name
                if event.unicode.isalpha():
                    if len(name) < 11:
                        name += event.unicode
                elif event.key == pygame.K_BACKSPACE:
                   name = name[:-1]
                elif event.key == pygame.K_SPACE and not len(name) == 0 and len(name) < 11:
                    name += " "
                ### user input for name
            if event.type == pygame.QUIT:
                quitGame()
        screen.fill(white)
        # Show username input
        textbox(name,50,randColor,650,420)
        # Title
        textbox('''Booga's Welcome of Fate''',80,blue,screenW/2,200)
        # ask for name
        textbox('Enter your name: ',50,red,250,420)
        # Start buttion
        button('Start',40,250,550,150,100,green,lightGreen,checkLenName,name)
        # Quit button
        button('Quit',40,650,550,150,100,red,lightRed,quitGame,None)
        pygame.display.update()

def checkLenName(name):
    if len(name.strip()) == 0:
        textbox('Please enter a name',40,black,screenW/2,500)
    else:
        instructions()

def instructions():
    global inSome
    inSome = True
    timer = 0
    while inSome:
        timer += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
        screen.fill(white)
        textbox('''INSTRUCTIONS''',50,red,screenW/2,150)
        textbox('''Use WASD keys to move, press the 1 key to see your inventory''',30,black,screenW/2,screenH/2-100)
        textbox('''Press the 2 key to see your stats, the 3 Key to see your skills''',30,black,screenW/2,screenH/2-55)
        textbox('''If something has                           use A and D to use the arrows''',30,black,screenW/2,screenH/2)
        screen.blit(small_arrow_left,centerIMG(30,30,390,385))
        screen.blit(small_arrow_right,centerIMG(30,30,465,385))
        if timer >= 180:
            button('OKAY',30,screenW/2-50,550,100,100,green,lightGreen,instructions_2,None)
        pygame.display.update()

def instructions_2():
    global inSome
    inSome = True
    timer = 0
    while inSome:
        timer += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
        screen.fill(white)
        screen.blit(pygame.image.load('instruct_1.png',),(0,0))
        if timer >= 80:
            button('OKAY',30,screenW/2-26,525,100,100,green,lightGreen,leaveSome,None)
        pygame.display.update()

def stats():
    player.statUpdate()
    global inSome
    inSome = True
    while inSome:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
        screen.fill(white)
        # str
        button('+',50,150,100,75,75,cyan,lightCyan,player.add_stat,'s')
        button('-',50,50,100,75,75,cyan,lightCyan,player.rem_stat,'s')
        textbox('Strength: %i. Increases max HP, increases Physical Damage, slightly increases Armor'%player.stren,22,black,screenW/2,75)
        # int
        button('+',50,150,250,75,75,cyan,lightCyan,player.add_stat,'i')
        button('-',50,50,250,75,75,cyan,lightCyan,player.rem_stat,'i')
        textbox('Intelligence: %i. Increases max MP, increases Magical Damage, slightly increases Resist'%player.intel,22,black,screenW/2,225)
        # agi
        button('+',50,150,425,75,75,cyan,lightCyan,player.add_stat,'a')
        button('-',50,50,425,75,75,cyan,lightCyan,player.rem_stat,'a')
        textbox('Agility: %i. Slightly increases both max HP/MP, increases Crit Rate and Dodge Rate'%player.agi,22,black,screenW/2,400)
        # luck
        button('+',50,150,575,75,75,cyan,lightCyan,player.add_stat,'l')
        button('-',50,50,575,75,75,cyan,lightCyan,player.rem_stat,'l')
        textbox('Luck: %i. Slightly increases many different factors, generally gives good fortune'%player.luck,22,black,screenW/2,550)
        # AP
        textbox(('AP (Ability Points) Available: %i' %player.AP),30,black,700,320)
        # Finished
        if player.AP == 0:
            button('Continue',30,850,screenH/1.35,75,75,green,lightGreen,leaveSome,None)
        status_bar()
        pygame.display.update()
        clock.tick(15)


def selected_job(selected_job):
    global player
    global inSome
    global name
    if selected_job == 'Mage':
        player = Mage()
        player.name = name
        inSome = False
        del name
    elif selected_job == 'Warrior':
        textbox('Available soon!',80,black,screenW/2,200)
        #player = Warrior()
    else:
        textbox('Available soon!',80,black,screenW/2,200)
        #player = Rouge()
    

def job_select():
    global inSome
    inSome = True
    while inSome:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
        screen.fill(white)
        textbox('Select Your Job',100,black,screenW/2,100)
        button('Mage',40,85,275,250,250,blue,lightBlue,selected_job,'Mage')
        button('Rouge',40,385,275,250,250,green,lightGreen,selected_job,'Rouge')
        button('Warrior',40,685,275,250,250,red,lightRed,selected_job,'Warrior')
        textbox('Mage: Excels with magic, high MP and Magical DMG but low HP, armor, and physical dmg',23,lightBlue,screenW/2,600)
        textbox('Rouge: Fast and sharp, high crit and dodge but low HP and defense',23,lightGreen,screenW/2,650)
        textbox('Warrior: Strong and sturdy, high physical dmg and armor but low hit chance and weak to magic',23,lightRed,screenW/2,700)
        pygame.display.update()

def statsPage():
    player.statUpdate()
    global inSome
    inSome = True
    while inSome:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_2:
                    inSome = False
        screen.fill(cyan)
        status_bar()
        textbox('STATS',60,lightRed,screenW/2,40)
        textbox('LV: %i'%player.LV,35,black,screenW/2,100)
        textbox('Job: %s'%player.job,35,red,screenW/2,140)
        textbox('Strength: %i + %i = %i'%(player.new_stren,player.bonusStren,player.stren),35,yellow,screenW/2,140+40)
        textbox('Intelligence: %i + %i = %i'%(player.new_intel,player.bonusIntel,player.intel),35,yellow,screenW/2,180+40)
        textbox('Agility: %i + %i = %i'%(player.new_agi,player.bonusAgi,player.agi),35,yellow,screenW/2,220+40)
        textbox('Luck: %i + %i = %i'%(player.new_luck,player.bonusLuck,player.luck),35,yellow,screenW/2,260+40)
        textbox('Max HP: %i + %i = %i'%(player.maxHPU(),player.bonusMaxHP,player.maxHP),35,red,screenW/2,300+40)
        textbox('Max MP: %i + %i = %i'%(player.maxMPU(),player.bonusMaxMP,player.maxMP),35,blue,screenW/2,340+40)
        textbox('Physical Damage: %i + %i = %i'%(player.damageU(),player.bonusPdmg,player.damage),35,red,screenW/2,300+120)
        textbox('Magic Damage: %i + %i = %i'%(player.mag_damageU(),player.bonusMdmg,player.mag_damage),35,blue,screenW/2,340+120)
        textbox('Armor: %i + %i = %i'%(player.armorU(),player.bonusArmor,player.armor),35,red,screenW/2,380+120)
        textbox('Resist: %i + %i = %i'%(player.mag_armorU(),player.bonusMag_armor,player.mag_armor),35,blue,screenW/2,420+120)
        textbox('Hit Rate: %i%% + %i%% = %i%%'%(player.hitU(),player.bonusHit,player.hit),35,red,screenW/2,460+120)
        textbox('Dodge Chance: %i%% + %i%% = %i%%'%(player.dodgeU(),player.bonusDodge,player.dodge),35,blue,screenW/2,500+120)
        textbox('Critical Chance: %i%% + %i%% = %i%%'%(player.critU(),player.bonusCrit,player.crit),35,red,screenW/2,540+120)
        textbox('Experience: %i / %i'%(player.exp,player.max_exp),35,yellow,screenW/2,570+120)
        textbox('''Press 2 to leave''',30,brown,875,screenH/2)
        pygame.display.update()
        
def checkEquip(slot):
    if isinstance(slot,Weapon) and slot is not player.weapon and slot != player.weapon: # and player.weapon == fists
        if isinstance(slot,Staff): # two handed weapon
            if player.lefthand != fap:
                player.lefthand.noBonus()
                player.inv[player.numItemInv] = player.lefthand
                player.numItemInv += 1
            player.lefthand = no_left
        else:
            if player.lefthand == no_left:
                player.lefthand = fap
        if slot.weapon_requirement():
            saved_item = None
            if player.weapon != fists and slot != player.weapon: # if has weapon equipped already
                saved_item = player.weapon
                player.weapon.noBonus()
            player.weapon = slot
            player.weapon.addBonus()
            player.numItemInv -= 1
            player.inv.remove(slot)
            player.inv.append(None)
            if saved_item != None:   # put weapon in inv
                player.inv[player.numItemInv] = saved_item
                player.numItemInv += 1
            sound = pygame.mixer.Sound('atk4.wav')
            sound.play()
            time.sleep(0.3)
        else:
            textbox('Requirements not met!',50,black,500,500)
    # remove weapon
    elif slot is player.weapon and player.weapon != fists and player.numItemInv < player.numMaxItem:
        if isinstance(slot,Staff):
            player.lefthand = fap
        player.weapon.noBonus()
        player.inv[player.numItemInv] = player.weapon
        player.numItemInv += 1
        player.weapon = fists
        sound = pygame.mixer.Sound('atk4.wav')
        sound.play()
    # put body on
    elif isinstance(slot,Body) and slot is not player.body: #and player.body == shirt_jeans
        saved_item = None
        if player.body != shirt_jeans and slot != player.body: # if has weapon equipped already
            saved_item = player.body
            player.body.noBonus()
        player.body = slot
        player.body.addBonus()
        player.numItemInv -= 1
        player.inv.remove(slot)
        player.inv.append(None)
        if saved_item != None:   # put weapon in inv
            player.inv[player.numItemInv] = saved_item
            player.numItemInv += 1
        wear.play()
        time.sleep(0.3)
    # remove body
    elif slot == player.body and player.body != shirt_jeans and slot not in player.inv and player.numItemInv < player.numMaxItem:
        player.body.noBonus()
        player.inv[player.numItemInv] = player.body
        player.numItemInv += 1
        player.body = shirt_jeans
        wear.play()
    # put on l_hand
    elif isinstance(slot,L_hand) and slot is not player.lefthand and player.lefthand != no_left:
        saved_item = None
        if player.lefthand != fap and slot != player.lefthand: # if has weapon equipped already
            saved_item = player.lefthand
            player.lefthand.noBonus()
        player.lefthand = slot
        player.lefthand.addBonus()
        player.numItemInv -= 1
        player.inv.remove(slot)
        player.inv.append(None)
        if saved_item != None:   # put weapon in inv
            player.inv[player.numItemInv] = saved_item
            player.numItemInv += 1
        wear.play()
        time.sleep(0.3)
    #remove l_hand
    elif slot == player.lefthand and player.lefthand != fap and player.lefthand != no_left and slot not in player.inv and player.numItemInv < player.numMaxItem:
        player.lefthand.noBonus()
        player.inv[player.numItemInv] = player.lefthand
        player.numItemInv += 1
        player.lefthand = fap
        wear.play()
    # put on hat
    elif isinstance(slot,Head) and slot is not player.head:
        saved_item = None
        if player.head != china_hat and slot != player.head: # if has weapon equipped already
            saved_item = player.head
            player.head.noBonus()
        player.head = slot
        player.head.addBonus()
        player.numItemInv -= 1
        player.inv.remove(slot)
        player.inv.append(None)
        if saved_item != None:   # put weapon in inv
            player.inv[player.numItemInv] = saved_item
            player.numItemInv += 1
        wear.play()
        time.sleep(0.3)
    # remove on hat
    elif slot == player.head and player.head != china_hat and slot not in player.inv and player.numItemInv < player.numMaxItem:
        player.head.noBonus()
        player.inv[player.numItemInv] = player.head
        player.numItemInv += 1
        player.head = china_hat
        wear.play()
    # use potion
    if isinstance(slot,Potion) and not inFight:
        # all pot activation effects
        Potion.activate_eff(slot)
        time.sleep(0.3)
    player.statUpdate()
    skillUpdate()
    trimExtraHPMP()

def trimExtraHPMP():
    if player.HP > player.maxHP:
        player.HP = player.maxHP
    if player.MP > player.maxMP:
        player.MP = player.maxMP

def slotButton(slot,x,y,w,h):
    global inInv
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
##    player.skillUpdate()
    #print(click) (left click,scroll click, right click)
    if inSkill or inLearnSkill: # skill page shows if requirement is met
        if slot != None:
            if slot.skill_requirement():
                if x+w > mouse[0] > x and y+h > mouse[1] > y:  # show box and highlight when mouse hovers over
                    pygame.draw.rect(screen, green, (x,y,w,h))
                else:
                    pygame.draw.rect(screen, lightGreen, (x,y,w,h))
            else:
                if x+w > mouse[0] > x and y+h > mouse[1] > y:  # show box and highlight when mouse hovers over
                    pygame.draw.rect(screen, orange, (x,y,w,h))
                else:
                    pygame.draw.rect(screen, brown, (x,y,w,h))
    elif inFight and not inInv: # some reason when using skill the boxes show up so i use this to not show boxes after using skill (?????????????????)
        if slot != None:
            if x+w > mouse[0] > x and y+h > mouse[1] > y:  # show box and highlight when mouse hovers over
                pygame.draw.rect(screen, green, (x,y,w,h))
            else:
                pygame.draw.rect(screen, lightGreen, (x,y,w,h))
    else:
        if x+w > mouse[0] > x and y+h > mouse[1] > y:  # show box and highlight when mouse hovers over
            pygame.draw.rect(screen, green, (x,y,w,h))
        else:
            pygame.draw.rect(screen, lightGreen, (x,y,w,h))
    # Show images
    if slot != None:
        screen.blit(slot.img,centerIMG(80,80,x+w/2,y+h/2))
    # When mouse hover slot box
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        if inSkill or inLearnSkill:
            if not inFight or enemy.HP <= 0:
                if slot != None:
                    itemValue(slot)
                if pygame.mouse.get_pressed()[0]:
                    # rank up skill
                    if not inFight or enemy.HP <= 0:
                        if player.SP > 0 and slot != None:
                            if player.numLearnedSkills != player.numMaxSkills:
                                if slot.skill_requirement():
                                    if slot.rank == 0 or slot not in player.learned_skills: # add skill into leanred skill
                                        player.learned_skills[player.numLearnedSkills] = slot
                                        player.numLearnedSkills += 1
                                    if not slot.rank == slot.maxRank:    
                                        slot.rank += 1
                                        player.SP -= 1
                                        rank_up.play()
                                        time.sleep(0.16)
                                        skillUpdate()
                                        if isinstance(slot,Passive):
                                            slot.giveBonus()
                                            player.statUpdate()
                                            skillUpdate()
                                    else:
                                        textbox('Skill at max rank!',35,blue,800,235)
                                else:
                                    textbox('Requirements not met!',35,blue,800,235)
                            elif slot in player.learned_skills:
                                if not slot.rank == slot.maxRank:    
                                    slot.rank += 1
                                    player.SP -= 1
                                    rank_up.play()
                                    time.sleep(0.16)
                                    skillUpdate()
                                    if isinstance(slot,Passive):
                                        slot.giveBonus()
                                        player.statUpdate()
                                        skillUpdate()
                                else:
                                    textbox('Skill at max rank!',35,blue,800,235)
                            else:
                                textbox('Maximum number of skills learned!',35,blue,800,235)
                        else:
                            if  slot != None and not slot.skill_requirement():
                                textbox('Requirements not met!',35,blue,800,235)
                            elif slot != None:
                                    textbox('Not enough SP!',50,blue,800,235)
                elif pygame.mouse.get_pressed()[2] and inLearnSkill and slot != None: # Remove a skill
                    removeSkill(slot)
            else: # inFight use skill
                if slot != None:
                    itemValue(slot)
                    if pygame.mouse.get_pressed()[0]:
                        if hasattr(slot,'cooldownEnd'):
                            if slot.cooldownEnd <= fight_turn:
                                del slot.cooldownEnd
                            else:
                                textbox('On cooldown! %i Turns Left'%(slot.cooldownEnd - fight_turn),30,blue,800,235)
                        elif player.MP - slot.mana < 0: # check if player has enough mana
                            textbox('Not enough MP!',50,blue,800,235)
                        else:
                            if isinstance(slot,Active):
                                if slot in player.fight_actives:
                                    textbox('Already active!',50,blue,800,235)
                                else:
                                    dmg_calc(slot)
                            elif isinstance(slot,Passive):
                                textbox('Cannot use Passive!',50,blue,800,235)
                            else:
                                dmg_calc(slot) # regular attack
        elif inInv:
            if slot != None:
                itemValue(slot)
            if not inFight:
                if pygame.mouse.get_pressed()[0]:
                    checkEquip(slot)
                # Sell Item
                elif not inFight and pygame.mouse.get_pressed()[2] and slot in player.inv and slot is not player.weapon and slot is not player.body and\
                     slot is not player.lefthand and slot is not player.head and slot != None:
                        sellItem(slot)
            else: # in fight potion/equip mechanic
                if pygame.mouse.get_pressed()[0] and slot in player.inv and slot is not player.weapon and slot is not player.body and\
                                                     slot is not player.lefthand and slot is not player.head and slot != None:
                    checkEquip(slot)
                    inInv = False
                    dmg_calc(slot)
        elif inHosp:
            if slot != None:
                itemValue(slot)
            if pygame.mouse.get_pressed()[0]:
                if player.numItemInv == player.numMaxItem:
                    textbox('Full inventory!',30,red,screenW/2,800)
                else:
                    buyItem(slot)
        elif inStore:
            itemValue(slot)
            if pygame.mouse.get_pressed()[0]:
                if player.numItemInv == player.numMaxItem:
                    textbox('Full inventory!',30,red,775,425)
                elif slot in player.inv or slot in [player.head,player.weapon,player.body,player.lefthand]:
                    textbox('You already have one!',30,red,775,425)
                else:
                    buyItem(slot)

def removeSkill(slot):
    asking = True
    while asking:
        screen.fill(brown)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    player.learned_skills.remove(slot)
                    player.learned_skills.append(None)
                    player.numLearnedSkills -= 1
                    sound = pygame.mixer.Sound('buy.wav')
                    sound.play()
                    asking = False
                elif event.key == pygame.K_e:
                    asking = False
        textbox('Remove this skill?',65,black,screenW/2,200)
        textbox('(You can relearn it by ranking it up)',65,black,screenW/2,440)
        textbox('%s'%slot.name,80,blue,screenW/2,315)
        textbox('Press (Q: Yes /E: No)',65,black,screenW/2,550)
        pygame.display.update()

def sellItem(slot):
    global inSome
    want = True
    sell_price = round(slot.cost/2)
    while want:
        screen.fill(brown)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    if isinstance(slot,Potion) and slot.num_held > 1:
                            slot.num_held -= 1
                            player.cash += sell_price
                    else:
                        player.cash += sell_price
                        player.inv.remove(slot)
                        player.inv.append(None)
                        player.numItemInv -= 1
                    sound = pygame.mixer.Sound('buy.wav')
                    sound.play()
                    want = False
                elif event.key == pygame.K_e:
                    want = False
        textbox('Are you sure you want to sell this?',65,black,screenW/2,200)
        textbox('%s'%slot.name,80,blue,screenW/2,315)
        textbox('$%i + $%i = $%i'%(player.cash,sell_price,(player.cash+sell_price)),65,black,screenW/2,440)
        textbox('Press (Q: Yes /E: No)',65,black,screenW/2,550)
        pygame.display.update()

def addItem(item):
    # potion can have multiple held
    if isinstance(item,Potion):
        if item not in player.inv:
            player.inv[player.numItemInv] = item
            player.numItemInv += 1
            item.num_held += 1
        else:
            item.num_held += 1
    else:
        player.inv[player.numItemInv] = item
        player.numItemInv += 1

def buyItem(slot):
    global inSome
    if player.cash < slot.cost:
        textbox('Not enough gold!',30,blue,775,425)
    else:
        want = True
        while want:
            screen.fill(lime)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quitGame()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        player.cash -= slot.cost
                        addItem(slot)
                        buySound.play()
                        want = False
                    elif event.key == pygame.K_e:
                        want = False
            textbox('Are you sure you want to buy this?',65,black,screenW/2,200)
            textbox('%s'%slot.name,80,red,screenW/2,315)
            textbox('$%i - $%i = $%i'%(player.cash,slot.cost,(player.cash-slot.cost)),65,black,screenW/2,440)
            textbox('Press (Q: Yes /E: No)',65,black,screenW/2,550)
            status_bar()
            pygame.display.update()

def itemValue(slot):
    if inStore and not inInv and slot != None: # IN STORE DETAILS
        textbox(slot.name,60,black,775,125)
        textbox('%s (%s)'%(slot.desc,slot.type),20,black,775,185)
        if isinstance(slot,Weapon):
            textbox('ATK: %i/MATK: %i Cost: $%i'%(slot.damage,slot.mag_damage,slot.cost),32,black,775,228)
        elif isinstance(slot,Armor):
            textbox('Cost: $%i'%slot.cost,32,black,775,228)
        if len(slot.bdesc_list) == 0:
            textbox('No Bonus',25,black,775,275)
        else:
            y = 0
            for index in range(len(slot.bdesc_list)):
                textbox(slot.bdesc_list[index],25,black,780,275+y)
                y += 35
    elif inSkill or inLearnSkill:
            textbox(slot.name,75,black,800,100)
            textbox(slot.desc,30,black,800,175)
            textbox('Rank: %i/%i (%s)'%(slot.rank,slot.maxRank,slot.type),40,black,800,300)
            if isinstance(slot,Physical):
                textbox('Physical Damage: %i, Mana Cost: %i'%(slot.damage,slot.mana),25,black,800,400)
            elif isinstance(slot,Magical):
                textbox('Magic Damage: %i, Mana Cost: %i'%(slot.damage,slot.mana),25,black,800,400)
            elif isinstance(slot,Active) or isinstance(slot,Passive): # actives have unique detail
                textbox('%s'%(slot.detail),20,black,800,400)
            textbox(slot.effdesc,20,black,800,475)
            if len(slot.requiredesc) != 0:
                textbox('Requirement(s):  (%s)'%slot.requiredesc,16,black,800,540)
    elif inInv:
        if isinstance(slot,Weapon):
            textbox('ATK: %i/MATK: %i Cost: $%i'%(slot.damage,slot.mag_damage,slot.cost),35,black,300,430)
        elif isinstance(slot,Armor):
            textbox('Cost: $%i'%(slot.cost),35,black,300,430)
        elif isinstance(slot,Potion):
            textbox('Held: x%i /Cost: $%i'%(slot.num_held,slot.cost),35,black,300,430)
            textbox(slot.bdesc,30,black,300,480)
        if slot != None:
            textbox(slot.name,60,black,300,325)
            textbox('%s (%s)'%(slot.desc,slot.type),25,black,300,385)
            if not isinstance(slot,Potion):
                if len(slot.bdesc_list) == 0:
                    textbox('No Bonus',30,black,300,480)
                else:
                    y = 0
                    for index in range(len(slot.bdesc_list)):
                        textbox(slot.bdesc_list[index],30,black,300,480+y)
                        y += 45
    elif inHosp:
        if slot != None:
            textbox(slot.name,65,black,screenW/2,50)
            textbox('%s (%s)'%(slot.desc,slot.type),40,black,screenW/2,110)
            textbox('Cost: $%i'%(slot.cost),40,black,screenW/2,175)
            textbox(slot.bdesc,40,black,screenW/2,250)


def leaveLearnSkill():
    global inLearnSkill
    inLearnSkill = False
    if not inFight or inLearnSkill:
        time.sleep(0.3)

def learnedSkillsPage():
    time.sleep(0.2)
    player.statUpdate()
    global inLearnSkill
    inLearnSkill = True
    while inLearnSkill:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
            elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_3 and inFight:
                        leaveLearnSkill()
        screen.fill(grey)
        textbox('Learned Skills',60,black,280,50)
        if player.learned_skills[0] == None:
            textbox('Learn skills by ranking them up using SP!',50,black,screenW/2,screenH/2)
        if not inFight or enemy.HP >= 0:
            textbox('SP: %i'%player.SP,50,black,905,630)
            textbox('Hover over a skill and right click to remove the skill',20,black,300,685)
            button('Leave',30,660,575,100,100,red,lightRed,leaveLearnSkill,None)
        else:
            textbox('Press 3 to leave',20,black,300,680)
        matrixSlot(4,4,player.learned_skills,40,125,140,140)
        status_bar()
        pygame.display.update()

def skillsPage():
    player.statUpdate()
    skillUpdate()
    global inSkill
    inSkill = True
    pg_num = 0
    while inSkill:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_3:
                    inSkill = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        if pg_num - 1 >= 0:
                            pg_num -= 1
                            pg_flip.play()
                    elif event.key == pygame.K_d:
                        if pg_num + 1 <= len(mage_skills_pg) - 1:
                            pg_num += 1
                            pg_flip.play()
        screen.fill(grey)
        textbox('%s Skills'%player.job,60,black,280,50)
        if player.job == 'Mage':
            matrixSlot(4,4,mage_skills_pg[pg_num],40,125,140,140)
        textbox('SP: %i'%player.SP,50,black,905,630)
        textbox('Press 3 to leave',20,black,300,680)
        button('Learned Skills',30,660,575,100,100,red,lightRed,learnedSkillsPage,None)
        if pg_num - 1 >= 0:
            screen.blit(small_arrow_left,centerIMG(30,30,25,75))
        if pg_num + 1 <= len(mage_skills_pg) - 1:
            screen.blit(small_arrow_right,centerIMG(30,30,550,75))
        status_bar()
        pygame.display.update()

def enemyAttack():
    fakeFight()
    fight_shown_text = []
    enemy.updateSkill()
    used_skill = enemy.randSkill()
    if not enemy.isPara:
        if enemy.MP - used_skill.mana < 0:
            used_skill = basic_attack
        damage = Action.skillAttack(enemy, player,used_skill)
        if damage != None:
            fight_shown_text.append(['Enemy uses %s'%used_skill.name,black])
            if enemy.didCrit:
                fight_shown_text.append(['Enemy critically strikes!',blue])
                crit.play()
            if isinstance(used_skill,Physical):
                fight_shown_text.append(['Enemy deals %i physical damage'%(damage),red])
            else:
                fight_shown_text.append(['Enemy deals %i magical damage'%(damage),red])
            # Status
            status_eff  = used_skill.status_effect(player)
            if status_eff == st_burn:
                fight_shown_text.append(['You are burned!',orange])
            elif status_eff == st_para:
                fight_shown_text.append(['You are paralyzed!',yellow])
            elif status_eff == st_curse:
                fight_shown_text.append(['You are cursed!',brown])
        else:
            fight_shown_text.append(['Enemy Misses!',orange])
        for status in player.fight_status:
            if status == st_burn:
                burn_damage = status_calc(st_burn,player)
                fight_shown_text.append(['You take %i burn damage'%burn_damage,lightRed])
            elif status == st_para:
                status_calc(st_para,player)
            elif status == st_curse:
                curse_damage = status_calc(st_curse,player)
                fight_shown_text.append(['You take %i curse damage'%curse_damage,lightRed])
        addFightDetailText(fight_shown_text)
        pygame.display.update()
    else:
        fight_shown_text.append(["Enemy can't move!",lightYellow])
        addFightDetailText(fight_shown_text)
        pygame.display.update()

def doNone():
    None

def fakeFight():
    screen.fill(white)
    textbox('%s'%enemy.name,40,black,800,175)
    textbox('HP: %i'%(enemy.HP),45,lightRed,800,520)
    textbox('MP: %i'%(enemy.MP),45,lightBlue,800,580)
    button('Attack',35,25,350,100,100,green,lightGreen,doNone,None)
    button('Skills',35,150,350,100,100,red,lightRed,doNone,None)
    button('Run',30,275,375,75,75,red,lightRed,doNone,None)
    screen.blit(player.img,(425,355))
    screen.blit(enemy.img, centerIMG(255,255,800,350))
    textbox('Turn: %i'%(fight_turn),25,black,330,340)
    showActivesAndStatus()
    status_bar()

def status_calc(status,victim):
    if status == st_burn:
        burn_damage = round(victim.maxHP/10 - random.choice(range(round(10 + victim.maxHP/100))) + random.choice(range(10 + round(victim.maxHP/80))))
        victim.HP -= burn_damage
        return burn_damage
    elif status == st_para:
        if 50 >= random.choice(range(101)):
            victim.isPara = True
        else:
            victim.isPara = False
    elif status == st_curse:
        curse_damage = round(victim.maxHP/20 - random.choice(range(round(10 +  victim.maxHP/75))) + random.choice(range(10 + round(victim.maxHP/80)))) 
        victim.HP -= curse_damage
        return curse_damage
    
def dmg_calc(used_skill):
    leaveLearnSkill()
    global fight_turn
    global text_detail_pg_num
    global inLearnSkill
    fight_turn += 1
    text_detail_pg_num = 1
    fight_shown_text = []
    success_run = None
    enemy.isPara = False
    if used_skill == 'run': # Run
        fight_shown_text.append(['You are trying to run away...',black])
        success_run = runChance()
        if not success_run:
            fight_shown_text.append(['You failed to run away!',blue])
            addFightDetailText(fight_shown_text)
        else:
            player.run_away = True
    elif isinstance(used_skill,Armor) or isinstance(used_skill,Weapon): # equip an item
        fight_shown_text.append(['You equipped %s'%used_skill.name,black])
        
    elif isinstance(used_skill,Magical) or isinstance(used_skill,Physical): # Skill
        fight_shown_text.append(['You use %s'%used_skill.name,black])
        damage = Action.skillAttack(player,enemy,used_skill)
        if damage != None:
            if player.didCrit:
                fight_shown_text.append(['You critically strike!',blue])
                crit.play()
            if isinstance(used_skill,Magical):
                fight_shown_text.append(['You deal %i magical damage'%damage,red])
            else: #isinstance(used_skill,Physical)
                fight_shown_text.append(['You deal %i physical damage'%damage,red])
            # Status
            status_eff  = used_skill.status_effect(enemy)
            if status_eff == st_burn:
                fight_shown_text.append(['You burned the enemy!',orange])
            elif status_eff == st_para:
                fight_shown_text.append(['You paralyzed the enemy!',yellow])
        else:
            fight_shown_text.append(['You Missed!',blue])
    elif isinstance(used_skill,Active):
        fight_shown_text.append(['You use %s'%used_skill.name,black])
        Action.skillActive(player,enemy,used_skill)
    elif isinstance(used_skill,Potion):
        fight_shown_text.append(['You use %s'%used_skill.name,black])
        Potion.activate_eff(used_skill)
    # status effects (status should be last effect that happens)
    for status in enemy.fight_status:
        if status == st_burn:
            burn_damage = status_calc(st_burn,enemy)
            fight_shown_text.append(['Enemy takes %i burn damage'%burn_damage,lightRed])
        elif status == st_para:
            status_calc(st_para,enemy)
        elif status == st_curse:
            curse_damage = status_calc(st_curse,enemy)
            fight_shown_text.append(['Enemy takes %i curse damage'%curse_damage,lightRed])
    if enemy.HP <= 0:
        fight_shown_text.append(['You have defeated the enemy!',brown])
    # refresh
    fakeFight()
    addFightDetailText(fight_shown_text)
    fightDetailText(text_detail_pg_num)
    pygame.display.update()
    time.sleep(1.1)
    # counter attack
    if enemy.HP > 0 and not success_run: # enemy counter attack
        enemyAttack()
    checkActiveDuration()    # ACTIVE DURATION LOSE EFFECT HERE

def checkActiveDuration():
    for skill in player.fight_actives:
        if hasattr(skill,'turnEnd') and fight_turn == skill.turnEnd:
            skill.loseEffect()
            player.fight_actives.remove(skill)

def addFightDetailText(aList):
    global fight_detail_text_list
    del fight_detail_text_list[0]
    fight_detail_text_list.append([['',black],['',black],['',black],['',black],['',black],['',black]])
    for text in aList:
        del fight_detail_text_list[1][0]
        fight_detail_text_list[1].append(text)
    

def fightDetailText(pg_num): # There are 2 pages with 6 textboxes
    textbox(fight_detail_text_list[pg_num][0][0],27,fight_detail_text_list[pg_num][0][1],350,25)
    textbox(fight_detail_text_list[pg_num][1][0],27,fight_detail_text_list[pg_num][1][1],350,75)
    textbox(fight_detail_text_list[pg_num][2][0],28,fight_detail_text_list[pg_num][2][1],350,125)
    textbox(fight_detail_text_list[pg_num][3][0],32,fight_detail_text_list[pg_num][3][1],350,175)
    textbox(fight_detail_text_list[pg_num][4][0],37,fight_detail_text_list[pg_num][4][1],350,225)
    textbox(fight_detail_text_list[pg_num][5][0],45,fight_detail_text_list[pg_num][5][1],350,275)#290

def level_up_greet():
    screen.fill(yellow)
    textbox('You leveled up!',75,black,screenW/2,screenH/2)
    pygame.mixer.music.load('complete.mp3')
    pygame.mixer.music.load('complete.mp3')
    pygame.mixer.music.play(0)
    pygame.display.update()
    time.sleep(1.75)

def fight():
    global inFight
    global enemy
    global fight_detail_text_list
    global fight_turn
    global text_detail_pg_num
    text_detail_pg_num = 1
    fight_turn = 0
    fight_detail_text_list = [[['',black],['',black],['',black],['',black],['',black],['',black]],\
                              [['',black],['',black],['',black],['',black],['',black],['',black]]]
    player.statUpdate()
    skillUpdate()
    player.run_away = False
    # resets
    player.fight_actives = []
    player.fight_status = []
    player.shield_hp = 0
    resetCooldown()
    #Enemy(self, name, img, HP,MP, damage,mag_damage, armor,mag_armor, hit,dodge,crit, loot,exp):
    #Low level mobs
    alec = Enemy('Alec','alec.png',300,400, 70,100, 25,40, 95,5,5, 25,10)
    sungmin = Enemy('Sungmin','sungmin.png',400,75, 80,55, 25,25, 95,5,4, 30,15)
    kaelan = Enemy('Kaelan','kaelan.png',425,40, 85,25, 40,10, 95,5,4, 35,17)
    #Medium level mobs
    alicky = Enemy('Alicky','alec.png',1500,500, 180,300, 200,200, 90,5,5, 125,100)
    sunger = Enemy('Sunger Munger','sungmin.png',1635,500, 200,250, 450,450, 92,5,5, 135,125)
    brownitron = Enemy('Brownitron','kaelan.png',1825,800, 250,175, 300,300, 87,5,4, 150,150)
    ryan = Enemy('Ryan','ryan.png',1369,30, 100,5, 0,0, 120,50,50, 175,125)
    tina = Enemy('Tina','tina.png',3750,1000, 50,100, 300,600, 85,10,6, 200,100)
    #High level mobs
    laluche = Enemy('La Lucha Libre','ryan.png',5000,100, 300,10, 0,0, 150,55,75, 400,150)
    dyonghae = Enemy('Dyonghae','tina.png',8000,4000, 400,800, 700,900, 95,5,5, 200,300)
    greasy_booga = Enemy('Greasy Booga','greasy_booga.png',11000,1200, 600,1000, 800,800, 85,20,20, 500,300)
    # Choose random enemy
    if player.LV < 5:
        enemy = random.choice([alec,sungmin,kaelan])
    elif player.LV < 11:
        enemy = random.choice([ryan,brownitron,sunger,alicky,tina])
    else:
        enemy = random.choice([laluche,dyonghae,greasy_booga])
    ### Music
    pygame.mixer.music.load(random.choice(['bgm_fight1.mp3','bgm_fight2.mp3','bgm_fight3.mp3',\
                                           'bgm_fight4.mp3','bgm_fight5.mp3','bgm_fight6.mp3','bgm_fight7.mp3']))
    pygame.mixer.music.play(-1)
    ##############################
    inFight = True
    time.sleep(0.5)
    while inFight: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    inventory()
                elif event.key == pygame.K_2:
                    statsPage()
                elif event.key == pygame.K_a:
                    if text_detail_pg_num - 1 >= 0:
                        text_detail_pg_num -= 1
                        pg_flip.play()
                elif event.key == pygame.K_d:
                    if text_detail_pg_num + 1 < 2:
                        text_detail_pg_num += 1
                        pg_flip.play()
        if enemy.HP <= 0:
            player.cash += enemy.loot
            player.exp += enemy.exp
            if player.exp >= player.max_exp:
                level_up_greet()
                player.level_up()
                skillsPage()
                fightAgain()
            else:
                fightAgain()
        if player.run_away:
            leaveFight()
        if player.HP <= 0:
            gameover()
        # refresh
        screen.fill(white)
        textbox('%s'%enemy.name,40,black,800,175)
        textbox('HP: %i'%(enemy.HP),45,lightRed,800,520)
        textbox('MP: %i'%(enemy.MP),45,lightBlue,800,580)
        button('Attack',35,25,350,100,100,green,lightGreen,dmg_calc,basic_attack)
        button('Skills',35,150,350,100,100,red,lightRed,learnedSkillsPage,None)
        button('Run',30,275,375,75,75,red,lightRed,dmg_calc,'run')
        screen.blit(player.img,(425,355))
        screen.blit(enemy.img, centerIMG(255,255,800,350))
        textbox('Turn: %i'%(fight_turn),25,black,330,340)
        if text_detail_pg_num - 1 >= 0:
            screen.blit(small_arrow_left,centerIMG(30,30,60,150))
        if text_detail_pg_num + 1 < 2:
            screen.blit(small_arrow_right,centerIMG(30,30,600,150))
        fightDetailText(text_detail_pg_num)
        showActivesAndStatus()
        status_bar()
        ###
        pygame.display.update()
        clock.tick(60)

def resetCooldown():
    for skill in [mana_gaurd,restore,barrier,meditate]:
        skill.delCooldownEnd()

def showActivesAndStatus():
    x = 0
    for skill in player.fight_actives:
        screen.blit(skill.img,centerIMG(80,80,50+x,525))
        x += 100
    x = 0
    for status in player.fight_status:
        screen.blit(status,centerIMG(80,80,50+x,650))
        x += 100
    x = 0
    for skill in enemy.fight_actives:
        screen.blit(skill.img,centerIMG(80,80,700+x,525))
        x += 100
    x = 0
    for status in enemy.fight_status:
        screen.blit(status,centerIMG(80,80,700+x,650))
        x += 100   


def fightAgain():
    for aSkill in player.fight_actives:
        Active.loseEffect(aSkill)
    while inFight:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
        screen.fill(white)
        textbox('Gained $%i and %i EXP'%(enemy.loot,enemy.exp),45,black,screenW/2,200)
        textbox('Keep exploring the dungeon?',50,black,screenW/2,325)
        button('Yes',80,200,450,200,200,green,lightGreen,fight,None)
        button('No',80,650,450,200,200,red,lightRed,leaveFight,None)
        pygame.display.update()

def leaveFight():
    global inFight
    inFight = False
    for aSkill in player.fight_actives:
        Active.loseEffect(aSkill)
    player.X = 800
    pygame.mixer.music.stop()
    pygame.mixer.music.load('bgm_home.mp3')
    pygame.mixer.music.play(-1)

def runChance():
    chance = 100
    chance -= round(enemy.HP/25)  + enemy.damage*3 - player.LV*35 - player.damage*4 - player.mag_damage*4
    success_run = chance >= random.choice(range(101))
    return success_run

def shop():
    global inStore
    inStore = True
##    pygame.mixer.music.load('bgm_shop.ogg')
##    pygame.mixer.music.play(-1)
    pg_num = 1
    ##
    while inStore:
        screen.fill(lime)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
##                    pygame.mixer.music.load('bgm_home.mp3')
##                    pygame.mixer.music.play(-1)
                    inStore = False
                elif event.key == pygame.K_a:
                    if pg_num - 1 >= 1:
                        pg_num -= 1
                        pg_flip.play()
                elif event.key == pygame.K_d:
                    if pg_num + 1 <= len(shop_pg):
                        pg_num += 1
                        pg_flip.play()
                elif event.key == pygame.K_1:
                    inventory()
                elif event.key == pygame.K_2:
                    statsPage()
        # display items
        matrixSlot(4,5,shop_pg[pg_num-1],50,60,125,125)
        ################
        # arrows
        if pg_num - 1 >= 1:
            screen.blit(small_arrow_left,centerIMG(30,30,25,screenH/2-30))
        if pg_num + 1 <= len(shop_pg):
            screen.blit(small_arrow_right,centerIMG(30,30,560,screenH/2-30))
        #########################
        textbox(str(pg_num),45,black,775,650)
        textbox('Press E to leave',15,black,775,485)
        status_bar()
        pygame.display.update()

def matrixSlot(column,row,what,x,y,xdis,ydis):
    x_start = 0
    y_start = 0
    index = 0
    for col in range(column):
        for slot in range(row):
            slotButton(what[index],x+x_start,y+y_start,100,100)
            y_start += ydis
            index += 1
        x_start += xdis
        y_start = 0

def inventory():
    global inInv
    inInv = True
    while inInv:
        player.statUpdate()
        screen.fill(brown)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    inInv = False
                if event.key == pygame.K_3:
                    statsPage()
        ### Inventory slots ###
        matrixSlot(3,5,player.inv,625,45,125,125)
        ### Equipment slots ####
        matrixSlot(3,1,[player.weapon,player.body,player.lefthand],100,170,125,0)
        slotButton(player.head,225,45,100,100)
        ##################
        textbox('Cash: $%i'%player.cash,30,yellow,screenW/2-40,100)
        textbox('Hover over an item and right click to sell',20,black,800,680)
        ##################
        status_bar()
        pygame.display.update()

def hospital():
    global inHosp
    inHosp = True
    while inHosp:
        screen.fill(orange)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    inHosp = False
        matrixSlot(6,3,hospital_pots,150,300,125,125)
        textbox('(Potions are usable in battle)',20,black,300,675)
        textbox('Press E to leave',20,black,800,675)
        status_bar()
        pygame.display.update()

def setLearnedSkills():
    player.numLearnedSkills = 0
    player.numMaxSkills = 16
    for i in range(16):
        player.learned_skills.append(None)

def setInv():
    player.inv = []
    player.numItemInv = 0
    player.numMaxItem = 15
    for i in range(15):
        player.inv.append(None)
    if player.job == 'Mage':
        addItem(basic_wand)


def game_loop():
    clock.tick(60)
    setInv()
    setLearnedSkills()
##    addItem(katana)
##    addItem(shld_star)
##    addItem(bronze_body)
##    addItem(staff)
    # images in game
    bg = pygame.image.load('hometown.png')
    # player coordinates
    player.X = 500
    player.Y = 600
    player.W = 90
    player.H = 90
    player.Xchange = 0
    player.Ychange = 0
    player.direction = 0
    # restore HP/MP upon starting and give some starting cash
    player.healFullHP()
    player.healFullMP()
    player.cash = 125
    play = True
    pygame.mixer.music.load('bgm_home.mp3')
    pygame.mixer.music.play(-1)
    while play:
        screen.blit(bg,(0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    player.img = rotate_img(player.direction,2,player.img)
                    player.direction = 2
                    player.Xchange = -5
                elif event.key == pygame.K_d:
                    player.img = rotate_img(player.direction,6,player.img)
                    player.direction = 6
                    player.Xchange = 5
                elif event.key == pygame.K_w:
                    player.img = rotate_img(player.direction,0,player.img)
                    player.direction = 0
                    player.Ychange = -5
                elif event.key == pygame.K_s:
                    player.img = rotate_img(player.direction,4,player.img)
                    player.direction = 4
                    player.Ychange = 5
                elif event.key == pygame.K_1:
                    inventory()
                elif event.key == pygame.K_2:
                    statsPage()
                elif event.key == pygame.K_3:
                    skillsPage()
                elif event.key == pygame.K_e:
                    if (player.X + 30 >= 470 and player.X <= 576) and (player.Y+30 >= 485 and player.Y <= 556):
                        hospital()
                    elif (player.X + 30 >= 87 and player.X <= 215) and (player.Y+30 >= 132 and player.Y <= 265):
                        shop()
            elif event.type == pygame.KEYUP: # lifts up key
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    player.Xchange = 0
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    player.Ychange = 0
        # boundary
        if not player.X + player.Xchange < 0 and not player.X + player.Xchange + player.W > screenW:
            player.X += player.Xchange
        if not player.Y + player.Ychange < 0 and not player.Y + player.Ychange + player.H > screenH :
            player.Y += player.Ychange
        # Level one dungeon
        if player.X > screenW - 100:
            pygame.mixer.music.stop()
            fight()
            player.Xchange = 0
            player.Ychange = 0
        #refresh
        # buy heal
        elif (player.X + 30 >= 470 and player.X <= 576) and (player.Y+30 >= 485 and player.Y <= 556):
            textbox('You can heal and buy potions here. Press E to enter.',30,red,screenW/2,250)
        # shop
        elif (player.X + 30 >= 87 and player.X <= 215) and (player.Y+30 >= 132 and player.Y <= 265):
            textbox('You can buy stuff here. Press E to shop.',30,black,screenW/2,250)
        screen.blit(player.img,centerIMG(player.W,player.H,player.X,player.Y))
        status_bar()
        pygame.display.update()

# Main
intro()
job_select()
stats()
game_loop()
pygame.quit()
quit()
