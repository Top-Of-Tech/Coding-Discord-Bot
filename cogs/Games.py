import discord
from discord.ext import commands
import random

class Games(commands.Cog):
    def __init__(self, client):
        self.client = client

    # ---------------------------------------------------

    # Roles a dice for you
    @commands.command()
    async def dice(self, ctx):
        embed=discord.Embed(title=f"The dice rolled {random.randint(1, 6)}", color=0x1479d2)
        await ctx.send(embed=embed)
    
def setup(client):
    client.add_cog(Games(client))