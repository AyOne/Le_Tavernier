import discord

async def purge(author:discord.Member, channel:discord.TextChannel, limit:int=0, debug:bool=False):
	if author.permissions_in(channel).manage_messages == True:
		if debug == True:
			print("[DEBUG] - {0} has the right to manage messages on channel {}".format(author.name, channel.name))
		await channel.purge(limit=limit)
	
