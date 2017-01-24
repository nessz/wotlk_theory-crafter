from collections import OrderedDict
from WowItem import Item
import math


class Character:

	def __init__(self):
		# base stats are taken from a lvl 70 character
		# or look those stats up from wowwiki
		self._baseStats = OrderedDict([		
		("mana",                        0),
		("spellcrit",                   0),
		("intellect",                   0),
		("spirit",                      0),
		("intToSpellcrit",              0),			# intellect needed for 1% spell crit
		("spellcritRatingToSpellcrit",  22.08)		# spell crit rating needed for 1% spell crit
		])

		self._itemStats = Item()		# stats gained from items
		self._gemStats = Item()			# stats gained from gems
		self._enchantStats = Item()		# stats gained from enchants

		self._totalStats = Item()
		self._totalStats.ItemStatDict().update({"mana": 0})					# adding mana as stat


	def UpdateTotalStat(self, key):
		if key not in self._itemStats.ItemStatDict() or 						\
			key not in self._totalStats.ItemStatDict():
			print "'", key, "' not in Character (Character.UpdateTotalStat)"
			return

		# not all stats are base stats
		if key not in self._baseStats:
			self._totalStats.Set(key,											\
			self._itemStats.Get(key) +											\
			self._gemStats.Get(key) +											\
			self._enchantStats.Get(key)											\
			)
		else:
			self._totalStats.Set(key,											\
			self._baseStats[key] + 												\
			self._itemStats.Get(key) +											\
			self._gemStats.Get(key) +											\
			self._enchantStats.Get(key)											\
			)

	def UpdateTotalStats(self):
		for key in self._itemStats.ItemStatDict():
			# note that itemStats, gemStats, enchantStats should be updated at this point
			# itemStats holds stats of all items plus potentially activated socket boni
			# gemStats holds stats coming purely from gems
			# enchantStats holds stats coming purely from enchants
			# and since all of the above are 'Item's, we are skipping name, slot and id since those are non-stat fields
			if key == "name" or key == "slot" or key == "id" or key == "s_bonus":
					continue

			self.UpdateTotalStat(key)

		self.UpdateTotalMana()
		self.UpdateTotalSpellCrit()

	def UpdateTotalMana(self):
		# should update intellect before calling this
		key = "mana"
		self._totalStats.Set(key,												\
			self._baseStats[key] + 												\
			(20 + (15 * (self._totalStats.Get("intellect") - 20)))				\
			)

	def UpdateTotalSpellCrit(self):
		if self._baseStats["intToSpellcrit"] == 0:
			print "intToSpellcrit has to be non-zero (Character.UpdateTotalSpellCrit)"

		# should update intellect before calling this

		self._totalStats.Set("spellcrit",
			(self._totalStats.Get("intellect") / self._baseStats["intToSpellcrit"]) +					\
			self._baseStats["spellcrit"] + 																\
			(self._totalStats.Get("spellcritRating") / self._baseStats["spellcritRatingToSpellcrit"])	\
			)

		'''# TODO might need to add _totalStatsGems
		print self._gemStats.Get("spellcrit")
		self._gemStats.Set("spellcrit",
			(self._gemStats.Get("intellect") / self._baseStats["intToSpellcrit"]) +						\
			(self._gemStats.Get("spellcritRating") / self._baseStats["spellcritRatingToSpellcrit"])		\
			)
		print self._gemStats.Get("spellcrit")
		'''


	#--------------------------------------------------------------------------
	# getter and setter

	def Get(self, key):
		if key not in self._baseStats:
			print "'", key, "'  not in Character (Character.Get)"
			return

		return self._baseStats[key]

	def Set(self, key, value):
		if key not in self._baseStats:
			print "'", key, "'  not in Character (Character.Set)"
			return

		self._baseStats[key] = value

	def SetItemStats(self, stats):
		self._itemStats = stats

	def SetGemStats(self, stats):
		self._gemStats = stats

	def SetEnchantStats(self, stats):
		self._enchantStats = stats


	#--------------------------------------------------------------------------
	# following functions break down some data, interesting for some classes

	def ManaFromInt(self):
		return (20 + (15 * (self._totalStats.Get("intellect") - 20)))

	def SpellCritFromInt(self):
		return (self._totalStats.Get("intellect") / self._baseStats["intToSpellcrit"])
