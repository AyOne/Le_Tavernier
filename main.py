import sys

DEBUG = False
HELP = False


argc = len(sys.argv)
for arg in sys.argv:
	if (arg.lower() == "debug"):
		DEBUG = True

		
if DEBUG == True:
	print("[DEBUG] - Debug mod has been activated. from now on the programme might be slower but it will update modified files and some extra informations will be displayed")
	from importlib import reload


import discord
import re
from sources import parser




class Tavernier(discord.Client):
	async def on_message(self, message):
		match = re.match("^\\!(?P<content>.*)$", message.content)
		if match != None:
			if DEBUG == True:
				reload(parser)
			await parser(message, match.group("content"))

	async def on_ready(self):
		print("[READY] - {} has connected to Discord".format(client.user))


token_fd = open("token", "r")
token = token_fd.read(60)

client = Tavernier()

client.run(token)