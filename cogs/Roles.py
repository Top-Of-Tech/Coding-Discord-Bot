import discord
from discord.ext import commands


class Roles(commands.Cog):
    def __init__(self, client):
        self.client = client

    # ---------------------------------------------------

    @commands.command()
    async def getrole(self, ctx, role_key):
        roles = self.client.db.select(
            table="Roles",
            columns="RoleID",
            condition=f"RoleKey = '{role_key}'"
        )
        try:
            role = ctx.guild.get_role(roles[0][0])
            await ctx.author.add_roles(role)
            await ctx.send("Gave you the role!")
        except Exception as e:
            await ctx.send(e)


def setup(client):
    client.add_cog(Roles(client))
