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
		try:
			await roll.roll(message.author, message.channel, match.group("content"), debug=debug)
		except:
			await message.channel.send("`{}` make the programme crash !! but no panic. this has been handled. everything is fine now".format(message.content))
		return
	
	#purge command
	match = re.match("^(?P<command>purge) (?P<msgs>[0-9]+)$", content)
	if match is not None:
		if debug == True:
			print("[DEBUG] - purge command recognised")
			reload(purge)
		try:
			await purge.purge(message.author, message.channel, int(match.group("msgs")))
		except:
			await message.channel.send("`{}` make the programme crash !! but no panic. this has been handled. everything is fine now".format(message.content))
		return
	
	#help command
	match = re.match("^(?P<command>help)$", content)
	if match is not None:
		if debug == True:
			print("[DEBUG] - usage command recognised")
		await usage(message.channel)
		return
	
	else:
		await message.channel.send("`{}` could not be understand :(".format(message.content))


async def usage(channel:discord.TextChannel):
	await channel.send("""```
	!help					  | display this message
	!roll <pattern>			| roll the dices ! see pattern for more.
	!purge <number of line>	| purge a channel

	Pattern :
	two patherns are to consider
		1) - the dice : [advantage/disadvantage][number]d[size]
		exemples :
			- roll a simple d20 : !roll 1d20
			- roll a d20 with advantage : !roll a1d20
			- roll a d20 with disadvantage : !roll d1d20
			- roll 3d6 with adventage : !roll a3d6
		
		2) - the bonus [] : [sign][number]
		the sign can be '+' or '-'

		complexe exemple :
			!roll a2d20 + 3 + 1 + 1d4
			!roll 1d10 + a2d6 + 2
	```""")