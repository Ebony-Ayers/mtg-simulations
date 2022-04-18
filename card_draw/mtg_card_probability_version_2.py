import random
import sys
import matplotlib.pyplot as plt

DECK_SIZE = 100
TURN_DESIRED = 4
NUM_LANDS = 36
NUM_RAMP = 10
NUM_DRAW = 5
NUM_DESIRED = 1
if len(sys.argv) >= 7: DECK_SIZE =		int(sys.argv[6])
if len(sys.argv) >= 6: TURN_DESIRED =	int(sys.argv[5])
if len(sys.argv) >= 5: NUM_DRAW =		int(sys.argv[4])
if len(sys.argv) >= 4: NUM_RAMP =		int(sys.argv[3])
if len(sys.argv) >= 3: NUM_LANDS =		int(sys.argv[2])
if len(sys.argv) >= 2: NUM_DESIRED =	int(sys.argv[1])
#default deck size of of 100 cards (commander format)
#default searching for 1 card by the end of turn 4

numLandsRemaining = 0
numRampRemaining = 0
numDrawRemaining = 0
numDesiredRemaining = 0
numGenericRemaining = 0

#since the deck is removed from resetting the deck is required for a new simulation
def resetDeck(nDesited):
	global numLandsRemaining, numRampRemaining, numDrawRemaining, numDesiredRemaining, numGenericRemaining
	
	numLandsRemaining = NUM_LANDS
	numRampRemaining = NUM_RAMP
	numDrawRemaining = NUM_DRAW
	numDesiredRemaining = nDesited
	numGenericRemaining = DECK_SIZE - (numLandsRemaining + numRampRemaining + numDrawRemaining + numDesiredRemaining)
	
#debug tool
def printDeck():
	print("lands:", numLandsRemaining, "ramp:", numRampRemaining, "draw:", numDrawRemaining, "desired:", numDesiredRemaining, "generic:", numGenericRemaining)

#assigning numerical values to each type of card
LAND = 0
RAMP = 1
DRAW = 2
DESIRED = 3
GENERIC = 4
#draw a card and return the number of the ascociated card
def draw(suppressError = False):
	global numLandsRemaining, numRampRemaining, numDrawRemaining, numDesiredRemaining, numGenericRemaining
	total = numLandsRemaining + numRampRemaining + numDrawRemaining + numDesiredRemaining + numGenericRemaining
	
	r = random.randint(0, total - 1)
	
	#the needed ifs accomplish the following
	#if r < numLandsRemaining return LAND
	#elif r < numLandsRemaining + numRampRemaining return RAMP
	#...
	#which effectivly says
	#if r is between 0 and numLandsRemaining return LAND
	#if r is between numLandsRemaining and numDrawRemaining return draw 
	returnTotal = numLandsRemaining
	if r < returnTotal:
		numLandsRemaining -= 1
		if numLandsRemaining < 0: numLandsRemaining = 0
		return LAND
	else:
		returnTotal += numRampRemaining
		if r < returnTotal:
			numRampRemaining -= 1
			if numRampRemaining < 0: numRampRemaining = 0
			return RAMP
		else:
			returnTotal += numDrawRemaining
			if r < returnTotal:
				numDrawRemaining -= 1
				if numDrawRemaining < 0: numDrawRemaining = 0
				return DRAW
			else:
				returnTotal += numDesiredRemaining
				if r < returnTotal:
					numDesiredRemaining -= 1
					if numDesiredRemaining < 0: numDesiredRemaining = 0
					return DESIRED
				else:
					returnTotal += numGenericRemaining
					if r < returnTotal:
						numGenericRemaining -= 1
						if numGenericRemaining < 0: numGenericRemaining = 0
						return GENERIC
					else:
						#the error message is for debugging and should never actuall come up unless there is an error elsewhere in the code
						if suppressError != True:
							print("error", r)
						return -1

#draw starting hand and check if the had meets one of a set of requirements otherwise muligan and repeat. Won't mulligan below 5 cards.
#conditions:
#3 lands
#2 lands and 1 ramp
def drawAndMulligan(nDesited):
	HAND_SIZE = 7
	
	hand = [0] * 5
	i = 0
	while i < 3:
		resetDeck(nDesited)
		hand = [0] * 5
		j = 0
		while j < HAND_SIZE - i:
			hand[draw()] += 1
			j += 1
		
		if hand[LAND] >= 3: return hand
		elif hand[LAND] == 2 and hand[RAMP] >= 1: return hand
		
		
		i += 1
	return hand

#draw and muligan then keep drawing untill the a desired card is drawn
def drawUntilDesired(nDesited):
	hand = drawAndMulligan(nDesited)
	
	if hand[DESIRED] >= 1: return 1
	else:
		i = 2
		while True:
			card = draw(True)
			if card == -1:
				break
			hand[card] += 1
			if hand[DESIRED] >= 1:
				return i
			
			i += 1
		return i

#run many games and record how many turned are needed on average
def simulation(nDesited, itterations = 1000):
	drawnByTurnN = [0] * (DECK_SIZE + 1)
	
	i = 0
	while i < itterations:
		turn = drawUntilDesired(nDesited)
		drawnByTurnN[turn] += 1
	
		i += 1
	
	return drawnByTurnN

#arbitarily chosen percentiles to measure
PERCENTILES = [0.159, 0.500, 0.841, 0.900, 0.950, 0.977]
#run the simulation and return the number of turns required to draw a card with certanty equal to the given percentile
def computerPercentileResults(nDesited):
	turns = [0] * len(PERCENTILES)
	
	numItterations = 100
	simulationResult = simulation(nDesited, numItterations)[1:]
	i = 0
	while i < len(simulationResult):
		simulationResult[i] /= numItterations
		i += 1
		
	total = 0
	i = 0
	j = 0
	while i < len(simulationResult) and j < len(PERCENTILES):
		total += simulationResult[i]
		if total > PERCENTILES[j]:
			turns[j] = i
			j += 1
		i += 1
	return turns

#compute the percentiles for a variation of numbers of the desired card in the deck
def metaSimulation():
	resultsForEachN = []
	i = 1
	while i < 10:
		j = 0
		totalResults = [0] * len(PERCENTILES)
		NUM_SIMULATIONS = 100
		while j < NUM_SIMULATIONS:
			result = computerPercentileResults(i)
			k = 0
			while k < len(result):
				totalResults[k] += result[k]
				k += 1
			j += 1
		j = 0
		while j < len(totalResults):
			totalResults[j] /= NUM_SIMULATIONS
			j += 1
		resultsForEachN.append(totalResults)
		
		i += 1
	return resultsForEachN

def main():
	#plot the data as is
	results = metaSimulation()
	xAxis = PERCENTILES.copy()
	legend = [""] * len(results)
	i = 0
	while i < len(legend):
		legend[i] = "n = " + str(i+1)
		i += 1
	i = 0
	while i < len(xAxis):
		xAxis[i] *= 100
		i += 1
	fig, plots = plt.subplots(1,2)
	i = 0
	while i < len(results):
		plots[0].plot(xAxis, results[i])
		i += 1
	plots[0].set(xlabel="Probability of drawing a desired card", ylabel="Number of turns required to draw card with given number of desired cards in deck")
	plots[0].legend(legend)
	
	#take the transpose of the results to get more meaningful results
	tResults = []
	i = 0
	while i < len(results[0]):
		temp = [0] * len(results)
		tResults.append(temp.copy())
		i += 1
	i = 0
	while i < len(tResults):
		j = 0
		while j < len(tResults[0]):
			tResults[i][j] = results[j][i]
			j += 1
		i += 1
	
	#plot the transposed data
	legend = list(map(str, xAxis))
	i = 0
	while i < len(legend):
		legend[i] += "%"
		i += 1
	xAxis = [0] * len(tResults[0])
	i = 0
	while i < len(tResults[0]):
		xAxis[i] = i + 1
		i += 1
	i = 0
	while i < len(tResults):
		plots[1].plot(xAxis, tResults[i])
		i += 1
	plots[1].set(xlabel="Number of desiered cards in the deck", ylabel="Number of turns required to draw card with given probability")
	plots[1].legend(legend)
	
	plt.show()

if __name__ == "__main__":
	main()		
