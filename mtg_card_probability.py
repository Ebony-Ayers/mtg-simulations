import random
import sys

DECK_SIZE = 100
NUM_CARDS_DESIRED = 1
TURN_DESIRED = 4
if len(sys.argv) >= 4: DECK_SIZE =			int(sys.argv[3])
if len(sys.argv) >= 3: TURN_DESIRED =		int(sys.argv[2])
if len(sys.argv) >= 2: NUM_CARDS_DESIRED =	int(sys.argv[1])
#default deck size of of 100 cards (commander format)
#default searching for 1 card by the end of turn 4

#assume a deck is made of 2 cards A and B where there are n A cards and 100-n B cards
#draw cards untill the desired turn and return the number of A cards drawn
def draw(numACards, startingHandSize = 7):
	numDrawn = 0
	aCardsRemaining = numACards
	for i in range(TURN_DESIRED + startingHandSize):
		didDraw random.randint(0, DECK_SIZE - 1 - i) < aCardsRemaining
		if didDraw:
			if aCardsRemaining > 0:
				aCardsRemaining -= 1
				numDrawn += 1
			else:
				break
	return numDrawn

#assuming replacment how many A cards will we draw by round r with m mulligans
def numberByRoundN(n, r, mulligan = 0):
	counter = 0
	extraCardDraw = 0
	for i in range(6, 6 - mulligan, -1):
		extraCardDraw += i
	for i in range(7+extraCardDraw+r):
		counter += draw(n)
	return counter

#calculate the probability of drawing at least 1 A card by round r with m mulligans
def Pr1(n, r, itterations, mulligan = 0):
	counter = 0
	for i in range(itterations):
		counter += numberByRoundN(n, r, mulligan) > 0
	return counter / itterations

#calculate the probability of drawing at least N A cards by round r with m mulligans
def PrN(N, n, r, itterations, mulligan = 0):
	counter = 0
	for i in range(itterations):
		counter += numberByRoundN(n, r, mulligan) > (N - 1)
	return counter / itterations

#simply linear search for certain card types
for i in range(4):
	print(f"With {i} muligans:")
	for j in range(100):
		if Pr1(j, 4, 100000, i) > 0.9:
			print(f"\t{j} tutors required to get one before round 4 with 90% probability")
			break
	else:
		print(f"\t100 tutors will draw one before round 4 with {Pr1(j, 4, 100000, i)}% probability")
	for j in range(100):
		if PrN(2, j, 4, 100000, i) > 0.9:
			print(f"\t{j} ramp spells required to get at least 2 before round 4 with 90% probability")
			break
	else:
		print(f"\t100 ramp spells will draw 2 spells before round 4 with {PrN(2, j, 4, 100000, i)}% probability")
