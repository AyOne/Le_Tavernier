class Bonus():
	def __init__(self, plus:bool, value:int, debug:bool=False):
		self.plus = plus
		self.value = value
		self.str = "{} {}".format("+" if self.plus == True else "-", self.value)
		self.result = self.value if self.plus == True else -self.value
		self.next = None
		if debug == True:
			print("[DEBUG] - a new Bonus is initiated ({0}{1})".format("+" if plus == True else "-", value))


	def __add__(self, other):
		self.next = other
		return self

	def __str__(self):
		return self.str