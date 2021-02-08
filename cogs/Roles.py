import discord
from discord.ext import commands


class Roles(commands.Cog):
    def __init__(self, client):
        self.client = client

    # ---------------------------------------------------

    @commands.command()
    async def getrole(self, ctx, role_key):
        roles = self.client.db.select(
            table="Roles", columns="RoleID", condition=f"RoleKey = '{role_key}'"
        )
        try:
            role = ctx.guild.get_role(roles[0][0])
            await ctx.author.add_roles(role)
            await ctx.send("Gave you the role!")
        except Exception as e:
            await ctx.send(e)

    @commands.command()
    async def listroles(self, ctx):
        role_list = self.client.db.select(
            table="Roles", columns="RoleID, RoleKey", condition="RoleID >= 0"
        )
        embed = discord.Embed(
            title="List of Language Roles",
            description="",
            colour=discord.Colour.orange(),
        )
        for role_desc in role_list:
            role_name = ctx.guild.get_role(int(role_desc[0])).name
            embed.add_field(name=role_name, value=f"Key: {role_desc[1]}", inline=False)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Roles(client))
