import discord
from discord.ext import commands

class Moderation(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.command()
	@commands.has_any_role('Admin', 'Owner', 'ADMIN')
	async def ban(self, ctx, member, reason):
		try:
			await ctx.guild.ban(member, reason=reason)
			await ctx.send(f"Succesfully banned {member}")
			print(f"Banned {member}")
		except:
			await ctx.guild.ban(member, reason=reason)
			await ctx.send(f"Was not able to ban `{member}`")


def setup(client):
	client.add_cog(Moderation(client))