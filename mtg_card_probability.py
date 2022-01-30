import random
#for a deck of 100 cards (commander format)

#assume a deck is made of 2 cards A and B where there are n A cards and 100-n B cards
#draw a random card and return weather that card is A or not where n is the number of A cards
def draw(n):
	return random.randint(0, 99) < n

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
