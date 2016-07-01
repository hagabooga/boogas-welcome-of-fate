from class_items import *

pot_hp = Potion('Health Potion','potion/pot_hp.png','A simple potion that restores health','Restore: +500 HP',500,0,\
           0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 50)
pot_mp = Potion('Mana Potion','potion/pot_mp.png','A simple potion that restores mana','Restore: +450 MP',0,450,\
           0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 70)
pot_purple = Potion('Purple Potion','potion/pot_purple.png','A potion that restores both health and mana','Restore: +350 HP, +350 MP',350,350,\
           0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 60)
hospital_pots = [pot_hp,pot_mp,pot_purple]
for i in range(15):
    hospital_pots.append(None)
