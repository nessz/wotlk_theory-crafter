from WowItem import Item


class ItemRack:

	def __init__(self):
		self._rack = {
		"head": None,
		"neck": None,
		"shoulders": None,
		"back": None,
		"chest": None,
		"bracers": None,
		"gloves": None,
		"belt": None,
		"legs": None,
		"boots": None,
		"ring1": None,
		"ring2": None,
		"trinket1": None,
		"trinket2": None,
		"weapon": None,
		"offhand": None
		}

	def Set(self, key, value):
		if key not in self._rack:
			print "'", key, "'  not in ItemRack"
			return

		self._rack[key] = value

	def Rack(self, key):
		if key not in self._rack:
			print "'", key, "'  not in ItemRack"
			return -1

		return self._rack[key]

	def UpdateStats(self):
		item = Item()
		for key in self._rack:
			for key_ in self._rack[key].Stats():
				if key_ == "name" or key_ == "slot" or key_ == "id":
					continue

				item.Set(key_, item.Get(key_) + self._rack[key].Get(key_))


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
			string += "{:<12}".format(key) + self._rack[key].GetName() + "; " + ', '.join(str(e.GetName()) for e in self._rack[key].Get("gems")) + "\n"

		return string	

