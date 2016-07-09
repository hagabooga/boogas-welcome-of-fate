import pygame
import random

pygame.init()

def weapon_atk_sound():
    atk_sound = pygame.mixer.Sound(random.choice(['game/sounds/atk1.wav','game/sounds/atk2.wav','game/sounds/atk3.wav',\
                                                  'game/sounds/atk4.wav','game/sounds/atk5.wav','game/sounds/atk6.wav','game/sounds/atk7.wav']))
    return atk_sound

heal = pygame.mixer.Sound('game/sounds/heal.wav')
wear = pygame.mixer.Sound('game/sounds/wear.wav')
buySound = pygame.mixer.Sound('game/sounds/buy.wav')
potSound = pygame.mixer.Sound('game/sounds/pheal.wav')
rank_up = pygame.mixer.Sound('game/sounds/rank_up.wav')
pg_flip = pygame.mixer.Sound('game/sounds/page_flip.wav')
crit = pygame.mixer.Sound('game/sounds/crit.wav')
select = pygame.mixer.Sound('game/sounds/select.wav')
equip_sound = pygame.mixer.Sound('game/sounds/atk4.wav')
