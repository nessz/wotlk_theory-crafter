from WowItem import Item
from StandardCharacter import Character


class PaladinHoly(Character):

	def __init__(self):
		Character.__init__(self)
		self._baseStats["intellect"] = 87
		self._baseStats["spellcrit"] = 3.336
		self._baseStats["intToSpellcrit"] = 80.05

		self._divineIntellect = 0.1		# improves intellect by 10%
		self._divineGuidance = 0.35		# improves healing bonus by 35% of intellect

		# meta 12, chest 6, shield 12
		self._enchantStats.Set("intellect", 30)
		# head 35, shoulders 33, bracers 30, gloves 35, legs 66, rings 40, weapon 81
		self._enchantStats.Set("hb", 320)
		# head 7, shoulders 4
		self._enchantStats.Set("mp5", 11)
		
		'''
		self.UpdateTotalIntellect()
		self.UpdateTotalMana()
		self.UpdateTotalCrit()
		self.UpdateHealingBonus()
		'''


	def UpdateTotalIntellect(self):
		Character.UpdateTotalIntellect(self)
		key = "intellect"
		self._totalStats.Set(key, self._totalStats.Get(key) * self._divineIntellect)

	def UpdateTotalHealingBonus(self):
		Character.UpdateTotalHealingBonus(self)
		key = "hb"
		self._totalStats.Set(key, self._totalStats.Get(key) 					\
			+ (self._totalStats.Get("intellect") * self._divineGuidance))

	def ManaFromInt(self):
		return (20 + (15 * (self._totalIntellect - 20)))

	def CritFromInt(self):
		return (self._totalIntellect / 80.05)

	def HealingBonusFromInt(self):
		return (self._totalIntellect * self._divineGuidance)


	def ManaFromIntGems(self):
		return (20 + (15 * ((self._int_FromGems * (1 + self._divineIntellect)) - 20)))

	def CritFromIntGems(self):
		return ((self._int_FromGems * (1 + self._divineIntellect)) / 80.05)

	def HealingBonusFromIntGems(self):
		return ((self._int_FromGems * (1 + self._divineIntellect)) * self._divineGuidance)

	'''
	def UpdateStatsFromItems(self, hb_items, int_items, crit_items, mp5_items, haste_items):
		self._hb_FromItems = hb_items
		self._int_FromItems = int_items
		self._critRating_FromItems = crit_items
		self._mp5_FromItems = mp5_items
		self._haste_FromItems = haste_items

		self.UpdateTotalIntellect()
		self.UpdateTotalMana()
		self.UpdateTotalCrit()
		self.UpdateHealingBonus()

	def UpdateStatsFromGems(self, hb_gems, int_gems, crit_gems, mp5_gems, haste_gems):
		self._hb_FromGems = hb_gems
		self._int_FromGems = int_gems
		self._critRating_FromGems = crit_gems
		self._mp5_FromGems = mp5_gems
		self._haste_FromGems = haste_gems

		self.UpdateTotalIntellect()
		self.UpdateTotalMana()
		self.UpdateTotalCrit()
		self.UpdateHealingBonus()
	'''

	def ToString(self):
		string =  "__TOTAL__" + "\n"
		string += "Healing Bonus         " + str(self._totalStats.Get("hb")) + "\n"
		string += "Base Int              " + str(self._baseStats["intellect"]) + "\n"
		string += "Base Mana             " + str(self._baseStats["mana"]) + "\n"
		string += "Total Int             " + str(self._totalStats.Get("intellect")) + "\n"
		string += "Total Mana            " + str(self._totalStats.Get("mana")) + "\n"
		#string += "Crit Rating           " + str(self.) + "\n"
		string += "Total Crit            " + str(self._totalStats.Get("spellcrit")) + "\n"
		string += "Mp5                   " + str(self._totalStats.Get("mp5")) + "\n"
		string += "Haste                 " + str(self._totalStats.Get("haste")) + "\n\n"

		string += "__GEMS__" + "\n"
		string += "Gems Healing Bonus    " + str(self._gemStats.Get("hb")) + "\n"
		#string += "Gems Crit Rating      " + str(self._critRating_FromGems) + "\n"
		string += "Gems Crit             " + str(self._gemStats.Get("spellcrit")) + "\n"
		string += "Gems Mp5              " + str(self._gemStats.Get("mp5")) + "\n"
		string += "Gems Haste            " + str(self._gemStats.Get("haste")) + "\n"
		string += "Gems Intellect        " + str(self._gemStats.Get("intellect")) + "\n"
		string += "Gems Mana from Int    " #+ str(self.ManaFromIntGems()) + "\n"
		string += "Gems Crit from Int    " + str(self._gemStats.Get("spellcrit")) + "\n"
		string += "Gems HB from Int      " #+ str(self.HealingBonusFromIntGems()) + "\n"
		#string += "Gems Total Crit       " + str(self._totalCritGems + self.CritFromIntGems()) + "\n"
		string += "Gems Total HB         " #+ str(self._hb_FromGems + self.HealingBonusFromIntGems()) + "\n\n"

		string += "__INT__" + "\n"
		string += "Mana from Total Int   " #+ str(self.ManaFromInt()) + "\n"
		string += "Crit from Total Int   " #+ str(self.CritFromInt()) + "\n"
		string += "HB from Total Int     " #+ str(self.HealingBonusFromInt()) + "\n\n"

		string += "\nNote:\n- Socket Boni are NOT considered!\n- Enchants are considered (your Rings are enchanted).\n- You have Insightful Earthstorm Diamond (+12 Int).\n- You are wearing a shield (+10 Int).\n- You are Aldor (shoulder enchant)."

		return string