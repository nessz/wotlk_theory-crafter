from WowItem import Item
from collections import OrderedDict


class ItemRack:

	def __init__(self):
		# using OrderedDict, because we want the iteration order to stay the same (nicer logs)
		self._rack = OrderedDict([
		("head", None),
		("neck", None),
		("shoulders", None),
		("back", None),
		("chest", None),
		("bracers", None),
		("gloves", None),
		("belt", None),
		("legs", None),
		("boots", None),
		("ring1", None),
		("ring2", None),
		("trinket1", None),
		("trinket2", None),
		("weapon", None),
		("offhand", None),
		("ranged", None),
		])

		# for the sake of completeness those are defined here, their values are set in UpdateStats
		# note that itemsStats are pure stats collected from items (no gems, no enchants)
		# --> following from that gemsStats collects only stats from gems
		self._itemsStats = None
		self._gemsStats = None

	def Set(self, key, value):
		if key not in self._rack:
			print "'", key, "'  not in ItemRack (ItemRack.Set)"
			return

		self._rack[key] = value

	def Rack(self, key):
		if key not in self._rack:
			print "'", key, "'  not in ItemRack (ItemRack.Rack)"
			return -1

		return self._rack[key]

	def UpdateStats(self):
		# iterating through all relevant items in the ItemRack and summing up their stats
		# note that gems are a special case, since they are they only stat which is a list
		# --> from that follows that "summing up" will lead to a list with all gems 
		item = Item()
		for key in self._rack:
			if self._rack[key] is None:
				continue

			for key_ in self._rack[key].Stats():
				if key_ == "name" or key_ == "slot" or key_ == "id":
					continue

				item.Set(key_, item.Get(key_) + self._rack[key].Get(key_))

		# iterating over all gems in the gear and summing up their stats
		itemGems = Item()
		for g in item.Get("gems"):
			for key_ in g.Stats():
				if key_ == "name" or key_ == "slot" or key_ == "id":
					continue

				itemGems.Set(key_, itemGems.Get(key_) + g.Get(key_))

		self._itemsStats = item
		self._gemsStats = itemGems

	def ItemsStats(self):
		self.UpdateStats()
		return self._itemsStats

	def GemsStats(self):
		self.UpdateStats()
		return self._gemsStats

	def ContainedItems(self):
		string = "__Given_ItemRack__\n"
		for key in self._rack:
			if self._rack[key] is not None:
				string += "{:<12}".format(key) + self._rack[key].GetName() + "; " + ', '.join(str(e.GetName()) for e in self._rack[key].Get("gems")) + "\n"

		return string	

