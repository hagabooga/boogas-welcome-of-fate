
def skill_requirement(aSkill): ##### ALL SKILL REQUIREMENTS
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
        elif isinstance(self,Passive):
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
