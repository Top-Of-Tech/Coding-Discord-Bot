import discord
from discord.ext import commands
import inspect
from types import FunctionType

class Source(commands.Cog):
	"""Obtain source code for the bot. Use `.cs help Source` to know more!"""

	def __init__(self, client):
		self.client = client

# ---------------------------------------------------

	@commands.command(aliases=["gsc", "src"])
	async def get_source_code(self, ctx, command):
		"""Get the code for any bot command!\nUsage: `.cs source (command)`"""

		cmd = self.client.get_command(command)
		if cmd is None:
			return await ctx.send(f"The command {command} does not exist!")


		source = self.cleanup_code(inspect.getsource(cmd.callback))

		for block in source:
			await ctx.send(f"```py\n{block}```")

# ---------------------------------------------------

	def cleanup_code(self, code):
		lines = code.split("\n")
		code_list = [""]

		char_count = 0

		for line in lines:
			if char_count < 1600:
				code_list[-1] += "\n" + line
				char_count += len(line) + 1
			else:
				code_list.append(line)
				char_count = len(line)

		return code_list

# ---------------------------------------------------

	@commands.command(aliases=["bsrc"])
	async def bot_source(self, ctx):
		"""Get a link for the Github repository!\nUsage: `.cs bot_source`"""

		await ctx.send("https://github.com/Connection-Software/Discord-Bot")

# ---------------------------------------------------

def setup(client):
	client.add_cog(Source(client))