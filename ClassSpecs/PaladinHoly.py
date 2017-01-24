from WowItem import Item
from StandardCharacter import Character


class PaladinHoly(Character):

	def __init__(self):
		Character.__init__(self)
		self._baseStats["intellect"] = 87.0
		self._baseStats["spellcrit"] = 3.336
		self._baseStats["intToSpellcrit"] = 80.05
		self._baseStats["mana"] = 2953

		self._divineIntellect = 0.1		# improves intellect by 10%
		self._divineGuidance = 0.35		# improves healing bonus by 35% of intellect

		# meta 12, chest 6, shield 12
		self._enchantStats.Set("intellect", 30)
		# head 35, shoulders 33, bracers 30, gloves 35, legs 66, rings 40, weapon 81
		self._enchantStats.Set("hb", 320)
		# head 7, shoulders 4
		self._enchantStats.Set("mp5", 11)
		

	def UpdateTotalIntellect(self):
		key = "intellect"
		# update intellect before applying talent multiplier
		self.UpdateTotalStat("intellect")
		self._totalStats.Set(key, self._totalStats.Get(key) * (1 + self._divineIntellect))

	def UpdateTotalHealingBonus(self):
		key = "hb"
		# update hb before applying talent multiplier
		self.UpdateTotalStat("hb")
		self._totalStats.Set(key, self._totalStats.Get(key) 					\
			+ (self._totalStats.Get("intellect") * self._divineGuidance))

	def UpdateTotalStats(self):
		# this is overriding UpdateTotalStats from base
		Character.UpdateTotalStats(self)
		self.UpdateTotalIntellect()
		self.UpdateTotalHealingBonus()

		# since intellect, update the affected stats as well
		self.UpdateTotalMana()
		self.UpdateTotalSpellCrit()


	def HealingBonusFromInt(self):
		return (self._totalStats.Get("intellect") * self._divineGuidance)


	def ManaFromIntGems(self):
		return (20 + (15 * ((self._gemStats.Get("intellect") * (1 + self._divineIntellect)) - 20)))

	def SpellCritFromIntGems(self):
		return ((self._gemStats.Get("intellect") * (1 + self._divineIntellect)) / self._baseStats["intToSpellcrit"])

	def HealingBonusFromIntGems(self):
		return ((self._gemStats.Get("intellect") * (1 + self._divineIntellect)) * self._divineGuidance)


	def ToString(self):
		string =  "__TOTAL__" + "\n"
		string += "{:<30}".format("Healing Bonus") 			+ str(self._totalStats.Get("hb")) + "\n"
		string += "{:<30}".format("Base Int") 				+ str(self._baseStats["intellect"]) + "\n"
		string += "{:<30}".format("Base Mana") 				+ str(self._baseStats["mana"]) + "\n"
		string += "{:<30}".format("Total Int")				+ str(self._totalStats.Get("intellect")) + "\n"
		string += "{:<30}".format("Total Mana") 			+ str(self._totalStats.Get("mana")) + "\n"
		string += "{:<30}".format("Spell-Crit Rating") 		+ str(self._totalStats.Get("spellcritRating")) + "\n"
		string += "{:<30}".format("Total Spell-Crit") 		+ str(self._totalStats.Get("spellcrit")) + "\n"
		string += "{:<30}".format("Mp5") 					+ str(self._totalStats.Get("mp5")) + "\n"
		string += "{:<30}".format("Haste") 					+ str(self._totalStats.Get("haste")) + "\n\n"

		string += "__GEMS__" + "\n"
		string += "{:<30}".format("Gems Healing Bonus") 	+ str(self._gemStats.Get("hb")) + "\n"
		string += "{:<30}".format("Gems Spell-Crit Rating") + str(self._gemStats.Get("spellcritRating")) + "\n"
		string += "{:<30}".format("Gems Spell-Crit") 		+ str(self._gemStats.Get("spellcrit")) + "\n"
		string += "{:<30}".format("Gems Mp5") 				+ str(self._gemStats.Get("mp5")) + "\n"
		string += "{:<30}".format("Gems Haste") 			+ str(self._gemStats.Get("haste")) + "\n"
		string += "{:<30}".format("Gems Intellect") 		+ str(self._gemStats.Get("intellect")) + "\n"
		string += "{:<30}".format("Gems Mana from Int") 	+ str(self.ManaFromIntGems()) + "\n"
		string += "{:<30}".format("Gems Crit from Int") 	+ str(self.SpellCritFromIntGems()) + "\n"
		string += "{:<30}".format("Gems HB from Int") 		+ str(self.HealingBonusFromIntGems()) + "\n"
		string += "{:<30}".format("Gems Total HB") 			+ str(self._gemStats.Get("hb") + self.HealingBonusFromIntGems()) + "\n\n"

		string += "__INT__" + "\n"
		string += "{:<30}".format("Mana from Total Int") 	+ str(self.ManaFromInt()) + "\n"
		string += "{:<30}".format("Crit from Total Int") 	+ str(self.SpellCritFromInt()) + "\n"
		string += "{:<30}".format("HB from Total Int") 		+ str(self.HealingBonusFromInt()) + "\n\n"

		string += "\nNote:														\
					\n- Socket Boni are NOT considered!							\
					\n- Enchants are considered (your Rings are enchanted).		\
					\n- You have Insightful Earthstorm Diamond (+12 Int).		\
					\n- You are wearing a shield (+10 Int).						\
					\n- You are Aldor (shoulder enchant)."

		return string