import discord
from discord.ext import commands
import requests


class Github(commands.Cog):
    """Commands to search for Github Repositories. Use `.cs help github` to get more info!"""

    def __init__(self, client):
        self.client = client

    # ---------------------------------------------------

    # Fetches specified Github repository
    @commands.command(aliases=["gh", "ghrepo"])
    async def github(self, ctx, repo):
        """Command to get info on github repositories.\nUsage: `.cs github (full_repo_name)`"""

        repo_object = requests.get(f"https://api.github.com/repos/{repo}").json()

        embed = discord.Embed(title=f"{repo_object['full_name']}", color=0x0066FF)
        embed.add_field(
            name="Stars", value=f"{repo_object['stargazers_count']}", inline=True
        )
        embed.add_field(name="Forks", value=f"{repo_object['forks']}", inline=True)
        embed.add_field(
            name="Watchers", value=f"{repo_object['watchers_count']}", inline=True
        )
        embed.add_field(
            name="Issues", value=f"{repo_object['open_issues']}", inline=True
        )
        embed.add_field(
            name="Language", value=f"{repo_object['language']}", inline=True
        )
        embed.add_field(
            name="Description", value=f"{repo_object['description']}", inline=True
        )

        await ctx.send(embed=embed)

    # ---------------------------------------------------

    # Fetches specified Github user
    @commands.command(aliases=["ghu", "ghuser", "githubuser"])
    async def github_user(self, ctx, *, user):
        user_object = requests.get(f"https://api.github.com/users/{user}").json()

        embed = discord.Embed(title=user, url=user_object['url'], color=0x0066ff)

        if user_object['name'] != None:
            embed.add_field(name="Name", value=str(user_object['name']), inline=True)
        if user_object['company'] != None:
            embed.add_field(name="Company", value=str(user_object['company']), inline=True)
        if user_object['blog'] != None or user_object['blog'] != "":
            embed.add_field(name="Blog", value=str(user_object['blog']), inline=True)
        if user_object['location'] != None:
            embed.add_field(name="Location", value=str(user_object['location']), inline=True)
        if user_object['twitter_username'] != None:
            embed.add_field(name="Twitter Username", value=str(user_object['location']), inline=True)
        if user_object['bio'] != None or user_object['bio'] != "":
            embed.add_field(name="Bio", value=str(user_object['bio']), inline=True)
        
        embed.add_field(name="Repos", value=str(user_object['public_repos']), inline=True)
        embed.add_field(name="Gists", value=str(user_object['public_gists']), inline=True)
        embed.add_field(name="Followers", value=str(user_object['followers']), inline=True)
        embed.add_field(name="Following", value=str(user_object['following']), inline=True)
        embed.add_field(name="Created At", value=str(user_object['created_at'].split('T')[0]) + " .", inline=True)
        embed.set_thumbnail(url=user_object['avatar_url'])

        await ctx.send(embed=embed)

    # ---------------------------------------------------

    # Fetches specified Gitub organization
    @commands.command(aliases=["ghorg", "githuborg"])
    async def github_organization(self, ctx, org):
        org_object = requests.get(f"https://api.github.com/orgs/{org}").json()

        embed = discord.Embed(title=org, url=org_object['url'], color=0x0066ff)
        
        embed.add_field(name="Name", value=org_object['name'], inline=True)

        if org_object['company'] != None:
            embed.add_field(name="Company", value=org_object['company'], inline=True)
        if org_object['blog'] != None:
            embed.add_field(name="Blog", value=org_object['blog'], inline=True)
        if org_object['location'] != None:
            embed.add_field(name="Location", value=org_object['location'], inline=True)
        if org_object['twitter_username'] != None:
            embed.add_field(name="Twitter Username", value=org_object['location'], inline=True)

        embed.add_field(name="Repos", value=org_object['public_repos'], inline=True)
        embed.add_field(name="Gists", value=org_object['public_gists'], inline=True)
        embed.add_field(name="Created At", value=org_object['created_at'].split('T')[0], inline=True)
        embed.set_thumbnail(url=org_object['avatar_url'])

        await ctx.send(embed=embed)

    # ---------------------------------------------------

    # Gives you the organization link
    @commands.command(aliases=["org"])
    async def organization(self, ctx):
        """Command to get info about our github organization!\nUsage: `.cs organization`"""
        await ctx.send("https://github.com/Connection-Software")


def setup(client):
    client.add_cog(Github(client))
