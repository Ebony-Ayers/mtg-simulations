from card_data import getParsedData
import value_of
import sys

def main():
	data = getParsedData()
	length = len(data)
	if len(sys.argv) == 2:
		length = int(sys.argv[1])
	i = 0
	with open("output/value_of_generic_creatures.csv", 'w') as outputFile:
		for card in data:
			#for attribute in card:
			#	print(attribute, card[attribute])
			#break
			
			if card.get("oracle_text", "") == "":
				cost = card.get("mana_cost", "")
				if cost != "" and cost.find("//") == -1:
					power = card.get("power", "")
					toughness = card.get("toughness", "")
					if power == "" or toughness == "" or power.find(".") != -1 or toughness.find(".") != -1: continue
					outputFile.write(f"{value_of.manaCostToGME(cost)},{int(power)+int(toughness)}\n")
			
			
			if i > length: break
			i += 1

if __name__ == "__main__":
	main()
