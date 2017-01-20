

# centralised imports for all specs

from PaladinHoly import PaladinHoly


ClassSpec = {
	"PriestHoly": PaladinHoly,
	"PaladinHoly": PaladinHoly,
}

def GetClassSpec(filename):
	
	with open(filename, "r") as f:
		content = f.readlines()
		line = content[0].split()

		if line[0] != "class":
			print "File now well defined. (Specs.GetClassSpec)"

		return ClassSpec[line[1]]
