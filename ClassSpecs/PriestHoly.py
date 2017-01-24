from WowItem import Item
from StandardCharacter import Character
import math


class PriestHoly(Character):

	def __init__(self):
		Character.__init__(self)
		self._baseStats["intellect"] = 149.0
		self._baseStats["spirit"] = 150.0
		self._baseStats["spellcrit"] = 1.24
		self._baseStats["intToSpellcrit"] = 80.0
		self._baseStats["mana"] = 2620

		self._spiritOfRedemption = 0.05		# improves total spirit by 5%
		self._spiritualGuidance = 0.25		# increases spell dmg and healing by up to 25% of total spirit

		# meta 12
		self._enchantStats.Set("intellect", 12)
		# head 35, shoulders 33, bracers 30, gloves 35, legs 66, rings 40, weapon 81
		self._enchantStats.Set("hb", 320)
		# head 7, shoulders 4
		self._enchantStats.Set("mp5", 11)
		# chest 15
		self._enchantStats.Set("spirit", 15)


	def UpdateTotalSpirit(self):
		key = "spirit"
		# update spirit before applying talent multiplier
		self.UpdateTotalStat("spirit")
		self._totalStats.Set(key, self._totalStats.Get(key) * (1 + self._spiritOfRedemption))

	def UpdateTotalHealingBonus(self):
		key = "hb"
		# update hb before applying talent multiplier
		self.UpdateTotalStat("hb")
		self._totalStats.Set(key, self._totalStats.Get(key) 					\
			+ (self._totalStats.Get("spirit") * self._spiritualGuidance))

	def UpdateTotalStats(self):
		# this is overriding UpdateTotalStats from base
		Character.UpdateTotalStats(self)
		self.UpdateTotalSpirit()
		self.UpdateTotalHealingBonus()


	def HealingBonusFromSpirit(self):
		return (self._totalStats.Get("spirit") * self._spiritualGuidance)

	def Mp5NotCasting(self):
 		# formula from http://www.wowhead.com/forums&topic=12237&p=344228#p106810
 		# 5* 0.00932715221261 * sqrt(Int) * Spirit
 		# there is no 100% accurate formula available, not even on wowwiki
 		# this formula works pretty good for priests and mages
 		return 5 * 0.00932715221261 * self._totalStats.Get("spirit") * 			\
			math.sqrt(self._totalStats.Get("intellect")) +  self._totalStats.Get("mp5")


	def ManaFromIntGems(self):
		if self._gemStats.Get("intellect") > 100:
			return (20 + (15 * (self._gemStats.Get("intellect") - 20)))
		else:
			return 0.0

	def SpellCritFromIntGems(self):
		return (self._gemStats.Get("intellect") / self._baseStats["intToSpellcrit"])

	def HealingBonusFromSpiritGems(self):
		return ((self._gemStats.Get("spirit") * (1 + self._spiritOfRedemption)) * self._spiritualGuidance)


	def ToString(self):
		string =  "__TOTAL__" + "\n"
		string += "{:<30}".format("Healing Bonus") 			+ str(self._totalStats.Get("hb")) + "\n"
		string += "{:<30}".format("Base Int") 				+ str(self._baseStats["intellect"]) + "\n"
		string += "{:<30}".format("Base Spirit") 			+ str(self._baseStats["spirit"]) + "\n"
		string += "{:<30}".format("Base Mana") 				+ str(self._baseStats["mana"]) + "\n"
		string += "{:<30}".format("Total Int")				+ str(self._totalStats.Get("intellect")) + "\n"
		string += "{:<30}".format("Total Spirit")			+ str(self._totalStats.Get("spirit")) + "\n"
		string += "{:<30}".format("Total Mana") 			+ str(self._totalStats.Get("mana")) + "\n"
		string += "{:<30}".format("Spell-Crit Rating") 		+ str(self._totalStats.Get("spellcritRating")) + "\n"
		string += "{:<30}".format("Total Spell-Crit") 		+ str(self._totalStats.Get("spellcrit")) + "\n"
		string += "{:<30}".format("Mp5 pure (-spirit)")		+ str(self._totalStats.Get("mp5")) + "\n"
		string += "{:<30}".format("Mp5 OO5SR (+spirit)")	+ str(self.Mp5NotCasting()) + "\n"
		string += "{:<30}".format("Haste") 					+ str(self._totalStats.Get("haste")) + "\n\n"

		string += "__GEMS__" + "\n"
		string += "{:<30}".format("Gems Healing Bonus") 	+ str(self._gemStats.Get("hb")) + "\n"
		string += "{:<30}".format("Gems Spell-Crit Rating") + str(self._gemStats.Get("spellcritRating")) + "\n"
		string += "{:<30}".format("Gems Spell-Crit") 		+ str(self._gemStats.Get("spellcrit")) + "\n"
		string += "{:<30}".format("Gems Mp5 (-spirit)")		+ str(self._gemStats.Get("mp5")) + "\n"
		string += "{:<30}".format("Gems Haste") 			+ str(self._gemStats.Get("haste")) + "\n"
		string += "{:<30}".format("Gems Intellect") 		+ str(self._gemStats.Get("intellect")) + "\n"
		string += "{:<30}".format("Gems Spirit")	 		+ str(self._gemStats.Get("spirit")) + "\n"
		string += "{:<30}".format("Gems Mana from Int") 	+ str(self.ManaFromIntGems()) + "\n"
		string += "{:<30}".format("Gems Crit from Int") 	+ str(self.SpellCritFromIntGems()) + "\n"
		string += "{:<30}".format("Gems HB from Spirit") 	+ str(self.HealingBonusFromSpiritGems()) + "\n"
		string += "{:<30}".format("Gems Total HB") 			+ str(self._gemStats.Get("hb") + self.HealingBonusFromSpiritGems()) + "\n\n"

		string += "__INT__" + "\n"
		string += "{:<30}".format("Mana from Total Int") 	+ str(self.ManaFromInt()) + "\n"
		string += "{:<30}".format("Crit from Total Int") 	+ str(self.SpellCritFromInt()) + "\n\n"

		string += "__SPIRIT__" + "\n"
		string += "{:<30}".format("HB from Total Spirit")	+ str(self.HealingBonusFromSpirit()) + "\n\n"

		string += "\nNote:														\
					\n- Socket Boni are NOT considered!							\
					\n- Enchants are considered (your Rings are enchanted).		\
					\n- You have Insightful Earthstorm Diamond (+12 Int).		\
					\n- You have +15 spirit chest enchant.						\
					\n- You are Aldor (shoulder enchant).						\
					\n- There are no accurate formulas out there when it comes to spirit and mp5, approximations at best."


		return string
