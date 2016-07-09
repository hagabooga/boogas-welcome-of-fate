import pygame
import random
from sounds import *

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
            if hasattr(user,'corpse_drain') and corpse_drain.bonus_chance >= random.choice(range(101)) and isinstance(used_skill,Magical):
                user.MP += round(used_skill.mana*.40)
            if hasattr(used_skill,'crit_chance'): # Crit increaser
                crit_chance += used_skill.crit_chance
            if crit_chance >= random.choice(range(101)): # Check if crit
                damage = round(damage*2.25) # crit multiplier
                user.didCrit = True
            else:
                user.didCrit = False
            if hasattr(user,'luck'):
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
            elif mana_gaurd in user.fight_actives and user == enemy: # MANA GAURD SKILL
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

st_burn = pygame.image.load('game/status/st_burn.png')
st_para = pygame.image.load('game/status/st_para.png')
st_bleed = pygame.image.load('game/status/st_bleed.png')
st_curse = pygame.image.load('game/status/st_curse.png')

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



### Rouge Skills #1
##bleed = Skill()
##cripple = Skill()
##cutthroat = Passive()
##stealth = Skill()


 ### Warrior Skills #1
##lunge = Skill('Lunge','lunge.png','Deal medium damage with increased crit chance but low hit chance')
##sonic = Skill()
##blaze = Skill()
