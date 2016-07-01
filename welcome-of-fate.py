import pygame
from colors import *
from class_player import *
from sounds import *
from images import *
from class_items import *
from weapons import *
from potions import *
import random
import math
import time

pygame.init()
pygame.display.set_caption('''Booga's Welcome of Fate''')
screenW = 1024
screenH = 768
screen = pygame.display.set_mode((screenW,screenH))
clock = pygame.time.Clock()

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
        if hit_chance >= random.choice(range(101)): # Check if hit
            if user == player and corpse_drain.bonus_chance >= random.choice(range(101)) and isinstance(used_skill,Magical):
                user.MP += round(used_skill.mana*.40)
            if hasattr(used_skill,'crit_chance'): # Crit increaser
                crit_chance += used_skill.crit_chance
            if crit_chance >= random.choice(range(101)): # Check if crit
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

             # if deal more than current MP##        elif self == player.skill_sonic:
##            dodge_rate = round(dodge_rate*0.43 - 1)
##            total = self.damage
##        ###############################
##        ### Sweep Damage Bonus ########a = 
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
            self.img = pygame.image.load('skills/%s'%img)
        if sound != None:
            self.sound = pygame.mixer.Sound('game/sounds/%s'%sound)
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
            mana_gaurd.setTurnEnd(fightText.turn,5)
            mana_gaurd.setCooldownEnd(fightText.turn,mana_gaurd.cooldown)
        elif used_skill == restore:
            player.restoreHP(restore.hp)
            player.bonusLuck += restore.bonus_stat
            player.bonusHit += restore.bonus_stat
            player.bonusCrit += restore.bonus_stat
            restore.setTurnEnd(fightText.turn,3)
            restore.setCooldownEnd(fightText.turn,restore.cooldown)
        elif used_skill == barrier:
            player.shield_hp = barrier.shield
            barrier.setTurnEnd(fightText.turn,3)
            barrier.setCooldownEnd(fightText.turn,barrier.cooldown)
        elif used_skill == meditate:
            meditate.setCooldownEnd(fightText.turn,meditate.cooldown)

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
        if name == 'Corpse Drain':
            self.rank += 1
        self.type = 'Passive'
        del self.damage
    def giveBonus(self):
        if self == max_mp_inc:
            player.bonusMaxMP += self.bonus
            player.MP += self.bonus
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
            
            

basic_attack = Physical('Basic Attack',None,None,'Attack with your weapon','Deals physical damage','',0)
# Mage Skills #1
# attack skills
ember = Magical('Ember','mage/damage/ember.png','fire.wav','Burn the enemy','Small chance to burn','',3)
shower = Magical('Shower','mage/damage/shower.png','water.wav','Call the rain to fall','Increased hit rate','',3)
breeze = Magical('Breeze','mage/damage/breeze.png','wind.wav','Blow the enemy away','Increased crit rate, decreased hit chance','',3)
shock = Magical('Shock','mage/damage/shock.png','thunder.wav','Shock with electricity','Small chance to paralyze, small increased crit rate','',3)
fireball = Magical('Fireball','mage/damage/fireball.png','fire.wav','Lob a ball of fire','Medium rate to burn','LV: 4, Ember: Rank 3',3)
river = Magical('River','mage/damage/river.png','water.wav','Call a river','More increased hit rate','LV: 4, Shower: Rank: 3',3)
gust = Magical('Gust','mage/damage/gust.png','wind.wav','Make the enemy fly','More increased crit rate, decreased hit chance','LV: 4, Breeze: Rank: 3',3)
thunderbolt = Magical('Thunderbolt','mage/damage/thunderbolt.png','thunder.wav','Pikachu','Medium chance to paralyze, increased crit rate','LV: 4, Shock: Rank: 3',3)
blaze = Magical('Blaze','mage/damage/blaze.png','fire.wav','Set enemy ablaze','High chance to burn','LV: 10, Fireball: Rank: 3',3)
waterfall = Magical('Waterfall','mage/damage/waterfall.png','water.wav','A fall of water','Greatly increased hit rate', 'LV: 10, River: Rank: 3',3)
whirlwind = Magical('Whirlwind','mage/damage/whirlwind.png','wind.wav','A strong wind','Greatly increased crit rate, decreased hit chance','LV: 10, Gust: Rank: 3',3)
lightning = Magical('Lightning','mage/damage/lightning.png','thunder.wav','Electrify the enemy','High chance to paralyze, more increased crit rate',\
                    'LV: 10, Thunderbolt: Rank: 3',3)
inferno = Magical('Inferno','mage/damage/inferno.png','fire.wav','The strongest flames in the game','Higher chance to burn','LV: 18, Blaze: Rank: 3',3)
tsunami = Magical('Tsunami','mage/damage/tsunami.png','water.wav','Wash away the enemy','Greater increased hit rate','LV: 18, Waterfall: Rank: 3',3)
tornado = Magical('Tornado','mage/damage/tornado.png','wind.wav','Blow away the enemy','Greater increased crit rate, decreased hit chance','LV: 18, Whirlwind: Rank: 3',3)
thunderstorm = Magical('Thunderstorm','mage/damage/thunderstorm.png','thunder.wav','A storm of lightning','Higher chance to paralyze, Greatly increased crit rate',\
                       'LV: 18, Lightning: Rank: 3',3)
## Actives
mana_gaurd = Active('Mana Gaurd','mage/active/mana_gaurd.png','pheal.wav','Mana gaurds your health','For 5 turns, take damage from mana instead of health','LV: 2',3)
restore = Active('Restore','mage/active/restore.png','heal.wav','Restore health','Restore health and gain temp. bonuses for 3 turns','LV: 4',5)
barrier = Active('Barrier','mage/active/barrier.png','charge.wav','Create a barrier','For 3 turns, create a shield','LV: 6',5)
meditate = Active('Meditate','mage/active/meditate.png','charge.wav','Focus your mind','Next spell deals massive damage','LV: 9',4)

## Passives
corpse_drain = Passive('Corpse Drain','mage/passive/corpse_drain.png',None,'Gain more when killing','Defeating enemy or using damaging skill, gain MP','',4)
max_mp_inc = Passive('Max MP +','mage/passive/max_mp_inc.png',None,'Expand your mind','Increases Maximum MP','',7)
magic_mast = Passive('Spell Mastery','mage/passive/magic_mast.png',None,'Train your skills','Increases Luck/Hit/Crit Chance','LV: 5',5)
mana_armor = Passive('Mana Armor','mage/passive/mana_armor.png',None,'Mana is Armor','Gain bonus Armor/Resist based on Current Max MP','LV: 8',3)
as_one = Passive('As One','mage/passive/as_one.png',None,'You are one','Set Str/HP = 1, gain bonus MP based on difference','LV: 5',1)

# lists in list
mage_skills_pg = [[ember,shower,breeze,shock,\
                   fireball,river,gust,thunderbolt,\
                   blaze,waterfall,whirlwind,lightning,\
                   inferno,tsunami,tornado,thunderstorm],\
                  [mana_gaurd,restore,barrier,meditate,None,None,None,None,\
                   max_mp_inc,magic_mast,mana_armor,as_one,corpse_drain,None,None,None]]

def skillUpdate():
    if player.job == 'Mage': # MAGE SKILLS
        # attack skills
        basic_attack.damage = player.damage
        basic_attack.mana = 0
        ### Damage Skills
        # Fire
        ember.damage = round(80 + (player.mag_damage/1.8)*(1.8 * (1 + ember.rank)))
        ember.mana = round(50 + ember.damage/(17-ember.rank) + ember.rank * 35)
        ember.burn_chance = round(15 + 3*ember.rank + player.mag_damage/(25 + player.mag_damage/4))
        fireball.damage = round(175*fireball.rank + ember.damage + (player.mag_damage/1.75)*(1.8 * (1 + fireball.rank)))
        fireball.mana = round(ember.mana + fireball.damage/(15-fireball.rank) + fireball.rank * 50)
        fireball.burn_chance = round(ember.burn_chance + 3*fireball.rank + player.mag_damage/(25 + player.mag_damage/4))
        blaze.damage = round(325*blaze.rank + fireball.damage + (player.mag_damage/1.7)*(1.8 * (1 + blaze.rank)))
        blaze.mana = round(fireball.mana + blaze.damage/(15-blaze.rank) + blaze.rank * 125)
        blaze.burn_chance = round(fireball.burn_chance + 4*blaze.rank + player.mag_damage/(25 + player.mag_damage/4))
        inferno.damage = round(450*inferno.rank + blaze.damage + (player.mag_damage/1.65)*(1.8 * (1 + inferno.rank)))
        inferno.mana = round(blaze.mana + inferno.damage/(15-inferno.rank) + inferno.rank * 210)
        inferno.burn_chance = round(blaze.burn_chance + 5*inferno.rank + player.mag_damage/(25 + player.mag_damage/4))
        # Water
        shower.damage = round(88 + (player.mag_damage/1.7)*(1.85 * (1 + shower.rank)))
        shower.mana = round(45 + shower.damage/(20-shower.rank) + shower.rank * 25)
        shower.hit_chance = round(20 + 3.5*shower.rank)
        river.damage = round(200*river.rank + shower.damage + (player.mag_damage/1.65)*(1.85 * (1 + river.rank)))
        river.mana = round(shower.mana + river.damage/(20-river.rank) + river.rank * 60)
        river.hit_chance = round(shower.hit_chance + 3.5*river.rank)
        waterfall.damage = round(375*waterfall.rank + river.damage + (player.mag_damage/1.6)*(1.85 * (1 + waterfall.rank)))
        waterfall.mana = round(river.mana + waterfall.damage/(20-waterfall.rank) + waterfall.rank * 100)
        waterfall.hit_chance = round(river.hit_chance + 3.5*waterfall.rank)
        tsunami.damage = round(500*tsunami.rank + waterfall.damage + (player.mag_damage/1.5)*(1.85 * (1 + tsunami.rank)))
        tsunami.mana = round(waterfall.mana + tsunami.damage/(20-tsunami.rank) + tsunami.rank * 225)
        tsunami.hit_chance = round(waterfall.hit_chance + 3.5*tsunami.rank)
        # Wind
        breeze.damage = round(70 + (player.mag_damage/2.1)*(1.6 * (1 + breeze.rank)))
        breeze.mana = round(30 + breeze.damage/(23-breeze.rank) + breeze.rank * 20)
        breeze.crit_chance = round(26 + 3*breeze.rank)
        breeze.hit_chance = round(-20 + 2*breeze.rank)
        gust.damage = round(140*gust.rank + breeze.damage + (player.mag_damage/2.0)*(1.65 * (1 + gust.rank)))
        gust.mana = round(breeze.mana + gust.damage/(23-gust.rank) + gust.rank * 40)
        gust.crit_chance = round(breeze.crit_chance + 3*gust.rank)
        gust.hit_chance = round(breeze.hit_chance + 2*gust.rank)
        whirlwind.damage = round(300*whirlwind.rank + gust.damage + (player.mag_damage/1.9)*(1.7 * (1 + whirlwind.rank)))
        whirlwind.mana = round(gust.mana + whirlwind.damage/(23-whirlwind.rank) + whirlwind.rank * 80)
        whirlwind.crit_chance = round(gust.crit_chance + 3*whirlwind.rank)
        whirlwind.hit_chance = round(gust.hit_chance + 1*whirlwind.rank)
        tornado.damage = round(415*tornado.rank + whirlwind.damage + (player.mag_damage/1.8)*(1.8 * (1 + tornado.rank)))
        tornado.mana = round(whirlwind.mana + tornado.damage/(23-tornado.rank) + tornado.rank * 200)
        tornado.crit_chance = round(whirlwind.crit_chance + 3*tornado.rank)
        tornado.hit_chance = round(whirlwind.hit_chance + 1*tornado.rank)
        # Electric
        shock.damage = round(100 + (player.mag_damage/1.7)*(1.9 * (1 + shock.rank)))
        shock.mana = round(60 + shock.damage/(14-shock.rank) + shock.rank * 50)
        shock.para_chance = round(20 + 3*shock.rank + player.mag_damage/(25 + player.mag_damage/4))
        shock.crit_chance = round(14 + 3*shock.rank)
        thunderbolt.damage = round(250*thunderbolt.rank + shock.damage + (player.mag_damage/1.6)*(2 * (1 + thunderbolt.rank)))
        thunderbolt.mana = round(shock.mana + thunderbolt.damage/(14-thunderbolt.rank) + thunderbolt.rank * 60)
        thunderbolt.para_chance = round(shock.para_chance + 3*thunderbolt.rank + player.mag_damage/(25 + player.mag_damage/3.8))
        thunderbolt.crit_chance = round(25 + 3*thunderbolt.rank)
        lightning.damage = round(425*lightning.rank + thunderbolt.damage + (player.mag_damage/1.5)*(2.1 * (1 + lightning.rank)))
        lightning.mana = round(thunderbolt.mana + lightning.damage/(14-lightning.rank) + lightning.rank * 100)
        lightning.para_chance = round(thunderbolt.para_chance + 3*lightning.rank + player.mag_damage/(25 + player.mag_damage/3.6))
        lightning.crit_chance = round(35 + 2*lightning.rank)
        thunderstorm.damage = round(525*thunderstorm.rank + lightning.damage + (player.mag_damage/1.4)*(2.2 * (1 + thunderstorm.rank)))
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
        corpse_drain.bonus_chance = round(15+player.LV/5+6*corpse_drain.rank)
        corpse_drain.detail = 'Activate chance: %i%%'%corpse_drain.bonus_chance
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
        return stat

class Enemy:
    def __init__(self, name, img, HP, MP, damage, mag_damage, armor, mag_armor, hit, dodge, crit, loot, exp):
        self.name = name
        self.img = pygame.image.load('game/enemy/%s'%img)
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


class Page:
    def __init__(self):
        self.show = False
    def enter(self):
        self.show = True
    def leave(self):
        self.show = False

inSome = Page()
inFight = Page()
inStore = Page()
inInv = Page()
inHosp = Page()
inSkill = Page()
inLearnSkill = Page()

class switchTextbox: # each page has x amount of columns of textboxes
    def __init__(self,pages,column):
        self.text_list = [] # each row has ['aText',aColor]
        startText = []
        for page in range(pages):
            for col in range(column):
                startText.append(['',black])
            self.text_list.append(startText)
            startText = []
        self.column = column
        self.pg_num = 1
        self.pages = pages - 1
    def addText(self,newTextList):
        del self.text_list[0]
        new_text_list = []
        for col in range(self.column):
            new_text_list.append(['',black])            
        self.text_list.append(new_text_list)
        for text in newTextList:
            del self.text_list[self.pages][0]
            self.text_list[self.pages].append(text)
    def reset(self):
        startText = []
        for page in range(self.pages+1):
            for col in range(self.column):
                startText.append(['',black])
            self.addText(startText)
    def showText(self,textSizeList,x,x_dis,y,y_dis):
        xdis = 0
        ydis = 0
        for col in range(self.column):
            textbox(self.text_list[self.pg_num][col][0],textSizeList[col],self.text_list[self.pg_num][col][1],x+xdis,y+ydis)
            x += x_dis
            y += y_dis

fightText = switchTextbox(2,6) # used in fight

enemy = 'some Enemy()'
name = ''


def doNone():
    None
    
# place center img
def centerIMG(imgX, imgY, x, y):
    center = ((x - imgX / 2), (y - imgY / 2))
    return center

# Make a textbox
def textObj(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def textbox(msg, size, color, x, y):
    fontSize = pygame.font.Font('game/font/segoeuil.ttf',size)
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

def boolButton(msg, msgSize, x, y, w, h, color, onColor):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, color, (x, y, w, h))
        textbox(msg, msgSize, black, x + w / 2, y + h / 2)
        if click[0] == 1:
            return True
    else:
        pygame.draw.rect(screen, onColor, (x, y, w, h))
        textbox(msg, msgSize, black, x + w / 2, y + h / 2)
        return False


def quitGame():
    pygame.quit()
    quit()

def gameover():
    inSome.enter()
    while inSome.show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
        screen.fill(white)
        textbox('You Died! Try Again?',50,black,screenW/2,325)
        textbox('(you will lose all money)',30,black,screenW/2,380)
        button('Yes',80,200,450,200,200,green,lightGreen,inSome.leave,None)
        button('No',80,650,450,200,200,red,lightRed,quitGame,None)
        pygame.display.update()
    player.healFullHP()
    player.cash = 0
    time.sleep(0.5)

def status_bar():
    if player.shield_hp > 0 and inFight.show and not inInv.show and not inSome.show and not inSkill.show:
        textbox('Shield: %i'%player.shield_hp,50,orange,500,650)
    textbox(player.name,25,black,80+(len(player.name)*5),725)
    textbox(('LV %i     HP  %i / %i   MP  %i / %i' %(player.LV,player.HP,player.maxHP,player.MP,player.maxMP)),40,black,610,725)

def intro():
    pygame.mixer.music.load('game/music/bgm_intro.mp3')
    pygame.mixer.music.play(-1)
    inSome.show = True
    while inSome.show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
        screen.fill(white)
        # Title
        textbox('''Booga's Welcome of Fate''',80,blue,screenW/2,200)
        # Start buttion
        button('Start',60,175,375,250,250,green,lightGreen,instructions,None)
        # Quit button
        button('Quit',60,600,375,250,250,red,lightRed,quitGame,None)
        pygame.display.update()

def enter_name():
    name = ''
    enter_pressed = False
    inSome.show = True
    while inSome.show:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                ### user input for name
                if event.unicode.isalpha():
                    if len(name) < 12:
                        name += event.unicode
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                       name = name[:-1]
                    elif event.key == pygame.K_SPACE and not len(name) == 0 and len(name) < 12:
                        name += " "
                    elif event.key == pygame.K_RETURN:
                        enter_pressed = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:
                    enter_pressed = False
                ### user input for name
            elif event.type == pygame.QUIT:
                quitGame()
        screen.fill(white)
        # Show username input
        textbox(name,50,purple,655+(len(name)*4),300)
        # ask for name
        textbox('Enter your name: ',50,blue,250,300)
        textbox('Press Enter when done',60,black,screenW/2,535)
        if enter_pressed:
            if len(name.strip()) == 0:
                textbox('Please enter a name',60,red,screenW/2,425)
            else:
                player.name = name
                inSome.leave()
        pygame.display.update()

def instructions():
    timer = 0
    while inSome.show:
        timer += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
        screen.fill(white)
        textbox('''INSTRUCTIONS''',50,red,screenW/2,150)
        textbox('''Use WASD keys to move, press the 1 key to see your inventory''',30,black,screenW/2,screenH/2-100)
        textbox('''Press the 2 key to see your stats, the 3 key to see your skills''',30,black,screenW/2,screenH/2-55)
        textbox('''If something has                           use A and D to use the arrows''',30,black,screenW/2,screenH/2)
        screen.blit(small_arrow_left,centerIMG(30,30,390,385))
        screen.blit(small_arrow_right,centerIMG(30,30,465,385))
        if timer >= 180:
            button('OKAY',30,screenW/2-50,550,100,100,green,lightGreen,instructions_2,None)
        pygame.display.update()

def instructions_2():
    timer = 0
    while inSome.show:
        timer += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
        screen.fill(white)
        screen.blit(pygame.image.load('game/general/instruct_1.png'),(0,0))
        if timer >= 80:
            button('OKAY',30,screenW/2-26,525,100,100,green,lightGreen,inSome.leave,None)
        pygame.display.update()

def stats():
    player.statUpdate()
    inSome.show = True
    while inSome.show:
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
            button('Continue',30,850,screenH/1.35,75,75,green,lightGreen,inSome.leave,None)
        status_bar()
        pygame.display.update()
        clock.tick(15)


def job_select():
    inSome.show = True
    while inSome.show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
        screen.fill(white)
        textbox('Select Your Job',100,black,screenW/2,100)
        if boolButton('Mage',40,85,275,250,250,blue,lightBlue):
            return Mage()
        if boolButton('Rogue',40,385,275,250,250,green,lightGreen):
            textbox('Available Soon!',60,black,screenW/2,200)
            #return Rouge()
        if boolButton('Warrior',40,685,275,250,250,red,lightRed):
                textbox('Available Soon!',60,black,screenW/2,200)
            #return Warrior()
        textbox('Mage: Excels with magic, high MP and Magical DMG but low HP, armor, and physical dmg',23,lightBlue,screenW/2,600)
        textbox('Rouge: Fast and sharp, high crit and dodge but low HP and defense',23,lightGreen,screenW/2,650)
        textbox('Warrior: Strong and sturdy, high physical dmg and armor but low hit chance and weak to magic',23,lightRed,screenW/2,700)
        pygame.display.update()



def statsPage():
    player.statUpdate()
    inSome.show = True
    while inSome.show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_2:
                    inSome.show = False
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
            if player.lefthand != player.fap and player.lefthand != no_left:
                player.loseItemBonus(player.lefthand)
                player.inv[player.numItemInv] = player.lefthand
                player.numItemInv += 1
            player.lefthand = no_left
        else:
            if player.lefthand == no_left:
                player.lefthand = player.fap
        if weapon_requirement(slot):
            saved_item = None
            if player.weapon != player.fists and slot != player.weapon: # if has weapon equipped already
                saved_item = player.weapon
                player.loseItemBonus(saved_item)
            player.weapon = slot
            player.addItemBonus(slot)
            player.numItemInv -= 1
            player.inv.remove(slot)
            player.inv.append(None)
            if saved_item != None:   # put weapon in inv
                player.inv[player.numItemInv] = saved_item
                player.numItemInv += 1
            equip_sound.play()
            time.sleep(0.3)
        else:
            textbox('Requirements not met!',50,black,500,500)
    # remove weapon
    elif slot is player.weapon and player.weapon != player.fists and player.numItemInv < player.numMaxItem:
        if isinstance(slot,Staff):
            player.lefthand = player.fap
        player.loseItemBonus(player.weapon)
        player.inv[player.numItemInv] = player.weapon
        player.numItemInv += 1
        player.weapon = player.fists
        equip_sound.play()
    # put body on
    elif isinstance(slot,Body) and slot is not player.body: #and player.body == shirt_jeans
        saved_item = None
        if player.body != player.shirt_jeans and slot != player.body: # if has weapon equipped already
            saved_item = player.body
            player.loseItemBonus(saved_item)
        player.body = slot
        player.addItemBonus(slot)
        player.numItemInv -= 1
        player.inv.remove(slot)
        player.inv.append(None)
        if saved_item != None:   # put weapon in inv
            player.inv[player.numItemInv] = saved_item
            player.numItemInv += 1
        wear.play()
        time.sleep(0.3)
    # remove body
    elif slot == player.body and player.body != player.shirt_jeans and slot not in player.inv and player.numItemInv < player.numMaxItem:
        player.loseItemBonus(player.body)
        player.inv[player.numItemInv] = player.body
        player.numItemInv += 1
        player.body = player.shirt_jeans
        wear.play()
    # put on l_hand
    elif isinstance(slot,L_hand) and slot is not player.lefthand and player.lefthand != no_left:
        saved_item = None
        if player.lefthand != player.fap and slot != player.lefthand: # if has weapon equipped already
            saved_item = player.lefthand
            player.loseItemBonus(saved_item)
        player.lefthand = slot
        player.addItemBonus(slot)
        player.numItemInv -= 1
        player.inv.remove(slot)
        player.inv.append(None)
        if saved_item != None:   # put weapon in inv
            player.inv[player.numItemInv] = saved_item
            player.numItemInv += 1
        wear.play()
        time.sleep(0.3)
    #remove l_hand
    elif slot == player.lefthand and player.lefthand != player.fap and player.lefthand != no_left and slot not in player.inv and player.numItemInv < player.numMaxItem:
        player.loseItemBonus(player.lefthand)
        player.inv[player.numItemInv] = player.lefthand
        player.numItemInv += 1
        player.lefthand = player.fap
        wear.play()
    # put on hat
    elif isinstance(slot,Head) and slot is not player.head:
        saved_item = None
        if player.head != player.china_hat and slot != player.head: # if has weapon equipped already
            saved_item = player.head
            player.loseItemBonus(saved_item)
        player.head = slot
        player.addItemBonus(slot)
        player.numItemInv -= 1
        player.inv.remove(slot)
        player.inv.append(None)
        if saved_item != None:   # put weapon in inv
            player.inv[player.numItemInv] = saved_item
            player.numItemInv += 1
        wear.play()
        time.sleep(0.3)
    # remove on hat
    elif slot == player.head and player.head != player.china_hat and slot not in player.inv and player.numItemInv < player.numMaxItem:
        player.loseItemBonus(player.head)
        player.inv[player.numItemInv] = player.head
        player.numItemInv += 1
        player.head = player.china_hat
        wear.play()
    # use potion
    if isinstance(slot,Potion) and not inFight.show:
        slot.activate_eff(player)
        potSound.play()
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
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if inSkill.show or inLearnSkill.show: # skill page shows if requirement is met
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
    elif inFight.show and not inInv.show: # some reason when using skill the boxes show up so i use this to not show boxes after using skill (?????????????????)
        # i know why the boxes show up its bcuz enemy attack overlaps screen and then closes :(, must put enemy attack in the (fight() while loop)
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
        if inSkill.show or inLearnSkill.show:
            if not inFight.show or enemy.HP <= 0:
                if slot != None:
                    itemValue(slot)
                if pygame.mouse.get_pressed()[0]:
                    # rank up skill
                    if not inFight.show or enemy.HP <= 0:
                        if player.SP > 0 and slot != None:
                            if player.numLearnedSkills != player.numMaxSkills:
                                if slot.skill_requirement():
                                    if slot.rank == 0 or slot not in player.learned_skills: # add skill into leanred skill
                                        if not isinstance(slot,Passive):
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
                            if slot.cooldownEnd <= fightText.turn:
                                del slot.cooldownEnd
                            else:
                                textbox('On cooldown! %i Turns Left'%(slot.cooldownEnd - fightText.turn),30,blue,800,235)
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
        elif inInv.show:
            if slot != None:
                itemValue(slot)
            if not inFight.show:
                if pygame.mouse.get_pressed()[0]:
                    checkEquip(slot)
                # Sell Item
                elif not inFight.show and pygame.mouse.get_pressed()[2] and slot in player.inv and slot is not player.weapon and slot is not player.body and\
                     slot is not player.lefthand and slot is not player.head and slot != None:
                        sellItem(slot)
            else: # in fight potion/equip mechanic
                if pygame.mouse.get_pressed()[0] and slot in player.inv and slot is not player.weapon and slot is not player.body and\
                                                     slot is not player.lefthand and slot is not player.head and slot != None:
                    checkEquip(slot)
                    inInv.show = False
                    dmg_calc(slot)
        elif inHosp.show:
            if slot != None:
                itemValue(slot)
            if pygame.mouse.get_pressed()[0]:
                if player.numItemInv == player.numMaxItem:
                    textbox('Full inventory!',30,red,screenW/2,800)
                else:
                    buyItem(slot)
        elif inStore.show:
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
                    sound = pygame.mixer.Sound('game/sounds/buy.wav')
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
    want = True
    sell_price = round(slot.cost/2)
    while want:
        screen.fill(brown)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    if isinstance(slot,Potion) and slot.num_held > 1:
                            slot.num_held -= 1
                            player.cash += sell_price
                    else:
                        player.cash += sell_price
                        player.inv.remove(slot)
                        player.inv.append(None)
                        player.numItemInv -= 1
                    sound = pygame.mixer.Sound('game/sounds/buy.wav')
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
    if slot != None:
        if player.cash < slot.cost:
            if inStore:
                textbox('Not enough gold!',30,blue,775,425)
            elif inHosp:
                textbox('Not enough gold!',30,blue,825,175)
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
    if inStore.show and not inInv.show and slot != None: # IN STORE DETAILS
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
    elif inSkill.show or inLearnSkill.show:
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
    elif inInv.show:
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
    elif inHosp.show:
        if slot != None:
            textbox(slot.name,65,black,screenW/2,50)
            textbox('%s (%s)'%(slot.desc,slot.type),40,black,screenW/2,110)
            textbox('Cost: $%i'%(slot.cost),40,black,screenW/2,175)
            textbox(slot.bdesc,40,black,screenW/2,250)


def leaveLearnSkill():
    inLearnSkill.show = False
    if not inFight.show or inLearnSkill.show:
        time.sleep(0.3)

def learnedSkillsPage():
    time.sleep(0.2)
    player.statUpdate()
    inLearnSkill.show = True
    while inLearnSkill.show:
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
        if not inFight.show or enemy.HP >= 0:
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
    inSkill.show = True
    pg_num = 0
    while inSkill.show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_3:
                    inSkill.show = False
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
        fightText.addText(fight_shown_text)
        pygame.display.update()
    else:
        fight_shown_text.append(["Enemy can't move!",lightYellow])
        fightText.addText(fight_shown_text)
        pygame.display.update()

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
    textbox('Turn: %i'%(fightText.turn),25,black,330,340)
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
    fightText.turn += 1
    fightText.pg_num = fightText.pages
    fight_shown_text = []
    success_run = None
    enemy.isPara = False
    if used_skill == 'run': # Run
        fight_shown_text.append(['You are trying to run away...',black])
        success_run = runChance()
        if not success_run:
            fight_shown_text = []
            fight_shown_text.append(['You failed to run away!',blue])
            fightText.addText(fight_shown_text)
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
        used_skill.activate_eff(player)
        potSound.play()
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
    fightText.addText(fight_shown_text)
    fightText.showText([27,27,28,32,37,45],350,0,25,50)
    pygame.display.update()
    time.sleep(1.1)
    # counter attack
    if enemy.HP > 0 and not success_run: # enemy counter attack
        enemyAttack()
    checkActiveDuration()    # ACTIVE DURATION LOSE EFFECT HERE

def checkActiveDuration():
    for skill in player.fight_actives:
        if hasattr(skill,'turnEnd') and fightText.turn == skill.turnEnd:
            skill.loseEffect()
            player.fight_actives.remove(skill)

def level_up_greet():
    screen.fill(yellow)
    textbox('You leveled up!',75,black,screenW/2,screenH/2)
    pygame.mixer.music.load('game/music/complete.mp3')
    pygame.mixer.music.load('game/music/complete.mp3')
    pygame.mixer.music.play(0)
    pygame.mixer.music.play(0)
    pygame.display.update()
    time.sleep(1.75)

def fight():
    global enemy
    fightText.turn = 0
    fightText.reset()
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
    alec = Enemy('Alec','alec.png',300,130, 70,100, 25,40, 95,5,5, 50,12)
    sungmin = Enemy('Sungmin','sungmin.png',400,500, 80,55, 25,25, 95,5,4, 50,14)
    kaelan = Enemy('Kaelan','kaelan.png',425,40, 85,25, 40,10, 95,5,4, 60,16)
    #Medium level mobs
    alicky = Enemy('Alicky','alec.png',1500,500, 180,250, 175,125, 90,5,5, 125,100)
    sunger = Enemy('Sunger Munger','sungmin.png',1635,1000, 115,200, 150,150, 92,5,5, 135,125)
    brownitron = Enemy('Brownitron','kaelan.png',1825,400, 130,125, 200,200, 87,5,4, 150,150)
    ryan = Enemy('Ryan','ryan.png',1369,7, 500,10, 0,0, 120,60,50, 175,125)
    tina = Enemy('Tina','tina.png',2000,1000, 50,100, 200,175, 85,10,6, 200,100)
    #High level mobs
    laluche = Enemy('La Lucha Libre','ryan.png',5000,0, 800,10, 0,0, 150,60,75, 400,150)
    dyonghae = Enemy('Dyonghae','tina.png',7500,4000, 400,1200, 700,900, 95,5,5, 200,300)
    greasy_booga = Enemy('Greasy Booga','greasy_booga.png',10500,1200, 800,600, 800,800, 85,20,20, 500,300)
    # Choose random enemy
    if player.LV < 5:
        enemy = random.choice([alec,sungmin,kaelan])
    elif player.LV < 11:
        enemy = random.choice([ryan,brownitron,sunger,alicky,tina])
    else:
        enemy = random.choice([laluche,dyonghae,greasy_booga])
    ### Music
    pygame.mixer.music.load(random.choice(['game/music/bgm_fight1.mp3','game/music/bgm_fight2.mp3','game/music/bgm_fight3.mp3',\
                                           'game/music/bgm_fight4.mp3','game/music/bgm_fight5.mp3','game/music/bgm_fight6.mp3','game/music/bgm_fight7.mp3']))
    pygame.mixer.music.play(-1)
    ##############################
    inFight.show = True
    time.sleep(0.5)
    while inFight.show: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    inventory()
                elif event.key == pygame.K_2:
                    statsPage()
                elif event.key == pygame.K_a:
                    if fightText.pg_num - 1 >= 0:
                        fightText.pg_num -= 1
                        pg_flip.play()
                elif event.key == pygame.K_d:
                    if fightText.pg_num + 1 < fightText.pages+1:
                        fightText.pg_num += 1
                        pg_flip.play()
        if player.run_away:
            leaveFight()
        elif enemy.HP <= 0:
            player.cash += enemy.loot
            player.exp += enemy.exp
            if corpse_drain.bonus_chance >= random.choice(range(101)):
                    player.MP += round(player.maxMP*.20)
                    trimExtraHPMP()
            if player.exp >= player.max_exp:
                level_up_greet()
                player.level_up()
                skillsPage()
                player.healFullHP()
                player.healFullMP()
                fightAgain()
            else:
                fightAgain()
        elif player.HP <= 0:
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
        textbox('Turn: %i'%(fightText.turn),25,black,330,340)
        if fightText.pg_num - 1 >= 0:
            screen.blit(small_arrow_left,centerIMG(30,30,60,150))
        if fightText.pg_num + 1 < fightText.pages+1:
            screen.blit(small_arrow_right,centerIMG(30,30,600,150))
        fightText.showText([27,27,28,32,37,45],350,0,25,50)
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
    while inFight.show:
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
    inFight.show = False
    for aSkill in player.fight_actives:
        Active.loseEffect(aSkill)
    player.X = 800
    pygame.mixer.music.stop()
    pygame.mixer.music.load('game/music/bgm_home.mp3')
    pygame.mixer.music.play(-1)

def runChance():
    chance = 100
    chance -= round(enemy.HP/15)  + enemy.damage*3 - player.LV*75 - player.damage*4 - player.mag_damage*4
    success_run = chance >= random.choice(range(101))
    return success_run

def shop():
    inStore.show = True
##    pygame.mixer.music.load('bgm_shop.ogg')
##    pygame.mixer.music.play(-1)
    pg_num = 1
    ##
    while inStore.show:
        screen.fill(lime)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
##                    pygame.mixer.music.load('bgm_home.mp3')
##                    pygame.mixer.music.play(-1)
                    inStore.show = False
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
        textbox('Cash: %i'%player.cash,60,yellow,775,560)
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
    inInv.show = True
    while inInv.show:
        player.statUpdate()
        screen.fill(brown)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    inInv.show = False
                if event.key == pygame.K_2:
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
    inHosp.show = True
    while inHosp.show:
        screen.fill(orange)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    inHosp.show = False
        textbox('Cash: %i'%player.cash,40,yellow,140,175)
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
    bg = pygame.image.load('game/general/hometown.png')
    # player coordinates
    player.X = 500
    player.Y = 600
    player.W = player.img.get_rect()[2]
    player.H = player.img.get_rect()[3]
    player.Xchange = 0
    player.Ychange = 0
    player.direction = 0
    # restore HP/MP upon starting and give some starting cash
    player.healFullHP()
    player.healFullMP()
    player.cash = 1000000
    play = True
    pygame.mixer.music.load('game/music/bgm_home.mp3')
    pygame.mixer.music.play(-1)
    timer = 0
    while play:
        screen.blit(bg,(0,0))
        timer += 1
        if timer <= 300:
            textbox('Equip a weapon. Press 1 and click your weapon to equip',35,black,screenW/2,300)
        elif timer <= 600:
            textbox('Rank up a skill. Press 3 and click a skill to it rank up',35,black,screenW/2,300)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pygame.display.toggle_fullscreen()
                elif event.key == pygame.K_a:
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
                    # Pretty sure all boundaries for player are broken now, need to fix
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
            timer = 650
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
player = job_select()
enter_name()
stats()
game_loop()
pygame.quit()
quit()
