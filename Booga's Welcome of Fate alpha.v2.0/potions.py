from items import *

pot_hp = Potion('Health Potion','potion/pot_hp.png','A simple potion that restores health','Restore: +500 HP',500,0,\
           0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 40)
pot_mp = Potion('Mana Potion','potion/pot_mp.png','A simple potion that restores mana','Restore: +450 MP',0,450,\
           0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 60)
pot_purple = Potion('Purple Potion','potion/pot_purple.png','A potion that restores both health and mana','Restore: +350 HP, +350 MP',350,350,\
           0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 50)
pot_hp_bet = Potion('Better Health Potion','potion/pot_hp_bet.png','A simple potion that restores health','Restore: +1500 HP',1500,0,\
           0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 90)
pot_mp_bet = Potion('Better Mana Potion','potion/pot_mp_bet.png','A simple potion that restores mana','Restore: +2000 MP',0,2000,\
           0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 130)
pot_purple_bet = Potion('Better Purple Potion','potion/pot_purple_bet.png','A potion that restores both health and mana','Restore: +900 HP, +900 MP',900,900,\
           0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 110)

hospital_pots = [pot_hp,pot_mp,pot_purple,\
                 pot_hp_bet,pot_mp_bet,pot_purple_bet]
for i in range(12):
    hospital_pots.append(None)
