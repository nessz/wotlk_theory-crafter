from bs4 import BeautifulSoup
import re
from collections import OrderedDict


class Item:

	# parsing might not work for other sites than http://wow-one.com/database/ at the moment
	def __init__(self, Id = -1, response = ""):
		# using OrderedDict, because we want the iteration order to stay the same (nicer logs)
		self._stats = OrderedDict([
		("id", 0),
		("name", 0),
		("slot", 0),
		("intellect", 0),
		("spirit", 0),
		("spellcrit", 0),
		("hb", 0),
		("haste", 0),
		("mp5", 0),
		("yellow", 0),
		("red", 0),
		("blue", 0),
		("gems", []),
		("s_bonus", None)	# socket bonus
		])

		# empty item for summing up stats
		if Id == -1 and response == "":
			self._stats["id"] = "~"
			self._stats["name"] = "~"
			self._stats["slot"] = "~"
			return

		# socket bonus items
		if Id == -42:
			self._stats["id"] = "~"
			self._stats["name"] = "~"
			self._stats["slot"] = "~"
			self.ParseGemStats(response)	# in this case 'response' is just text
			return

		# get data part of response
		soup = BeautifulSoup(response.text, "lxml")
		data = soup.find("div", {"id": "tooltip" + str(Id) + "-generic"})

		# id
		self._stats["id"] = Id

		# name
		tmp = data.find("b", {"class": "q4"})
		self._stats["name"] = re.search(r".*", tmp.text).group(0)

		# check if its a gem or an actual item
		tmp = re.search("\"Matches a", response.text)

		#----------------------------------------------------------------------
		# Gem
		# it's a Gem! Do something different.
		if tmp:
			self._stats["slot"] = "gem"
			self.ParseGemStats(response.text)
			return

		#----------------------------------------------------------------------
		# Item
		# item slot
		tmp = data.find("table", {"width": "100%"}).find("td")
		self._stats["slot"] = re.search(r".*", tmp.text).group(0)
		self.ParseItemStats(response.text)

	# this function parses for gem stats and sets them; note that items and gems have to be parsed differently
	def ParseGemStats(self, text):
		# pattern for later
		regex_digits = re.compile("\d+")

		# intellect
		tmp = re.search("\+\d+ Intellect", text)
		if tmp:
			self._stats["intellect"] = int(regex_digits.search(str(tmp.group())).group())

		# spirit
		tmp = re.search("\+\d+ Spirit", text)
		if tmp:
			self._stats["spirit"] = int(regex_digits.search(str(tmp.group())).group())

		# healing bonus
		tmp = re.search("\+\d+ Healing", text)
		if tmp:
			self._stats["hb"] = int(regex_digits.search(str(tmp.group())).group())

		# spell crit
		tmp = re.search("\+\d+ Spell Critical Rating", text)
		if tmp:
			self._stats["spellcrit"] = int(regex_digits.search(str(tmp.group())).group())

		# haste
		tmp = re.search("\+\d+ Spell Haste Rating", text)
		if tmp:
			self._stats["haste"] = int(regex_digits.search(str(tmp.group())).group())

		# mp5
		# 'Mana every' is used in gems; 'mana per' is used in socket boni
		tmp = re.search("\d+ [mM]ana (every|per)", text)
		if tmp:
			self._stats["mp5"] = int(regex_digits.search(str(tmp.group())).group())

	# this function parses for items stats and sets them
	def ParseItemStats(self, text):
		# pattern for later
		regex_digits = re.compile("\d+")

		# intellect
		tmp = re.search("\+\d+ Intellect", text)
		if tmp:
			self._stats["intellect"] = int(regex_digits.search(str(tmp.group())).group())

		# spirit
		tmp = re.search("\+\d+ Spirit", text)
		if tmp:
			self._stats["spirit"] = int(regex_digits.search(str(tmp.group())).group())

		# spell crit
		tmp = re.search("Equip: Spell critical strike rating \+ \d+", text)
		if tmp:
			self._stats["spellcrit"] = int(regex_digits.search(str(tmp.group())).group())

		# healing bonus
		tmp = re.search("Increases healing done by up to \d+", text)
		if tmp:
			self._stats["hb"] = int(regex_digits.search(str(tmp.group())).group())

		# haste
		tmp = re.search("Spell haste rating \+ \d+", text)
		if tmp:
			self._stats["haste"] = int(regex_digits.search(str(tmp.group())).group())

		# mp5
		tmp = re.search("Restores \d+", text)
		if tmp:
			self._stats["mp5"] = int(regex_digits.search(str(tmp.group())).group())

		# available gem slots
		tmp = re.findall("(Yellow|Blue|Red) Socket", text)
		self._stats["yellow"] = tmp.count("Yellow")
		self._stats["red"] = tmp.count("Red")
		self._stats["blue"] = tmp.count("Blue")

		if tmp:
			# that means that there is at least one gem and therefore a socket bonus
			tmp = re.search("Socket Bonus: \+*\d* \w+(\s\w*\s\w*)*", text)
			#print self._stats["name"], " ", str(tmp.group())
			i = Item(-42, str(tmp.group()))
			self._stats["s_bonus"] = i

	def IsRegularItem(self):
		if self._stats["id"] != "~" and self._stats["name"] != "~" and self._stats["slot"] != "~":
			return True
		else:
			return False

	def IsSocketBonusActive(self):
		if self._stats["s_bonus"] is None:
			return False

		# TODO don't know yet how to perform this check yet
		return False

	def GetName(self):
		return self._stats["name"]

	def Set(self, key, value):
		if self.IsRegularItem() and key != "gems":
			print "This action is not allowed for regular items.", key
			return 

		if self.IsRegularItem() and key is "gems" and \
		(len(value) > (self._stats["yellow"] + self._stats["blue"] + self._stats["red"])):
			print "That many gems do not fit in this item.", self._stats["name"]
			return

		if key not in self._stats:
			print "'", key, "'  not in dictionary"
			return		

		self._stats[key] = value

	def Get(self, key):
		return self._stats[key]

	def ItemStatDict(self):
		# don't use this to set values... things can go wrong; see function Set(...)
		return self._stats

	def ToString(self):
		# TODO introduce blacklist for skipping useless stats in logs

		string = ""
		for key in self._stats:
			if key == "gems":
				string += "{:<12}".format(key) + str(len(self._stats["gems"])) + "\n"
			elif key == "s_bonus" and self._stats["s_bonus"]:
				string += "{:<12}".format(key) + "\n" + self._stats["s_bonus"].ToString()
			else:
				string += "{:<12}".format(key) + str(self._stats[key]) + "\n"

		return string