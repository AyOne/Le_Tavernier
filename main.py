import sys
import discord
import re
import referral

DEBUG = False
HELP = False


argc = len(sys.argv)
for arg in sys.argv:
	if (arg.lower() == "debug"):
		DEBUG = True

		
if DEBUG == True:
	print("[DEBUG] - Debug mod has been activated. from now on the programme might be slower but it will update modified files and some extra informations will be displayed")
	from importlib import reload







class Tavernier(discord.Client):
	async def on_message(self, message:discord.Message):
		match = re.match("^\\!(?P<content>.*)$", message.content)
		if match != None:
			if DEBUG == True:
				reload(referral)
				print("[DEBUG] - {0} typed this \"{1}\"".format(message.author.name, message.content))
			await referral.mainParser(message, match.group("content"), debug=DEBUG)

	async def on_ready(self):
		print("[READY] - {} has connected to Discord".format(client.user))


token_fd = open("token", "r")
token = token_fd.read(60)

client = Tavernier()

client.run(token)