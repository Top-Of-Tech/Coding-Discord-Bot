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
    async def ban(self, ctx, member: discord.Member, reason):
        """Ban a user.\nUsage: `.cs ban (user)`\nOnly Admins and Owners can use this!"""

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
        """Kick a user.\nUsage: `.cs kick (member) (reason)`"""

        try:
            await member.kick(reason=reason)
            await ctx.send(f"User {member.mention} has kicked.")
        except Exception as e:
            await ctx.send(f"Was not able to kick `{member}`")
            await ctx.send(f"Error:\n```{e}```")
            
    # ---------------------------------------------------

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if not before.author.bot:

            embed = discord.Embed(
                title="Edited Message",
                description=before.channel.mention,
                color=0xFF9F29,
            )

            embed.add_field(name="Before", value=f"```{before.content}```", inline=True)
            embed.add_field(name="After", value=f"```{after.content}```", inline=True)
            embed.add_field(name="Author", value=f"{before.author.mention}")

            text = f"Time: {before.created_at.strftime('%d-%m-%y at %H:%M')}\nEdited at: {after.edited_at.strftime('%d-%m-%y at %H:%M')}\nMessage URL: {before.jump_url}\nMessage ID: {before.id}"
            embed.add_field(name="Info", value=text, inline=False)

            await self.client.logs_channel.send(embed=embed)

    # ---------------------------------------------------

    @commands.Cog.listener()
    async def on_message_delete(self, before):
        if before.author.id != self.client.user.id or before.author.bot:
            embed = discord.Embed(
                title="Deleted Message",
                description=before.channel.mention,
                color=0xE32C29,
            )
            embed.add_field(
                name="Message", value=f"```{before.content}```", inline=True
            )
            embed.add_field(name="Author", value=f"{before.author.mention}")
            text = f"Time: {before.created_at.strftime('%d-%m-%y at %H:%M')}\nMessage ID: {before.id}"
            embed.add_field(name="Info", value=text, inline=False)
            await self.client.logs_channel.send(embed=embed)


def random_colour():
    return discord.Colour.from_rgb(
        random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
    )


def setup(client):
    client.add_cog(Moderation(client))
