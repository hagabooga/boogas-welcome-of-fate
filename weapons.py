from class_items import *
inner = Sword('Inner','warrior/sword/inner.png','Strong base, weak tip',16,1,\
               4, 0, 0, 0, 0, 0, 0, 0, 0, 0, -15, 0, 0, 200)
katana = Sword('Katana','warrior/sword/katana.png','A sharp sword that easily cuts',25,15,\
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 20, 450)
scimitar = Sword('Scimitar','warrior/sword/scimitar.png','A curved and very sharp blade',29,9,
                  12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1000)
# Axe
battleaxe = Axe('Battleaxe','warrior/axe/battleaxe.png','Can chop a tree with one swing',30,2,\
                   6, 0, 0, 0, 0, 0, 0, 0, 0, 0, -20, 0, 0, 460)
big_axe = Axe('Big Axe','warrior/axe/big_axe.png','A huge axe that can cause an earthquake',70,0,\
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4500)
# Wand
wand = Wand('Wand','mage/wand/app_wand.png','A wooden wand',3,7,\
            0, 5, 0, 0, 0, 10, 0, 0, 0, 0, 0, 0, 0, 225)
mag_wand = Wand('Magic Wand','mage/wand/mag_wand.png','A magic wand',7,17,\
            0, 14, 0, 0, 0, 20, 0, 0, 0, 0, 0, 0, 0, 450)

star_wand = Wand('Star Wand','mage/wand/star_wand.png','A Star wand',9,27,\
            0, 25, 0, 0, 0, 60, 0, 0, 0, 0, 0, 0, 0, 800)

element_wand = Wand('Element Wand','mage/wand/element_wand.png','An Elemental wand',14,50,\
            0, 42, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 1500)
# Staff
staff = Staff('Staff','mage/staff/app_staff.png','A wooden staff used by novice mages',5,9,\
               0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 250)
mag_staff = Staff('Magic Staff','mage/staff/mag_staff.png','A staff powered up by magic',9,21,\
                     0, 17, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 500)
star_staff = Staff('Star Staff','mage/staff/star_staff.png','A staff blessed by the power of the stars',10,32,\
                    0, 31, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 900)
element_staff = Staff('Elemental Staff','mage/staff/element_staff.png','A staff imbued with fire, wind and water',16,55,\
                       0, 47, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1600)
# Dagger
long_dag = Dagger('Long Dagger','rouge/dagger/long_dag.png','A long blade dagger',12,12,\
                  0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 25, 250)
edge_dag = Dagger('Edged Dagger','rouge/dagger/edge_dag.png','A sharper dagger',18,18,\
                  0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 28, 550)
poison_dag = Dagger('Poisoned Dagger','rouge/dagger/poison_dag.png','A dagger dipped in poison',23,23,\
                    0, 0, 12, 12, 0, 0, 0, 0, 0, 0, 0, 0, 32, 650)
balance_dag = Dagger('Balanced Dagger','rouge/dagger/balance_dag.png','Sharp and fast',32,32,\
                     15, 15, 15, 15, 0, 0, 0, 0, 0, 0, 0, 0, 38, 875)
# Shuriken
# Balanced
shortsword = Dagger('Shortsword','balance/weapon/shortsword.png','A cheap, simple and easy to use sword',7,7,\
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 125)
longsword = Sword('Longsword','balance/weapon/longsword.png','A standard sword used by many swordsmen',19,5,\
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 225)
tipper = Sword('Tipper','balance/weapon/tipper.png','Strong at the tip but weak at the base',15,10,\
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 200)
def_sword = Sword('Defensive Sword','balance/weapon/def_sword.png','Big and heavy sword',14,14,\
                   0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 325)
# Fun
fire_sword = Sword('Fire Sword','balance/weapon/fire_sword.png','Blaze Strike: +5 ranks, -15 mana cost',35,25,\
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1250)
fruit = Axe('The Fruits of Booga','fun/weapon/fruit.png','Fruits saved when Booga dropped them from the sky',70,70,\
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6000)
allin = Axe('All In','fun/weapon/allin.png','HP set to 8',120,120,\
               50, 50, 50, 50, 0, 0, 0, 0, 0, 0, 0, 0, 0, 12000)
shop_weapons_1 = [inner,battleaxe,katana,scimitar,shortsword,longsword,tipper,def_sword,staff,mag_staff,star_staff,element_staff,\
       long_dag,edge_dag,poison_dag,balance_dag,fire_sword,big_axe,fruit,allin]
givebdesc(shop_weapons_1)
## pg2 Armors Body
# Warrior
bronze_body = Body('Bronze Armour','warrior/body/bronze_body.png','Armour made from bronze',\
                   3, 0, 0, 0, 10, 0, 0, 0, 10, 2, 0, 0, 0, 100)
iron_body = Body('Iron Armour','warrior/body/iron_body.png','Armour made from iron. Stronger than bronze',\
                 5, 0, 0, 0, 20, 0, 0, 0, 16, 4, 0, 0, 0, 250)
steel_body = Body('Steel Armour','warrior/body/steel_body.png','Armour made from Steel. Stronger than iron',\
                  9, 0, 0, 0, 30, 0, 0, 0, 30, 6, 0, 0, 0, 650)
dia_body = Body('Diamond Armour','warrior/body/dia_body.png','Armour made from Diamond. The strongest armour',\
                15, 0, 0, 0, 50, 0, 0, 0, 49, 9, 0, 0, 0, 1200)
# Rouge
cloak = Body('Cloak','rouge/body/cloak.png','A cloak made to blend in with the shadows',\
             0, 0, 5, 0, 0, 0, 0, 0, 7, 7, 0, 10, 0, 150)
black_cloak = Body('Black Cloak','rouge/body/black_cloak.png','A cloak darker than the night',\
                   0, 0, 8, 0, 0, 0, 0, 0, 12, 12, 5, 20, 0, 400)
stealth_cloak = Body('Stealth Cloak','rouge/body/stealth_cloak.png','A cloak that blends in with its surroundings',\
                     0, 0, 12, 0, 0, 0, 0, 0, 20, 20, 10, 30, 0, 1000)
ass_cloak = Body('''Assasin's Cloak''','rouge/body/ass_cloak.png','think ur good?',\
                 0, 0, 20, 0, 0, 0, 0, 0, 31, 31, 15, 40, 0, 1500)
# Mage
robe = Body('Robe','mage/body/app_robe.png','A simple robe made from cloth',\
            0, 5, 0, 0, 0, 15, 0, 0, 5, 9, 0, 0, 0, 125)
mag_robe = Body("Magician's Robe",'mage/body/mag_robe.png','A robe used by experienced mages',\
                0, 10, 0, 0, 0, 30, 0, 0, 8, 16, 0, 0, 0, 300)
star_robe = Body('Star Robe','mage/body/star_robe.png','A robe blessed by the stars',\
                0, 14, 0, 0, 0, 20, 0, 0, 0, 0, 0, 0, 0, 450)

star_wand = Wand('Star Wand','mage/wand/star_wand.png','A Star wand',9,27,\
            0, 25, 0, 0, 0, 60, 0, 0, 0, 0, 0, 0, 0, 800)

element_wand = Wand('Element Wand','mage/wand/element_wand.png','An Elemental wand',14,50,\
            0, 42, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 1500)
# Staff
staff = Staff('Staff','mage/staff/app_staff.png','A wooden staff used by novice mages',5,9,\
               0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 250)
mag_staff = Staff('Magic Staff','mage/staff/mag_staff.png','A staff powered up by magic',9,21,\
                     0, 17, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 500)
star_staff = Staff('Star Staff','mage/staff/star_staff.png','A staff blessed by the power of the stars',10,32,\
                    0, 31, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 900)
element_staff = Staff('Elemental Staff','mage/staff/element_staff.png','A staff imbued with fire, wind and water',16,55,\
                       0, 47, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1600)
# Dagger
long_dag = Dagger('Long Dagger','rouge/dagger/long_dag.png','A long blade dagger',12,12,\
                  0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 25, 250)
edge_dag = Dagger('Edged Dagger','rouge/dagger/edge_dag.png','A sharper dagger',18,18,\
                  0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 28, 550)
poison_dag = Dagger('Poisoned Dagger','rouge/dagger/poison_dag.png','A dagger dipped in poison',23,23,\
                    0, 0, 12, 12, 0, 0, 0, 0, 0, 0, 0, 0, 32, 650)
balance_dag = Dagger('Balanced Dagger','rouge/dagger/balance_dag.png','Sharp and fast',32,32,\
                     15, 15, 15, 15, 0, 0, 0, 0, 0, 0, 0, 0, 38, 875)
# Shuriken
# Balanced
shortsword = Dagger('Shortsword','balance/weapon/shortsword.png','A cheap, simple and easy to use sword',7,7,\
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 125)
longsword = Sword('Longsword','balance/weapon/longsword.png','A standard sword used by many swordsmen',19,5,\
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 225)
tipper = Sword('Tipper','balance/weapon/tipper.png','Strong at the tip but weak at the base',15,10,\
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 200)
def_sword = Sword('Defensive Sword','balance/weapon/def_sword.png','Big and heavy sword',14,14,\
                   0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 325)
# Fun
fire_sword = Sword('Fire Sword','balance/weapon/fire_sword.png','Blaze Strike: +5 ranks, -15 mana cost',35,25,\
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1250)
fruit = Axe('The Fruits of Booga','fun/weapon/fruit.png','Fruits saved when Booga dropped them from the sky',70,70,\
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6000)
allin = Axe('All In','fun/weapon/allin.png','HP set to 8',120,120,\
               50, 50, 50, 50, 0, 0, 0, 0, 0, 0, 0, 0, 0, 12000)
shop_weapons_1 = [inner,battleaxe,katana,scimitar,shortsword,longsword,tipper,def_sword,staff,mag_staff,star_staff,element_staff,\
       long_dag,edge_dag,poison_dag,balance_dag,fire_sword,big_axe,fruit,allin]
givebdesc(shop_weapons_1)
## pg2 Armors Body
# Warrior
bronze_body = Body('Bronze Armour','warrior/body/bronze_body.png','Armour made from bronze',\
                   3, 0, 0, 0, 10, 0, 0, 0, 10, 2, 0, 0, 0, 100)
iron_body = Body('Iron Armour','warrior/body/iron_body.png','Armour made from iron. Stronger than bronze',\
                 5, 0, 0, 0, 20, 0, 0, 0, 16, 4, 0, 0, 0, 250)
steel_body = Body('Steel Armour','warrior/body/steel_body.png','Armour made from Steel. Stronger than iron',\
                  9, 0, 0, 0, 30, 0, 0, 0, 30, 6, 0, 0, 0, 650)
dia_body = Body('Diamond Armour','warrior/body/dia_body.png','Armour made from Diamond. The strongest armour',\
                15, 0, 0, 0, 50, 0, 0, 0, 49, 9, 0, 0, 0, 1200)
element_robe = Body('Elemental Robe','mage/body/element_robe.png','A robe that gaurds the 3 elements',\
                    0, 30, 0, 0, 0, 70, 0, 0, 21, 43, 0, 0, 0, 1350)
# Balanced
blanket = Body('Blanket','balance/body/blanket.png','A blanket to sleep with',\
               1, 2, 3, 4, 8, 8, 1, 1, 2, 2, 5, 5, 5, 75)
leather = Body('Leather Armour','balance/body/leather.png','Cheap and durable armour',\
               1, 1, 1, 1, 0, 0, 0, 0, 5, 5, 0, 0, 0, 60)
chain = Body('Chainmail','balance/body/chain.png','Chains made from steel',\
             0, 0, 0, 0, 0, 0, 0, 0, 42, 6, 0, 0, 0, 900)
reflect = L_hand('Reflector','balance/left/reflect.png','Any magic dmg taken, deal back half',\
               0, 0, 0, 0, 0, 0, 0, 0, 30, 100, 0, 0, 0, 3000)
# Fun
toast = Body('Toast','fun/body/toast.png','All toasters toast toast',\
             0, 0, 0, 0, 0, 0, 0, 0, 100, 0, 0, 0, 0, 4500)
smile = L_hand('Smile','fun/left/smile.png','A smile can make you happy',\
             0, 0, 0, 0, 0, 0, 0, 0, 50, 200, 0, 0, 0, 5000)
god = Body('God of Elements','fun/body/god.png','Control the elements as you will',\
           0, 0, 0, 0, 0, 0, 0, 0, 500, 800, 0, 0, 0, 10000)

shop_body_1 = [bronze_body,iron_body,steel_body,dia_body,cloak,black_cloak,stealth_cloak,ass_cloak,robe,mag_robe,star_robe,element_robe,\
       leather,chain,reflect,blanket,toast,smile,god]
givebdesc(shop_body_1)

##pg3 Left hand
#mage
shld_wood = L_hand('Wooden Shield','mage/left/shld_wood.png','A shield made from wood',\
                    0, 0, 0, 0, 15, 75, 0, 0, 17, 37, 0, 0, 0, 400)
shld_mana = L_hand('Mana Shield','mage/left/shld_mana.png','Shield imbued with mana',\
                   0, 0, 0, 0, 30, 150, 0, 0, 48, 75, 0, 0, 0, 900)
shld_star = L_hand('Star Shield','mage/left/shld_star.png','Stars is your shield',\
                   0, 0, 0, 0, 45, 450, 0, 0, 72, 134, 0, 0, 0, 1900)
shld_element = L_hand('Elemental Shield','mage/left/shld_element.png','The elements gaurds you',\
                      0, 0, 0, 0, 75, 600, 0, 0, 100, 215, 0, 0, 0, 4200)
##pg4 Head(helmets)
#mage
app_hat = Head("Apprentice's Hat",'mage/head/app_hat.png','A hat used by apprentices',\
              0, 5, 0, 0, 0, 0, 0, 0, 12, 40, 0, 0, 0, 500)
mage_hat = Head('Mage Hat','mage/head/mage_hat.png','Experienced mages wears this',\
               0, 10, 0, 0, 0, 0, 0, 0, 32, 75, 0, 0, 0, 1100)
star_hat = Head('Star Hat','mage/head/star_hat.png','This hat glows a bit',\
               0, 18, 0, 0, 0, 0, 0, 0, 60, 152, 0, 0, 0, 2500)
element_hat = Head('Element Hat','mage/head/element_hat.png','Focus the elements',\
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
basic_wand = Wand('Basic Wand','basic/bas_wand.png','A basic wand',2,6,\
                    0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
basic_dag = Dagger('Basic Dagger','basic/bas_dag.png','A basic dagger',4,4,\
                   0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
basic_sword = Sword('Basic Sword','basic/bas_sword.png','A basic sword',6,2,\
                     2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
# Strating armors
no_left = L_hand('Cannot Equip','basic/no.png','Two-handed weapon equipped',\
                  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

start_items = [basic_wand,basic_dag,basic_sword,no_left]
givebdesc(start_items)

def weapon_requirement(self):
    if self == inner:
        return player.requirement(player.LV,5)
    else:
        return True
