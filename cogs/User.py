import discord
from discord.ext import commands


class User(commands.Cog):
    def __init__(self, client):
        self.client = client

    # ---------------------------------------------------

    # Gives info about the user
    @commands.command()
    async def userinfo(self, ctx, member: discord.Member):
        if member:
            author = member
        else:
            author = ctx.message.author

        embed = discord.Embed(title=f"{author}", color=0x0000ff)

        embed.add_field(name="User Info",
                        value=f"Joined On: `{str(author.joined_at).split()[0]}`"
                              f"\nCreated On: `{str(author.created_at).split()[0]}`"
                              f"\nUser ID: `{author.id}`",
                        inline=False)

        await ctx.send(embed=embed)

    # ---------------------------------------------------

    # Shows a picture of the user's avatar
    @commands.command(aliases=["av"])
    async def avatar(self, ctx, member: discord.Member = None):
        if member:
            author = member
        else:
            author = ctx.message.author

        embed = discord.Embed(title=f"{author}", color=0x0000ff)

        embed.set_image(url=author.avatar_url)

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(User(client))
