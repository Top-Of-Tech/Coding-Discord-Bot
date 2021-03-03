import discord
from discord.ext import commands
import random


class Games(commands.Cog):
    """Game commands. Use `.cs help games` to know more!"""

    def __init__(self, client):
        self.client = client

        # ---------------------------------------------------

        # Roles a dice for you

    @commands.command()
    async def dice(self, ctx):
        """Roll a dice!\nUsage: `.cs dice`"""

        embed = discord.Embed(
            title=f"The dice rolled {random.randint(1, 6)}", color=0x1479D2
        )

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Games(client))
