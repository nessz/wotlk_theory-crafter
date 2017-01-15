
class Paladin:

	def __init__(self):
		self._baseIntellect = 87 #+ 65   # 65 distilled wisdom
		self._baseMana = 2953
		self._divineIntellect = 0.1		# improves intellect by 10%
		self._divineGuidance = 0.35		# improves healing bonus by 35% of intellect
		self._baseCrit = 3.336			# from WowWiki
		self._hbTotal = 0

		self._int_FromItems = 0
		self._critRating_FromItems = 0
		self._mp5_FromItems = 0
		self._hb_FromItems = 0
		self._haste_FromItems = 0

		self._int_FromGems = 0;
		self._critRating_FromGems = 0
		self._mp5_FromGems = 0
		self._hb_FromGems = 0
		self._haste_FromGems = 0

		# meta 12, chest 6, shield 12
		self._int_FromEnchants = 30;
		# head 35, shoulders 33, bracers 30, gloves 35, legs 66, rings 40, weapon 81
		self._hb_FromEnchants = 320;
		# head 7, shoulders 4
		self._mp5_FromEnchants = 11;
		

		self.UpdateTotalIntellect()
		self.UpdateTotalMana()
		self.UpdateTotalCrit()
		self.UpdateHealingBonus()


	def UpdateTotalIntellect(self):
		self._totalIntellect = (self._baseIntellect + self._int_FromItems \
							+ self._int_FromGems + self._int_FromEnchants) * (1 + self._divineIntellect)
		#self._totalIntellect = self._totalIntellect * 1.1 		# Kings

	def UpdateTotalMana(self):
		# formula from WowWiki
		self._totalMana = self._baseMana + (20 + (15 * (self._totalIntellect - 20)))

	def UpdateTotalCrit(self):
		# formula from WowWiki
		self._totalCrit = (self._totalIntellect / 80.05) + self._baseCrit + \
						((self._critRating_FromItems + self._critRating_FromGems) / 22.08)
		self._totalCritGems = (self._critRating_FromGems / 22.08)

	def UpdateHealingBonus(self):
		self._hbTotal = self._hb_FromItems + self._hb_FromGems + self._hb_FromEnchants \
					+ (self._totalIntellect * self._divineGuidance)


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


	def ToString(self):
		string =  "__TOTAL__" + "\n"
		string += "Healing Bonus         " + str(self._hbTotal) + "\n"
		string += "Base Int              " + str(self._baseIntellect) + "\n"
		string += "Base Mana             " + str(self._baseMana) + "\n"
		string += "Total Int             " + str(self._totalIntellect) + "\n"
		string += "Total Mana            " + str(self._totalMana) + "\n"
		string += "Crit Rating           " + str(self._critRating_FromItems + self._critRating_FromGems) + "\n"
		string += "Total Crit            " + str(self._totalCrit) + "\n"
		string += "Mp5                   " + str(self._mp5_FromItems + self._mp5_FromGems + self._mp5_FromEnchants) + "\n"
		string += "Haste                 " + str(self._haste_FromItems + self._haste_FromGems) + "\n\n"

		string += "__GEMS__" + "\n"
		string += "Gems Healing Bonus    " + str(self._hb_FromGems) + "\n"
		string += "Gems Crit Rating      " + str(self._critRating_FromGems) + "\n"
		string += "Gems Crit             " + str(self._totalCritGems) + "\n"
		string += "Gems Mp5              " + str(self._mp5_FromGems) + "\n"
		string += "Gems Haste            " + str(self._haste_FromGems) + "\n"
		string += "Gems Intellect        " + str(self._int_FromGems) + "\n"
		string += "Gems Mana from Int    " + str(self.ManaFromIntGems()) + "\n"
		string += "Gems Crit from Int    " + str(self.CritFromIntGems()) + "\n"
		string += "Gems HB from Int      " + str(self.HealingBonusFromIntGems()) + "\n"
		string += "Gems Total Crit       " + str(self._totalCritGems + self.CritFromIntGems()) + "\n"
		string += "Gems Total HB         " + str(self._hb_FromGems + self.HealingBonusFromIntGems()) + "\n\n"

		string += "__INT__" + "\n"
		string += "Mana from Total Int   " + str(self.ManaFromInt()) + "\n"
		string += "Crit from Total Int   " + str(self.CritFromInt()) + "\n"
		string += "HB from Total Int     " + str(self.HealingBonusFromInt()) + "\n\n"

		string += "\nNote:\n- Socket Boni are NOT considered!\n- Enchants are considered (your Rings are enchanted).\n- You have Insightful Earthstorm Diamond (+12 Int).\n- You are wearing a shield (+10 Int).\n- You are Aldor (shoulder enchant)."

		return string