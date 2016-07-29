import pygame
import random
from sounds import *
from colors import *


class Status:
    def __init__(self,img,text):
         self.img = pygame.image.load(img)
         self.text = text # text s [string,color]

st_burn = Status('game/status/st_burn.png',['You are burned!',orange])
st_para = Status('game/status/st_para.png',['You are paralyzed!',yellow])
st_bleed = Status('game/status/st_bleed.png',['Enemy is bleeding severely!',red])
st_curse = Status('game/status/st_curse.png',['You are cursed!',brown])
st_poison = Status('game/status/st_poison.png',['You poisoned the enemy!',purple])
st_crip = Status('game/status/st_crip.png',['You crippled the enemy!',brown])
st_blind = Status('game/status/st_blind.png',['Enemy is blinded!',lighterGreen])
st_conf =  Status('game/status/st_conf.png',['Enemy is confused!',orange])


allStatus = [st_burn,st_para,st_bleed,st_curse,st_poison,st_crip,st_blind,st_conf]


def dmgModifier(user,victim,used_skill):
    if isinstance(used_skill,Physical):
        dmg = used_skill.damage - victim.armor
    else:
        dmg = used_skill.damage - victim.mag_armor
    ### Mage
    # Meditate
    if meditate in user.fight_actives and isinstance(used_skill,Magical):
        dmg *= meditate.scale/100 # a percentage
        user.fight_actives.remove(meditate)
    ### Rogue
    # Stealth
    if stealth in user.fight_actives:
        stealth.turnEnd = 0
    # Initimidate
    if intimidate in user.fight_actives or intimidate in victim.fight_actives:
        dmg += intimidate.bonus_damage
    # Cutthroat
    if hasattr(user,'job') and cutthroat.rank > 0:
        dmg += cutthroat.bonus_dmg
    ### Status
    if st_crip in victim.fight_status:
        dmg += round(victim.maxHP*0.15)
    return dmg

def hitModifier(user,victim,used_skill):
    hit = user.hit - victim.dodge
    # Basic Damaging Skill
    if hasattr(used_skill,'hit_chance'):
        hit += used_skill.hit_chance
    ### Rogue
    # Sneaky
    if hasattr(victim,'sneaky'):
        hit -= sneaky.bonus        
    ### Status
    if st_blind in user.fight_status:
        hit = round(hit/2 - 15)
        if random.choice(range(6)) == 0:
            user.fight_status.remove(st_blind)
    if st_crip in user.fight_status:
        hit /= round(victim.maxHP/victim.HP)
    if st_conf in user.fight_status:
        hit = round(hit/2)
        if random.choice(range(5)) == 0:
            user.fight_status.remove(st_conf)
    return hit

def onHitEff(user,victim,used_skill):
    # Corpse Drain
    if hasattr(user,'corpse_drain') and corpse_drain.bonus_chance2 >= random.choice(range(101)) and isinstance(used_skill,Magical):
                user.MP += round(used_skill.mana*corpse_drain.restore_mp2)

def critChanceModifier(user,victim,used_skill):
    crit = user.crit
    if hasattr(used_skill,'crit_chance'): # Crit increaser
                crit += used_skill.crit_chance
    return crit

def dmgCalcModifier(uesr,victim,used_skill):
    #### Priority: 1, Shield Damage
    if victim.shield_hp > 0: 
        if victim.shield_hp - damage < 0:
            victim.shield_hp = 0
            victim.HP -= damage - victim.shield_hp 
        else:
            victim.shield_hp -= damage
        return True
    #### Priority: 2, Mana Gaurd Skill
    elif mana_gaurd in victim.fight_actives: 
            if victim.MP - damage < 0: # if deal more than current MP
                victim.HP -= damage - victim.MP
                victim.MP = 0
            else: # else regular
                victim.MP -= damage
            return True
    else:
        return False


def playAttackSound(used_skill):
    if hasattr(used_skill,'sound'):
        used_skill.sound.play() # sound play if hit
    else: #generic hit sound
        weapon_atk_sound().play()

class Action:
    def skillAttack(user,victim,used_skill):
        # Mana Cost
        user.MP -= used_skill.mana
        # Damage
        damage = dmgModifier(user,victim,used_skill)
        # Crit Chance
        crit_chance = critChanceModifier(user,victim,used_skill)
        # Hit Chance
        hit_chance = hitModifier(user,victim,used_skill)
        ifHit = hit_chance >= random.choice(range(101))
        ######
        if ifHit:
            onHitEff(user,victim,used_skill)
            #### Check if crit
            if crit_chance >= random.choice(range(101)):
                #### Crit multiplier
                if hasattr(used_skill,'crit_multi'): 
                    damage = round(damage*(user.crit_multi+used_skill.crit_multi)/100)
                else:
                    damage = round(damage*(user.crit_multi/100))
                user.didCrit = True
                crit.play()
                ####
            #### Didn't Crit
            else:
                user.didCrit = False
            #### Bonus Damage
            if hasattr(user,'luck'):
                damage += random.choice(range(0+user.luck,15+user.luck))
            else:
                damage += random.choice(range(0,round(15+user.damage/90)))
            #### if damage less than 0, damage = 0 so no heal
            if damage < 0:
                damage = 0
            ###### Damage Calculation
            if dmgCalcModifier(user,victim,used_skill):
                None # dmg calc modified
            #### Regular Damage Calculation
            else: 
                victim.HP -= damage
            if used_skill == life_steal:
                user.HP += round(damage*(life_steal.steal/100))
                if user.HP > user.maxHP:
                    user.HP = user.maxHP
                
            ### End
            playAttackSound(used_skill) # play sound
            return damage
        else: # player miss
            wear.play()

    def skillActive(user,victim,used_skill): # all skill actives
        user.MP -= used_skill.mana
        used_skill.sound.play()
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


class Skill(Action):
    def __init__(self,name,img,sound,desc,requiredesc,maxRank):
        self.name = name
        if img != None:
            self.img = pygame.image.load('skills/%s'%img)
        if sound != None:
            self.sound = pygame.mixer.Sound('game/sounds/%s'%sound)
        self.desc = desc
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
                if st_para not in victim.fight_status:
                    victim.fight_status.append(st_para)
                return st_para
        elif hasattr(self,'bleed_chance'):
            if self.bleed_chance >= random.choice(range(101)):
                if st_bleed not in victim.fight_status:
                    victim.fight_status.append(st_bleed)
                return st_bleed
        elif hasattr(self,'poison_chance'):
            if self.poison_chance >= random.choice(range(101)):
                if st_poison not in victim.fight_status:
                    victim.fight_status.append(st_poison)
                return st_poison
        elif hasattr(self,'curse_chance'):
            if self.curse_chance >= random.choice(range(101)):
                if st_curse not in victim.fight_status:
                    victim.fight_status.append(st_curse)
                return st_curse
        elif hasattr(self,'cripple_chance'):
                if self.cripple_chance >= random.choice(range(101)):
                    if st_crip not in victim.fight_status:
                        victim.fight_status.append(st_crip)
                    return st_crip
        elif hasattr(self,'blind_chance'):
                if self.blind_chance >= random.choice(range(101)):
                    if st_blind not in victim.fight_status:
                        victim.fight_status.append(st_blind)
                    return st_blind
        else:
            return None
    

class Physical(Skill):
    def __init__(self,name,img,sound,desc,requiredesc,maxRank):
        super(Physical,self).__init__(name,img,sound,desc,requiredesc,maxRank)
        self.type = 'Damage'
class Magical(Skill):
    def __init__(self,name,img,sound,desc,requiredesc,maxRank):
        super(Magical,self).__init__(name,img,sound,desc,requiredesc,maxRank)
        self.type = 'Damage'
        
# actives and passives have unique detail
class Active(Skill):
    def __init__(self,name,img,sound,desc,requiredesc,maxRank):
        super(Active,self).__init__(name,img,sound,desc,requiredesc,maxRank)
        self.type = 'Active' 
        del self.damage
    def effect(used_skill,who):
        who.fight_actives.append(used_skill)
        if who.job == 'Mage':
            if used_skill == restore:
                who.restoreHP(restore.hp)
                who.bonusLuck += restore.bonus_stat
                who.bonusHit += restore.bonus_stat
                who.bonusCrit += restore.bonus_stat
            elif used_skill == barrier:
                who.shield_hp = barrier.shield
        if who.job == 'Rogue':
            if used_skill == stealth:
                who.bonusDodge += stealth.dodge_chance
                who.bonusCrit += stealth.crit_chance
                who.bonusCritMulti += stealth.crit_multi
            elif used_skill == illusion:
                illusion.notHit = True
                who.bonusDodge += illusion.dodge_chance
            elif used_skill == intimidate:
                who.bonusDodge += intimidate.dodge_chance
            elif used_skill == blood_rit:
                who.HP -= blood_rit.mana
                who.bonusStren += blood_rit.bonus
                who.bonusIntel += blood_rit.bonus
                who.bonusCrit += blood_rit.crit_chance
                who.bonusCritMulti += blood_rit.crit_multi
    def loseEffect(self,who):
        if who.job == 'Mage':
            if self == restore:
                who.bonusLuck -= restore.bonus_stat
                who.bonusHit -= restore.bonus_stat
                who.bonusCrit -= restore.bonus_stat
            elif self == barrier:
                who.shield_hp -= barrier.shield
        elif who.job == 'Rogue':
            if self == stealth:
                who.bonusDodge -= stealth.dodge_chance
                who.bonusCrit -= stealth.crit_chance
                who.bonusCritMulti -= stealth.crit_multi
            elif self == illusion:
                who.bonusDodge -= illusion.dodge_chance
            elif self == intimidate:
                who.bonusDodge -= intimidate.dodge_chance
            elif self == blood_rit:
                who.bonusStren -= blood_rit.bonus
                who.bonusIntel -= blood_rit.bonus
                who.bonusCrit -= blood_rit.crit_chance
                who.bonusCritMulti -= blood_rit.crit_multi
            
    def setTurnEnd(self,turn,duration):
        self.turnEnd = turn + duration
    def setCooldownEnd(self,turn,duration):
        self.cooldownEnd = turn + duration
    def delCooldownEnd(self):
        if hasattr(self,'cooldownEnd'):
            del self.cooldownEnd
                
class Passive(Skill):
    def __init__(self,name,img,sound,desc,requiredesc,maxRank):
        super(Passive,self).__init__(name,img,sound,desc,requiredesc,maxRank)
        if name == 'Corpse Drain':
            self.rank += 1
        elif name == 'Sneaky':
            self.rank += 1
        self.type = 'Passive'
        del self.damage
    def giveBonus(self,who):
        if who.job == 'Mage':
            if self == max_mp_inc:
                who.bonusMaxMP += self.bonus
                who.MP += self.bonus
            elif self == magic_mast:
                who.bonusLuck += self.bonus
                who.bonusCrit += self.bonus
                who.bonusHit += self.bonus
            elif self == mana_armor:
                who.bonusArmor += self.bonus
                who.bonusMag_armor += self.bonus
            elif self == as_one:
                who.rank_up_as_one = True
                who.bonusMaxMP += as_one.bonus
                as_one.given_bonus = as_one.bonus
        elif who.job == 'Rogue':
            if self == cutthroat:
                who.bonusCritMulti += cutthroat.bonus_crit_multi
            elif self == dagshur_mast:
                who.bonusAgi += dagshur_mast.bonus
                who.bonusLuck += dagshur_mast.bonus
                who.bonusHit += dagshur_mast.bonus
                who.bonusCrit += dagshur_mast.bonus
            elif self == fast_def:
                who.bonusArmor += fast_def.bonus
                who.bonusMag_armor += fast_def.bonus
            
                


basic_attack = Physical('Basic Attack',None,None,'Attack with your weapon','',0)
# Mage Skills #1
# attack skills
ember = Magical('Ember','mage/damage/ember.png','fire.wav','Burn the enemy','',3)
shower = Magical('Shower','mage/damage/shower.png','water.wav','Call the rain to fall','',3)
breeze = Magical('Breeze','mage/damage/breeze.png','wind.wav','Blow the enemy away','',3)
shock = Magical('Shock','mage/damage/shock.png','thunder.wav','Shock with electricity','',3)
fireball = Magical('Fireball','mage/damage/fireball.png','fire.wav','Lob a ball of fire','LV: 4, Ember: Rank 3',3)
river = Magical('River','mage/damage/river.png','water.wav','Call a river','LV: 4, Shower: Rank: 3',3)
gust = Magical('Gust','mage/damage/gust.png','wind.wav','Make the enemy fly','LV: 4, Breeze: Rank: 3',3)
thunderbolt = Magical('Thunderbolt','mage/damage/thunderbolt.png','thunder.wav','Pikachu','LV: 4, Shock: Rank: 3',3)
blaze = Magical('Blaze','mage/damage/blaze.png','fire.wav','Set enemy ablaze','LV: 10, Fireball: Rank: 3',3)
waterfall = Magical('Waterfall','mage/damage/waterfall.png','water.wav','A fall of water', 'LV: 10, River: Rank: 3',3)
whirlwind = Magical('Whirlwind','mage/damage/whirlwind.png','wind.wav','A strong wind','LV: 10, Gust: Rank: 3',3)
lightning = Magical('Lightning','mage/damage/lightning.png','thunder.wav','Electrify the enemy','LV: 10, Thunderbolt: Rank: 3',3)
inferno = Magical('Inferno','mage/damage/inferno.png','fire.wav','The strongest flames in the game','LV: 18, Blaze: Rank: 3',3)
tsunami = Magical('Tsunami','mage/damage/tsunami.png','water.wav','Wash away the enemy','LV: 18, Waterfall: Rank: 3',3)
tornado = Magical('Tornado','mage/damage/tornado.png','wind.wav','Blow away the enemy','LV: 18, Whirlwind: Rank: 3',3)
thunderstorm = Magical('Thunderstorm','mage/damage/thunderstorm.png','thunder.wav','Call thunder','LV: 18, Lightning: Rank: 3',3)
## Actives
mana_gaurd = Active('Mana Gaurd','mage/active/mana_gaurd.png','pheal.wav','Mana gaurds your health','LV: 2',3)
restore = Active('Restore','mage/active/restore.png','heal.wav','Restore health','LV: 4',5)
barrier = Active('Barrier','mage/active/barrier.png','charge.wav','Create a barrier','LV: 6',5)
meditate = Active('Meditate','mage/active/meditate.png','charge.wav','Focus your mind','LV: 9',4)

## Passives
corpse_drain = Passive('Corpse Drain','mage/passive/corpse_drain.png',None,'Gain more when killing','',1)
max_mp_inc = Passive('Max MP +','mage/passive/max_mp_inc.png',None,'Expand your mind','',7)
magic_mast = Passive('Spell Mastery','mage/passive/magic_mast.png',None,'Train your skills','LV: 5',5)
mana_armor = Passive('Mana Armor','mage/passive/mana_armor.png',None,'Mana is Armor','LV: 8',3)
as_one = Passive('As One','mage/passive/as_one.png',None,'You are one','LV: 5',1)

# lists in list
mage_skills_pg = [[ember,shower,breeze,shock,\
                   fireball,river,gust,thunderbolt,\
                   blaze,waterfall,whirlwind,lightning,\
                   inferno,tsunami,tornado,thunderstorm],\
                  [mana_gaurd,restore,barrier,meditate,None,None,None,None,\
                   max_mp_inc,magic_mast,mana_armor,as_one,corpse_drain,None,None,None]]



##### Rogue Skills
##
###name,img,sound,desc,requiredesc,maxRank):
### damage
bleed = Physical('Bleed','rogue/damage/bleed.png',None,'Enemy bleeds','',3)
cripple = Physical('Cripple','rogue/damage/cripple.png',None,'Cripple the enemy','',3)
life_steal = Physical('Life Steal','rogue/damage/double.png',None,'Steal health','LV: 2',3)
critical = Physical('Critcal Strike','rogue/damage/critical.png',None,'Attack critical spots','LV: 9',3)
mag_strike = Magical('Magic Strike','rogue/damage/mag_strike.png',None,'Imbue magic to weapon','',3)
poison_strike = Magical('Poison Strike','rogue/damage/poison_strike.png',None,'Weapon is dipped in poison','',3)
flash_bomb = Magical('Flash Bomb','rogue/damage/flash_bomb.png',None,'Throw a flash bomb','LV: 4',3)
swift = Magical('Swift','rogue/damage/swift.png',None,'Homing attack','LV: 7',3)
##
##
###actives
stealth = Active('Stealth','rogue/actives/stealth.png','stealth.wav',"Can't see me",'',5)
illusion = Active('Illusion','rogue/actives/illusion.png','multi_charge.wav','Where are you','',5)
intimidate = Active('Intimidate','rogue/actives/intimidate.png','stench.wav',"Make enemy mad",'',3)
blood_rit = Active('Blood Ritual','rogue/actives/blood_rit.png','blood_rit.wav',"Can't see you",'LV: 5',3)

### passives
cutthroat = Passive('Cutthroat','rogue/passive/cutthroat.png',None,'Want to kill','LV: 2',4)
dagshur_mast = Passive('Dag/Shur Mast.','rogue/passive/dagshur_mast.png',None,'Train your skills','LV: 5',5)
dual_wield = Passive('Dual Wield','rogue/passive/dual_wield.png',None,'Equip 2 weapons','LV: 3',1)
fast_def = Passive('Fast Defense','rogue/passive/fast_def.png',None,'Fast is defense','LV: 7',3)
sneaky = Passive('Sneaky','rogue/passive/sneaky.png',None,'Hide to be hidden','',1)
##
rogue_skills_pg = [[bleed,poison_strike,critical,mag_strike,\
                    life_steal,swift,cripple,flash_bomb,\
                    None,None,None,None,\
                    None,None,None,None],\
                   [stealth,illusion,intimidate,blood_rit,\
                    None,None,None,None,\
                    cutthroat,dagshur_mast,dual_wield,fast_def,\
                    sneaky,None,None,None]]




 ### Warrior Skills #1
##lunge = Skill('Lunge','lunge.png','Deal medium damage with increased crit chance but low hit chance')
##sonic = Skill()
##blaze = Skill()



























