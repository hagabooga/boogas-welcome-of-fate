import pygame
pygame.init()

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
    return aStr

def givebdesc(aList):
    for item in aList:
        item.giveBonusDesc()

class Item(object):
    def __init__(self,name,img,desc,\
                 bstr,bint,bagi,bluk,bhp,bmp,bpdmg,bmdmg,barm,bmarm,bhit,bdge,bcrt,cost):
        self.name = name
        self.cost = cost
        self.img = pygame.image.load('items/%s'%img)
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
