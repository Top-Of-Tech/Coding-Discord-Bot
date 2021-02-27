import discord
from discord.ext import commands
import requests

class Github(commands.Cog):
    def __init__(self, client):
        self.client = client

    # ---------------------------------------------------

    # Fetches specified Github repository
    @commands.command(aliases=["gh"])
    async def github(self, ctx, repo):
        repo_object = requests.get(f"https://api.github.com/repos/{repo}").json()

        embed=discord.Embed(title=f"{repo_object['full_name']}", color=0x0066ff)
        embed.add_field(name="Stars", value=f"{repo_object['stargazers_count']}", inline=True)
        embed.add_field(name="Forks", value=f"{repo_object['forks']}", inline=True)
        embed.add_field(name="Watchers", value=f"{repo_object['watchers_count']}", inline=True)
        embed.add_field(name="Issues", value=f"{repo_object['open_issues']}", inline=True)
        embed.add_field(name="Language", value=f"{repo_object['language']}", inline=True)
        embed.add_field(name="Description", value=f"{repo_object['description']}", inline=True)
        await ctx.send(embed=embed)

    # ---------------------------------------------------

    # Gives you the organization link
    @commands.command(aliases=["org"])
    async def organization(self, ctx):
        await ctx.send("https://github.com/Connection-Software")


def setup(client):
    client.add_cog(Github(client))
