import os
import discord
import random
import re
from functools import cmp_to_key



class Roll():
	def __init__(self, number, size, aventage, desaventage):
		self.number = number
		self.size = size
		self.aventage = aventage
		self.desaventage = desaventage
		self.dices = []
		self.roll()
		self.str = self.parse()
		self.result = self.calc()
		self.next = None

	def __add__(self, other):
		self.next = other
		return self

	def __str__(self):
		return self.str

	def parse(self):
		result = "["
		for i in range(self.number):
			result += " "
			if self.aventage:
				if self.dices[i][0] > self.dices[i][1]:
					result += "**{}**|{}".format(self.dices[i][0], self.dices[i][1])
				elif self.dices[i][0] < self.dices[i][1]:
					result += "{}|**{}**".format(self.dices[i][0], self.dices[i][1])
				else:
					result += "**{}**|**{}**".format(self.dices[i][0], self.dices[i][1])
			elif self.desaventage:
				if self.dices[i][0] < self.dices[i][1]:
					result += "**{}**|{}".format(self.dices[i][0], self.dices[i][1])
				elif self.dices[i][0] > self.dices[i][1]:
					result += "{}|**{}**".format(self.dices[i][0], self.dices[i][1])
				else:
					result += "**{}**|**{}**".format(self.dices[i][0], self.dices[i][1])
			else:
				result += "{}".format(self.dices[i])
		result += " ]"
		return result

	def calc(self):
		result = 0
		for i in range(self.number):
			if self.aventage:
				if self.dices[i][0] > self.dices[i][1]:
					result += self.dices[i][0]
				else:
					result += self.dices[i][1]
			elif self.desaventage:
				if self.dices[i][0] < self.dices[i][1]:
					result += self.dices[i][0]
				else:
					result += self.dices[i][1]
			else:
				result += self.dices[i]
		return result


	def roll(self):
		for i in range(self.number):
			result = random.randint(1, self.size)
			if self.aventage or self.desaventage:
				self.dices.append([result, random.randint(1, self.size)])
			else:
				self.dices.append(result)

class Bonus():
	def __init__(self, plus, value):
		self.plus = plus
		self.value = value
		self.str = "{} {}".format("+" if self.plus == True else "-", self.value)
		self.result = self.value if self.plus == True else -self.value
		self.next = None

	def __add__(self, other):
		self.next = other
		return self

	def __str__(self):
		return self.str



async def parser(message, content):
	match = re.match("^(?P<command>r|roll) (?P<content>.*)$", content)
	if match is not None:
		result = await new_roll_parser(message, match.group("content"))
		await new_role_printer(message, result)
		return
	match = re.match("^(?P<command>purge) (?P<msgs>[0-9]+)$", content)
	if match is not None:
		await message.delete()
		await message.channel.purge(limit=int(match.group("msgs")))
		return
	match = re.match("^(?P<command>help)$", content)
	if match is not None:
		await message.delete()
		await usage(message)
		return

	print("g pa konpri")



async def usage(message):
	await message.channel.send("""```
	!help				 | display this message
	!roll[!] <pattern>	| roll the dices ! see pattern for more.

	Pattern :
	important : everything must be separated with spaces.
	accepted pattern : 
		- "XdY" where X is the number of dices and Y the size. (X can be omitted)
		- "+ x" where X is a constant that will be added to the result.
	example :
		!roll 1d10 + 2d5
		!roll 2d20 + 7
		!roll 2d5 + 2 + 1d10
		!roll! 2d10 + 1d5 + 5 + 3 + 1d10 + 2
	```""")

def role_sort(a, b):
	if type(a[0]) == int and type(b[0]) == int:
		return 0
	elif type(a[0]) == int:
		return -1
	else:
		return 1


async def new_roll_parser(message, content):
	match = re.match("^(?: ?\+ ?)?(?P<option>[aAdD]?)((?P<dice>[0-9]*)[dD](?P<size>[0-9]+))(?P<content>.*)$", content)
	if match is not None:
		dice = 1 if match.group("dice") == "" else int(match.group("dice"))
		dsize = int(match.group("size"))
		aventage = True if match.group("option") == "a" or match.group("option") == "A" else False
		desavantage = True if match.group("option") == "d" or match.group("option") == "D" else False
		if dice == 0 or dsize == 0:
			raise(Exception("wtf {}d{}".format(dice, dsize)))
		return Roll(dice, dsize, aventage, desavantage) + await new_roll_parser(message, match.group("content"))
	
	match = re.match("^ ?(?P<plus>[+-]) ?(?P<value>[0-9]+)(?P<content>.*)$", content)
	if match is not None:
		plus = True if match.group("plus") == "+" else False
		return Bonus(plus, int(match.group("value"))) + await new_roll_parser(message, match.group("content"))

	return None

async def new_role_printer(message, first):
	actual = first
	embed = discord.Embed(
		title = "{}'s Roll".format(message.author.name),
		colour = discord.Color.dark_grey()
	)
	result = 0





	msg = ""

	while (True):
		#msg += str(actual)
		embed.add_field(name = "Dice" if isinstance(actual, Roll) == True else "Constant", value = actual.str, inline = False)
		result += actual.result
		actual = actual.next
		if actual != None:
			msg += " "
		else:
			break

	embed.add_field(name = "Result", value = result, inline = True)






	#await message.channel.send("`" + str(result) + "`")
	await message.channel.send(embed = embed)





class Tavernier(discord.Client):
	async def on_message(self, message):
		match = re.match("^\!(?P<content>.*)$", message.content)
		if match != None:
			await parser(message, match.group("content"))

	async def on_ready(self):
		print("{} has connected to Discord".format(client.user))




client = Tavernier()

client.run("NjkzNDk4MTQ4MjMxOTcwODU2.Xn9_6g.b0men1SrgB4OyTUgwUPe6SD5eE8")