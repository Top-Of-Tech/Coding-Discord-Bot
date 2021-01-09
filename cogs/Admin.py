import discord
from discord.ext import commands

class Admin(commands.Cog):
	def __init__(self, client):
		self.client = client


	@commands.command()
	@commands.has_any_role('Admin', 'Owner')
	async def loadMembers(self, ctx):
		async for member in ctx.guild.fetch_members(limit = None):
			self.client.db.insert(table = "Members", values = (member.id, member.name, 0, 0), ignore = True)

def setup(client):
	client.add_cog(Admin(client))