import requests
from WowItem import Item
from Character import Paladin
from ItemRack import ItemRack

website_database_url = "http://wow-one.com/database/?item=";


# this is some item build (with gems), for testing purposes
def LoadItems_TEST():
	r = ItemRack()
	r.Set("head", GetItem(30988))
	r.Rack("head").Set("gems", [GetItem(32204)])
	
	r.Set("neck", GetItem(37929))
	r.Rack("neck").Set("gems", [GetItem(32204)])

	r.Set("shoulders", GetItem(30996))
	r.Rack("shoulders").Set("gems", [GetItem(32204), GetItem(32216)])

	r.Set("back", GetItem(32524))

	r.Set("chest", GetItem(34375))
	r.Rack("chest").Set("gems", [GetItem(32204), GetItem(32204), GetItem(32204)])

	r.Set("bracers", GetItem(34432))
	r.Rack("bracers").Set("gems", [GetItem(32204)])

	r.Set("gloves", GetItem(34380))
	r.Rack("gloves").Set("gems", [GetItem(32204), GetItem(32204)])

	r.Set("belt", GetItem(34487))
	r.Rack("belt").Set("gems", [GetItem(33134)])	

	r.Set("legs", GetItem(30994))
	r.Rack("legs").Set("gems", [GetItem(32204)])

	r.Set("boots", GetItem(33324))
	r.Rack("boots").Set("gems", [GetItem(32204), GetItem(32216)])

	r.Set("ring1", GetItem(32528))
	r.Set("ring2", GetItem(32528))
	r.Set("trinket1", GetItem(32496))
	r.Set("trinket2", GetItem(28727))
	r.Set("weapon", GetItem(32500))
	r.Set("offhand", GetItem(32255))

	return r

def LoadItems(filename):

	r = ItemRack()

	with open(filename, "r") as f:
		content = f.readlines()

		# iterate each line of the input file
		for c in content:
			# per default split() splits on whitepaces, tabs, ...
			line = c.split()

			slot = line[0]
			itemId = line[1]
			gems = []
			for i in range(2, len(line)):
				# "#" marks the start of a comment, we are not interested in the rest of the line
				if line[i] == "#":
					break
				gems.append(GetItem(line[i]))

			r.Set(slot, GetItem(itemId))
			if gems:
				r.Rack(slot).Set("gems", gems)

	return r

def GetItem(Id):
	page = requests.get(website_database_url + str(Id))
	return Item(Id, page)
