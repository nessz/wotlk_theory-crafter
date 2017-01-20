import sys
sys.path.append("Specs")

import ManageItems
import Specs


def main():

	item_rack_file = sys.argv[1]
	item_rack_file_out = item_rack_file + "__out"

	print "Welcome to TBC TheoryCrafter."
	print "Your input file:  ", item_rack_file
	print "Your output file: ", item_rack_file_out
	print "This might take a while ..."

	f_o = open(item_rack_file_out, "w+")

	r = ManageItems.LoadItems(item_rack_file)
	f_o.write(r.ContainedItems() + "\n")

	items_stats = r.ItemsStats()
	gems_stats = r.GemsStats()
	f_o.write("__Items_Stats__" + "\n")
	f_o.write(items_stats.ToString() + "\n\n")

	f_o.write("__Gems_Stats__" + "\n")
	f_o.write(gems_stats.ToString() + "\n\n")

	c = Specs.GetClassSpec(item_rack_file)()
	c.UpdateStatsFromItems(
		items_stats.Get("hb"), 
		items_stats.Get("intellect"), 
		items_stats.Get("crit"), 
		items_stats.Get("mp5"), 
		items_stats.Get("haste"))
	c.UpdateStatsFromGems(
		gems_stats.Get("hb"), 
		gems_stats.Get("intellect"), 
		gems_stats.Get("crit"), 
		gems_stats.Get("mp5"), 
		gems_stats.Get("haste"))
	f_o.write(c.ToString() + "\n")

	f_o.close()


if __name__ == "__main__":
    main()