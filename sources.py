import discord
import random
import re

import commands.roll as roll
import commands.purge as purge


async def mainParser(message:discord.Message, content:str, debug:bool=False):
	if debug == True:
		from importlib import reload
	await message.delete()

	#roll command
	match = re.match("^(?P<command>r|roll) (?P<content>.*)$", content)
	if match is not None:
		if debug == True:
			print("[DEBUG] - roll command recognised")
			reload(roll)
		await roll.roll(message.author, message.channel, match.group("content"), debug=debug)
		return
	
	#purge command
	match = re.match("^(?P<command>purge) (?P<msgs>[0-9]+)$", content)
	if match is not None:
		if debug == True:
			print("[DEBUG] - purge command recognised")
			reload(purge)
		await purge.purge(message.author, message.channel, int(match.group("msgs")))
		return
	
	#help command
	match = re.match("^(?P<command>help)$", content)
	if match is not None:
		if debug == True:
			print("[DEBUG] - usage command recognised")
		await usage(message)
		return


async def usage(channel:discord.TextChannel):
	await channel.send("""```
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