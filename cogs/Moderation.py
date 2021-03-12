import discord
from discord.ext import commands
import random
import datetime


class Moderation(commands.Cog):
    """Commands related to moderation. Use `.cs help moderation` to know more!"""

    def __init__(self, client):
        self.client = client

    # ---------------------------------------------------

    # Ban a User
    @commands.command()
    @commands.has_any_role("Admin", "Owner")
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        """Ban a user.\nUsage: `.cs ban (user) <reason>`\nOnly Admins and Owners can use this!"""

        try:
            await ctx.guild.ban(member, reason=reason)
            await ctx.send(f"Successfully banned {member.mention}")
        except Exception as e:
            await ctx.send(f"Was not able to ban `{member.mention}`")
            await ctx.send(f"Error:\n```{e}```")

    # ---------------------------------------------------

    # Purge Messages
    @commands.command()
    @commands.has_any_role("Admin", "Owner", "Moderator")
    async def purge(self, ctx, limit=50, member: discord.Member = None):
        """Purge the messages in a channel.\nUsage: `.cs purge <message_count> <user>`\nOnly Admins and Owners can use this!"""

        await ctx.message.delete()
        msg = []

        try:
            limit = int(limit)
        except:
            return await ctx.send("Please pass in an integer as limit")

        if not member:
            await ctx.channel.purge(limit=limit)
            return await ctx.send(f"Purged {limit} messages", delete_after=3)
        async for m in ctx.channel.history():
            if len(msg) == limit:
                break
            if m.author == member:
                msg.append(m)

        await ctx.channel.delete_messages(msg)
        await ctx.send(f"Purged {limit} messages of {member.mention}", delete_after=3)

    # ---------------------------------------------------

    # Kick a user
    @commands.command()
    @commands.has_any_role("Admin", "Owner", "Moderator")
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        """Kick a user.\nUsage: `.cs kick (member) <reason>`"""

        try:
            await member.kick(reason=reason)
            await ctx.send(f"User {member.mention} has kicked.")
        except Exception as e:
            await ctx.send(f"Was not able to kick `{member}`")
            await ctx.send(f"Error:\n```{e}```")

    # ---------------------------------------------------


def setup(client):
    client.add_cog(Moderation(client))
