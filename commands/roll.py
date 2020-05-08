import discord
import re

import classes.dice as Dice
import classes.bonus as Bonus

async def roll(author:discord.Member, channel:discord.TextChannel, content:str, debug:bool=False):
	if debug == True:
		from importlib import reload
		reload(Dice)
		reload(Bonus)

	await displayer(author, channel, recursiveParser(content, debug=debug), debug=debug)

def recursiveParser(content:str, debug:bool=False):
	match = re.match("^(?: ?\\+ ?)?(?P<option>[aAdD]?)((?P<dice>[0-9]*)[dD](?P<size>[0-9]+))(?P<content>.*)$", content)
	if match is not None:
		dice = 1 if match.group("dice") == "" else int(match.group("dice"))
		dsize = int(match.group("size"))
		aventage = True if match.group("option") == "a" or match.group("option") == "A" else False
		desavantage = True if match.group("option") == "d" or match.group("option") == "D" else False
		if dice == 0 or dsize == 0:
			raise(Exception("wtf {}d{}".format(dice, dsize)))
		return Dice.Dice(dice, dsize, aventage, desavantage, debug) + recursiveParser(match.group("content"))
	
	match = re.match("^ ?(?P<plus>[+-]) ?(?P<value>[0-9]+)(?P<content>.*)$", content)
	if match is not None:
		plus = True if match.group("plus") == "+" else False
		return Bonus.Bonus(plus, int(match.group("value")), debug) + recursiveParser(match.group("content"))

	return None

async def displayer(author:discord.Member, channel:discord.TextChannel, first:[Dice.Dice, Bonus.Bonus], debug:bool=False):
	actual = first
	embed = discord.Embed(
		title = "{}'s Roll".format(author.name),
		colour = discord.Color.dark_grey()
	)
	result = 0





	msg = ""

	while (True):
		#msg += str(actual)
		embed.add_field(name = "Dice" if isinstance(actual, Dice.Dice) == True else "Constant", value = actual.str, inline = False)
		result += actual.result
		actual = actual.next
		if actual != None:
			msg += " "
		else:
			break

	embed.add_field(name = "Result", value = result, inline = True)






	#await message.channel.send("`" + str(result) + "`")
	await channel.send(embed = embed)
