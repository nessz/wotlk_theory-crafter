from bs4 import BeautifulSoup
import re


class Item:

	# parsing might not work for other sites than http://wow-one.com/database/ at the moment
	def __init__(self, Id = -1, response = ""):
		self._stats = {
		"id": 0,
		"name": 0,
		"slot": 0,
		"intellect": 0,
		"crit": 0,
		"hb": 0,
		"haste": 0,
		"mp5": 0,
		"yellow": 0,
		"red": 0,
		"blue": 0,
		"gems": []
		}

		if Id == -1 and response == "":
			self._stats["id"] = "~"
			self._stats["name"] = "~"
			self._stats["slot"] = "~"			
			return

		# get data part of response
		soup = BeautifulSoup(response.text, "lxml")
		data = soup.find("div", {"id": "tooltip" + str(Id) + "-generic"})

		# pattern for later
		regex_digits = re.compile("\d+")

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

			# intellect
			tmp = re.search("\+\d+ Intellect", response.text)
			if tmp:
				self._stats["intellect"] = int(regex_digits.search(str(tmp.group())).group())

			# healing bonus
			tmp = re.search("\+\d+ Healing", response.text)
			if tmp:
				self._stats["hb"] = int(regex_digits.search(str(tmp.group())).group())

			# spell crit
			tmp = re.search("\+\d+ Spell Critical Rating", response.text)
			if tmp:
				self._stats["crit"] = int(regex_digits.search(str(tmp.group())).group())

			# haste
			tmp = re.search("\+\d+ Spell Haste Rating", response.text)
			if tmp:
				self._stats["haste"] = int(regex_digits.search(str(tmp.group())).group())

			# mp5
			tmp = re.search("\+\d+ Mana every", response.text)
			if tmp:	
				self._stats["mp5"] = int(regex_digits.search(str(tmp.group())).group())

			return		

		#----------------------------------------------------------------------
		# Item

		# item slot
		tmp = data.find("table", {"width": "100%"}).find("td")
		self._stats["slot"] = re.search(r".*", tmp.text).group(0)

		# intellect
		tmp = re.search("\+\d+ Intellect", response.text)
		if tmp:
			self._stats["intellect"] = int(regex_digits.search(str(tmp.group())).group())

		# spell crit
		tmp = re.search("Equip: Spell critical strike rating \+ \d+", response.text)
		if tmp:
			self._stats["crit"] = int(regex_digits.search(str(tmp.group())).group())

		# healing bonus
		tmp = re.search("Increases healing done by up to \d+", response.text)
		if tmp:
			self._stats["hb"] = int(regex_digits.search(str(tmp.group())).group())

		# haste
		tmp = re.search("Spell haste rating \+ \d+", response.text)
		if tmp:
			self._stats["haste"] = int(regex_digits.search(str(tmp.group())).group())

		# mp5
		tmp = re.search("Restores \d+", response.text)
		if tmp:
			self._stats["mp5"] = int(regex_digits.search(str(tmp.group())).group())

		#gems
		tmp = data.findAll(text=re.compile(".*"))

		# yellow
		search_text = "Yellow Socket"
		counter = 0
		for i in range(len(tmp)):
			if search_text in tmp[i]:
				counter += 1

		self._stats["yellow"] = counter

		# red
		search_text = "Red Socket"
		counter = 0
		for i in range(len(tmp)):
			if search_text in tmp[i]:
				counter += 1

		self._stats["red"] = counter

		# Blue
		search_text = "Blue Socket"
		counter = 0
		for i in range(len(tmp)):
			if search_text in tmp[i]:
				counter += 1

		self._stats["blue"] = counter

	def IsRegularItem(self):
		if self._stats["id"] != "~" and self._stats["name"] != "~" and self._stats["slot"] != "~":
			return True
		else:
			return False

	def GetName(self):
		return self._stats["name"]

	def Set(self, key, value):
		if self.IsRegularItem() and key != "gems":
			print "This action is not allowed for regular items.", key
			return 

		if self.IsRegularItem() and key is "gems" and (len(value) > (self._stats["yellow"] + self._stats["blue"] + self._stats["red"])):
			print "That many gems do not fit in this item.", self._stats["name"]
			return

		if key not in self._stats:
			print "'", key, "'  not in dictionary"
			return		

		self._stats[key] = value

	def Get(self, key):
		return self._stats[key]

	def Stats(self):
		# don't use this to set values... things can go wrong; see function Set(...)
		return self._stats

	def ToString(self):
		string =  "Name   " + str(self._stats["name"]) + "\n"
		string += "Id     " + str(self._stats["id"]) + "\n"
		string += "Slot   " + str(self._stats["slot"]) + "\n"
		string += "Int    " + str(self._stats["intellect"]) + "\n"
		string += "Crit   " + str(self._stats["crit"]) + "\n"
		string += "Hb     " + str(self._stats["hb"]) + "\n"
		string += "Haste  " + str(self._stats["haste"]) + "\n"
		string += "Mp5    " + str(self._stats["mp5"]) + "\n"
		string += "Y      " + str(self._stats["yellow"]) + "\n"
		string += "R      " + str(self._stats["red"]) + "\n"
		string += "B      " + str(self._stats["blue"]) + "\n"
		string += "Gems   " + str(len(self._stats["gems"])) #'  '.join(str(e.GetName()) for e in self._stats["gems"])

		return string