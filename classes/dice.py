import random

class Dice():
	def __init__(self, number:int, size:int, advantage:bool, disadvantage:bool, debug=False):
		self.number = number
		self.size = size
		self.advantage = advantage
		self.disadvantage = disadvantage
		self.rolls = []
		self.roll()
		self.str = self.parse()
		self.result = self.calc()
		self.next = None
		if debug == True:
			print("[DEBUG] - a new Dice is initiated ({0}d{1}{2}) with a result of {3}".format(number, size, " with advantage" if advantage == True else " with disadvantage" if disadvantage == True else "", self.result))

	def __add__(self, other):
		self.next = other
		return self

	def __str__(self):
		return self.str

	def roll(self):
		for i in range(self.number):
			i = i #remove annoying warning "unused variable i"
			result = random.randint(1, self.size)
			if self.advantage or self.disadvantage:
				self.rolls.append([result, random.randint(1, self.size)])
			else:
				self.rolls.append(result)
	
	def calc(self):
		result = 0
		for i in range(self.number):
			if self.advantage:
				if self.rolls[i][0] > self.rolls[i][1]:
					result += self.rolls[i][0]
				else:
					result += self.rolls[i][1]
			elif self.disadvantage:
				if self.rolls[i][0] < self.rolls[i][1]:
					result += self.rolls[i][0]
				else:
					result += self.rolls[i][1]
			else:
				result += self.rolls[i]
		return result

	def parse(self):
		result = "["
		for i in range(self.number):
			result += " "
			if self.advantage:
				if self.rolls[i][0] > self.rolls[i][1]:
					result += "**{}**|{}".format(self.rolls[i][0], self.rolls[i][1])
				elif self.rolls[i][0] < self.rolls[i][1]:
					result += "{}|**{}**".format(self.rolls[i][0], self.rolls[i][1])
				else:
					result += "**{}**|**{}**".format(self.rolls[i][0], self.rolls[i][1])
			elif self.disadvantage:
				if self.rolls[i][0] < self.rolls[i][1]:
					result += "**{}**|{}".format(self.rolls[i][0], self.rolls[i][1])
				elif self.rolls[i][0] > self.rolls[i][1]:
					result += "{}|**{}**".format(self.rolls[i][0], self.rolls[i][1])
				else:
					result += "**{}**|**{}**".format(self.rolls[i][0], self.rolls[i][1])
			else:
				result += "{}".format(self.rolls[i])
		result += " ]"
		return result