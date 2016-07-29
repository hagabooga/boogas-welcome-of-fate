import pygame
from sounds import *
from images import *
from colors import *
from player import *
from items import *
from actions import *
from jobs import *
from weapons import *
from potions import *
from utilities import *
import random
import math
import time
import shelve


pygame.init()

inSome = Page()
inFight = Page()
inStore = Page()
inInv = Page()
inHosp = Page()
inSkill = Page()
inLearnSkill = Page()

fightText = switchTextbox(2,6) # used in fight

enemy = 'some Enemy()'


def skill_requirement(aSkill): ##### ALL SKILL REQUIREMENTS
    if player.job == 'Mage':
        if isinstance(aSkill,Magical):
            if aSkill == fireball:
                return player.LV >= 4 and ember.rank >= 3
            elif aSkill == river:
                return player.LV >= 4 and shower.rank >= 3
            elif aSkill == gust:
                return player.LV >= 4 and breeze.rank >= 3
            elif aSkill == thunderbolt:
                return player.LV >= 4 and shock.rank >= 3
            elif aSkill == blaze:
                return player.LV >= 10 and fireball.rank >= 3
            elif aSkill == waterfall:
                return player.LV >= 10 and river.rank >= 3
            elif aSkill == whirlwind:
                return player.LV >= 10 and gust.rank >= 3
            elif aSkill == lightning:
                return player.LV >= 10 and thunderbolt.rank >= 3
            elif aSkill == inferno:
                return player.LV >= 18 and blaze.rank >= 3
            elif aSkill == tsunami:
                return player.LV >= 18 and waterfall.rank >= 3
            elif aSkill == tornado:
                return player.LV >= 18 and whirlwind.rank >= 3
            elif aSkill == thunderstorm:
                return player.LV >= 18 and lightning.rank >= 3
            else:
                return True
        elif isinstance(aSkill,Active):
            if aSkill == mana_gaurd:
                return player.LV >= 2
            elif aSkill == restore:
                return player.LV >= 4
            elif aSkill == barrier:
                return player.LV >= 6
            elif aSkill == meditate:
                return player.LV >= 9
            else:
                return True
        elif isinstance(aSkill,Passive):
            if aSkill == magic_mast:
                return player.LV >= 5
            elif aSkill == mana_armor:
                return player.LV >= 8
            elif aSkill == as_one:
                return player.LV >=5
            else:
                return True
        else:
            return True
    elif player.job == 'Rogue':
        if isinstance(aSkill,Magical) or isinstance(aSkill,Physical):
            if aSkill == life_steal:
                return player.LV >= 2
            elif aSkill == critical:
                return player.LV >= 9
            elif aSkill == flash_bomb:
                return player.LV >= 4
            elif aSkill == swift:
                return player.LV >= 7
            else:
                return True
        elif isinstance(aSkill,Active):
            if aSkill == blood_rit:
                return player.LV >= 5
            else:
                return True
        elif isinstance(aSkill,Passive):
            if aSkill == cutthroat:
                return player.LV >= 2
            elif aSkill == dagshur_mast:
                return player.LV >= 5
            elif aSkill == dual_wield:
                return player.LV >= 3
            elif aSkill == fast_def:
                return player.LV >= 7
            else:
                return True
        else:
            return True
        

def skillUpdate():
    # attack skills
    basic_attack.damage = player.damage
    if dual_wield.rank > 0 and isinstance(player.lefthand,Weapon):
        basic_attack.damage = round(player.damage/2)
    basic_attack.mana = 0
    if player.job == 'Mage': # MAGE SKILLS
        ### Damage Skills
        # Fire
        ember.damage = round(80 + (player.mag_damage/1.8)*(1.8 * (1 + ember.rank)))
        ember.mana = round(50 + ember.damage/(17-ember.rank) + ember.rank * 35)
        ember.burn_chance = round(15 + 3*ember.rank + player.mag_damage/(25 + player.mag_damage/4))
        ember.effdesc = ['Chance to inflict Burn: %i%%'%ember.burn_chance]
        fireball.damage = round(175*fireball.rank + ember.damage + (player.mag_damage/1.75)*(1.8 * (1 + fireball.rank)))
        fireball.mana = round(ember.mana + fireball.damage/(15-fireball.rank) + fireball.rank * 50)
        fireball.burn_chance = round(ember.burn_chance + 3*fireball.rank + player.mag_damage/(25 + player.mag_damage/4))
        fireball.effdesc = ['Chance to inflict Burn: %i%%'%fireball.burn_chance]
        blaze.damage = round(325*blaze.rank + fireball.damage + (player.mag_damage/1.7)*(1.8 * (1 + blaze.rank)))
        blaze.mana = round(fireball.mana + blaze.damage/(15-blaze.rank) + blaze.rank * 125)
        blaze.burn_chance = round(fireball.burn_chance + 4*blaze.rank + player.mag_damage/(25 + player.mag_damage/4))
        blaze.effdesc = ['Chance to inflict Burn: %i%%'%blaze.burn_chance]
        inferno.damage = round(450*inferno.rank + blaze.damage + (player.mag_damage/1.65)*(1.8 * (1 + inferno.rank)))
        inferno.mana = round(blaze.mana + inferno.damage/(15-inferno.rank) + inferno.rank * 210)
        inferno.burn_chance = round(blaze.burn_chance + 5*inferno.rank + player.mag_damage/(25 + player.mag_damage/4))
        inferno.effdesc = ['Chance to inflict Burn: %i%%'%inferno.burn_chance]
        # Water
        shower.damage = round(88 + (player.mag_damage/1.7)*(1.85 * (1 + shower.rank)))
        shower.mana = round(45 + shower.damage/(20-shower.rank) + shower.rank * 25)
        shower.hit_chance = round(20 + 3.5*shower.rank)
        shower.effdesc = ['Hit Chance: +%i%%'%shower.hit_chance]
        river.damage = round(200*river.rank + shower.damage + (player.mag_damage/1.65)*(1.85 * (1 + river.rank)))
        river.mana = round(shower.mana + river.damage/(20-river.rank) + river.rank * 60)
        river.hit_chance = round(shower.hit_chance + 3.5*river.rank)
        river.effdesc = ['Hit Chance: +%i%%'%river.hit_chance]
        waterfall.damage = round(375*waterfall.rank + river.damage + (player.mag_damage/1.6)*(1.85 * (1 + waterfall.rank)))
        waterfall.mana = round(river.mana + waterfall.damage/(20-waterfall.rank) + waterfall.rank * 100)
        waterfall.hit_chance = round(river.hit_chance + 3.5*waterfall.rank)
        waterfall.effdesc = ['Hit Chance: +%i%%'%waterfall.hit_chance]
        tsunami.damage = round(500*tsunami.rank + waterfall.damage + (player.mag_damage/1.5)*(1.85 * (1 + tsunami.rank)))
        tsunami.mana = round(waterfall.mana + tsunami.damage/(20-tsunami.rank) + tsunami.rank * 225)
        tsunami.hit_chance = round(waterfall.hit_chance + 3.5*tsunami.rank)
        tsunami.effdesc = ['Hit Chance: +%i%%'%tsunami.hit_chance]
        # Wind
        breeze.damage = round(76 + (player.mag_damage/2.0)*(2.1 * (1 + breeze.rank)))
        breeze.mana = round(60 + breeze.damage/(23-breeze.rank) + breeze.rank * 20)
        breeze.crit_chance = round(26 + 4*breeze.rank)
        breeze.hit_chance = round(-20 + 2*breeze.rank)
        breeze.effdesc = ['Crit Chance: +%i%%, Hit Chance: %i%%'%(breeze.crit_chance,breeze.hit_chance)]
        gust.damage = round(140*gust.rank + breeze.damage + (player.mag_damage/2.0)*(2.2 * (1 + gust.rank)))
        gust.mana = round(breeze.mana + gust.damage/(23-gust.rank) + gust.rank * 40)
        gust.crit_chance = round(breeze.crit_chance + 3*gust.rank)
        gust.hit_chance = round(breeze.hit_chance + 2*gust.rank)
        gust.effdesc = ['Crit Chance: +%i%%, Hit Chance: %i%%'%(gust.crit_chance,gust.hit_chance)]
        whirlwind.damage = round(300*whirlwind.rank + gust.damage + (player.mag_damage/1.9)*(2.3 * (1 + whirlwind.rank)))
        whirlwind.mana = round(gust.mana + whirlwind.damage/(23-whirlwind.rank) + whirlwind.rank * 80)
        whirlwind.crit_chance = round(gust.crit_chance + 3*whirlwind.rank)
        whirlwind.hit_chance = round(gust.hit_chance + 1*whirlwind.rank)
        whirlwind.effdesc = ['Crit Chance: +%i%%, Hit Chance: %i%%'%(whirlwind.crit_chance,whirlwind.hit_chance)]
        tornado.damage = round(415*tornado.rank + whirlwind.damage + (player.mag_damage/1.8)*(2.4 * (1 + tornado.rank)))
        tornado.mana = round(whirlwind.mana + tornado.damage/(23-tornado.rank) + tornado.rank * 200)
        tornado.crit_chance = round(whirlwind.crit_chance + 3*tornado.rank)
        tornado.hit_chance = round(whirlwind.hit_chance + 1*tornado.rank)
        tornado.effdesc = ['Crit Chance: +%i%%, Hit Chance: %i%%'%(tornado.crit_chance,tornado.hit_chance)]
        # Electric
        shock.damage = round(100 + (player.mag_damage/1.7)*(1.9 * (1 + shock.rank)))
        shock.mana = round(60 + shock.damage/(14-shock.rank) + shock.rank * 50)
        shock.para_chance = round(20 + 3*shock.rank + player.mag_damage/(25 + player.mag_damage/4))
        shock.crit_chance = round(14 + 3*shock.rank)
        shock.effdesc = ['Chance to Paralyze: %i%%, Crit Chance: +%i%%'%(shock.para_chance,shock.crit_chance)]
        thunderbolt.damage = round(250*thunderbolt.rank + shock.damage + (player.mag_damage/1.6)*(2 * (1 + thunderbolt.rank)))
        thunderbolt.mana = round(shock.mana + thunderbolt.damage/(14-thunderbolt.rank) + thunderbolt.rank * 60)
        thunderbolt.para_chance = round(shock.para_chance + 3*thunderbolt.rank + player.mag_damage/(25 + player.mag_damage/3.8))
        thunderbolt.crit_chance = round(25 + 3*thunderbolt.rank)
        thunderbolt.effdesc = ['Chance to Paralyze: %i%%, Crit Chance: +%i%%'%(thunderbolt.para_chance,thunderbolt.crit_chance)]
        lightning.damage = round(425*lightning.rank + thunderbolt.damage + (player.mag_damage/1.5)*(2.1 * (1 + lightning.rank)))
        lightning.mana = round(thunderbolt.mana + lightning.damage/(14-lightning.rank) + lightning.rank * 100)
        lightning.para_chance = round(thunderbolt.para_chance + 3*lightning.rank + player.mag_damage/(25 + player.mag_damage/3.6))
        lightning.crit_chance = round(35 + 2*lightning.rank)
        lightning.effdesc = ['Chance to Paralyze: %i%%, Crit Chance: +%i%%'%(lightning.para_chance,lightning.crit_chance)]
        thunderstorm.damage = round(525*thunderstorm.rank + lightning.damage + (player.mag_damage/1.4)*(2.2 * (1 + thunderstorm.rank)))
        thunderstorm.mana = round(lightning.mana + thunderstorm.damage/(14-thunderstorm.rank) + thunderstorm.rank * 200)
        thunderstorm.para_chance = round(lightning.para_chance + 4*thunderstorm.rank + player.mag_damage/(25 + player.mag_damage/3.4))
        thunderstorm.crit_chance = round(42 + 2*thunderstorm.rank)
        thunderstorm.effdesc = ['Chance to Paralyze: %i%%, Crit Chance: +%i%%'%(thunderstorm.para_chance,thunderstorm.crit_chance)]
        ### Actives (has unique detail)
        mana_gaurd.mana = round(75*mana_gaurd.rank + (player.MP*0.25)/(mana_gaurd.rank+1))
        mana_gaurd.cooldown = 5
        mana_gaurd.turnEnd = 5
        mana_gaurd.effdesc = ['For 5 turns, when recieving damage from enemy,','your Current Mana takes the damage instead'\
                              ,'of your HP. When no MP is available,','damage is applied normally','',\
                              'Cooldown: %i Turns, Mana Cost: %i'%(mana_gaurd.cooldown,mana_gaurd.mana)]
        restore.hp = round(150+restore.rank*50 + player.maxHP/(8 - restore.rank) + player.mag_damage*0.5/player.maxHP)
        restore.bonus_stat = round(player.mag_damage/99 + restore.rank*6.5)
        restore.cooldown = 3
        restore.turnEnd = 3
        restore.mana = round(50 + player.mag_damage*0.6*(1 - restore.rank/20))
        restore.effdesc = ['For 3 turns, gain Luck/Hit/Crit: +%i'%restore.bonus_stat,\
                          'and restore HP: +%i'%(restore.hp),'',\
                          'Cooldown: %i Turns, Mana Cost: %i'%(restore.cooldown,restore.mana)]
        barrier.shield = round(75 + barrier.rank*6 + player.mag_damage*(1.5+0.8*barrier.rank)*(1+barrier.rank/5))
        barrier.cooldown = 5
        barrier.turnEnd = 3
        barrier.mana = round(60 + barrier.rank*50 + player.mag_damage*0.25)
        barrier.effdesc = ['For 3 turns, create a damage blocking shield.','Shield always takes damage first.','',\
                           'Shield Amount: %i,'%barrier.shield,\
                           'Cooldown: %i Turns, Mana Cost: %i'%(barrier.cooldown,barrier.mana)]
        meditate.scale = round(215 + (meditate.rank-1)*15)
        meditate.cooldown = 7 - meditate.rank
        meditate.mana = round(200 + player.maxMP/(15 + meditate.rank))
        meditate.effdesc = ['The next Magical Damage Skill you cast','will deal massive damage.','',\
                            'Multiplier: %i%%, Cooldown: %i Turns'%(meditate.scale,meditate.cooldown),\
                           'Mana Cost: %i'%meditate.mana]
        ### Passives (has unique detail)
        corpse_drain.bonus_chance1 = round(15+player.LV/5+6*corpse_drain.rank)
        corpse_drain.bonus_chance2 = round(8+player.LV/2+4*corpse_drain.rank)
        corpse_drain.restore_mp1 = 30+2*corpse_drain.rank
        corpse_drain.restore_mp2 = 35+3*corpse_drain.rank
        corpse_drain.effdesc = ['Whenever you defeat and enemy,',\
                                'you have %i%% chance to gain %i%% of maxMP as MP'%(corpse_drain.bonus_chance1,corpse_drain.restore_mp1),\
                                'Also whenever you cast a Damaging Skill,',\
                                'you have a %i%% chance to gain %i%% of its cost'%(corpse_drain.bonus_chance2,corpse_drain.restore_mp2)]
        max_mp_inc.bonus = round((320 + 245*max_mp_inc.rank)*(1 + max_mp_inc.rank/65)) # each level gains amount
        max_mp_inc.effdesc = ['Each time you Rank up this skill,',\
                              'gain a set amount of Max MP permanantly.',''\
                              'Gain Max MP: +%i'%(max_mp_inc.bonus)]
        magic_mast.bonus = 6
        magic_mast.effdesc = ['When wielding a Staff or a Wand,','',\
                              'Luck/Hit/Crit: +%i, Next rank: +%i'%(magic_mast.bonus*magic_mast.rank,magic_mast.bonus*(magic_mast.rank+1))]
        mana_armor.bonus = round(player.maxMP/40)
        mana_armor.effdesc = ['Instantly gain Bonus Armor/Resist',\
                              'based off your Current Maximum MP',''\
                              'When ranked up, Armor/Resist: +%i instantly'%mana_armor.bonus]
        as_one.bonus = (player.stren*2 + player.maxHP)*3
        as_one.effdesc = ['Permamantly set your Strength AND HP to 1',\
                          'and gain bonus MP based off the difference',\
                          'of your Strength and HP']
        if not player.rank_up_as_one:
            as_one.effdesc = ['When ranked up, Max MP:  +%i'%as_one.bonus]
        else:
            as_one.effdesc = ['You have gained, Max MP: +%i'%as_one.given_bonus]
    elif player.job == 'Rogue': # ROGUE SKILL
        #damaging
        bleed.damage = round(35 + 8*bleed.rank + (player.damage/1.2)*(1.175 + bleed.rank/1.5))
        bleed.mana = round(30 + bleed.damage/(17-bleed.rank) + bleed.rank * 35)
        bleed.bleed_chance = round(15 + 3*bleed.rank + player.damage/(25 + player.mag_damage/4))
        bleed.effdesc = ['Chance to inflict Bleed: %i%%'%bleed.bleed_chance]
        cripple.damage = round(50 + 8*cripple.rank + (player.damage/1.3)*(1.1 + cripple.rank/2))
        cripple.mana = round(60 + cripple.damage/(17-cripple.rank) + cripple.rank * 50)
        cripple.cripple_chance = round(16 + 5*cripple.rank + player.damage/(25 + player.damage/4))
        cripple.effdesc = ['Chance to inflict Cripple: %i%%'%cripple.cripple_chance]
        life_steal.damage = round(40 + player.damage*(1+life_steal.rank*0.5))
        life_steal.steal = 30+10*life_steal.rank
        life_steal.mana = round(60 + life_steal.damage/(15-life_steal.rank) + life_steal.rank * 35)
        life_steal.effdesc = ['Damage dealt will be restored as HP',''\
                              'Damage Dealt: %i%% Restored'%life_steal.steal]
        critical.crit_multi = 50*critical.rank
        critical.damage = round(player.damage)
        critical.mana = round(100 + critical.damage/(13-critical.rank) + critical.rank * 52)
        critical.crit_chance = round(999)
        critical.effdesc = ['Gaurentees crit and crit multiplier +%i%%'%critical.crit_multi]
        mag_strike.damage = round(player.mag_damage + 30*mag_strike.rank + (player.mag_damage/1.17)*(1.6 + mag_strike.rank/2.4))
        mag_strike.mana = round(35 + mag_strike.damage/(16-mag_strike.rank) + mag_strike.rank * 40)
        mag_strike.effdesc = ['Deal Magic damage']
        poison_strike.damage = round(player.mag_damage*(0.35+poison_strike.rank*0.06))
        poison_strike.mana = round(45 + poison_strike.damage/(17-poison_strike.rank) + poison_strike.rank * 35)
        poison_strike.poison_chance = round(56 + 4*poison_strike.rank + player.mag_damage/(25 + player.mag_damage/4))
        poison_strike.effdesc = ['Chance to Poison: %i%%'%poison_strike.poison_chance]
        flash_bomb.damage = round(35 + 65*flash_bomb.rank)
        flash_bomb.mana = round(50 + flash_bomb.rank * 35)
        flash_bomb.blind_chance = round(55 + 5*flash_bomb.rank)
        flash_bomb.effdesc = ['Chance to blind enemy: %i%%'%flash_bomb.blind_chance]
        swift.damage = round(75 + 20*swift.rank + (player.damage/2)*(1.6 + swift.rank/5))
        swift.hit_chance = 999
        swift.mana = round(75 + swift.damage/(17-swift.rank) + swift.rank * 25)
        swift.effdesc = ['This skill cannot miss']
        # Actives
        stealth.mana = 100 + 100*stealth.rank
        stealth.dodge_chance = round(43 + 7*stealth.rank)
        stealth.crit_chance = round(47 + 6*stealth.rank)
        stealth.crit_multi = round(25 + 10*stealth.rank)
        stealth.cooldown = 5
        stealth.turnEnd = 3
        stealth.effdesc = ['Gain %i%% Dodge Chance for 3 Turns,'%stealth.dodge_chance,\
                           'This effect ends when you attack.','',\
                           'While still active, your next attack will have:',\
                           'Critical Chance: +%i%% and Crit Multiplier: +%i%%'%(stealth.crit_chance,stealth.crit_multi),'',\
                           'Cooldown: %i Turns, Mana Cost: %i'%(stealth.cooldown,stealth.mana)]
        illusion.mana = 150 + 75*illusion.rank
        illusion.dodge_chance = round(34 + 13*illusion.rank)
        illusion.cooldown = 3
        illusion.turnEnd = 2
        illusion.effdesc = ['For 2 turns, gain %i%% Dodge Chance.'%illusion.dodge_chance,\
                            'If no damage is taken during these 2 turns,',\
                            '(does not include status effect damage)',\
                            'inflict Confuse plus another random status','',\
                            'Cooldown: %i Turns, Mana Cost: %i'%(illusion.cooldown,illusion.mana)]
        intimidate.mana = 180 + 50*stealth.rank
        intimidate.bonus_damage = round(10 + player.LV*(2*intimidate.rank) + 50*intimidate.rank)
        intimidate.dodge_chance = round(13 + 12*intimidate.rank)
        intimidate.effdesc = ['You and Enemy take %i Bonus Damage'%intimidate.bonus_damage,\
                              'from any attack BUT gain %i%% Dodge Chance'%intimidate.dodge_chance,\
                              '(scales with LV)','',\
                              'Mana Cost: %i'%intimidate.mana]
        blood_rit.mana = round(player.maxHP/20 + 100 + player.LV*200/(7-blood_rit.rank*1.3))
        blood_rit.bonus = 5 + 25*blood_rit.rank
        blood_rit.crit_chance = round(15 + blood_rit.mana/18) 
        blood_rit.crit_multi = round(blood_rit.crit_chance/1.2)
        blood_rit.effdesc = ["Lose %i HP to gain Str/Mag: +%i for 5 Turns"%(blood_rit.mana,blood_rit.bonus),\
                             'Also, Crit Chance: +%i%%, Crit Multiplier: +%i%%'%(blood_rit.crit_chance,blood_rit.crit_multi),'',\
                             'Mana Cost: %i'%blood_rit.mana]
        # Passives
        cutthroat.bonus_dmg = round((10 + (5*cutthroat.rank)*cutthroat.rank))
        cutthroat.bonus_crit_multi = 15
        cutthroat.effdesc = ['Any attack, Damage: +%i'%cutthroat.bonus_dmg,\
                             'Crit Multiplier: +%i%%'%(cutthroat.bonus_crit_multi*cutthroat.rank)]
        dagshur_mast.bonus = 6
        dagshur_mast.effdesc = ['When a Wand or Staff is equipped,',
                               'Agi/Luck/Hit/Crit: +%i, Next rank: +%i'%(dagshur_mast.bonus*dagshur_mast.rank,dagshur_mast.bonus*(dagshur_mast.rank+1))]
        dual_wield.damage = 65
        dual_wield.effdesc = ['Allows a Weapon to be equipped on the ',\
                              'Left Hand. Basic Attacks now attack ',\
                              'twice when a second weapon is equipped,',\
                              'each dealing 50% of your total attack','',\
                              'Left Hand Weapon ATK/MATK Bonus: %i%%'%dual_wield.damage]
        fast_def.bonus = round(player.dodge*(5+7*fast_def.rank))
        fast_def.effdesc = ['When ranked up,',\
                            'gain Armor/Resist: +%i instantly.'%fast_def.bonus,'',\
                            'Bonus is based of current Dodge Chance']
        sneaky.bonus = 1 + player.LV
        sneaky.effdesc = ['Chance for enemy to miss an attack: +%i%%'%sneaky.bonus,\
                          'Does not increase Dodge Chance']
        
        
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
        self.crit_multi = 225
        ## SKILLS
        self.basic = Physical('Basic Attack',None,None,'','',0)
        self.curse = Magical('Curse',None,'curse.wav','','',0)
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
        
def gameover():
    inSome.enter()
    pygame.mixer.music.load('fail.mp3')
    pygame.mixer.music.load('fail.mp3')
    pygame.mixer.music.play(0)
    pygame.mixer.music.play(0)
    while inSome.show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
        screen.fill(white)
        textbox('You Died! Try Again?',50,black,screenW/2,325)
        textbox('(you will lose half of your money)',30,black,screenW/2,380)
        button('Yes',80,200,450,200,200,green,lightGreen,inSome.leave,None)
        button('No',80,650,450,200,200,red,lightRed,quitGame,None)
        pygame.display.update()
    player.healFullHP()
    player.cash = round(player.cash/2)
    time.sleep(0.5)

def status_bar():
    ### SHIELD BAR
    if player.shield_hp > 0:
        shield_perc = (player.shield_hp/barrier.shield)*100
        pygame.draw.rect(screen, orange, (190,708 , 400/(100/round(shield_perc)),50)) # BAR
        pygame.draw.rect(screen, lightOrange, (190,708 , 400,50), 4) # OUTLINE
        textbox('Shield',40,black,245,730)
        textbox('%i / %i'%(player.shield_hp,barrier.shield),40,black,420,730)
    else:
    #### HP BAR
        hp_perc = round((player.HP/player.maxHP)*100)
        if hp_perc == 0:
            pygame.draw.rect(screen, red, (190,708 , 0,50)) # BAR
        else:
            pygame.draw.rect(screen, red, (190,708 , 400/(100/hp_perc),50)) # BAR
        pygame.draw.rect(screen, lightestRed, (190,708 , 400,50), 4) # OUTLINE
        textbox('HP',40,black,220,730)
        textbox('%i / %i'%(player.HP,player.maxHP),40,black,400,730)
    #### MP BAR
    mp_perc = round((player.MP/player.maxMP)*100)
    if mp_perc == 0:
        pygame.draw.rect(screen, lightCyan, (604,708 , 0, 50)) # BAR
    else:
        pygame.draw.rect(screen, lightCyan, (604,708 , 400/(100/mp_perc),50)) # BAR
    pygame.draw.rect(screen, cyan, (604,708 , 400,50),4 ) # OUTLINE
    textbox('MP',40,black,635,730)
    textbox('%i / %i'%(player.MP,player.maxMP),40,black,814,730)
    ## LEVEL AND NAME
    textbox('LV %i  %s'%(player.LV,player.job),25,black,95,717)
    textbox(player.name,39-2*len(player.name),black,90,742)

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
            if boolButton('Continue',30,850,screenH/1.35,75,75,green,lightGreen):
                inSome.leave()
                player.old_stren = player.new_stren
                player.old_intel = player.new_intel
                player.old_agi = player.new_agi
                player.old_luck = player.new_luck
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
            return Rogue()
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
                if event.key == pygame.K_2 or event.key == pygame.K_ESCAPE:
                    inSome.show = False
        screen.fill(cyan)
        status_bar()
        textbox('STATS',60,lightRed,screenW/2,40)
        #
        textbox('LV: %i'%player.LV,35,black,220,50)
        textbox('Job: %s'%player.job,35,purple,220,90)
        textbox('Strength: %i + %i = %i'%(player.new_stren,player.bonusStren,player.stren),35,red,220,130)
        textbox('Intelligence: %i + %i = %i'%(player.new_intel,player.bonusIntel,player.intel),35,blue,220,170)
        textbox('Agility: %i + %i = %i'%(player.new_agi,player.bonusAgi,player.agi),35,lighterGreen,220,210)
        textbox('Luck: %i + %i = %i'%(player.new_luck,player.bonusLuck,player.luck),35,yellow,220,250)
        #
        textbox('Armor: %i + %i = %i'%(player.armorU(),player.bonusArmor,player.armor),35,red,220,320)
        textbox('Resist: %i + %i = %i'%(player.mag_armorU(),player.bonusMag_armor,player.mag_armor),35,blue,220,360)
        #
        textbox('Max HP: %i + %i = %i'%(player.maxHPU(),player.bonusMaxHP,player.maxHP),35,red,700,170)
        textbox('Max MP: %i + %i = %i'%(player.maxMPU(),player.bonusMaxMP,player.maxMP),35,blue,700,210)
        textbox('Physical Damage: %i + %i = %i'%(player.damageU(),player.bonusPdmg,player.damage),35,red,700,300)
        textbox('Magic Damage: %i + %i = %i'%(player.mag_damageU(),player.bonusMdmg,player.mag_damage),35,blue,700,340)
        #
        textbox('Hit Rate: %i%% + %i%% = %i%%'%(player.hitU(),player.bonusHit,player.hit),35,lighterGreen,450,430)
        textbox('Dodge Chance: %i%% + %i%% = %i%%'%(player.dodgeU(),player.bonusDodge,player.dodge),35,blue,450,470)
        textbox('Critical Chance: %i%% + %i%% = %i%%'%(player.critU(),player.bonusCrit,player.crit),35,red,450,530)
        textbox('Critical Mutliplier: 225 + %i%% = %i%%'%(player.bonusCritMulti,225+player.bonusCritMulti),35,yellow,450,570)
        #
        textbox('Experience: %i / %i'%(player.exp,player.max_exp),35,yellow,450,640)
        textbox('''Press 2 to leave''',30,brown,875,510)
        pygame.display.update()
        
def checkEquip(slot):
    if isinstance(slot,Weapon) and slot is not player.weapon and slot != player.weapon and slot != player.lefthand: # and player.weapon == fists
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
            if player.job == 'Rogue' and dual_wield.rank > 0 and player.weapon != player.fists and slot != player.weapon and slot != player.lefthand:
                saved_item = None
                if player.lefthand != player.fap and slot != player.lefthand: # if has weapon equipped already
                    saved_item = player.lefthand
                    player.loseItemBonus(saved_item)
                    # remove left hand weapon atk/matk
                    player.bonusPdmg -= dual_wield.equip_bonus[0]
                    player.bonusMdmg -= dual_wield.equip_bonus[1]
                player.lefthand = slot
                player.addItemBonus(slot)
                ### add left hand weapon atk/matk
                dual_wield.equip_bonus = [round((player.lefthand.damage*(1+player.stren/20))*(dual_wield.damage/100)),\
                                          round((player.lefthand.mag_damage*(1+player.intel/20))*(dual_wield.damage/100))]
                player.bonusPdmg += dual_wield.equip_bonus[0]
                player.bonusMdmg += dual_wield.equip_bonus[1]
                player.numItemInv -= 1
                player.inv.remove(slot)
                player.inv.append(None)
                if saved_item != None:   # put weapon in inv
                    player.inv[player.numItemInv] = saved_item
                    player.numItemInv += 1
                equip_sound.play()
                time.sleep(0.3)
            elif slot != player.lefthand:
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
    # remove lefthand weapons (ROGUE)
    elif dual_wield.rank > 0 and slot is player.lefthand and player.lefthand != player.fap and player.numItemInv < player.numMaxItem:
        player.loseItemBonus(slot)
        #lose bonus
        player.bonusPdmg -= dual_wield.equip_bonus[0]
        player.bonusMdmg -= dual_wield.equip_bonus[1]
        player.inv[player.numItemInv] = player.lefthand
        player.numItemInv += 1
        player.lefthand = player.fap
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
    elif slot == player.lefthand and player.lefthand != player.fap and player.lefthand != no_left \
         and slot not in player.inv and player.numItemInv < player.numMaxItem and isinstance(slot,Weapon):
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
        player.numItemInv -= status
        player.inv.remove(slot)
        player.inv.append(None)
        if saved_item != None:   # put weapon in invtime.sleep(0.3)
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
##    player.statUpdate()
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
            if skill_requirement(slot):
                if x+w > mouse[0] > x and y+h > mouse[1] > y:  # show box and highlight when mouse hovers over
                    pygame.draw.rect(screen, lightGrey, (x,y,w,h))
                else:
                    pygame.draw.rect(screen, skyBlue, (x,y,w,h))
            else:
                if x+w > mouse[0] > x and y+h > mouse[1] > y:  # show box and highlight when mouse hovers over
                    pygame.draw.rect(screen, orange, (x,y,w,h))
                else:
                    pygame.draw.rect(screen, brown, (x,y,w,h))
    elif inFight.show and not inInv.show: 
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
                                if skill_requirement(slot):
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
                                            slot.giveBonus(player)
                                            player.statUpdate()
                                            skillUpdate()
                                    else:
                                        textbox('Skill at max rank!',35,blue,800,304)
                                else:
                                    textbox('Requirements not met!',35,blue,800,304)
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
                                    textbox('Skill at max rank!',35,blue,800,304)
                            else:
                                textbox('Maximum number of skills learned!',35,blue,800,304)
                        else:
                            if  slot != None and not skill_requirement(slot):
                                textbox('Requirements not met!',35,blue,800,304)
                            elif slot != None:
                                    textbox('Not enough SP!',35,blue,800,304)
                elif pygame.mouse.get_pressed()[2] and inLearnSkill.show and slot != None: # Remove a skill
                    removeSkill(slot)
            else: # inFight use skill
                if slot != None:
                    itemValue(slot)
                    if pygame.mouse.get_pressed()[0]:
                        if hasattr(slot,'cooldownEnd'):
                            if slot.cooldownEnd <= fightText.turn:
                                del slot.cooldownEnd
                            else:
                                textbox('On cooldown! %i Turns Left'%(slot.cooldownEnd - fightText.turn),30,blue,800,304)
                        elif player.MP - slot.mana < 0: # check if player has enough mana
                            textbox('Not enough MP!',35,blue,800,304)
                        else:
                            if isinstance(slot,Active):
                                if slot in player.fight_actives:
                                    textbox('Already active!',35,blue,800,304)
                                else:
                                    dmg_calc(slot)
                            else:
                                dmg_calc(slot) # regular attack
                            player.statUpdate()
                            skillUpdate()
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
                elif event.key == pygame.K_e or event.key == pygame.K_ESCAPE:
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
                elif event.key == pygame.K_e or event.key == pygame.K_ESCAPE:
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
            if inStore.show:
                textbox('Not enough gold!',30,blue,775,425)
            elif inHosp.show:
                textbox('Not enough gold!',40,blue,835,180)
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
                        elif event.key == pygame.K_e or event.key == pygame.K_ESCAPE:
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
            textbox(slot.desc,30,black,800,170)
            if len(slot.requiredesc) != 0:
                textbox('Requirement(s):  (%s)'%slot.requiredesc,16,black,800,210)
            textbox('Rank: %i/%i (%s)'%(slot.rank,slot.maxRank,slot.type),40,black,800,250)
            y = 0
            for line in range(len(slot.effdesc)):
                textbox(slot.effdesc[line],20,black,800,350+y)
                y += 25 
            if isinstance(slot,Physical):
                textbox('Physical Damage: %i, Mana Cost: %i'%(slot.damage,slot.mana),25,black,800,390+y)
            elif isinstance(slot,Magical):
                textbox('Magic Damage: %i, Mana Cost: %i'%(slot.damage,slot.mana),25,black,800,390+y)
                    
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
                    if event.key == pygame.K_3 and inFight or event.key == pygame.K_ESCAPE:
                        leaveLearnSkill()
        screen.fill(skyBlue)
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
                if event.key == pygame.K_3 or event.key == pygame.K_ESCAPE:
                    inSkill.show = False
        screen.fill(skyBlue)
        if pg_num - 1 >= 0:
            if boolButton('',0,13,47,35,35,lightGrey,skyBlue):
                pg_num -= 1
                pg_flip.play()
            screen.blit(small_arrow_left,centerIMG(30,30,30,65))
        if pg_num + 1 <= len(mage_skills_pg) - 1:
            if boolButton('',0,528,47,35,35,lightGrey,skyBlue):
                pg_num += 1
                pg_flip.play()
            screen.blit(small_arrow_right,centerIMG(30,30,545,65))
        textbox('%s Skills'%player.job,60,black,280,50)
        if player.job == 'Mage':
            matrixSlot(4,4,mage_skills_pg[pg_num],40,125,140,140)
        elif player.job == 'Rogue':
                matrixSlot(4,4,rogue_skills_pg[pg_num],40,125,140,140)
        textbox('SP: %i'%player.SP,50,black,905,630)
        textbox('Press 3 to leave',20,black,300,680)
        button('Learned Skills',30,660,575,100,100,red,lightRed,learnedSkillsPage,None)
        status_bar()
        pygame.display.update()

def enemyAttack():
    fakeFight()
    fight_shown_text = []
    enemy.updateSkill()
    used_skill = enemy.randSkill()
    if enemy.isPara or enemy.isConf:
        if enemy.isPara:
            fight_shown_text.append(["Enemy can't move!",lightYellow])
        elif enemy.isConf:
            fight_shown_text.append(["Enemy is confused!",orange])
        fightText.addText(fight_shown_text)
        pygame.display.update()
    else:
        if enemy.MP - used_skill.mana < 0:
            used_skill = enemy.basic
        damage = Action.skillAttack(enemy, player,used_skill)
        if damage != None:
            if illusion in player.fight_actives:
                illusion.notHit = False
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
            if status_eff != None:
                fight_shown_text.append(status_eff.text)
        else:
            fight_shown_text.append(['Enemy Misses!',orange])
            # illusion activate
            if illusion in player.fight_actives and illusion.notHit and illusion.turnEnd == fightText.turn:
                player.fight_actives.remove(illusion)
                enemy.fight_status.append(st_conf)
                fight_shown_text.append(st_conf.text)
                random_status = random.choice(allStatus)
                enemy.fight_status.append(random_status)
                fight_shown_text.append(random_status.text)
                illusion.loseEffect(player)
            ###
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


def fakeFight():
    screen.fill(white)
    # Enemy Details
    screen.blit(enemy.img, centerIMG(255,255,800,175))
    textbox('%s'%enemy.name,40,black,800,340)
    textbox('HP: %i'%(enemy.HP),45,lightRed,800,395)
    textbox('MP: %i'%(enemy.MP),45,lightBlue,800,455)
    ###
    button('Attack',30,25,25,75,75,green,lightGreen,doNone,None)
    button('Skills',30,25,125,75,75,lightCyan,cyan,doNone,None)
    button('Run',30,25,225,75,75,red,lightRed,doNone,None)
    textbox('Turn: %i'%(fightText.turn),25,black,60,340)
    screen.blit(player.img,(325,150))
    showActivesAndStatus()
    status_bar()


def status_calc(status,victim):
    if status == st_burn:
        burn_damage = round(victim.maxHP/10 - random.choice(range(round(victim.maxHP/100))) + random.choice(range(10 + round(victim.maxHP/80))))
        victim.HP -= burn_damage
        return burn_damage
    elif status == st_para:
        if 50 >= random.choice(range(101)):
            victim.isPara = True
        else:
            victim.isPara = False
    elif status == st_curse:
        curse_damage = round(victim.maxHP/20 + random.choice(range(10 + round(victim.maxHP/80)))) 
        victim.HP -= curse_damage
        return curse_damage
    elif status == st_bleed:
        bleed_damage = round(victim.maxHP/8 + random.choice(range(10 + round(victim.maxHP/80))))
        victim.HP -= bleed_damage
        return bleed_damage
    elif status == st_poison:
        poison_damage = round(victim.maxHP/4 + random.choice(range(10 + round(victim.maxHP/80))))
        victim.HP -= poison_damage
        return poison_damage
    elif status == st_conf:
        chance = random.choice(range(2)) == 0
        if chance:
            enemy.isConf = True
            conf_damage = round(random.choice(range(10 + round(victim.maxHP*0.25))))
        else:
            enemy.isConf = False
            conf_damage = None
        return conf_damage
    else:
        return None
    
def dmg_calc(used_skill):
    leaveLearnSkill()
    fightText.turn += 1
    fightText.pg_num = fightText.pages
    fight_shown_text = []
    success_run = None
    ### Reset status 
    enemy.isPara = False
    enemy.isConf = False
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
            if status_eff != None:
                fight_shown_text.append(status_eff.text)
        else:
            fight_shown_text.append(['You Missed!',blue])
        #### DUAL WIELD ATTACK #####
        if player.job == 'Rogue' and dual_wield.rank > 0 and used_skill == basic_attack and isinstance(player.lefthand,Weapon):
            fight_shown_text.append(['You use %s (Left)'%used_skill.name,black])
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
                if status_eff != None:
                    fight_shown_text.append(status_eff.text)
            else:
                fight_shown_text.append(['You Missed!',blue])
    #################    
    elif isinstance(used_skill,Active):
        fight_shown_text.append(['You use %s'%used_skill.name,black])
        Action.skillActive(player,enemy,used_skill)
        Active.effect(used_skill,player)
        player.statUpdate()
        if hasattr(used_skill,'turnEnd'):
                used_skill.setTurnEnd(fightText.turn,used_skill.turnEnd)
        if hasattr(used_skill,'cooldown'):
                used_skill.setCooldownEnd(fightText.turn,used_skill.cooldown)
    elif isinstance(used_skill,Potion):
        fight_shown_text.append(['You use %s'%used_skill.name,black])
        used_skill.activate_eff(player)
        potSound.play()
    # status effects (status damage should be last effect that happens)
    for status in enemy.fight_status:
        if status == st_burn:
            burn_damage = status_calc(st_burn,enemy)
            fight_shown_text.append(['Enemy takes %i burn damage'%burn_damage,lightRed])
        elif status == st_para:
            status_calc(st_para,enemy)
        elif status == st_curse:
            curse_damage = status_calc(st_curse,enemy)
            fight_shown_text.append(['Enemy takes %i curse damage'%curse_damage,lightRed])
        elif status == st_bleed:
            bleed_damage = status_calc(st_bleed,enemy)
            fight_shown_text.append(['Enemy takes %i bleed damage'%bleed_damage,lightRed])
        elif status == st_poison:
            poison_damage = status_calc(st_poison,enemy)
            fight_shown_text.append(['Enemy takes %i bleed damage'%poison_damage,purple])
        elif status == st_conf:
            conf_damage = status_calc(st_conf,enemy)
            if conf_damage != None:
                fight_shown_text.append(['Enemy hurts itself for %i damage'%conf_damage,orange])
    if enemy.HP <= 0:
        fight_shown_text.append(['You have defeated the enemy!',brown])
    # refresh
    fakeFight()
    fightText.addText(fight_shown_text)
    fightText.showText([27,27,28,32,37,45],screenW/2,0,400,50)
    pygame.display.update()
    time.sleep(1.1)
    # counter attack
    if enemy.HP > 0 and not success_run: # enemy counter attack
        enemyAttack()
    checkActiveDuration()    # ACTIVE DURATION LOSE EFFECT HERE

def checkActiveDuration():
    for skill in player.fight_actives:
        if hasattr(skill,'turnEnd') and fightText.turn >= skill.turnEnd:
            skill.loseEffect(player)
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


def pickFloor():
    inSome.enter()
    pygame.mixer.music.load('game/music/adventure.mp3')
    pygame.mixer.music.play(-1)
    while inSome.show:
        screen.fill(blue)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
        if boolButton('Leave',20,25,600,100,100,red,lightRed):
            inSome.leave()
            return None
        floor_lv_require = [0,4,4,8,8,11,13,13,16,16]
        y = 0
        for floor in range(10):
            if player.LV >= floor_lv_require[floor]:
                if floor + 1 == 3:
                    if player.floors_beaten >= 1:
                        if boolButton('Floor %i'%(floor+1),25,screenW/2-275,675-y,175,50,green,lightGreen):
                            inSome.leave()
                            return floor
                    else:
                        if boolButton('Floor %i'%(floor+1),25,screenW/2-275,675-y,175,50,orange,brown):
                            textbox('Need to clear: Floor %i to enter!'%(floor),45,cyan,725,screenH/2)
                elif floor + 1 == 5:
                    if player.floors_beaten >= 2:
                        if boolButton('Floor %i'%(floor+1),25,screenW/2-275,675-y,175,50,green,lightGreen):
                            inSome.leave()
                            return floor
                    else:
                        if boolButton('Floor %i'%(floor+1),25,screenW/2-275,675-y,175,50,orange,brown):
                            textbox('Need to clear: Floor %i to enter!'%(floor),45,cyan,725,screenH/2)
                elif floor + 1 == 8:
                    if player.floors_beaten >= 3:
                        if boolButton('Floor %i'%(floor+1),25,screenW/2-275,675-y,175,50,green,lightGreen):
                            inSome.leave()
                            return floor
                    else:
                        if boolButton('Floor %i'%(floor+1),25,screenW/2-275,675-y,175,50,orange,brown):
                            textbox('Need to clear: Floor %i to enter!'%(floor),45,cyan,725,screenH/2)
                elif floor + 1 == 10:
                    if player.floors_beaten >= 4:
                        if boolButton('Floor %i'%(floor+1),25,screenW/2-275,675-y,175,50,green,lightGreen):
                            inSome.leave()
                            return floor
                    else:
                        if boolButton('Floor %i'%(floor+1),25,screenW/2-275,675-y,175,50,orange,brown):
                            textbox('Need to clear: Floor %i to enter!'%(floor),45,cyan,725,screenH/2)
                else:
                    if boolButton('Floor %i'%(floor+1),25,screenW/2-275,675-y,175,50,green,lightGreen):
                        inSome.leave()
                        return floor
            else:
                if boolButton('Floor %i'%(floor+1),25,screenW/2-275,675-y,175,50,orange,brown):
                    textbox('Need to be LV: %i to enter!'%floor_lv_require[floor],45,cyan,725,screenH/2)
            y += 70
##            dungeon_floor =
##                    1 [[alec,sungmin,kaelan],\ 
##                    2 [huoniao],\
##                    3 [aneal,avery,ryan,tina],\
##                    4 [clean_booga],\
##                    5 [alicky,sunger,brownitron,jihoon,yoonho],\
##                    6 [minji,clara,greasy_avery,michael],\
##                    7 [clavery],\
##                    8 [laluche,dyonghae,greasy_booga,flower_minji],\
##                    9 [booga_cat],\
##                    10 [king_booga]]
        pygame.display.update()
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
    if not fightText.stillFight:
        fightText.floor = pickFloor()
    # Floor 1
    alec = Enemy('Alec','alec.png',325,130, 110,110, 20,40, 95,5,5, 50,12)
    sungmin = Enemy('Sungmin','sungmin.png',425,500, 80,130, 25,25, 95,5,4, 50,14)
    kaelan = Enemy('Kaelan','kaelan.png',450,110, 100,100, 40,10, 95,5,4, 60,16)
    # Boss 2
    huoniao = Enemy('Huoniao','huoniao.png', 1000,600, 300,150, 60,70, 80,8,8, 200,100)
    # Floor 3
    aneal = Enemy('Aneal','aneal.png', 900,200, 200,70, 50,40, 95,5,5, 90,28)
    avery = Enemy('Avery','avery.png', 1400,50, 160,30, 20,20, 95,5,5, 150,19)
    ryan = Enemy('Ryan','ryan.png',700,10, 300,11, -70,-70, 110,40,20, 100,55)
    tina = Enemy('Tina','tina.png',800,600, 40,275, 30,60, 100,4,4, 100,30)
    # Boss 4
    clean_booga = Enemy('Clean Booga','clean_booga.png',2250,500, 325,225, 70,70, 85,8,8, 300,150)
    # Floor5
    alicky = Enemy('Alicky','alec.png',1700,500, 375,375, 80,100, 90,5,5, 125,100)
    sunger = Enemy('Sunger Munger','sungmin.png',1900,1000, 140,425, 80,150, 92,5,5, 135,125)
    brownitron = Enemy('Brownitron','kaelan.png',2400,400, 180,125, 110,200, 87,5,4, 150,150)
    jihoon = Enemy('Jihoon','jihoon.png',1000,7, 250,10, -100,-100, 80,90,0, 175,125)
    yoonho = Enemy('Yoonho','yoonho.png',1500,2000, 70,400, 135,160, 85,10,6, 200,100)
    # Floor 6
    minji = Enemy('Minji','minji.png',2050,650, 400,200, 125,175, 95,7,7,  250,200)
    clara = Enemy('Clara','clara.png',1500,300, 500,278, 95,125, 85,11,11, 200,250)
    greasy_avery = Enemy('Greasy Avery','greasy_avery.png',3250,500, 275,100, 70,90, 95,5,5, 300,225)
    michael = Enemy('Michael','michael.png',1750,600, 225,125, 175,125, 80,10,10, 200,250)
    # Boss 7
    clavery = Enemy('Clavery','clavery.png',3750,400, 375,300, 120,120, 75,17,16, 500,500)
    # Floor 8
    laluche = Enemy('La Lucha Libre','ryan.png',3000,0, 800,10, -300,-300, 150,60,75, 400,150)
    dyonghae = Enemy('Dyonghae','tina.png',6800,4000, 400,1200, 400,750, 95,5,5, 200,300)
    greasy_booga = Enemy('Greasy Booga','greasy_booga.png',7600,1200, 800,600, 400,400, 85,20,20, 500,300)
    flower_minji = Enemy('Flower Minji','flower_minji.png',7000,1500, 550,500, 475,325, 90,10,10, 450,450)
    # Boss 9
    booga_cat = Enemy("Booga's Cat",'booga_cat.png',4000,800, 1000,750, 0,0, 125,65,30, 1750,1000)
    # Final Boss 10
    king_booga = Enemy('King Booga','king_booga.png',19369,8000, 1350,1000, 700,1000, 100,20,20, 2000,2500)
                     # Floor 1 
    dungeon_floor = [[alec,sungmin,kaelan],\
                     # Floor 2 BOSS
                     [huoniao],\
                     # Floor 3 
                     [aneal,avery,ryan,tina],\
                     # Floor 4 Boss
                     [clean_booga],\
                     # Floor 5  
                     [alicky,sunger,brownitron,jihoon,yoonho],\
                     # Floor 6 
                     [minji,clara,greasy_avery,michael],\
                     # Floor 7 BOSS
                     [clavery],\
                     # Floor 8 
                     [laluche,dyonghae,greasy_booga,flower_minji],\
                     # Floor 9 BOSS
                     [booga_cat],\
                     # Floor 10 BOSS
                     [king_booga]]

    ### Music
    if fightText.floor == 1 or fightText.floor == 3 or fightText.floor ==6 or fightText.floor == 8 or fightText.floor == 9:
        pygame.mixer.music.load('game/music/boss.mp3')
    else:
        pygame.mixer.music.load(random.choice(['game/music/bgm_fight1.mp3','game/music/bgm_fight2.mp3','game/music/bgm_fight3.mp3',\
                                               'game/music/bgm_fight4.mp3','game/music/bgm_fight5.mp3','game/music/bgm_fight6.mp3','game/music/bgm_fight7.mp3']))
    pygame.mixer.music.play(-1)
    ##############################
    if fightText.floor == None:
        leaveFight()
    else:
        enemy = random.choice(dungeon_floor[fightText.floor])
        inFight.enter()
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
        if player.run_away:
            for aSkill in player.fight_actives:
                Active.loseEffect(aSkill,player)
            player.statUpdate()
            trimExtraHPMP()
            leaveFight()
        elif enemy.HP <= 0:
            ### BOSS FLOORS ###
            if fightText.floor +1 == 2:
                if player.floors_beaten == 0:
                    player.floors_beaten += 1
            if fightText.floor +1 == 4:
                if player.floors_beaten == 1:
                    player.floors_beaten += 1
            if fightText.floor +1 == 7:
                if player.floors_beaten == 2:
                    player.floors_beaten += 1
            if fightText.floor +1 == 9:
                if player.floors_beaten == 3:
                    player.floors_beaten += 1
            player.cash += enemy.loot
            player.exp += enemy.exp
            for aSkill in player.fight_actives:
                Active.loseEffect(aSkill,player)
            player.statUpdate()
            trimExtraHPMP()
            # Corpse Drain
            if isinstance(player,Mage) and corpse_drain.bonus_chance1 >= random.choice(range(101)):
                    player.MP += round(corpse_drain.restore_mp1*player.maxMP)
                    trimExtraHPMP()
            if player.exp >= player.max_exp:
                level_up_greet()
                player.level_up()
                stats()
                skillsPage()
                player.healFullHP()
                player.healFullMP()
                fightAgain()
            else:
                fightAgain()
        elif player.HP <= 0:
            gameover()
        # refresh8
        screen.fill(white)
        # Enemy Details
        screen.blit(enemy.img, centerIMG(255,255,800,175))
        textbox('%s'%enemy.name,40,black,800,340)
        textbox('HP: %i'%(enemy.HP),45,lightRed,800,395)
        textbox('MP: %i'%(enemy.MP),45,lightBlue,800,455)
        ###
        button('Attack',30,25,25,75,75,green,lightGreen,dmg_calc,basic_attack)
        button('Skills',30,25,125,75,75,lightCyan,cyan,learnedSkillsPage,None)
        button('Run',30,25,225,75,75,red,lightRed,dmg_calc,'run')
        screen.blit(player.img,(325,150))
        textbox('Turn: %i'%(fightText.turn),25,black,60,340)
        if fightText.pg_num - 1 >= 0:
            if boolButton('',0,233,533,35,35,green,lightGreen):
                fightText.pg_num -= 1
                pg_flip.play()
            screen.blit(small_arrow_left,centerIMG(30,30,250,550))
        if fightText.pg_num + 1 < fightText.pages + 1:
            if boolButton('',0,734,533,35,35,green,lightGreen):
                fightText.pg_num += 1
                pg_flip.play()
            screen.blit(small_arrow_right,centerIMG(30,30,750,550))
        fightText.showText([27,27,28,32,37,45],screenW/2,0,400,50)
        showActivesAndStatus()
        status_bar()
        ###
        pygame.display.update()
        clock.tick(60)
        
def resetCooldown():
    for skill in [mana_gaurd,restore,barrier,meditate,stealth,illusion,intimidate,blood_rit]:
        skill.delCooldownEnd()

def showActivesAndStatus():
    y = 0
    for skill in player.fight_actives:
        screen.blit(skill.img,(125,25+y))
        y += 100
    for status in player.fight_status:
        screen.blit(status.img,(125,25+y))
        y += 100
    y = 0
    for skill in enemy.fight_actives:
        screen.blit(skill.img,(935,25+y))
        y += 100
    for status in enemy.fight_status:
        screen.blit(status.img,(935,25+y))
        y += 100


def fightAgain():
    while inFight.show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
        screen.fill(white)
        textbox('Cash gained: +$%i'%(enemy.loot),50,black,screenW/2,125)
        textbox('EXP gained: +%i'%(enemy.exp),50,black,screenW/2,225)
        textbox('Keep exploring the dungeon?',50,black,screenW/2,325)
        if boolButton('Yes',80,200,450,200,200,green,lightGreen):
            fightText.stillFight = True
            fight()
        button('No',80,650,450,200,200,red,lightRed,leaveFight,None)
        status_bar()
        pygame.display.update()

def leaveFight():
    inFight.show = False
    player.X = 800
    pygame.mixer.music.stop()
    pygame.mixer.music.load('game/music/bgm_home.mp3')
    pygame.mixer.music.play(-1)

def runChance():
    chance = enemy.HP/enemy.maxHP - 10
    chance -= player.agi + player.LV
    success_run = round(chance) <= random.choice(range(101))
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
                if event.key == pygame.K_e or event.key == pygame.K_ESCAPE:
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
                if event.key == pygame.K_1 or event.key == pygame.K_ESCAPE:
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
                if event.key == pygame.K_e or event.key == pygame.K_ESCAPE:
                    inHosp.show = False
        textbox('Cash: %i'%player.cash,40,yellow,140,175)
        matrixSlot(6,3,hospital_pots,150,300,125,125)
        textbox('(Potions are usable in battle)',20,black,300,675)
        textbox('Press E to leave',20,black,800,675)
        if boolButton('Rest',25,50,46,50,50,green,lightGreen):
            player.rest()
            potSound.play()
            time.sleep(0.4)
        textbox('When low on HP/MP, click Rest to restore HP/MP',10,black,107,27)
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
    if player.job == 'Rogue':
        addItem(basic_dag)

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
##                if event.key == pygame.K_p:
##                    pygame.display.toggle_fullscreen()
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
            fightText.stillFight = False
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
        button('Save',40,25,25,50,50,red,lightRed,saveGame,None)
        status_bar()
        pygame.display.update() 

def showStats():
    inSkill.enter()
    time.sleep(0.2)
    while inSkill.show:
        screen.fill(grey)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
        textbox('STATS',60,lightRed,screenW/2,40)
        #
        textbox('LV: %i'%player.LV,35,black,220,50)
        textbox('Job: %s'%player.job,35,purple,220,90)
        textbox('Strength: %i + %i = %i'%(player.new_stren,player.bonusStren,player.stren),35,red,220,130)
        textbox('Intelligence: %i + %i = %i'%(player.new_intel,player.bonusIntel,player.intel),35,blue,220,170)
        textbox('Agility: %i + %i = %i'%(player.new_agi,player.bonusAgi,player.agi),35,lighterGreen,220,210)
        textbox('Luck: %i + %i = %i'%(player.new_luck,player.bonusLuck,player.luck),35,yellow,220,250)
        #
        textbox('Armor: %i + %i = %i'%(player.armorU(),player.bonusArmor,player.armor),35,red,220,320)
        textbox('Resist: %i + %i = %i'%(player.mag_armorU(),player.bonusMag_armor,player.mag_armor),35,blue,220,360)
        #
        textbox('Max HP: %i + %i = %i'%(player.maxHPU(),player.bonusMaxHP,player.maxHP),35,red,700,170)
        textbox('Max MP: %i + %i = %i'%(player.maxMPU(),player.bonusMaxMP,player.maxMP),35,blue,700,210)
        textbox('Physical Damage: %i + %i = %i'%(player.damageU(),player.bonusPdmg,player.damage),35,red,700,300)
        textbox('Magic Damage: %i + %i = %i'%(player.mag_damageU(),player.bonusMdmg,player.mag_damage),35,blue,700,340)
        #
        textbox('Hit Rate: %i%% + %i%% = %i%%'%(player.hitU(),player.bonusHit,player.hit),35,lighterGreen,450,430)
        textbox('Dodge Chance: %i%% + %i%% = %i%%'%(player.dodgeU(),player.bonusDodge,player.dodge),35,blue,450,470)
        textbox('Critical Chance: %i%% + %i%% = %i%%'%(player.critU(),player.bonusCrit,player.crit),35,red,450,530)
        textbox('Critical Mutliplier: 225 + %i%% = %i%%'%(player.bonusCritMulti,225+player.bonusCritMulti),35,lighterYellow,450,570)
        #
        textbox('Experience: %i / %i'%(player.exp,player.max_exp),35,lighterYellow,450,640)
        textbox('Cash: $%i'%(player.cash),35,lighterYellow,450,606)
        textbox('SAVE GAME?',40,blue,890,560)
        if boolButton('YES',25,screenW/2+300,600,75,75,red,lightRed):
            actualSave()
            heal.play()
            time.sleep(0.5)
            inSkill.leave()
        if boolButton('NO',25,screenW/2+400,600,75,75,red,lightRed):
            inSkill.leave()
            
        status_bar()
        pygame.display.update()
        

def actualSave():
        shelfFile = shelve.open('saved_game')
        shelfFile['name'] = player.name
        shelfFile['job'] = player.job
        shelfFile['date'] = time.localtime()
        # Attributes
        shelfFile['new_stren'] = player.new_stren 
        shelfFile['new_intel'] = player.new_intel 
        shelfFile['new_agi'] = player.new_agi 
        shelfFile['new_luck'] = player.new_luck 
        shelfFile['stren'] = player.stren 
        shelfFile['intel'] = player.intel 
        shelfFile['agi'] = player.agi
        shelfFile['luck'] = player.luck 
        shelfFile['old_stren'] = player.old_stren
        shelfFile['old_intel'] = player.old_intel 
        shelfFile['old_agi'] = player.old_agi 
        shelfFile['old_luck'] = player.old_luck 
        # Bonus
        shelfFile['HP'] = player.HP
        shelfFile['MP'] = player.MP
        shelfFile['bonusStren'] = player.bonusStren 
        shelfFile['bonusIntel'] = player.bonusIntel 
        shelfFile['bonusAgi'] = player.bonusAgi 
        shelfFile['bonusLuck'] = player.bonusLuck 
        shelfFile['bonusMaxHP'] = player.bonusMaxHP 
        shelfFile['bonusMaxMP'] = player.bonusMaxMP 
        shelfFile['bonusPdmg'] = player.bonusPdmg 
        shelfFile['bonusMdmg'] = player.bonusMdmg 
        shelfFile['bonusArmor'] = player.bonusArmor 
        shelfFile['bonusMag_armor'] = player.bonusMag_armor
        shelfFile['bonusHit'] = player.bonusHit
        shelfFile['bonusDodge'] = player.bonusDodge 
        shelfFile['bonusCrit'] = player.bonusCrit
        shelfFile['bonusCritMulti'] = player.bonusCritMulti
        shelfFile['weapon'] = player.weapon
        shelfFile['lefthand'] = player.lefthand
        shelfFile['head'] = player.head
        shelfFile['body'] = player.body
        # General
        shelfFile['LV'] = player.LV 
        shelfFile['SP'] = player.SP
        shelfFile['exp'] = player.exp 
        shelfFile['max_exp'] = player.max_exp
        sellValue = 0
        for item in player.inv:
            if item != None:
                sellValue += item.cost
        for item in [player.weapon,player.body,player.lefthand]:
            if item != None:
                sellValue += item.cost
        shelfFile['cash'] = player.cash + sellValue
        shelfFile['learned_skills'] = player.learned_skills
        shelfFile['fight_actives'] = player.fight_actives 
        shelfFile['fight_status'] = player.fight_status 
        shelfFile['floors_beaten'] = player.floors_beaten 
        shelfFile['crit_multi'] = player.crit_multi
        # Special Skills
        shelfFile['rank_up_as_one'] = player.rank_up_as_one
        shelfFile.close()

def loadGame():
    shelfFile = shelve.open('saved_game')
    player.name = shelfFile['name']
    player.job = shelfFile['job'] 
    # Attributes
    player.new_stren = shelfFile['new_stren']
    player.new_intel = shelfFile['new_intel']
    player.new_agi  = shelfFile['new_agi']
    player.new_luck  = shelfFile['new_luck']
    player.stren  = shelfFile['stren']
    player.intel = shelfFile['intel']
    player.agi = shelfFile['agi']
    player.luck  = shelfFile['luck']
    player.old_stren = shelfFile['old_stren']
    player.old_intel  = shelfFile['old_intel']
    player.old_agi = shelfFile['old_agi']
    player.old_luck = shelfFile['old_luck'] 
    # Bonus
    player.HP = shelfFile['HP']
    player.MP = shelfFile['MP']
    player.bonusStren = shelfFile['bonusStren'] 
    player.bonusIntel  = shelfFile['bonusIntel'] 
    player.bonusAgi  = shelfFile['bonusAgi'] 
    player.bonusLuck = shelfFile['bonusLuck'] 
    player.bonusMaxHP  = shelfFile['bonusMaxHP']
    player.bonusMaxMP  = shelfFile['bonusMaxMP'] 
    player.bonusPdmg  = shelfFile['bonusPdmg'] 
    player.bonusMdmg  = shelfFile['bonusMdmg'] 
    player.bonusArmor  = shelfFile['bonusArmor'] 
    player.bonusMag_armor = shelfFile['bonusMag_armor'] 
    player.bonusHit = shelfFile['bonusHit'] 
    player.bonusDodge  = shelfFile['bonusDodge'] 
    player.bonusCrit = shelfFile['bonusCrit'] 
    player.bonusCritMulti = shelfFile['bonusCritMulti'] 
    player.weapon = player.fists #shelfFile['weapon']
    player.lefthand = player.fap#shelfFile['lefthand'] 
    player.head = player.china_hat#shelfFile['head'] 
    player.body = player.shirt_jeans#shelfFile['body'] 
    # General
    player.LV = shelfFile['LV'] 
    player.SP = shelfFile['SP']
    player.exp = shelfFile['exp']
    player.max_exp = shelfFile['max_exp']
    player.cash  = shelfFile['cash']
    player.learned_skills = shelfFile['learned_skills']
    player.fight_actives  = shelfFile['fight_actives']
    player.fight_status  = shelfFile['fight_status']
    player.floors_beaten  = shelfFile['floors_beaten'] 
    player.crit_multi = shelfFile['crit_multi']
    setInv()
    # Special Skills
    player.rank_up_as_one = shelfFile['rank_up_as_one'] 
    shelfFile.close()
    player.statUpdate()
    skillUpdate()

def askLoad():
    inSkill.enter()
    shelfFile = shelve.open('saved_game')
    while inSkill.show:
        screen.fill(lime)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    loadGame()
                    heal.play()
                    time.sleep(0.2)
                    inSkill.leave()
                elif event.key == pygame.K_e or event.key == pygame.K_ESCAPE:
                    inSkill.leave()
        textbox('Do you want to load this save?',65,black,screenW/2,200)
        textbox('%i,%i,%i   %ihr:%imin:%isec'%(shelfFile['date'][0],shelfFile['date'][1],shelfFile['date'][2],\
                               shelfFile['date'][3],shelfFile['date'][4],shelfFile['date'][5]),80,red,screenW/2,315)
        textbox('Press (Q: Yes /E: No)',65,black,screenW/2,550)
        status_bar()
        pygame.display.update()

def saveGame():
    inSome.enter()
    time.sleep(0.2)
    pygame.mixer.music.load('game/music/save.mp3')
    pygame.mixer.music.play(-1)
    while inSome.show:
        screen.fill(grey)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
        if boolButton('Save',25,50,50,100,100,red,lightRed):
            showStats()
        textbox('When loading your save, your items will be sold for full price',35,black,screenW/2,250)
        if boolButton('Leave',25,100,400,75,75,red,lightRed):
            pygame.mixer.music.load('game/music/bgm_home.mp3')
            pygame.mixer.music.play(-1)
            inSome.leave()
        if boolButton('Load',25,200,50,100,100,red,lightRed):
            askLoad()
            
        status_bar()
        pygame.display.update()
    

    
            

# Main
##intro()
player = job_select()
enter_name()
stats()
game_loop()
pygame.quit()
quit()
