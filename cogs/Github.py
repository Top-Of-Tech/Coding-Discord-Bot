import discord
from discord.ext import commands
from github import Github

class Github(commands.Cog):
    def __init__(self, client):
        self.client = client

    # ---------------------------------------------------

    # Fetches specified Github repository
    @commands.command(aliases=["gh"])
    async def github(self, ctx, repo):
        repo_object = list(Github().search_repositories(repo))[0]

        embed=discord.Embed(title=f"{repo_object.full_name}", color=0x0000ff)
        embed.add_field(name="Stars", value=f"{repo_object.stargazers_count}", inline=True)
        embed.add_field(name="Forks", value=f"{repo_object.forks}", inline=True)
        embed.add_field(name="Watchers", value=f"{repo_object.watchers}", inline=True)
        embed.add_field(name="Issues", value=f"{len(repo_object.get_issues(state='open'))}", inline=True)
        embed.add_field(name="Language", value=f"{repo_object.language}", inline=True)
        embed.add_field(name="Description", value=f"{repo_object.description}", inline=True)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Github(client))