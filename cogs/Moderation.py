import discord
from discord.ext import commands
import random
import datetime


class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    # ---------------------------------------------------

    # Warn a User
    @commands.command()
    @commands.has_any_role('Admin', 'Owner')
    async def warn(self, ctx, member, reason):

        t = datetime.datetime.utcnow()
        form = t.strftime("%H:%M-%d-%m-%y")

        num_logs = len(self.client.db.select(table="Modlogs", columns="*", condition="ID >= 0"))
        values = (num_logs + 1, member.id, ctx.author.id, reason, form)

        output = self.client.db.insert(
                table = "ModLogs",
                values = values
            )

        try:
            dm = await member.create_dm()
            dm.send(f"You were warned in the {ctx.guild} server. Reason: {reason}")
            await ctx.send(f"Warned {member.mention}")
            return
        except:
            ctx.send(f"{member.mention}, you have been warned here.")
            return

        if output != 1:
            await ctx.send(f"Could not warn {member.mention}!")
            return
        await ctx.send(f"Warned {member.mention}")

    # ---------------------------------------------------

    # Ban a User
    @commands.command()
    @commands.has_any_role('Admin', 'Owner')
    async def ban(self, ctx, member: discord.Member, reason):
        try:
            await ctx.guild.ban(member, reason=reason)
            await ctx.send(f"Successfully banned {member.mention}")
            print(f"Banned {member}")
        except Exception as e:
            await ctx.send(f"Was not able to ban `{member.mention}`")
            await ctx.send(f"Error:\n```{e}```")

    # ---------------------------------------------------

    # Purge Messages
    @commands.command()
    @commands.has_any_role('Admin', 'Owner')
    async def purge(self, ctx, limit=50, member: discord.Member = None):
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
    @commands.has_any_role('Admin', 'Owner')
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        try:
            await member.kick(reason=reason)
            await ctx.send(f'User {member.mention} has kicked.')
        except Exception as e:
            await ctx.send(f"Was not able to kick `{member}`")
            await ctx.send(f"Error:\n```{e}```")

    # ---------------------------------------------------

    # List the Modlogs of a user
    @commands.command(aliases=["ll"])
    @commands.has_any_role('Admin', 'Owner')
    async def listlogs(self, ctx, member_id):

        logs = self.client.db.select(
            table="ModLogs",
            columns="ID, UserID, ModeratorID, Reason, Date",
            condition=f"UserID = {member_id}"
        )

        member = await self.client.fetch_user(member_id)

        embedVar = discord.Embed(title=f"Modlogs of {member.name}", description=f"{len(logs)} Modlogs",
                                 color=0x0000ff)

        for n, log in enumerate(logs):
            mod = await self.client.fetch_user(log[2])
            us = await self.client.fetch_user(log[1])
            m = f"ID: {log[0]}\n"
            m += f"User: {us.name}\n"
            m += f"Moderator: {mod.name}\n"
            m += f"Date: {log[4]}\n"

            embedVar.add_field(name=f"{n + 1}. {log[3]}", value=m, inline=False)

        await ctx.send(embed=embedVar)

    # ---------------------------------------------------

    # Report a user
    @commands.command()
    async def report(self, ctx, member: discord.Member, *reason):
        reason = " ".join(reason).strip()

        n = len(self.client.db.select(table="Reports", columns="ID", condition="ID > 0"))
        t = datetime.datetime.utcnow()
        form = t.strftime("%H:%M-%d-%m-%y")
        
        self.client.db.insert(table="Reports", values=(n + 1, ctx.author.id, member.id, reason, form, 0))

        embed = discord.Embed(title="New Report", description=f"From: {ctx.author.mention}\nAgainst: {member.mention}",
                              color=random_colour())

        embed.add_field(name="Reason", value=f"```{reason}```", inline=False)
        text = f"Time Reported: {ctx.message.created_at.strftime('%d-%m-%y at %H:%M')}\nID: {n + 1}"
        embed.add_field(name="Info", value=text, inline=False)
        
        await self.client.reports_channel.send(embed=embed)
        await ctx.message.delete()
        await ctx.send(f"Reported {member.mention} for {reason}.")

    # ---------------------------------------------------

    # List reports
    @commands.command(aliases=["lr"])
    @commands.has_any_role('Admin', 'Owner')
    async def listreports(self, ctx, resolved=0, size=5):

        logs = self.client.db.select(
            table="Reports",
            columns="ID, ReporterID, UserID, Reason, Date",
            size=size,
            condition=f"Resolved = {resolved}"
        )[:size]

        embedVar = discord.Embed(title="Reports", description=f"{len(logs)} Reports", color=0x0000ff)

        for n, i in enumerate(logs):
            r = await self.client.fetch_user(i[1])
            m = f"ID: {i[0]}\n"
            m += f"Reporter: {r.name}\n"
            m += f"Reason: {i[3]}\n"
            m += f"Date: {i[4]}\n"
            u = await self.client.fetch_user(i[2])
            embedVar.add_field(name=f"{n + 1}. {u.name}", value=m, inline=False)

        await ctx.send(embed=embedVar)

    # ---------------------------------------------------

    # Mark a report as resloved(1)
    @commands.command(aliases=["cr"])
    @commands.has_any_role('Admin', 'Owner')
    async def closereport(self, ctx, report_id):
        report = self.client.db.update(
            table="Reports",
            command="Resolved = 1",
            condition=f"ID = {int(report_id)}")
        if report == 1:
            await ctx.send(f"Closed report {report_id} successfully.")
        else:
            await ctx.send("Was not able to close report!")

    # ---------------------------------------------------

    # Allow mods to add language roles
    @commands.command()
    @commands.has_any_role('Admin', 'Owner')
    async def createrole(self, ctx, role_id, role_key):
        role_name = ctx.guild.get_role(int(role_id)).name
        report = self.client.db.insert(table="Roles", values=(role_id, role_name, role_key))
        if report == 1:
            embed = discord.Embed(title="New Language Role", description=f"{role_name} - {role_key}",
                                  color=0x0000ff)
            embed.set_footer(text=f"Called by: {ctx.author.display_name}")
            embed.set_author(name=self.client.user.display_name)
            embed.set_thumbnail(url=ctx.guild.icon_url)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"Error:\n```\n{report}```")

    # ---------------------------------------------------

    # Allow mods to remove language roles from the DB
    @commands.command()
    @commands.has_any_role('Admin', 'Owner')
    async def deleterole(self, ctx, role_id):
        delete = self.client.db.delete(table="Roles", condition=f"RoleID = {int(role_id)}")
        if delete == 1:
            await ctx.send("Succesfully deleted role!")
        else:
            await ctx.send(f"Error:```{delete}```")

    # ---------------------------------------------------

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if not before.author.bot:
            embed = discord.Embed(title="Edited Message", description=before.channel.mention, color=0x0000ff)
            embed.add_field(name="Before", value=f"```{before.content}```", inline=True)
            embed.add_field(name="After", value=f"```{after.content}```", inline=True)
            embed.add_field(name="Author", value=f"{before.author.mention}")
            text = f"Time: {before.created_at.strftime('%d-%m-%y at %H:%M')}\nEdited at: {after.edited_at.strftime('%d-%m-%y at %H:%M')}\nMessage URL: {before.jump_url}\nMessage ID: {before.id}"
            embed.add_field(name="Info", value=text, inline=False)
            await self.client.logs_channel.send(embed=embed)

    # ---------------------------------------------------

    @commands.Cog.listener()
    async def on_message_delete(self, before):
        if before.author.id != self.client.user.id:
            embed = discord.Embed(title="Deleted Message", description=before.channel.mention, color=0x0000ff)
            embed.add_field(name="Message", value=f"```{before.content}```", inline=True)
            text = f"Time: {before.created_at.strftime('%d-%m-%y at %H:%M')}\nMessage ID: {before.id}"
            embed.add_field(name="Info", value=text, inline=False)
            await self.client.logs_channel.send(embed=embed)


def random_colour():
    return discord.Colour.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


def setup(client):
    client.add_cog(Moderation(client))
