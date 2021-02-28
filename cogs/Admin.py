import discord
from discord.ext import commands


class Admin(commands.Cog):
    """Owner commands. Use `.cs help admin` to know more!"""

    def __init__(self, client):
        self.client = client

    # ---------------------------------------------------

    @commands.command(aliases=["lm"])
    @commands.has_any_role("Admin", "Owner")
    async def loadMembers(self, ctx):
        """Update the database to include the latest members that may have joined when the bot was down.\nUsage:\n`.cs loadMembers` or `.cs lm`\nOnly Owners can use this!"""

        async for member in ctx.guild.fetch_members(limit=None):
            print(
                member.name,
                self.client.db.insert_ignore(
                    table="Members", values=(member.id, member.name, 0)
                ),
            )


def setup(client):
    client.add_cog(Admin(client))
