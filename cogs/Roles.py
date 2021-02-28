import discord
from discord.ext import commands


class Roles(commands.Cog):
    """Commands related to roles. Use `.cs help roles` to get more info"""

    def __init__(self, client):
        self.client = client

    # ---------------------------------------------------

    @commands.command()
    async def getrole(self, ctx, role_key):
        """Get a role using its key.\nUsage:\n`.cs getrole (role key)`"""

        roles = self.client.db.select(
            table="Roles", columns="RoleID", condition=f"RoleKey = '{role_key}'"
        )

        try:
            role = ctx.guild.get_role(roles[0][0])
            await ctx.author.add_roles(role)
            await ctx.send("Gave you the role!")
        except Exception as e:
            await ctx.send(e)

    # ---------------------------------------------------

    @commands.command()
    async def listroles(self, ctx):
        """List all the gettable roles.\nUsage:\n`.cs listroles`"""

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

    # ---------------------------------------------------

    # Allow mods to add language roles
    @commands.command()
    @commands.has_any_role("Admin", "Owner", "Moderator")
    async def createrole(self, ctx, role_id, role_key):
        """Remove a language role from the database/\nUsage\n`.cs deleterole (role id)\nCan only be used by Admins and Owners!"""

        role_name = ctx.guild.get_role(int(role_id)).name
        result = self.client.db.insert(
            table="Roles", values=(role_id, role_name, role_key)
        )

        if result == 1:
            embed = discord.Embed(
                title="New Language Role",
                description=f"{role_name} - {role_key}",
                color=0x0000FF,
            )
            embed.set_footer(text=f"Called by: {ctx.author.display_name}")
            embed.set_author(name=self.client.user.display_name)
            embed.set_thumbnail(url=ctx.guild.icon_url)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"Error:\n```\n{result}```")

    # ---------------------------------------------------

    # Allow mods to remove language roles from the DB
    @commands.command()
    @commands.has_any_role("Admin", "Owner", "Moderator")
    async def deleterole(self, ctx, role_id):
        """Add a language role to the database, with a unique key for members to use.\nUsage:\n`.cs createrole (role id) (role key)`\nCan only be used by Admins and Owners!"""

        delete = self.client.db.delete(
            table="Roles", condition=f"RoleID = {int(role_id)}"
        )
        if delete == 1:
            await ctx.send("Succesfully deleted role!")
        else:
            await ctx.send(f"Error:```{delete}```")


def setup(client):
    client.add_cog(Roles(client))
