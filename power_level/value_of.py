#GME = Generic Mana Equivilent
#attempts to take into account factors such as {W}{W} being harder to cast than {2}
def manaCostToGME(cost, xMultiplier = 1):
	parts = cost.split("}")
	parts.pop()
	
	gme = 0
	pips = 0
	for part in parts:
		if part.find("/") != -1:
			pips += 0.833
		elif part == "{W":
			pips += 1
		elif part == "{U":
			pips += 1
		elif part == "{B":
			pips += 1
		elif part == "{R":
			pips += 1
		elif part == "{G":
			pips += 1
		elif part == "{C":
			pips += 1
		elif part == "{X":
			gme += 2.5 * xMultiplier
		else:
			gme += int(part[1:])
	
	if pips > 0:
		if pips < 1:
			gme += pips
		else:
			pips -= 1
			gme += 1
			gme += 1.5 * pips
	
	return gme

#the value of the power and toughness alone of a creature
def powerAndToughnessToGME(power, toughness):
	x = power + toughness
	return 1.7 + (0.834 * x) + (0.0926 * (x * x))

if __name__ == "__main__":
	print(manaCostToGME("{3}{G}{B}"))
